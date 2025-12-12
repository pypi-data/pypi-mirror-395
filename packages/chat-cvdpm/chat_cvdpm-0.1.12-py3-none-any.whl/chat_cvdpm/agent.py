from enum import Enum
import operator

from typing import Annotated, List, Optional

from typing_extensions import TypedDict

import pandas as pd
import re
import numpy as np
import json
from datetime import datetime
import csv
import argparse

from typing import Callable
from langchain_core.tools import BaseTool, tool as create_tool
from langchain_core.runnables import RunnableConfig

from langgraph.types import interrupt
from langgraph.errors import GraphInterrupt
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from langchain.chat_models import init_chat_model

from langchain_core.tools import tool

from langchain_core.messages import ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_anthropic import ChatAnthropic

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate



from pydantic import BaseModel, Field

label_pattern = r"^[a-zA-Z0-9_+-\\$#/]+$"

def print_out(message: str):
    print(message)

import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

def parse_irregular_table(raw_data):
    """Parses the raw text data into a clean, wide pandas DataFrame."""
    first_line = 3 if 'summed years' in raw_data else 0
    lines = raw_data.strip().split('\n')
    lines = lines[first_line:]
    header_line = lines[0].strip()
    # print(lines)
    # Find column names based on non-whitespace sequences
    column_names = re.findall(r'\b\S+\b', header_line)

    data_rows = []
    index_names = []

    for line in lines[1:]:
        parts = line.strip().split()
        if not parts:
            continue

        # Clean index name (e.g., 'DISC_DHINTERV$' -> 'DISC_DHINTERV')
        index_name = parts[0].replace('.', '').replace('$', '')
        index_names.append(index_name)

        numerical_values = []
        for val_str in parts[1:]:
            # Remove trailing periods and convert to integer (or 0 if problematic)
            cleaned_val_str = val_str.replace('.', '')
            try:
                numerical_values.append(int(cleaned_val_str))
            except ValueError:
                numerical_values.append(0)

        data_rows.append(numerical_values)

    df = pd.DataFrame(data_rows, columns=column_names, index=index_names)
    df.index.name = 'Metric'
    df = df.apply(pd.to_numeric)
    return df

# --- Data Restructuring Logic ---

def restructure_to_tidy_format(df_wide):
    """
    Transforms the wide DataFrame into a long format indexed by Gender, Age Range,
    and Metric, handling the summary columns explicitly.
    """
    # 1. Melt the DataFrame to long format
    df_melted = df_wide.reset_index().melt(
        id_vars='Metric',
        var_name='Group',
        value_name='Value'
    )

    # 2. Function to extract Gender and Age Range
    def extract_components(group):
        if group == 'Total':
            return 'M+F', 'Sum'
        elif group == 'Msum':
            return 'M', 'Sum'
        elif group == 'Fsum':
            return 'F', 'Sum'

        # For standard groups like M35-44, F65-74, etc.
        match = re.match(r'([MF])(\d{2}-\d{2})', group)
        if match:
            gender = match.group(1)
            age_range = match.group(2)
            return gender, age_range
        return None, None

    # 3. Apply extraction and assign new columns
    df_melted[['Gender', 'Age Range']] = df_melted['Group'].apply(
        lambda x: pd.Series(extract_components(x))
    )

    # 4. Filter out any rows that couldn't be parsed (should be none with this data)
    df_final = df_melted.dropna(subset=['Gender', 'Age Range']).copy()

    # 5. Drop the temporary 'Group' column and restructure
    df_final.drop(columns=['Group'], inplace=True)

    # 6. Set the final desired index
    # df_final.set_index(['Gender', 'Age Range', 'Metric'], inplace=True)

    # 7. Convert the 'Value' column to a clean integer type
    df_final['Value'] = df_final['Value'].astype('int64')
    df_final['is_delta'] = False
    df_final['is_percent_delta'] = False

    return df_final

from .format import get_dfs

outfiles = [f for f in os.listdir('.') if f.endswith('.out')]

outfile_dfs = {}
for o in outfiles:
    o = o[:-4]
    dfs = get_dfs(o)
    outfile_dfs[o] = dfs

def write_augmented_files(total_df, arms=None):
    import os
    OUTDIR = 'augmented_dat/'
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    if 'is_delta' not in total_df.columns:
        total_df['is_delta'] = False
    if 'is_percent_delta' not in total_df.columns:
        total_df['is_delta'] = False
    total_df.to_parquet(OUTDIR + 'df.parquet')
    csv_dir = OUTDIR + '\\csv'
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    df_baseline = total_df.copy()
    df_baseline = df_baseline.fillna(0)
    df_baseline['Value'] = df_baseline['Value'].apply(lambda x: f"{x:.2f}" if abs(x - round(x))>0 else str(int(x)))
    delta_modifider = df_baseline.apply(lambda x: 'delta ' if x['is_delta'] else '\% delta' if x['is_percent_delta'] else '', axis=1)
    df_baseline['Column_Header'] =  delta_modifider + df_baseline['Gender'] + ' ' + df_baseline['Age Range']
    if arms:
        df_baseline = df_baseline[df_baseline['arm'].isin(arms)]
    print_out(f"Saving '.dat' files {', '.join(list(df_baseline.arm.unique()))} to {OUTDIR}")
    for arm in df_baseline.arm.unique():
        table = df_baseline[df_baseline['arm'] == arm].pivot_table(
            index='Metric',            # Rows: PREV, CHD_DEATH, etc.
            columns='Column_Header',   # Columns: M All Ages (Sum), Both All Ages (Total), etc.
            values='Value',            # Cell values
            aggfunc='first',           # Use 'first' since there should be only one baseline 'Value' per Metric/AgeGroup combination
            fill_value=0,
            sort=False
        )
        path = os.path.join(OUTDIR, f'{arm}')
        # print(f"Writing augmented data to {path}")
        with open(path, 'w') as f:
            f.write(table.to_string())


def load_df(dir='augmented_dat\\'):
    if 'df.parquet' in os.listdir(dir):
        total_df = pd.read_parquet(dir + 'df.parquet')
        return total_df, None


    files = []
    for file_name in os.listdir('.'):
        if not file_name.endswith('.dat'):
            continue
        with open((dir if dir is not None else '') + file_name, "r") as file:
            content = file.read()
        
        # Execute parsing and restructuring
        df_wide = parse_irregular_table(content)
        df_tidy = restructure_to_tidy_format(df_wide)
        df_tidy['arm'] = file_name

        files.append({'name': file_name, 'df': df_tidy})

    df_metadata = {
        'experiment_arm': [f['name'] for f in files],
    }

    total_df = pd.concat([f['df'] for f in files])
    return total_df, df_metadata

init_df, metadata_df = load_df('.\\')
write_augmented_files(init_df)

class AggEnum(Enum):
    SUM = 'sum'
    MEAN = 'mean'

MetricEnum = Enum('MetricEnum', [(m,m) for m in list(init_df['Metric'].unique())])
AgeRangeEnum = Enum('AgeRangeEnum', [(m,m) for m in list(init_df['Age Range'].unique())])
ColumnEnum = Enum('ColumnEnum', [(c,c) for c in list(init_df.columns.tolist())])
ArmEnum = Enum('ArmEnum', [(m,m) for m in list(init_df['arm'].unique())])

DatfileEnum = Enum('DatfileEnum', [(m,m) for m in list(init_df['arm'].unique())])
OutfileEnum = Enum('OutfileEnum', [(m,m) for m in set(outfile_dfs.keys()) & set([a[:-4] for a in init_df['arm'].unique()])])
OutfileMetricEnum = Enum('OutfileMetricEnum', [(m,m) for m in list(list(outfile_dfs.values())[0].keys())])
class AppendFromOutfileInputs(BaseModel):
    metric: OutfileMetricEnum = Field(description="Metric to add from '.out' file")
    arm: OutfileEnum = Field(description="arm to use")
    years: Optional[List[int]] = Field(description="years to aggregate, or None to use all years", default=None)
    year_agg: AggEnum = Field(description="Type of aggregation: sum, or mean", default=AggEnum.SUM)
    label: str = Field(description="Label for the new field in the table", pattern=label_pattern)

@tool(args_schema=AppendFromOutfileInputs)
def append_from_outfile(metric: OutfileMetricEnum, arm: OutfileEnum, year_agg: AggEnum, label: str, years: Optional[List[int]] = None):
    """Append a metric from '.out' file to the main data table
    Check if an equivalent metric already exists in the main table before using this tool
    
    Args:
        metric: metric to add
    """
    metric = metric.value
    res, _ = load_df()
    arm = arm.value
    print_out(f"📊 Appending metric '{label}' from .out files to main dataframe for arm: {arm}")
    outfile_df = outfile_dfs[arm][metric]
    if years and len(years) > 0:
        outfile_df = outfile_df[outfile_df['year'].isin(years)]
    outfile_df = outfile_df.groupby(['Age Range', 'Gender'])['Value'].agg(year_agg.value).reset_index()

    filename = f'{arm}.dat'
    outfile_df['Metric'] = label
    outfile_df['arm'] = filename
    outfile_df['Value'] = outfile_df['Value'].fillna(0)
    outfile_df['is_delta'] = False
    outfile_df['is_percent_delta'] = False
    outfile_df = groupby_sum(outfile_df, 'Sum', ['35-44', '45-54', '55-64', '65-74', '75-84', '85-94'], 'Age Range', save=False)
    totals = groupby_sum(outfile_df, 'M+F', ['M' ,'F'], 'Gender', save=False)
    outfile_df = pd.concat([outfile_df, totals[(totals['Age Range'] == 'Sum') & (totals['Gender'] == 'M+F')]])
    res = pd.concat([res, outfile_df])
    
    write_augmented_files(res, [filename])
    df = res
    
    state_update={
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

class DatfileInputs(BaseModel):
    arm1: DatfileEnum = Field(description="Arm to calculate diff with")
    arm2: DatfileEnum = Field(description="Arm to calculate diff with")
    use_percent: bool = Field(description="Whether to calculate the deltas as a percent (rather than difference)", default=False)
    age_ranges: Optional[List[AgeRangeEnum]] = Field(description="Age ranges to use: default all", default=None)

@tool(args_schema=DatfileInputs)
def add_deltas(arm2: ArmEnum, arm1: ArmEnum, use_percent: bool = False, age_ranges: Optional[List[AgeRangeEnum]] = None):
    """Calculate deltas between two arms 
    Args:
        arm1: the arm to add data to
        use_percent: whether to calculate the deltas as a percent (rather than difference)
        arm2: the arm to calculate deltas from
    """
    df, _ = load_df()
    delta_type = "percentage" if use_percent else "absolute difference"

    print_out(f"📈 Calculating {delta_type} deltas for metrics in '{arm1.value}' compared to '{arm2.value}'")
    GROUPING_FACTORS = ['Age Range', 'Gender', 'Metric']
    BASELINE_ARM = arm2.value
    NEW_ARM_LABEL = 'delta' # Label for the new rows

    df_comp = df.copy()
    if age_ranges is not None:
        age_ranges = [age_range.value for age_range in age_ranges]
        df_comp = df[df['Age Range'].isin(age_ranges)]
    
    # 1. Determine the Baseline
    # Group by the factors and filter for the baseline 'arm' to get the baseline value
    baseline_df = df[df['arm'] == BASELINE_ARM].copy()
    baseline_df = baseline_df.rename(columns={'Value': 'baseline_value'})
    baseline_df = baseline_df.drop(columns=['arm']) # Drop 'arm' as it's now implied (Pre)

    # 2. Merge the Baseline
    # Merge the baseline value back into the original DataFrame on the common factors
    df_comp = df_comp[df_comp['arm']  == arm1.value]
    df_merged = pd.merge(df_comp, baseline_df,
                        on=GROUPING_FACTORS,
                        how='left')

    # 3. Calculate the Difference
    if use_percent:
        df_merged['difference'] = 100 * (df_merged['Value'] - df_merged['baseline_value']) / df_merged['baseline_value']
        df_merged['difference'] = df_merged['difference'].replace([np.inf, -np.inf], 0).fillna(0)
    else:
        df_merged['difference'] = (df_merged['Value'] - df_merged['baseline_value'])


    # 4. Format the New Rows
    # Filter to select only the rows where the difference is calculated (e.g., 'Post' arm)
    # If you want the 'Change' row to represent the change *from* Pre to Post,
    # you might only select the 'Post' rows and calculate the change.
    # For simplicity, let's take the 'Post' rows as the basis for the 'Change' rows.

    df_new_rows = df_merged[df_merged['arm'] != BASELINE_ARM].copy()
    # df_new_rows['Gender'] = 'delta ' + df_new_rows['Gender'] # Set the new label
    if use_percent:
        df_new_rows['is_percent_delta'] = True
        df_new_rows['is_delta'] = False
    else:
        df_new_rows['is_delta'] = True
        df_new_rows['is_percent_delta'] = False
    df_new_rows['Value'] = df_new_rows['difference'] # The new 'value' is the calculated difference

    # Select only the necessary columns for the final append
    df_new_rows = df_new_rows[df.columns]

    # 5. Append to Original
    df_final = pd.concat([df, df_new_rows], ignore_index=True)

    # Optional: Sort the final DataFrame for better readability
    # df_final = df_final.sort_values(by=GROUPING_FACTORS + ['arm']).reset_index(drop=True)
    df = df_final
    write_augmented_files(df)
    state_update={
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

class GroupByMetricInput(BaseModel):
    label: str = Field(description="Label for the metric (shouldn't include information about age range, gender, or arm)", pattern=label_pattern)
    components: List[str] = Field(description="List of metrics to aggregate")

class GroupByAgeInput(BaseModel):
    label: str = Field(description="Label for the new age range", pattern=label_pattern)
    components: List[str] = Field(description="List of age ranges to aggregate")

@tool(args_schema=GroupByAgeInput)
def groupby_age_range(label: str, components: List[str]):
    """
    Sums data from multiple age ranges

    Args:
        label: a new key for the summed result
        components: The keys to sum together

    Returns:
        A new DataFrame containing the aggregated labels and their calculated totals.
    """
    print_out(f"🔢 Summing age ranges [{', '.join(components)}] into new age range '{label}'")
    df, _ = load_df()
    df = groupby_sum(df, label, components, 'Age Range')
    state_update={
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)


@tool(args_schema=GroupByMetricInput)
def groupby_metric(label: str, components: List[str]):
    """
    Sums data from multiple metrics

    Args:
        label: a new key for the summed result
        components: The keys to sum together

    Returns:
        A new DataFrame containing the aggregated labels and their calculated totals.
    """
    print_out(f"➕ Summing metrics [{', '.join(components)}] to create new metric '{label}'")
    df, _ = load_df()
    df = groupby_sum(df, label, components, 'Metric')

    state_update={
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

def groupby_sum(df, label: str, components: List[str], key_column: str, save=True) -> pd.DataFrame:
    """
    Sums data from multiple values of age range, gender, metric, or arm

    Args:
        df: The source DataFrame.
        label: a new key for the summed result
        components: The keys to sum together
        key_column: The name of the column containing the base categories (e.g., 'age_range').

    Returns:
        A new DataFrame containing the aggregated labels and their calculated totals.
    """
    value_column = 'Value'
    
    group_cols = [col for col in df.columns if col not in [key_column, value_column]]
    
    subset_df = df[df[key_column].isin(components)]
    aggregated_data = subset_df.groupby(group_cols).agg({
        value_column: 'sum'
    }).reset_index()
    
    
    aggregated_data[key_column] = label  
    df_updated = pd.concat([df, aggregated_data], ignore_index=True)

    # Reorder columns to match the original
    df = df_updated[df.columns]
    if save:
        write_augmented_files(df)
    return df

def perform_operation(df, field, label, col1, col2, op):
    """
    Performs a generic binary operation on two groups of values in a long-format DataFrame.
    Supports operations between two DataFrame columns or between a column and a constant.

    Args:
        df: The input DataFrame.
        field: The name of the categorical field to filter by (e.g. Age Range)
        label: The name for the new metric.
        col1: The name of the first metric column or a numeric constant.
        col2: The name of the second metric column or a numeric constant.
        op: A function that takes two pandas Series and returns one (e.g., operator.truediv).
    """
    # 1. Automatically determine the grouping columns (all columns except Metric and Value)

    group_cols = df.columns.drop([field, 'Value']).tolist()

    # 2. Pivot the table to get metrics as columns
    pivoted_df = df.pivot_table(index=group_cols, columns=field, values='Value')

    # 3. Helper function to get value (either from column or use constant)
    def get_operand(operand):
        """Returns either the column from pivoted_df or the constant value."""
        if isinstance(operand, (int, float)):
            # It's a constant - return it directly
            return operand
        else:
            # It's a column name - return the column
            return pivoted_df[operand]
    
    # 4. Get the operands (either columns or constants)
    operand1 = get_operand(col1)
    operand2 = get_operand(col2)
    
    # 5. Perform the operation in a single, vectorized step
    pivoted_df[label] = op(operand1, operand2)
    
    # 6. Isolate the new result and un-pivot it back to the original long format
    new_metric_df = pivoted_df[[label]].reset_index()
    new_metric_df = new_metric_df.rename(columns={label: 'Value'})
    new_metric_df[field] = label
    
    # 7. Combine the original data with the new metric's data
    return pd.concat([df, new_metric_df])

class BinaryOpInput(BaseModel):
    label: str = Field(description="Label for the metric (shouldn't include information about age range, gender, or arm)", pattern=label_pattern)
    col1: str = Field(description="First metric in binary operation")
    col2: str = Field(description="Second metric in binary operation")

@tool(args_schema=BinaryOpInput)
def divide(label, col1, col2):
    """
    Divide two metrics (or a metric by a constant) in the DataFrame.
    
    Args:
        label: The name of the new metric
        col1: The name of the numerator column or a numeric constant
        col2: The name of the denominator column or a numeric constant
    """
    col1_desc = str(col1) if isinstance(col1, (int, float)) else f"'{col1}'"
    col2_desc = str(col2) if isinstance(col2, (int, float)) else f"'{col2}'"
    print_out(f"➗ Dividing {col1_desc} by {col2_desc} to create new metric '{label}'")
    df, _ = load_df()

    # Define the division operation with protection for division by zero
    # This lambda function is passed as the 'op' argument
    div_op = lambda num, den: np.where(den != 0, num / den, np.nan)

    # Call the general function to do the heavy lifting
    df = perform_operation(df, 'Metric', label, col1, col2, div_op)

    # The rest of your tool-specific logic remains the same
    write_augmented_files(df)
    state_update = {
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

@tool(args_schema=BinaryOpInput)
def multiply(label, col1, col2):
    """
    Multiply two metrics (or a metric by a constant) in the DataFrame.
    
    Args:
        label: The name of the new metric
        col1: The name of the first column or a numeric constant
        col2: The name of the second column or a numeric constant
    """
    col1_desc = str(col1) if isinstance(col1, (int, float)) else f"'{col1}'"
    col2_desc = str(col2) if isinstance(col2, (int, float)) else f"'{col2}'"
    print_out(f"✖️ Multiplying {col1_desc} by {col2_desc} to create new metric '{label}'")
    df, _ = load_df()
    
    # Just call the same general function but with a different operator!
    df = perform_operation(df, 'Metric', label, col1, col2, operator.mul)

    write_augmented_files(df)
    state_update = {
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

@tool(args_schema=BinaryOpInput)
def subtract(label, col1, col2):
    """
    Subtract two metrics (or a metric minus/plus a constant) in the DataFrame.
    
    Args:
        field: The field to group by (e.g. 'arm' or 'Metric')
        label: The name of the new field ( )
        col1: The name of the first column or a numeric constant
        col2: The name of the second column or a numeric constant (will be subtracted from col1)
        secondary_field: optional secondary field, to add filter by (e.g. 'Metric' to compare a metric between two arms)
        secondary_filter: optional filter for type 'secondary_field' to use
    """
    col1_desc = str(col1) if isinstance(col1, (int, float)) else f"'{col1}'"
    col2_desc = str(col2) if isinstance(col2, (int, float)) else f"'{col2}'"
    print_out(f"➖ Subtracting {col2_desc} from {col1_desc} to create new metric '{label}'")
    df, _ = load_df()
    
    df = perform_operation(df, 'Metric', label, col1, col2, operator.sub)

    write_augmented_files(df)
    state_update = {
        "age_ranges": str(list(df['Age Range'].unique())),
        "columns": str(df.columns.tolist()),
        "metrics": str(list(df['Metric'].unique())),
    }
    return Command(update=state_update)

def add_human_in_the_loop(
    tool: Callable | BaseTool,
    *,
    interrupt_config: HumanInterruptConfig = None,
) -> BaseTool:
    """Wrap a tool to support human-in-the-loop review."""
    if not isinstance(tool, BaseTool):
        tool = create_tool(tool)

    if interrupt_config is None:
        interrupt_config = {
            "allow_accept": True,
            "allow_edit": True,
            "allow_respond": True,
        }

    @create_tool(  
        tool.name,
        description=tool.description,
        args_schema=tool.args_schema
    )
    def call_tool_with_interrupt(config: RunnableConfig, **tool_input):
        request = {
            "action_request": {
                "action": tool.name,
                "args": tool_input
            },
            "config": interrupt_config,
            "description": "Please review the tool call"
        }
        response = interrupt([request])[0]
        # approve the tool call
        if response["type"] == "accept":
            tool_response = tool.invoke(tool_input, config)
        # update tool call args
        elif response["type"] == "edit":
            tool_input = response["args"]["args"]
            tool_response = tool.invoke(tool_input, config)
        # respond to the LLM with user feedback
        elif response["type"] == "response":
            user_feedback = response["args"]
            tool_response = user_feedback
        else:
            raise ValueError(f"Unsupported interrupt response type: {response['type']}")

        return tool_response

    return call_tool_with_interrupt

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0)

def call_pandas_agent(input):
    total_df = pd.read_parquet('augmented_dat/df.parquet')
    pandas_agent = create_pandas_dataframe_agent(
        llm,
        total_df,
        agent_type="tool-calling",
        verbose=True,
        allow_dangerous_code=True
    )
    return pandas_agent.invoke(input)

from langchain.tools import Tool

pandas_tool = Tool(
    name="load_tables",
    func=call_pandas_agent,
    description="create new tables from 'main_df', outside of main aggregation functions and answer questions about data. rather than using this initially, first verify necessary columns have been added from outfile to the main dataframe with the user"
)

class Question(BaseModel):
    question: str = Field(description="The question to ask the user to understand what they're choosing")
    choices: List[str] = Field(description="The possible values for the field")

class Questions(BaseModel):
    questions: List[Question] = Field(description="The list of questions to ask the user to understand their inputs")

@tool(args_schema=Questions)
def ask_for_clarification(questions: List[Question]):
    """
    Call this tool to ensure inputs are accurate for each parameter going to tool calls, if it's ambiguous - in particular adding any fields from the outfile we should confirm the field names.
    Ask a targeted list of questions to get the exact values for each parameter.
    """
    
    responses = []
    for question in questions:
        request: HumanInterrupt = {
            "action_request": {
                "action": "clarification",
                "question": question.question,
                "choices": question.choices
            },
            "description": "Please specify the precise parameters"
        }
        
        response = interrupt([request])[0]
        responses.append({'question': question.question, 'response': response['args']})
    return responses

@tool
def create_summary_table(
    index: str,
    columns: str,
    values: str,
    query_filter: Optional[str] = None,
    aggfunc: str = 'sum'
) -> str:
    """
    Creates a customized pivot table from the main dataset.

    Use this tool to generate a summary table from the data. You can specify
    what the rows and columns should be, what values to display, and an
    optional filter to apply before summarizing.

    Args:
        index: The column to use for the table's rows (e.g., 'arm').
        columns: The column to use for the table's columns (e.g., 'Gender').
        values: The column to aggregate for the cell values (usually 'Value').
        query_filter: An optional string to filter the data before pivoting,
                      written as a pandas query (e.g., "Metric == 'CHD_DEATH' and `Age Range` == 'All Ages (Total)'").
        aggfunc: The aggregation function to use (e.g., 'sum', 'mean'). Defaults to 'sum'.

    Returns:
        A string containing the formatted markdown table of the summary.
    """
    try:
        df, _ = load_df()

        # 1. Apply the filter if provided
        if query_filter:
            # Note: Using backticks for column names with spaces is important for the .query() method
            filtered_df = df.query(query_filter)
        else:
            filtered_df = df

        # 2. Create the pivot table
        summary_table = filtered_df.pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc
        )

        # 3. Format the output as a markdown string for clean presentation
        return summary_table.to_markdown()

    except Exception as e:
        return f"An error occurred: {e}. Please check your column names and filter syntax."


# Augment the LLM with tools
tools = [add_deltas, groupby_metric, groupby_age_range, append_from_outfile, ask_for_clarification, divide, multiply, subtract, create_summary_table]
tools_by_name = {tool.name: tool for tool in tools}

llm = init_chat_model("anthropic:claude-sonnet-4-5-20250929")
llm_with_tools = llm.bind_tools(tools)

# CSV logging for tool calls
TOOL_CALLS_LOG = "tool_calls_log.csv"

def log_tool_call_to_csv(tool_name: str, args: dict, status: str = "success", error: str = None):
    """Log tool call to CSV file"""
    timestamp = datetime.now().isoformat()
    file_exists = os.path.exists(TOOL_CALLS_LOG)
    
    with open(TOOL_CALLS_LOG, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'tool_name', 'arguments', 'status', 'error'])
        writer.writerow([timestamp, tool_name, json.dumps(args), status, error or ''])

def replay_tool_calls_from_csv(csv_file: str = TOOL_CALLS_LOG, filter_status: str = "success"):
    """
    Read tool calls from CSV and execute them
    
    Args:
        csv_file: Path to the CSV file containing tool calls
        filter_status: Only replay calls with this status (default: "success")
    
    Returns:
        List of results from executed tool calls
    """
    if not os.path.exists(csv_file):
        print_out(f"❌ CSV file '{csv_file}' not found")
        return []
    
    results = []
    print_out(f"📖 Reading tool calls from '{csv_file}'")
    
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            tool_name = row['tool_name']
            status = row['status']
            
            if tool_name in ['ask_for_clarification', 'create_summary_table']:
                continue
            # Skip if not matching filter status
            if filter_status and status != filter_status:
                print_out(f"⏭️  Skipping call {i}: {tool_name} (status: {status})")
                continue
            
            try:
                # Parse arguments from JSON
                args = json.loads(row['arguments'])
                
                # Get the tool function
                if tool_name not in tools_by_name:
                    print_out(f"❌ Tool '{tool_name}' not found in available tools")
                    continue
                
                tool = tools_by_name[tool_name]
                
                print_out(f"▶️  Executing call {i}: {tool_name}")
                print_out(f"   Arguments: {args}")
                
                # Execute the tool
                result = tool.invoke(args)
                results.append({
                    'call_number': i,
                    'tool_name': tool_name,
                    'args': args,
                    'result': result,
                    'status': 'success'
                })
                
                print_out(f"✅ Call {i} completed successfully")
                
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                print_out(f"❌ Call {i} failed: {error_msg}")
                results.append({
                    'call_number': i,
                    'tool_name': tool_name,
                    'args': args,
                    'status': 'error',
                    'error': error_msg
                })
    
    print_out(f"\n📊 Replay complete: {len(results)} calls executed")
    return results

def tool_node(state: dict):
    """Performs the tool call with automatic retry on parameter errors"""
    from pydantic import ValidationError
    
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        
        # Log the tool call before execution
        log_tool_call_to_csv(tool_call["name"], tool_call["args"], "pending")
        
        try:
            # Attempt to invoke the tool with provided arguments
            observation = tool.invoke(tool_call["args"])
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "success")
            graph.update_state(config, {'approved': True})
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        
        except GraphInterrupt:
            # Re-raise HumanInterrupt exceptions - these are part of normal flow, not errors
            raise
            
        except ValidationError as e:
            # Pydantic validation error - parameters don't match schema
            error_details = "; ".join([f"{' -> '.join(str(x) for x in err['loc'])}: {err['msg']}" for err in e.errors()])
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "validation_error", error_details)
            
            error_msg = f"❌ Tool '{tool_call['name']}' called with invalid parameters.\n\n"
            error_msg += "Validation errors:\n"
            for error in e.errors():
                field = " -> ".join(str(x) for x in error['loc'])
                error_msg += f"  • Field '{field}': {error['msg']}\n"
            error_msg += f"\nProvided arguments: {tool_call['args']}\n"
            error_msg += f"\nPlease retry with correct parameters matching the tool's schema."
            
            result.append(ToolMessage(
                content=error_msg,
                tool_call_id=tool_call["id"],
                status="error"
            ))
            
        except TypeError as e:
            # Type error - wrong argument types or missing required arguments
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "type_error", str(e))
            
            error_msg = f"❌ Tool '{tool_call['name']}' called with wrong argument types.\n\n"
            error_msg += f"Error: {str(e)}\n"
            error_msg += f"Provided arguments: {tool_call['args']}\n"
            error_msg += f"\nPlease retry with correct parameter types."
            
            result.append(ToolMessage(
                content=error_msg,
                tool_call_id=tool_call["id"],
                status="error"
            ))
            
        except ValueError as e:
            # Value error - invalid values for parameters
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "value_error", str(e))
            
            error_msg = f"❌ Tool '{tool_call['name']}' called with invalid parameter values.\n\n"
            error_msg += f"Error: {str(e)}\n"
            error_msg += f"Provided arguments: {tool_call['args']}\n"
            error_msg += f"\nPlease retry with valid parameter values."
            
            result.append(ToolMessage(
                content=error_msg,
                tool_call_id=tool_call["id"],
                status="error"
            ))
            
        except KeyError as e:
            # Key error - referencing non-existent keys
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "key_error", str(e))
            
            error_msg = f"❌ Tool '{tool_call['name']}' referenced a non-existent key.\n\n"
            error_msg += f"Error: Key {str(e)} not found\n"
            error_msg += f"Provided arguments: {tool_call['args']}\n"
            error_msg += f"\nPlease check available keys and retry."
            
            result.append(ToolMessage(
                content=error_msg,
                tool_call_id=tool_call["id"],
                status="error"
            ))
            
        except Exception as e:
            # Catch-all for any other errors
            log_tool_call_to_csv(tool_call["name"], tool_call["args"], "error", f"{type(e).__name__}: {str(e)}")
            
            error_msg = f"❌ Tool '{tool_call['name']}' execution failed.\n\n"
            error_msg += f"Error type: {type(e).__name__}\n"
            error_msg += f"Error: {str(e)}\n"
            error_msg += f"Provided arguments: {tool_call['args']}\n"
            error_msg += f"\nPlease analyze the error and retry with corrected parameters."
            
            result.append(ToolMessage(
                content=error_msg,
                tool_call_id=tool_call["id"],
                status="error"
            ))
    
    return {"messages": result}

example = """
Documentation: Total Acute MI Deaths Calculation

## Objective
Calculate the total acute myocardial infarction (MI) deaths difference from baseline across all intervention scenarios.

## Definition
**Total Acute MI Deaths** = Sum of acute MI deaths across two population metrics:
1. Acute MI deaths in Bridge & DH populations combined
2. Acute MI deaths in Bridge population only

**Note**: These are separate accounting metrics in the model's output, and summing them gives the complete total of acute MI deaths.

## Required Metrics from Outfile

### Component Metrics:
- `"Acute CHD Deaths (Bridge & DH)-MI"` - Acute MI deaths from Bridge & DH combined accounting
- `"Acute CHD Deaths (Bridge)-MI"` - Acute MI deaths from Bridge-only accounting

### Why Both Metrics?
The model outputs these as separate metrics that need to be summed together to get the true total of all acute MI deaths in the simulation.
Bridge is the bridge for DE, and Bridge & DH covers the DH population

## Calculation Steps

### Step 1: Append Component Metrics
Add both component metrics from ".out" to ".dat":
```
append_from_outfile("Acute CHD Deaths (Bridge & DH)-MI")
append_from_outfile("Acute CHD Deaths (Bridge)-MI")
```

### Step 2: Create Summed Metric
Use groupby_sum to create a new combined metric:
```
groupby_sum(
    label="Total Acute MI Deaths",
    components=[
        "Acute CHD Deaths (Bridge & DH)-MI",
        "Acute CHD Deaths (Bridge)-MI"
    ],
    key_column="Metric"
)
```

"""



class State(TypedDict):
    messages: Annotated[list, add_messages]
    df: pd.DataFrame
    approved: bool


system_message_template = SystemMessagePromptTemplate.from_template(
    """You are an expert data analysis assistant for cardiovascular disease (CVD) microsimulation model researchers. Your primary role is to help researchers transform and analyze model output data from .dat and .out files.

## Your Core Capabilities

You help researchers:
1. **Build augmented data tables** by combining metrics from multiple sources
2. **Calculate derived metrics** (sums, ratios, differences, deltas)
3. **Create summary tables** for analysis and reporting
4. **Answer questions** about the processed data

## Data Context

The data you work with represents CVD model simulation outputs containing:
- **Metrics**: Health outcomes (CHD_DEATH, STROKE_DEATH, PREV, INC_CHD, etc.)
- **Arms**: Different intervention scenarios being compared
- **Demographics**: Broken down by Gender (M/F) and Age Range (35-44, 45-54, etc.)
- **Data sources**:
  - `.dat files`: Main baseline data already loaded into main_df
  - `.out files`: Additional time-series metrics that can be imported

## Critical Workflow Requirements

### ALWAYS START WITH CLARIFICATION
Before making ANY tool calls, you MUST:
1. Understand the user's complete analytical goal
2. Identify ALL required metrics and their exact names
3. Use `ask_for_clarification` to confirm:
   - Exact metric names from available options
   - Which arms to compare
   - Age ranges and demographics of interest
   - Whether they want absolute differences or percentages

**Never assume or guess parameter values.** Always verify against available data.

### Tool Usage Patterns

**For adding metrics from .out files:**
1. FIRST check if metric already exists in main_df metrics: {metrics}
2. If not, verify exact metric name in available outfile metrics: {outfile_metrics}
3. Use `ask_for_clarification` to confirm the exact metric name and parameters
4. Then call `append_from_outfile` with confirmed parameters

**For creating derived metrics:**
1. Verify all component metrics exist
2. Confirm the label follows naming convention (alphanumeric, _, +, -, \\, $, #, /)
3. Use appropriate tool: `groupby_metric`, `divide`, `multiply`, or `subtract`

**For calculating differences between arms:**
1. Confirm both arms exist in available arms
2. Clarify if user wants absolute difference or percent change
3. Specify relevant age ranges
4. Use `add_deltas` tool

**For creating summary tables:**
1. Confirm the structure (rows, columns, values)
2. Verify any filters reference valid column values
3. Use `create_summary_table` tool

## Available Data Reference

**Current main_df state:**
- Age Ranges: {age_ranges}
- Columns: {columns}
- Metrics: {metrics}

**Available outfile metrics** (not yet in main_df): {outfile_metrics}

## Response Guidelines

1. **Be conversational but precise** - Explain what you're doing and why
2. **Show your reasoning** - Walk through analytical steps
3. **Validate before executing** - Always confirm ambiguous parameters
4. **Provide context** - Explain what metrics mean if relevant
5. **Format output clearly** - Use markdown tables for summaries
6. **Handle errors gracefully** - If a tool call fails, explain why and suggest corrections

## Example Workflow

User: "I need total acute MI deaths compared between baseline and intervention"

Your response should:
1. Acknowledge the goal
2. Ask clarifying questions about:
   - Which specific acute MI metrics to use
   - Which arms represent baseline vs intervention
   - Whether they want absolute or percent difference
   - Which age ranges to include
3. Only after confirmation, execute the tool calls
4. Explain what you calculated
5. Present the results in a clear table

## Quality Standards for Augmented Data Files

Remember that researchers will use your output files (.dat files in augmented_dat/) as starting points for further analysis. Ensure:
- Metric labels are clear and self-documenting
- Calculations are correct and validated
- Age range aggregations maintain consistency
- Delta calculations specify whether they're absolute or percent

## Working Example

{example}

Now, carefully analyze the user's request and proceed methodically."""
)

# Define a human message template (optional, for user input)
human_message_template = HumanMessagePromptTemplate.from_template("{user_input}")

# Combine them into a ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template,
])

def chatbot(state: State):
    chain = prompt | llm_with_tools
    return {"messages": [chain.invoke({"user_input": state["messages"],
                                       "age_ranges": str(list(init_df['Age Range'].unique())),
                                       "columns": str(init_df.columns.tolist()),
                                       "metrics": str(list(init_df['Metric'].unique())),
                                       "outfile_metrics": str(list(list(outfile_dfs.values())[0].keys())),
                                       "example": example
                                       })]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)


memory = InMemorySaver()
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "2"}}


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode='updates'):
        if '__interrupt__' in event:
            return event['__interrupt__'][0].value[0]
        for value in event.values():
            
            if type(value) != dict:
                break
            
            if (type(value["messages"][-1].content) == str) and (value["messages"][-1].type != "tool"):
                print_out(value["messages"][-1].content)
    
    
    
# Parse command-line arguments
def main():
    parser = argparse.ArgumentParser(description='CVD Model Agent - LLM tool calling with CSV logging and replay')
    parser.add_argument('--replay', action='store_true', 
                       help='Enable replay mode to execute tool calls from CSV')
    parser.add_argument('--csv', type=str, default=TOOL_CALLS_LOG,
                       help=f'CSV file to replay from (default: {TOOL_CALLS_LOG})')
    parser.add_argument('--filter-status', type=str, default='success',
                       help='Only replay calls with this status (default: success)')
    
    args = parser.parse_args()

    if args.replay:
        print_out("🔄 REPLAY MODE ENABLED")
        print_out(f"Reading tool calls from: {args.csv}")
        print_out("-" * 50)
        
        # Execute replay
        results = replay_tool_calls_from_csv(args.csv, filter_status=args.filter_status)
        
        print_out("-" * 50)
        print_out(f"✅ Replay complete!")
        print_out(f"Total calls executed: {len(results)}")
        
        # Show summary
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = sum(1 for r in results if r['status'] == 'error')
        print_out(f"Successful: {success_count}")
        print_out(f"Failed: {error_count}")
        
    else:
        # Normal interactive mode
        graph.update_state(config, {'approved': False})
        interrupt_content = None
        while True:
            
            while interrupt_content is not None:
                interrupt_content = interrupt_content['action_request']
                choices = list(enumerate(interrupt_content['choices']))
                formatted_choices = '\n'.join([f"{n+1}: {c}" for n ,c in choices])
                res = None
                while res is None:
                    choice_id_list = {str(id+1): id  for id,_ in choices}
                    formatted_id_list = ','.join(choice_id_list.keys())
                    formatted_id_list += ',specify'
                    user_input = input(f"{interrupt_content['question']}: \n{formatted_choices}\n({formatted_id_list}):")
                    if user_input in choice_id_list:
                        res = choices[choice_id_list[user_input]][1]
                    else:
                        res = user_input

                for event in graph.stream(
                    Command(resume=[{"type": "accept", "args": res}]),
                    config,
                    stream_mode='updates'
                ):
                    interrupt_content = None
                    if '__interrupt__' in event:
                        interrupt_content = event['__interrupt__'][0].value[0]
                        break
                    for value in event.values():
                        if type(value) != dict:
                            break
                        if (type(value["messages"][-1].content) == str) and (value["messages"][-1].type != "tool"):
                            print_out(value["messages"][-1].content)
                    
            else:
                user_input = input("Analysis to add to .dat file: ")
                graph.update_state(config, {'approved': False})
                if user_input.lower() in ["quit", "exit", "q"]:
                    print_out("Goodbye!")
                    break

                interrupt_content = stream_graph_updates(user_input)

if __name__ == '__main__':
    main()

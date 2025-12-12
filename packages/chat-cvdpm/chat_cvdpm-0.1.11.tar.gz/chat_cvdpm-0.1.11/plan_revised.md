# Revised Refactoring Plan: State-Based DataFrame Management

## Overview
Refactor the agent to use `state.py` for centralized DataFrame tracking, replacing the current Command-based state update pattern. DataFrames will be organized into three categories with a simplified storage model.

## Clarifications from Review
- ✅ `df` field in State TypedDict is unused - safe to remove
- ✅ `chatbot()` called every turn - `get_context_summary()` is not expensive
- ✅ Keep DataFrame unified (not split by arm) - simpler architecture
- ✅ Use best judgment for testing - no need for elaborate test infrastructure

## Three DataFrame Categories

### 1. **Elevated DataFrame** (from .dat files)
- **Source**: `.dat` files in project root
- **Structure**: `['Metric', 'Gender', 'Age Range', 'Value', 'arm', 'is_delta', 'is_percent_delta']`
- **Storage**: Single unified `session_state.elevated_df`
- **Characteristics**: Core data that all operations build upon

### 2. **Outfile DataFrames** (from .out/.frmt files)
- **Source**: `.out` files processed by `format.py`
- **Structure**: `['Gender', 'Age Range', 'Value', 'year']` per metric
- **Storage**: `session_state.outfile_dfs` as `{arm_name: {metric_name: DataFrame}}`
- **Characteristics**: Temporal data used to append aggregated metrics

### 3. **Custom DataFrames** (from pandas_exec)
- **Source**: User-generated via `execute_pandas` tool
- **Structure**: Arbitrary (user-defined)
- **Storage**: `session_state.custom_dfs` as `{name: DataFrame}`
- **Characteristics**: Session-only, fully custom transformations

## Implementation Steps

### Step 1: Enhance state.py

**File**: `src/chat_cvdpm/state.py`

**Replace entire file with**:

```python
# state.py
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import pandas as pd

@dataclass
class SessionState:
    # Single unified DataFrame for elevated data
    elevated_df: Optional[pd.DataFrame] = None

    # Outfile DataFrames: {arm_name: {metric_name: DataFrame}}
    outfile_dfs: Dict[str, Dict[str, pd.DataFrame]] = field(default_factory=dict)

    # Custom user-created DataFrames: {name: DataFrame}
    custom_dfs: Dict[str, pd.DataFrame] = field(default_factory=dict)

    # Metadata for custom DataFrames: {name: description}
    custom_metadata: Dict[str, str] = field(default_factory=dict)

    # Transformation history
    transformation_history: List[str] = field(default_factory=list)

    def register_elevated_df(self, df: pd.DataFrame):
        """Register the main elevated DataFrame (unified, not split by arm)"""
        required_cols = {'Metric', 'Gender', 'Age Range', 'Value', 'arm'}
        if not required_cols.issubset(set(df.columns)):
            raise ValueError(f"Elevated DataFrame must have columns: {required_cols}")
        self.elevated_df = df

    def register_outfile_dfs(self, arm_name: str, dfs: Dict[str, pd.DataFrame]):
        """Register outfile DataFrames for a specific arm"""
        self.outfile_dfs[arm_name] = dfs

    def register_custom_df(self, name: str, df: pd.DataFrame, description: str = ""):
        """Register a custom user-created DataFrame"""
        self.custom_dfs[name] = df
        self.custom_metadata[name] = description

    def get_elevated_df(self) -> pd.DataFrame:
        """Get the unified elevated DataFrame"""
        if self.elevated_df is None:
            raise ValueError("Elevated DataFrame not initialized")
        return self.elevated_df

    def get_outfile_df(self, arm_name: str, metric: str) -> pd.DataFrame:
        """Get a specific outfile DataFrame"""
        if arm_name not in self.outfile_dfs:
            raise KeyError(f"Arm '{arm_name}' not found in outfile DataFrames")
        if metric not in self.outfile_dfs[arm_name]:
            raise KeyError(f"Metric '{metric}' not found for arm '{arm_name}'")
        return self.outfile_dfs[arm_name][metric]

    def get_custom_df(self, name: str) -> pd.DataFrame:
        """Get a custom DataFrame by name"""
        if name not in self.custom_dfs:
            raise KeyError(f"Custom DataFrame '{name}' not found")
        return self.custom_dfs[name]

    def get_all_elevated_metrics(self) -> List[str]:
        """Get list of all unique metrics in elevated DataFrame"""
        if self.elevated_df is None:
            return []
        return list(self.elevated_df['Metric'].unique())

    def get_all_outfile_metrics(self) -> List[str]:
        """Get list of all unique outfile metrics across all arms"""
        all_metrics = set()
        for arm_dfs in self.outfile_dfs.values():
            all_metrics.update(arm_dfs.keys())
        return sorted(list(all_metrics))

    def get_all_arms(self) -> List[str]:
        """Get list of all arms in elevated DataFrame"""
        if self.elevated_df is None:
            return []
        return list(self.elevated_df['arm'].unique())

    def list_custom_dfs(self) -> List[Tuple[str, str]]:
        """List all custom DataFrames with their descriptions"""
        return [(name, self.custom_metadata.get(name, ""))
                for name in self.custom_dfs.keys()]

    def get_context_summary(self) -> str:
        """Generate a summary of current state for LLM context"""
        lines = []

        # Elevated DataFrame
        if self.elevated_df is not None:
            lines.append("### Elevated DataFrame (Main Data)")
            lines.append(f"Shape: {self.elevated_df.shape}")
            lines.append(f"Arms: {list(self.elevated_df['arm'].unique())}")
            lines.append(f"Metrics: {len(self.elevated_df['Metric'].unique())} unique")
            lines.append(f"Age Ranges: {list(self.elevated_df['Age Range'].unique())}")

        # Outfile DataFrames
        if self.outfile_dfs:
            lines.append("\n### Outfile DataFrames (By-Year Source Data)")
            for arm, metrics_dict in self.outfile_dfs.items():
                lines.append(f"Arm '{arm}': {len(metrics_dict)} metrics available")

        # Custom DataFrames
        if self.custom_dfs:
            lines.append("\n### Custom DataFrames (User-Created)")
            for name, desc in self.list_custom_dfs():
                df = self.custom_dfs[name]
                lines.append(f"'{name}': {desc}")
                lines.append(f"  Shape: {df.shape}, Columns: {list(df.columns)}")

        return "\n".join(lines)

# Global state instance
session_state = SessionState()
```

### Step 2: Update pandas_exec.py

**File**: `src/chat_cvdpm/pandas_exec.py`

**Replace entire file with**:

```python
# pandas_exec.py
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from .state import session_state
import pandas as pd
import numpy as np

class PandasExecInput(BaseModel):
    code: str = Field(description="Pandas code to execute. All registered DataFrames are available by name.")
    result_name: str = Field(default=None, description="Optional name to register the result DataFrame under")
    description: str = Field(default="", description="Optional description of what this DataFrame contains")

@tool(args_schema=PandasExecInput)
def execute_pandas(code: str, result_name: str = None, description: str = "") -> str:
    """
    Execute arbitrary pandas code against the current dataframes.

    Available DataFrames:
    - elevated_df: Main elevated DataFrame with all metrics
    - outfile_dfs: Dict of outfile DataFrames (nested: arm -> metric -> df)
    - custom_dfs: Dict of custom user-created DataFrames

    Also available: pd (pandas), np (numpy)

    Args:
        code: Pandas code to execute
        result_name: If provided and code returns a DataFrame, register it with this name
        description: Description of the result DataFrame

    Returns:
        String representation of the result
    """
    namespace = {
        "pd": pd,
        "np": np,
        "elevated_df": session_state.get_elevated_df(),
        "outfile_dfs": session_state.outfile_dfs,
        "custom_dfs": session_state.custom_dfs,
    }

    try:
        # Try to evaluate as expression first
        exec_result = eval(code, namespace)
    except SyntaxError:
        # If it's statements, use exec
        exec(code, namespace)
        exec_result = namespace.get("result", "Code executed successfully")

    # Register result if it's a DataFrame and name provided
    if result_name and isinstance(exec_result, pd.DataFrame):
        final_desc = description or f"Created via: {code[:50]}..."
        session_state.register_custom_df(result_name, exec_result, final_desc)
        return f"DataFrame '{result_name}' registered successfully.\n{exec_result.to_string()}"

    # Return useful representation
    if isinstance(exec_result, pd.DataFrame):
        return f"DataFrame result:\n{exec_result.to_string()}"
    return str(exec_result)
```

### Step 3: Update agent.py - Add Imports and Initialize State

**File**: `src/chat_cvdpm/agent.py`

**Add after line 42** (after existing imports):
```python
from .state import session_state
from .pandas_exec import execute_pandas
```

**Replace lines 146-152** (outfile loading):
```python
# Load outfile DataFrames into session state
outfiles = [f for f in os.listdir('.') if f.endswith('.out')]
for o in outfiles:
    arm_name = o[:-4]
    dfs = get_dfs(arm_name)
    session_state.register_outfile_dfs(arm_name, dfs)
```

**Replace lines 218-219** (elevated df loading):
```python
# Load elevated DataFrame into session state
init_df, metadata_df = load_df('.\\')
session_state.register_elevated_df(init_df)
init_df = session_state.get_elevated_df()  # Keep for Enum creation
```

**Update lines 225-232** (Enum creation - use session_state methods):
```python
MetricEnum = Enum('MetricEnum', [(m,m) for m in session_state.get_all_elevated_metrics()])
AgeRangeEnum = Enum('AgeRangeEnum', [(m,m) for m in list(init_df['Age Range'].unique())])
ColumnEnum = Enum('ColumnEnum', [(c,c) for c in list(init_df.columns.tolist())])
ArmEnum = Enum('ArmEnum', [(m,m) for m in session_state.get_all_arms()])

DatfileEnum = Enum('DatfileEnum', [(m,m) for m in session_state.get_all_arms()])
OutfileEnum = Enum('OutfileEnum', [(m,m) for m in set(session_state.outfile_dfs.keys()) & set([a[:-4] for a in session_state.get_all_arms()])])
OutfileMetricEnum = Enum('OutfileMetricEnum', [(m,m) for m in session_state.get_all_outfile_metrics()])
```

### Step 4: Update agent.py - Update Helper Functions

**File**: `src/chat_cvdpm/agent.py`

**Update `load_df()` function (lines 191-216)** to sync with session_state:
```python
def load_df(dir='augmented_dat\\'):
    if 'df.parquet' in os.listdir(dir):
        total_df = pd.read_parquet(dir + 'df.parquet')
        session_state.register_elevated_df(total_df)
        return total_df, None

    files = []
    for file_name in os.listdir('.'):
        if not file_name.endswith('.dat'):
            continue
        with open((dir if dir is not None else '') + file_name, "r") as file:
            content = file.read()

        df_wide = parse_irregular_table(content)
        df_tidy = restructure_to_tidy_format(df_wide)
        df_tidy['arm'] = file_name
        files.append({'name': file_name, 'df': df_tidy})

    df_metadata = {
        'experiment_arm': [f['name'] for f in files],
    }

    total_df = pd.concat([f['df'] for f in files])
    session_state.register_elevated_df(total_df)
    return total_df, df_metadata
```

**Update `write_augmented_files()` function (lines 154-189)** to use session_state:
```python
def write_augmented_files(arms=None):
    import os
    OUTDIR = 'augmented_dat/'
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    total_df = session_state.get_elevated_df()

    if 'is_delta' not in total_df.columns:
        total_df['is_delta'] = False
    if 'is_percent_delta' not in total_df.columns:
        total_df['is_percent_delta'] = False

    total_df.to_parquet(OUTDIR + 'df.parquet')
    csv_dir = OUTDIR + '\\csv'
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    df_baseline = total_df.copy()
    df_baseline = df_baseline.fillna(0)
    df_baseline['Value'] = df_baseline['Value'].apply(lambda x: f"{x:.2f}" if abs(x - round(x))>0 else str(int(x)))
    delta_modifider = df_baseline.apply(lambda x: 'delta ' if x['is_delta'] else '\% delta' if x['is_percent_delta'] else '', axis=1)
    df_baseline['Column_Header'] = delta_modifider + df_baseline['Gender'] + ' ' + df_baseline['Age Range']

    if arms:
        df_baseline = df_baseline[df_baseline['arm'].isin(arms)]

    print_out(f"Saving '.dat' files {', '.join(list(df_baseline.arm.unique()))} to {OUTDIR}")

    for arm in df_baseline.arm.unique():
        table = df_baseline[df_baseline['arm'] == arm].pivot_table(
            index='Metric',
            columns='Column_Header',
            values='Value',
            aggfunc='first',
            fill_value=0,
            sort=False
        )
        path = os.path.join(OUTDIR, f'{arm}')
        with open(path, 'w') as f:
            f.write(table.to_string())
```

### Step 5: Update agent.py - Update All Tools to Remove Command Pattern

**Remove Command import (line 24)**:
```python
# DELETE: from langgraph.types import Command
```

**Update State TypedDict (lines 976-979)**:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    approved: bool
    # Removed: df field (unused)
```

**Update each tool to return string instead of Command**:

1. **`append_from_outfile` (line 240-276)**:
```python
@tool(args_schema=AppendFromOutfileInputs)
def append_from_outfile(metric: OutfileMetricEnum, arm: OutfileEnum, year_agg: AggEnum, label: str, years: Optional[List[int]] = None):
    """Append a metric from '.out' file to the main data table"""
    metric = metric.value
    arm = arm.value

    print_out(f"📊 Appending metric '{label}' from .out files to main dataframe for arm: {arm}")

    # Get data from session state
    outfile_df = session_state.get_outfile_df(arm, metric)
    elevated_df = session_state.get_elevated_df()

    # Aggregate by year
    if years and len(years) > 0:
        outfile_df = outfile_df[outfile_df['year'].isin(years)]
    outfile_df = outfile_df.groupby(['Age Range', 'Gender'])['Value'].agg(year_agg.value).reset_index()

    # Format to elevated structure
    filename = f'{arm}.dat'
    outfile_df['Metric'] = label
    outfile_df['arm'] = filename
    outfile_df['Value'] = outfile_df['Value'].fillna(0)
    outfile_df['is_delta'] = False
    outfile_df['is_percent_delta'] = False

    # Add aggregations
    outfile_df = groupby_sum(outfile_df, 'Sum', ['35-44', '45-54', '55-64', '65-74', '75-84', '85-94'], 'Age Range', save=False)
    totals = groupby_sum(outfile_df, 'M+F', ['M', 'F'], 'Gender', save=False)
    outfile_df = pd.concat([outfile_df, totals[(totals['Age Range'] == 'Sum') & (totals['Gender'] == 'M+F')]])

    # Update session state
    updated_df = pd.concat([elevated_df, outfile_df])
    session_state.register_elevated_df(updated_df)

    # Persist
    write_augmented_files([filename])

    return f"✅ Successfully appended metric '{label}' from outfile to elevated DataFrame for arm '{arm}'"
```

2. **`add_deltas` (line 284-357)**:
Replace the final return (line 357):
```python
    # Update state
    session_state.register_elevated_df(df_final)
    write_augmented_files()

    return f"✅ Successfully calculated {delta_type} deltas for '{arm1.value}' compared to '{arm2.value}'"
```

3. **`groupby_age_range` (line 367-387)**:
Replace return (line 387):
```python
    df = groupby_sum(df, label, components, 'Age Range')
    session_state.register_elevated_df(df)

    return f"✅ Successfully created age range '{label}' from {len(components)} components"
```

4. **`groupby_metric` (line 390-411)**:
Replace return (line 411):
```python
    df = groupby_sum(df, label, components, 'Metric')
    session_state.register_elevated_df(df)

    return f"✅ Successfully created metric '{label}' from {len(components)} components"
```

5. **`divide` (line 495-524)**:
Replace return (line 524):
```python
    df = perform_operation(df, 'Metric', label, col1, col2, div_op)
    session_state.register_elevated_df(df)
    write_augmented_files(df)

    return f"✅ Successfully created metric '{label}' by dividing {col1_desc} by {col2_desc}"
```

6. **`multiply` (line 526-550)**:
Replace return (line 550):
```python
    df = perform_operation(df, 'Metric', label, col1, col2, operator.mul)
    session_state.register_elevated_df(df)
    write_augmented_files(df)

    return f"✅ Successfully created metric '{label}' by multiplying {col1_desc} by {col2_desc}"
```

7. **`subtract` (line 552-578)**:
Replace return (line 578):
```python
    df = perform_operation(df, 'Metric', label, col1, col2, operator.sub)
    session_state.register_elevated_df(df)
    write_augmented_files(df)

    return f"✅ Successfully created metric '{label}' by subtracting {col2_desc} from {col1_desc}"
```

**Update `groupby_sum` helper (line 413-443)** to use session_state:
```python
def groupby_sum(df, label: str, components: List[str], key_column: str, save=True) -> pd.DataFrame:
    """Sum data from multiple values of age range, gender, metric, or arm"""
    value_column = 'Value'
    group_cols = [col for col in df.columns if col not in [key_column, value_column]]

    subset_df = df[df[key_column].isin(components)]
    aggregated_data = subset_df.groupby(group_cols).agg({
        value_column: 'sum'
    }).reset_index()

    aggregated_data[key_column] = label
    df_updated = pd.concat([df, aggregated_data], ignore_index=True)
    df = df_updated[df.columns]

    if save:
        session_state.register_elevated_df(df)
        write_augmented_files()

    return df
```

### Step 6: Update agent.py - Update Tools List and System Prompt

**Update tools list (line 731)**:
```python
tools = [add_deltas, groupby_metric, groupby_age_range, append_from_outfile,
         ask_for_clarification, divide, multiply, subtract, create_summary_table,
         execute_pandas]  # Add pandas_exec tool
tools_by_name = {tool.name: tool for tool in tools}
```

**Update system prompt (lines 982-1086)** - replace the data context section:
```python
## Available Data Reference

{context_summary}

**Available outfile metrics** (can be imported to main DataFrame): {outfile_metrics}
```

**Update chatbot function (lines 1098-1106)**:
```python
def chatbot(state: State):
    chain = prompt | llm_with_tools

    context_summary = session_state.get_context_summary()
    outfile_metrics = session_state.get_all_outfile_metrics()

    return {"messages": [chain.invoke({
        "user_input": state["messages"],
        "context_summary": context_summary,
        "outfile_metrics": str(outfile_metrics),
        "example": example
    })]}
```

### Step 7: Update load_df calls in tools

**Find all `load_df()` calls in tools** and replace with `session_state.get_elevated_df()`:

- Line 249 in `append_from_outfile`
- Line 292 in `add_deltas`
- Line 380 in `groupby_age_range`
- Line 403 in `groupby_metric`
- Line 508 in `divide`
- Line 539 in `multiply`
- Line 568 in `subtract`
- Line 706 in `create_summary_table`

Replace pattern:
```python
df, _ = load_df()
```
With:
```python
df = session_state.get_elevated_df()
```

## Testing Plan

### Manual Testing Sequence

1. **Test initialization**:
   - Run the agent
   - Verify it loads without errors
   - Check that session_state is populated

2. **Test append_from_outfile**:
   - Request to add a metric from .out file
   - Verify it appears in elevated_df
   - Check parquet file is updated

3. **Test execute_pandas**:
   - Create a simple custom DataFrame
   - Verify it's registered in session_state
   - Check agent can reference it

4. **Test existing functionality**:
   - Run a few commands from tool_calls_log.csv
   - Verify outputs match expected behavior

5. **Test state persistence**:
   - Make changes
   - Restart agent
   - Verify parquet loads correctly

## Summary of Changes

- ✅ Single unified `elevated_df` (not split by arm)
- ✅ Three-category DataFrame organization
- ✅ Command pattern completely removed
- ✅ Tools return descriptive strings
- ✅ Session state centralized in state.py
- ✅ pandas_exec integrated for custom DataFrames
- ✅ System prompt uses session_state context
- ✅ Parquet persistence maintained
- ✅ Backwards compatible with existing .dat/.out files

## Implementation Order

1. Update state.py (Step 1)
2. Update pandas_exec.py (Step 2)
3. Update agent.py imports and initialization (Step 3)
4. Update agent.py helper functions (Step 4)
5. Update agent.py tools (Step 5)
6. Update agent.py system prompt (Step 6)
7. Update load_df calls (Step 7)
8. Test manually

This approach is incremental and can be validated at each step.

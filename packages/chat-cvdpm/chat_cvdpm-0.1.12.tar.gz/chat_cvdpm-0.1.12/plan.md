# Refactoring Plan: State-Based DataFrame Management

## Overview
Refactor the agent to use `state.py` for centralized DataFrame tracking, replacing the current Command-based state update pattern. This will organize DataFrames into three categories and enable better reference and management.

## Current State Analysis

### Current Architecture
- **agent.py (line 146-152)**: Loads .out files into `outfile_dfs` dict at module level
- **agent.py (line 218)**: Loads .dat files into `init_df` at module level
- **Command Pattern (lines 276, 357, 387, 411, 524, 550, 578)**: Tools return `Command(update=state_update)` with metadata strings
- **State TypedDict (lines 976-979)**: Contains `messages`, `df`, and `approved` fields
- **No tracking of dynamically created DataFrames**: DataFrames created by pandas_exec are not registered

### Current Data Flow
1. `.dat` files → parsed → `init_df` (elevated format with Metric/Gender/Age Range/Value/arm)
2. `.out` files → `get_dfs()` → `outfile_dfs` dict (by-year format)
3. Tools modify `augmented_dat/df.parquet` file
4. Each tool reloads via `load_df()` and writes back via `write_augmented_files()`

## Proposed Architecture

### Three DataFrame Categories

#### 1. **Elevated DataFrames** (from .dat files)
- **Source**: `.dat` files in project root
- **Structure**: Wide format with columns `['Metric', 'Gender', 'Age Range', 'Value', 'arm', 'is_delta', 'is_percent_delta']`
- **Characteristics**:
  - Must maintain consistent structure throughout session
  - Core data that all other operations build upon
  - Loaded once at initialization
- **Storage in state**: `session_state.elevated_dfs`
- **Registration**: Auto-registered on load with arm name as key

#### 2. **Outfile DataFrames** (from .out/.frmt files)
- **Source**: `.out` files processed by `format.py`
- **Structure**: Long format with columns `['Gender', 'Age Range', 'Value', 'year']`
- **Characteristics**:
  - Organized by year (temporal data)
  - Read-only after loading
  - Used to append aggregated metrics to elevated DataFrames
- **Storage in state**: `session_state.outfile_dfs`
- **Registration**: Nested dict structure: `{arm_name: {metric_name: DataFrame}}`

#### 3. **Custom DataFrames** (from pandas_exec)
- **Source**: User-generated via `execute_pandas` tool
- **Structure**: Arbitrary (user-defined)
- **Characteristics**:
  - Created dynamically during session
  - Fully custom transformations
  - Can be referenced by name in subsequent operations
- **Storage in state**: `session_state.custom_dfs`
- **Registration**: User provides name and description via tool parameter

## Implementation Steps

### Step 1: Enhance state.py
**File**: `src/chat_cvdpm/state.py`

**Changes**:
1. Add three separate DataFrame collections:
   - `elevated_dfs: dict[str, pd.DataFrame]` - keyed by arm name
   - `outfile_dfs: dict[str, dict[str, pd.DataFrame]]` - nested: arm → metric → df
   - `custom_dfs: dict[str, pd.DataFrame]` - keyed by user-provided name

2. Add type-specific registration methods:
   - `register_elevated_df(arm_name: str, df: pd.DataFrame)`
   - `register_outfile_dfs(arm_name: str, dfs: dict[str, pd.DataFrame])`
   - `register_custom_df(name: str, df: pd.DataFrame, description: str)`

3. Add validation:
   - Validate elevated_df structure (required columns)
   - Validate outfile_df structure (required columns)
   - No validation for custom_dfs (user responsibility)

4. Add query methods:
   - `get_elevated_df(arm_name: str) -> pd.DataFrame`
   - `get_outfile_df(arm_name: str, metric: str) -> pd.DataFrame`
   - `get_custom_df(name: str) -> pd.DataFrame`
   - `get_all_elevated_metrics() -> List[str]`
   - `get_all_outfile_metrics() -> List[str]`
   - `list_custom_dfs() -> List[Tuple[str, str]]` - returns (name, description) pairs

5. Update `get_context_summary()`:
   - Separate sections for each DataFrame type
   - Show structure/schema expectations for elevated/outfile
   - Show descriptions for custom DataFrames

### Step 2: Update pandas_exec.py
**File**: `src/chat_cvdpm/pandas_exec.py`

**Changes**:
1. Import updated `session_state` from state.py

2. Update `execute_pandas` tool:
   - Add `description` parameter for better documentation
   - Make all three DataFrame collections available in namespace:
     ```python
     namespace = {
         "pd": pd,
         "np": np,
         "elevated_dfs": session_state.elevated_dfs,
         "outfile_dfs": session_state.outfile_dfs,
         "custom_dfs": session_state.custom_dfs,
     }
     ```
   - When `result_name` is provided, register result in `custom_dfs`:
     ```python
     if result_name and isinstance(exec_result, pd.DataFrame):
         session_state.register_custom_df(result_name, exec_result, description or f"Created via: {code[:50]}...")
     ```

3. Update tool description to explain DataFrame access patterns

### Step 3: Update agent.py - Initialization
**File**: `src/chat_cvdpm/agent.py`

**Changes**:

1. **Import state module** (after line 42):
   ```python
   from .state import session_state
   ```

2. **Replace module-level data loading** (lines 146-152):
   - Remove `outfiles = ...` and `outfile_dfs = {}`
   - Replace with:
     ```python
     # Load outfile DataFrames into state
     outfiles = [f for f in os.listdir('.') if f.endswith('.out')]
     for o in outfiles:
         arm_name = o[:-4]
         dfs = get_dfs(arm_name)
         session_state.register_outfile_dfs(arm_name, dfs)
     ```

3. **Replace init_df loading** (line 218):
   - Replace `init_df, metadata_df = load_df('.\\')` with:
     ```python
     # Load elevated DataFrames into state
     elevated_df, metadata_df = load_df('.\\')
     # Split by arm and register each
     for arm in elevated_df['arm'].unique():
         arm_df = elevated_df[elevated_df['arm'] == arm]
         session_state.register_elevated_df(arm, arm_df)
     ```

4. **Update Enum creation** (lines 225-232):
   - Replace direct `init_df` references with `session_state.get_all_elevated_metrics()`, etc.
   - Change:
     ```python
     MetricEnum = Enum('MetricEnum', [(m,m) for m in session_state.get_all_elevated_metrics()])
     OutfileMetricEnum = Enum('OutfileMetricEnum', [(m,m) for m in session_state.get_all_outfile_metrics()])
     ```

### Step 4: Update agent.py - Remove Command Pattern
**File**: `src/chat_cvdpm/agent.py`

**Changes**:

1. **Remove Command import** (line 24):
   - Delete `from langgraph.types import Command`

2. **Update State TypedDict** (lines 976-979):
   - Remove `df: pd.DataFrame` field (unused)
   - Keep `messages` and `approved`
   - Add session state reference if needed

3. **Update all tool return statements**:
   Replace pattern:
   ```python
   state_update = {
       "age_ranges": str(list(df['Age Range'].unique())),
       "columns": str(df.columns.tolist()),
       "metrics": str(list(df['Metric'].unique())),
   }
   return Command(update=state_update)
   ```

   With:
   ```python
   return f"Successfully added metric '{label}' to elevated DataFrame"
   ```

   **Affected locations**:
   - `append_from_outfile` (line 276)
   - `add_deltas` (line 357)
   - `groupby_age_range` (line 387)
   - `groupby_metric` (line 411)
   - `divide` (line 524)
   - `multiply` (line 550)
   - `subtract` (line 578)

### Step 5: Update agent.py - Tool Implementations
**File**: `src/chat_cvdpm/agent.py`

**Changes**:

1. **Update `load_df()` function** (lines 191-216):
   - Change to work with session_state
   - Return combined elevated DataFrame from all arms
   ```python
   def load_df(dir='augmented_dat\\'):
       if 'df.parquet' in os.listdir(dir):
           total_df = pd.read_parquet(dir + 'df.parquet')
           # Update session state with loaded data
           for arm in total_df['arm'].unique():
               arm_df = total_df[total_df['arm'] == arm]
               session_state.register_elevated_df(arm, arm_df)
           return total_df, None
       # ... rest of function
   ```

2. **Update `write_augmented_files()` function** (lines 154-189):
   - Accept arm names to write
   - Pull from session_state instead of passed DataFrame
   ```python
   def write_augmented_files(arms=None):
       # Combine all elevated DataFrames
       all_arms = session_state.elevated_dfs.keys() if arms is None else arms
       dfs_to_write = [session_state.get_elevated_df(arm) for arm in all_arms]
       total_df = pd.concat(dfs_to_write)
       # ... rest of function
   ```

3. **Update `append_from_outfile` tool** (lines 240-276):
   - Get outfile data from session_state
   - Update session_state elevated_df instead of returning Command
   ```python
   @tool(args_schema=AppendFromOutfileInputs)
   def append_from_outfile(metric: OutfileMetricEnum, arm: OutfileEnum, year_agg: AggEnum, label: str, years: Optional[List[int]] = None):
       metric_name = metric.value
       arm_name = arm.value

       # Get from state
       outfile_df = session_state.get_outfile_df(arm_name, metric_name)
       elevated_df = session_state.get_elevated_df(arm_name)

       # Aggregate by year
       if years and len(years) > 0:
           outfile_df = outfile_df[outfile_df['year'].isin(years)]
       aggregated = outfile_df.groupby(['Age Range', 'Gender'])['Value'].agg(year_agg.value).reset_index()

       # Format to elevated structure
       aggregated['Metric'] = label
       aggregated['arm'] = f'{arm_name}.dat'
       aggregated['is_delta'] = False
       aggregated['is_percent_delta'] = False

       # Add sum aggregations
       aggregated = groupby_sum(aggregated, 'Sum', ['35-44', '45-54', '55-64', '65-74', '75-84', '85-94'], 'Age Range', save=False)
       totals = groupby_sum(aggregated, 'M+F', ['M', 'F'], 'Gender', save=False)
       aggregated = pd.concat([aggregated, totals[(totals['Age Range'] == 'Sum') & (totals['Gender'] == 'M+F')]])

       # Update state
       updated_df = pd.concat([elevated_df, aggregated])
       session_state.register_elevated_df(arm_name, updated_df)

       # Persist to disk
       write_augmented_files([f'{arm_name}.dat'])

       return f"Successfully appended metric '{label}' from outfile to elevated DataFrame for arm '{arm_name}'"
   ```

4. **Update `add_deltas` tool** (lines 284-357):
   - Get elevated DataFrames from session_state
   - Update both arm DataFrames in session_state

5. **Update `groupby_age_range`, `groupby_metric`** (lines 367-411):
   - Work with session_state
   - Update affected arm DataFrames

6. **Update binary operation tools** (`divide`, `multiply`, `subtract`) (lines 495-578):
   - Get data from session_state
   - Update session_state after operation

### Step 6: Update agent.py - System Prompt
**File**: `src/chat_cvdpm/agent.py`

**Changes**:

1. **Update system_message_template** (lines 982-1086):
   - Remove references to `main_df`
   - Update to reference three DataFrame categories
   - Update context variables in prompt:
     ```python
     **Current Elevated DataFrames:**
     {elevated_summary}

     **Available Outfile Metrics:**
     {outfile_metrics}

     **Custom DataFrames Created This Session:**
     {custom_dfs_list}
     ```

2. **Update `chatbot` function** (lines 1098-1106):
   - Get summaries from session_state instead of init_df
   ```python
   def chatbot(state: State):
       chain = prompt | llm_with_tools

       elevated_summary = session_state.get_context_summary()
       outfile_metrics = list(session_state.get_all_outfile_metrics())
       custom_dfs = session_state.list_custom_dfs()

       return {"messages": [chain.invoke({
           "user_input": state["messages"],
           "elevated_summary": elevated_summary,
           "outfile_metrics": str(outfile_metrics),
           "custom_dfs_list": str(custom_dfs),
           "example": example
       })]}
   ```

### Step 7: Update pandas_exec Tool Integration
**File**: `src/chat_cvdpm/agent.py`

**Changes**:

1. **Import updated pandas_exec** (after line 28):
   ```python
   from .pandas_exec import execute_pandas
   ```

2. **Replace pandas_tool** (lines 642-648):
   - Remove old `call_pandas_agent` function (lines 631-640)
   - Remove old `pandas_tool` Tool wrapper (lines 644-648)
   - Add `execute_pandas` to tools list directly:
     ```python
     tools = [add_deltas, groupby_metric, groupby_age_range, append_from_outfile,
              ask_for_clarification, divide, multiply, subtract, create_summary_table,
              execute_pandas]  # Add the new tool
     ```

3. **Update tool description in system prompt**:
   - Document that `execute_pandas` is for custom analysis
   - Explain how to reference the three DataFrame categories
   - Provide examples of creating custom DataFrames

### Step 8: Testing & Validation

**Create test script**: `tests/test_state_refactor.py`

Test cases:
1. **Load elevated DataFrames**: Verify .dat files load correctly into session_state
2. **Load outfile DataFrames**: Verify .out files load correctly with year structure
3. **Append from outfile**: Test adding metric from outfile to elevated DataFrame
4. **Create custom DataFrame**: Test `execute_pandas` with result registration
5. **Reference custom DataFrame**: Test using a custom DataFrame in subsequent operations
6. **State persistence**: Verify augmented_dat files maintain consistency
7. **Context summary**: Verify `get_context_summary()` shows all three categories

**Validation checklist**:
- [ ] All .dat files load into `elevated_dfs`
- [ ] All .out files load into `outfile_dfs` with correct structure
- [ ] Tools successfully update session_state instead of returning Commands
- [ ] `write_augmented_files()` works with session_state
- [ ] System prompt receives correct context from session_state
- [ ] `execute_pandas` can create and register custom DataFrames
- [ ] Custom DataFrames are referenceable in agent responses
- [ ] No Command imports or usage remain
- [ ] Existing functionality preserved (backwards compatibility)

## Benefits of This Refactor

### 1. **Clear Separation of Concerns**
- Elevated DataFrames are clearly the "main" data
- Outfile DataFrames are clearly temporal/source data
- Custom DataFrames are clearly user-generated

### 2. **Better Agent Awareness**
- Agent can see what custom DataFrames exist
- Agent can reference them by name/description
- No more mystery about what data is available

### 3. **Simplified Tool Implementation**
- No more Command pattern boilerplate
- Direct state updates are clearer
- Tools return meaningful messages instead of metadata dicts

### 4. **Enhanced pandas_exec Capability**
- Users can create named DataFrames
- Named DataFrames persist in session
- Agent can recommend using custom DataFrames

### 5. **Improved Context Management**
- `get_context_summary()` provides comprehensive view
- System prompt has better awareness of data state
- Easier to debug and understand what data exists

## Backwards Compatibility Considerations

### Files to Keep Compatible
- `augmented_dat/df.parquet` - still written/read for persistence
- `.dat` file format - unchanged
- `.out` file format - unchanged
- Tool call logs - unchanged

### Breaking Changes
- State TypedDict no longer has `df` field (was unused)
- Tools return strings instead of Command objects
- Internal DataFrame references change (but APIs stay same)

## Migration Path

1. **Phase 1**: Add state.py enhancements (Step 1)
2. **Phase 2**: Update pandas_exec.py (Step 2)
3. **Phase 3**: Update initialization code (Step 3)
4. **Phase 4**: Remove Command pattern (Step 4)
5. **Phase 5**: Update tool implementations (Step 5)
6. **Phase 6**: Update system prompt (Step 6)
7. **Phase 7**: Integrate pandas_exec (Step 7)
8. **Phase 8**: Test thoroughly (Step 8)

Each phase should be tested independently before moving to the next.

## Risks & Mitigations

### Risk 1: Breaking existing tool call logs
**Mitigation**: Keep tool signatures identical; only change internals

### Risk 2: State not persisting across sessions
**Mitigation**: Augmented parquet files still serve as persistence layer

### Risk 3: Complex DataFrame access patterns
**Mitigation**: Clear naming conventions and helper methods in session_state

### Risk 4: LangGraph state compatibility
**Mitigation**: Keep State TypedDict minimal; use global session_state for data

## Open Questions
1. Should session_state be global or injected via tool configs?
   - **Recommendation**: Keep global for simplicity (current pattern)

2. Should we version the parquet files to track state changes?
   - **Recommendation**: Add in future iteration if needed

3. Should custom DataFrames be persisted to disk?
   - **Recommendation**: No, they're session-only; users can use execute_pandas to reload

4. How to handle multi-threading/concurrency?
   - **Recommendation**: Current implementation is single-threaded; no changes needed

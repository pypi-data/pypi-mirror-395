# Data Engineering: Global Table Updates

In data engineering workflows, you often need to update tables in-place from inside functions. This is different from analytics/quant work, which uses a purely functional style.

## The Problem

Q (the target language) can only update global tables in-place, not local variables. This creates a scope constraint that Qython makes explicit.

## Two APIs: Methods vs Functions

Qython provides two ways to update global tables in-place:

### Method API (Recommended - Safer)
Call methods on table variables with translation-time scope checking:

- `table.update_global_in_place(filter=[], update_columns={})`
- `table.update_aggregate_global_in_place(filter=[], group_by={}, update_columns={})`
- `table.update_aggregate_transform_global_in_place(filter=[], group_by=[], update_columns=[])`

**Returns:** Table name as str (modifies table in-place)

**Note:** Do not chain these methods - the return value is a str, not a table

**Safety:** Translation-time scope validation catches local/closure variable mistakes

### Function API (For Dynamic Names)
Call functions with table name as string - no scope checking:

- `update_global_in_place(table_name, filter=[], update_columns={})`
- `update_aggregate_global_in_place(table_name, filter=[], group_by={}, update_columns={})`
- `update_aggregate_transform_global_in_place(table_name, filter=[], group_by=[], update_columns=[])`

**Parameters:**
- `table_name`: str (literal or variable) with the name of the global table
- Other parameters same as method versions

**Returns:** Table name as str (modifies table in-place)

**Safety:** No scope checking - you must ensure table exists globally (runtime error if not)

## When to Use Method API vs Function API

### Use Method API when:

- You have the table variable directly
- You want translation-time scope checking
- Working with known table names

**Example:**
```python
prices = get_table()
prices.update_global_in_place(update_columns={'adjusted': 'price * 1.1'})
```

### Use Function API when:

- Table names are determined at runtime
- Working with multiple processes/dynamic table lists
- Updating tables by string name

**Example (Multi-Process Pattern):**
```python
# Assume global tables: trade, quote, orderbook already exist

# Get table names to process
table_names = ["trade", "quote", "orderbook"]

# Update each by name
def add_timestamp_column(table_name):
    update_global_in_place(table_name, update_columns={'processed_at': 'now_datetime_ns()'})
    return None

map(add_timestamp_column, table_names)
```

**Example (Dynamic Table Selection):**
```python
# Table name from configuration
table_name = config_get("target_table")

# Update by name
update_global_in_place(table_name, update_columns={'status': '"processed"'})
```

## What Works

### ✅ Module-level tables (always OK)

```python
# Module level - always works
prices = get_table()
prices.update_global_in_place(update_columns={'adjusted': 'price * 1.1'})
```

### ✅ Global tables from inside functions (with declaration)

```python
prices = get_table()

def process_data():
    global prices
    prices.update_global_in_place(update_columns={'adjusted': 'price * 1.1'})
```

### ✅ Global tables from inside functions (reading, not assigning)

```python
prices = get_table()

def process_data():
    # No 'global' needed - we're not assigning to prices
    prices.update_global_in_place(update_columns={'adjusted': 'price * 1.1'})
```

## What Doesn't Work

### ❌ Local variables

```python
def process_data():
    prices = get_table()  # Local assignment
    prices.update_global_in_place(...)  # ERROR at translation time
```

**Error message:**
```
update_global_in_place() cannot be used on local variable 'prices'.
Solutions:
  1. Use assignment: prices = prices.update(...)
  2. Declare 'global prices' at start of function
```

### ❌ Closure variables

```python
def outer():
    prices = get_table()
    def inner():
        prices.update_global_in_place(...)  # ERROR - closure variable
```

**Error message:**
```
update_global_in_place() cannot be used on closure variable 'prices'.
Closure variables are passed as copies in Q and cannot be modified.
Use assignment instead: prices = prices.update(...)
```

## When to Use Each Approach

### Use `_global_in_place` when:

- Building data pipelines that incrementally update shared tables
- Working with large tables where copying is expensive
- Implementing stateful data processing functions
- Need multiple functions to coordinate updates to the same table

**Example:**
```python
# Data pipeline with multiple stages
raw_data = load_raw_table()

def clean_data():
    global raw_data
    raw_data.update_global_in_place(
        update_columns={'clean_price': 'price.fillna(0)'}
    )

def enrich_data():
    global raw_data
    raw_data.update_global_in_place(
        update_columns={'log_return': 'log(price / prev(price))'}
    )

clean_data()
enrich_data()
```

### Use regular `.update()` when:

- Working with local tables inside functions
- Doing analytics/quant calculations (functional style)
- Want to create derived tables without modifying the source
- Working with closure variables

**Example:**
```python
def calculate_returns(prices):
    # Functional style - returns new table
    return prices.update(
        update_columns={'log_return': 'log(price / prev(price))'}
    )

result = calculate_returns(prices)
```

## Comparison: Functional vs In-Place

```python
# Functional style (analytics/quant)
def add_features(table):
    table = table.update(update_columns={'feature1': 'x * 2'})
    table = table.update(update_columns={'feature2': 'y + 1'})
    return table

result = add_features(data)

# In-place style (data engineering)
data = get_table()

def add_features_in_place():
    global data
    data.update_global_in_place(update_columns={'feature1': 'x * 2'})
    data.update_global_in_place(update_columns={'feature2': 'y + 1'})

add_features_in_place()
# data is now modified
```

## Notes

- Translation-time validation catches scope errors before running Q code
- You cannot use `_global_in_place` on local variables or closure variables
- These methods only work for update operations, not select operations
- When in doubt, use regular `.update()` with assignment - it always works

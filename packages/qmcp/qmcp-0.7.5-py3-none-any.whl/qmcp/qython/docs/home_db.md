# Database

## QMCP Tools

List tables: list_tables()
List table column names and types: describe_table(table_name)

## Creating Tables

`Table(dict)`: Create table from dictionary where keys are column names and values are column data
- Example: `Table({'a': [1, 2, 3], 'b': [4, 5, 6]})` creates a 2-column, 3-row table
- Keys: column names (strings)
- Values: column data as lists/arrays
- Also works with dictionary variables: `Table(my_dict)`

## Qython table properties

Get table shape: table.shape
Get table columns: table.columns
Get table columns types: table.dtypes
Get table values: `.values` (same as pandas, but inefficient) or `.values_T` (preferred - Q's native table format where table columns → matrix rows)

## Updating table rows in-place

### Update a single cell

`table[row_index, column_name] = value`

Example:
```python
# Update qty at row 0
orders[0, 'qty'] = 30

# Update active flag at row 5
orders[5, 'active'] = False
```

### Update an entire row

`table[row_index] = dict`

Example:
```python
# Update entire row at index 0
orders[0] = {
    'id': 1,
    'sym': 'ABC',
    'user': 99,
    'side': 'buy',
    'otype': 'limit',
    'price': 9999,
    'qty': 999,
    'origQty': 50,
    'tif': 'GTC',
    'active': True
}
```

**Important notes:**
- `row_index`: Integer row index (0-based)
- `column_name`: String literal column name
- Modifies the table in-place
- When updating entire row, dictionary must contain all columns

## Qython query methods

Select methods are used to retrieve data from a table, and they returns a new kdb table that may be assigned to a variable.
`table.select(filter=[],select_columns={},distinct=False,sort_column=None,sort_ascending=True,limit=None,start=None) -> Table`
- `filter`: List of Python expressions used to filter rows. Each expression is evaluated as a boolean condition. If empty, no filtering is performed. Multiple filters mean the intersection of all conditions, however order is relevant as each filter is applied one at a time from left to right. E.g. `['date.year == 2025', 'x>2*y']`
- `select_columns`: Dictionary literal where keys are string literals which represent column names and values are strings of Python expression for computing the column values. The expressions operate on full column arrays. If the list is empty, all original table columns will be returned
- `distinct`: select distinct rows from output
- `sort_column`: sort output by a single column
- `sort_ascending`: ascending if True, descending if False
- `limit`: Positive integer: number of rows to return from the top of the table (ie `head`); negative: from the bottom (ie `tail`). None returns all
- `start`: Integer row offset (discards first `start` rows). Avoid using without specifying limit. Requires non-negative `limit`.
Returns a new kdb table. This may be assigned to a variable.

`table.select_aggregate(filter=[],group_by={},select_columns={},distinct=False,sort_column=None,sort_ascending=True,limit=None,start=None) -> Table`
Used to compute aggregates (e.g. mean price by date). Parameters same as for `select`, except
- `group_by`: Dictionary literal defining the grouping columns where keys represent column names and values are expressions for computing the grouping key values. These columns are included in the new table like select columns. Data is partitioned into groups based on unique combinations of these values.
- `select_columns`: Like regular select but expressions operate on each group as partitioned by the group_by parameter, and typically contain aggregate expressions (e.g. `'np.average(points, weights=n)'`)
Returns a table with one row per group.

Update methods are used to add new columns to a table or massage existing ones. Very common approach is either `new_table=table.update(...)` or even multiple `table=table.update(...)` statements. They always return a new table with the same number of rows as the input.

**In-place variants:** For data engineering workflows that update global tables in-place from inside functions, see help topic "data_engineering" for `update_global_in_place()` and related methods.

`table.update(filter=[],update_columns={}) -> Table`
- `filter`: List of Python expressions used to filter rows to be updated. Note: all rows are returned.
- `update_columns`: Dictionary literal like for `select` method. For new column names, columns are added. For existing column names, their content is overwritten.

`table.update_aggregate(filter=[],group_by={},update_columns={}) -> Table`
Similar to `update` method, use this to create new columns where all entries within each group as defined by the group_by clause are replicated values of the aggregation function in the expression; e.g. `update_columns={'avg_price': 'np.mean(price)'}`

`table.update_aggregate_transform(filter=[],group_by=[],update_columns=[]) -> Table`
Similar to `update_aggregate` method, use this to create new columns where the entries within a group with N points are an N-to-N function of the input; e.g. `update_columns={'cum_volume': 'np.cumsum(volume)'}`

**IMPORTANT**
All Python expressions in queries are evaluated using `eval()`, where column names are bound to their corresponding column arrays. These expressions can be Turing-complete and may refer to any global or local variables or functions using usual scoping rules.
When using a column name as an input to a function, it is processed by the function as:
- **Full column arrays** for non-aggregated expressions
- **Group-scoped column arrays** for aggregated expressions (arrays containing only the values within each group)

### Query examples
Get a single column: table.select(select_columns={'column':'column'})
Get distinct values of a single column: table.select(select_columns={'column':'column'}, distinct = True)
Get distinct sorted values of a single column: sorted(table.select(select_columns={'column':'column'}, distinct = True))
Rename columns: table.select(select_columns={'old_name':'new_name', 'column_2':'column_2', ...}) # list all needed columns in dictionary

### Columns vs Lists

A table with only one column is distinct from a list.
Extract list from table with only one column: table['column']

Run function f on each distinct date in a partitioned table:

distinct_date_table = table.select(select_columns={'date':'date'}, distinct=True)
sorted_date_list = sorted(distinct_date_table['date'])
result = map(f, sorted_date_list)

### Incorrect example

❌ table.column # use select instead

## Qython join methods

`table.merge(right, on, how='left', fill_nulls_from_left=False) -> Table`: Performs table joins like pandas `.merge` method
- `right`: table to join
- `on`: column or list of columns to join on
- `how`: type of join: left, inner, outer. Only `left` available in current version.
- `fill_nulls_from_left`: when set to True, if right table columns would overwrite left table columns, left-table values are kept where nulls in the right table would otherwise overwrite them
NOTE: unlike in pandas, columns of the same name in the right table will overwrite those in the left table

`table.merge_asof(right, on, by=[], return_right_time=False, fill_nulls_from_left=False) -> Table`
`on`: Field name to join on. Must be found in both Tables. The data MUST be ordered. Furthermore this must be a numeric or date/time column.
`by`: column name or list of column names to match before performing merge operation
`return_right_time`: copy the matched value of column specified by `on` from right table into left table for matching rows

## Partitioned tables
**Key concept:** Query results return regular tables (not partitioned). 

### Core Restrictions
Only `filter`, `group_by`, `select_columns`, `distinct` work on partitioned tables `select` methods directly. 
To deal with this restriction, use method chaining `table.select(...).select(...)`: restrictions lifted after the first select.

### Recommended Patterns
1. **Single partition**: `table.select(filter=['date==...'])` # returns normal table
2. **Method chaining**: `table.select(filter=...).select(limit=10)` # ✅ second select is run on normal table

### Common Mistakes
❌ `table.select(limit=10)` - fails on partitioned tables
❌ `table[:idx]`
❌ `table.shape`
✅ `table.select(filter=[...]).select(limit=10)` - works via chaining

### Definition
Very large tables stored on disk as one table for each value of the partitioned_field (usually `date`). The `list_tables` tool will tell you which tables are partitioned.

### Best practices
It is recommended you read one partition at a time or few (for example, one day, or a few days) by using e.g. `table.select(filter=['date.within(Date("2000.01.01"),Date("2000.01.07"))'])`
This means that if you want to get the head of a partitioned table you can use method chaining `table.select(filter=...).select(limit=10)` 

You can also look at the date range: `table.select(select_columns={'min_date': 'min(date)', 'max_date': 'max(date)'})`
Or assign a few dates worth of data to a local variable: `x=table.select(filter=["date.within(Date('2020.01.01'), Date('2020.02.01'))"])` # x is not a partitioned table

### Reserved names

You may not use a reserved name as a column name:
❌ table.select_aggregate(select_columns={'count': 'len(i)'})
`count` is a reserved name
✅ table.select_aggregate(select_columns={'n': 'len(i)'})
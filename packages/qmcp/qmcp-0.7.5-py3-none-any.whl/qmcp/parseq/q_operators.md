# Q to Qython Translation Disambiguation Guide

This document provides disambiguation rules for translating intermediate Python function calls to Qython. The Q→Qython translation pipeline works as follows:

**Q Code** → **Intermediate Python-like** → **Qython**

The intermediate step converts Q operators into function calls that need disambiguation:
- `at()`
- `bang()`  
- `colon()`
- `colon_colon()`
- `dot()`
- `dollar()`
- `hash()`
- `query()`
- `underscore()`

This guide helps identify which variant of each overloaded function is being used and how to translate it to appropriate Qython constructs.

## Partial Application Rules

Q has two different types of functions that handle missing arguments in completely different ways:

### Built-in Glyphs (Variable Arity Functions)
Built-in operators like `at()`, `bang()`, `query()` can accept different numbers of arguments. Each number of arguments triggers a completely different operation.

- **Immediate dispatch when enough args**: If you provide enough arguments to match any valid pattern, Q immediately calls that specific variant. For example, `at(data, key)` with 2 arguments immediately calls the "Index At" or "Apply At" variant.
- **Partial only when too few args**: If you provide fewer arguments than the minimum required (usually 2), then Q creates a partial application. For example, `at(data)` with only 1 argument creates a partial because all `at()` variants need at least 2 arguments.
- **No middle partials**: You cannot create a partial of a 3-argument variant by providing 2 arguments. Q will immediately dispatch to the 2-argument variant instead.

Example: `at()` has 2-arg, 3-arg, and 4-arg variants
- `at(a, b)` → immediately calls 2-arg variant (Index At or Apply At)
- `at(a, b, c)` → immediately calls 3-arg variant (Trap At)  
- `at(a)` → creates partial because 1 < minimum arity of 2

### User-Defined Functions (Fixed Arity)
Functions that users write in Q must have a fixed number of arguments. They cannot be overloaded like built-in operators.

- **Exact arguments required**: User functions must receive exactly the number of arguments they were defined with, or Q creates a partial application.
- **Partial for any missing args**: If you provide fewer arguments than expected, Q always creates a partial application, no matter how many are missing.

Example: If `my_func` was defined to take 3 arguments
- `my_func(a, b, c)` → normal function call
- `my_func(a, b)` → creates partial (missing 1 argument)
- `my_func(a)` → creates partial (missing 2 arguments)

### Unknown Functions
When we see a function call in code but don't know if it's a built-in glyph or user-defined function, we should assume it behaves like a user-defined function. This is safer because user functions have stricter rules.

## CRITICAL OUTPUT INSTRUCTIONS

**REQUIRED:** Replace ambiguous function names with specific overload names and detect partial applications.

**OUTPUT FORMAT RULES:**
1. **Replace function names** with the correct overload (e.g., `hash()` → `take()` or `set_attribute()`)
2. **Detect partial applications** and wrap them with `partial()` 
3. **Add comments** explaining both disambiguation choices using `#`
4. **No free text allowed** - only code and comments starting with `#`

**PARTIAL APPLICATION DETECTION:**
- For built-in glyphs: Check if arguments < minimum arity → wrap in `partial()`
- For user/unknown functions: Check if arguments seem insufficient → wrap in `partial()`  

**Examples:**

❌ **Wrong - ambiguous function name:**
```python
result = hash(5, my_list)
```

✅ **Correct - specific overload with comment:**
```python
# Disambiguation: hash(int, list) → Take (positive int takes first n items)
result = take(5, my_list)
```

❌ **Wrong - ambiguous function name:**
```python
output = bang(keys, values)
```

✅ **Correct - specific overload with comment:**
```python
# Disambiguation: bang(list, list) with same-length lists → Dict
output = dict_create(keys, values)
```

❌ **Wrong - ambiguous function name:**
```python
value = dollar("i", data)
```

✅ **Correct - specific overload with comment:**
```python
# Disambiguation: dollar(type_string, value) → Cast (string "i" indicates int cast)  
value = cast("i", data)
```

**PARTIAL APPLICATION EXAMPLES:**

**Before partial analysis:**
```python
temp2 = at(data)
```

**After partial analysis:**
```python
temp2 = partial(at, data) # at() has variable arity 2-4, so temp2 has arity 1-3
```

**Before partial analysis:**
```python
temp3 = my_func(x, y)  # my_func defined elsewhere with 3 parameters
```

**After partial analysis:**
```python
temp3 = partial(my_func, x, y) # my_func has arity 3 so temp3 has arity 1
```

## Apply/Index Function Pair: at() and dot()

### Key Distinction
- **`at()`**: Unary functions, single indices → `u@ux` ≡ `u . enlist ux`
- **`dot()`**: Multi-argument functions, multi-dimensional indexing

### Shared Disambiguation Strategy

**Step 1: Check Function Name**
- `at()` → All operations get "_At" suffix
- `dot()` → Operations use base names

**Step 2: Check Arity**
- **2 args**: Index/Apply variants
- **3 args**: Trap/Amend variants  
- **4 args**: Amend/Replace variants

**Step 3: For 2 args, distinguish Index vs Apply**
- arg1 is data structure (list/dict) → Index variant
- arg1 is function → Apply variant

**Step 4: For 3+ args, check arg3**
- arg3 is error handler → Trap variant
- arg3 is `:` (colon) → Replace variant  
- arg3 is function → Amend variant

### at() Variants

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Index At** | 2 args, arg1 is list/dict, arg2 is single index/key | Gets item at index/key | Item from collection | `at(my_list, 0)` | Index At |
| **Apply At** | 2 args, arg1 is unary function, arg2 is argument | Applies unary function to argument | Function result | `at(func, arg)` | Apply At |
| **Trap At** | 3 args, arg3 is error handler | Tries function call, catches errors | Function result or error result | `at(func, arg, error_handler)` | Trap At |
| **Amend At** | 3 args, arg3 is update function / 4 args, arg3 is update function | Modifies item at index using function | Modified collection | `at(data, index, update_func)` | Amend At |
| **Replace At** | 4 args, arg3 is `:` (colon) | Replaces item at index with value | Modified collection | `at(data, index, colon(), value)` | Replace At |

### dot() Variants

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Index** | 2 args, arg1 is list/dict, arg2 is multi-dimensional indices | Gets items at depth using path | Item/items from deep structure | `dot(nested_list, [1, 2, 0])` | Index |
| **Apply** | 2 args, arg1 is multi-argument function, arg2 is argument list | Applies function to list of arguments | Function result | `dot(func, [arg1, arg2])` | Apply |
| **Trap** | 3 args, arg3 is error handler | Tries function call, catches errors | Function result or error result | `dot(func, args, error_handler)` | Trap |
| **Amend** | 3 args, arg3 is update function / 4 args, arg3 is update function | Modifies items at path using function | Modified collection | `dot(data, path, update_func)` | Amend |
| **Replace** | 4 args, arg3 is `:` (colon) | Replaces items at path with value | Modified collection | `dot(data, path, colon(), value)` | Replace |

## bang()

### Disambiguation Strategy

**Step 1: Check Arity**
- **4 args**: Functional qSQL (update/delete)
- **2 args**: Check arg1 pattern

**Step 2: For 2 args, check arg1 special values**
- `0` → Unkey
- `0N` (null) → Display  
- Negative integer → Internal
- Positive integer + table → Enkey

**Step 3: Check data structure patterns**

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Dict** | 2 same-length lists | Creates dictionary from keys and values | Dictionary | `bang(keys, values)` | Dict |
| **Enkey** | arg1 is positive integer, arg2 is table | Makes first i columns the key of table | Keyed table | `bang(2, table)` | Enkey |
| **Unkey** | arg1 is `0`, arg2 is keyed table | Removes keys from table | Simple table | `bang(0, keyed_table)` | Unkey |
| **Enumeration** | arg1 is symbol list handle, arg2 is int vector | Maps indices to symbols | Symbol list | `bang(symbol_handle, indices)` | Enumeration |
| **Flip** | arg1 is symbol list, arg2 is table handle | Flips splayed/partitioned table | Table | `bang(symbols, table_handle)` | Flip |
| **Display** | arg1 is `0N` (null) | Prints value to console and returns it | Same as input | `bang(null(), value)` | Display |
| **Internal** | arg1 is negative integer | Calls internal q function | Varies | `bang(-1, data)` | Internal |
| **Functional qSQL** | 4 args: `bang(t, c, b, a)` | Performs update/delete operation | Table | `bang(table, conditions, groupby, aggregations)` | Functional qSQL |

**Functional qSQL Parameters:**
- **t**: table or table name as symbol atom
- **c**: Where phrase - list of constraints (parse trees for boolean expressions)
- **b**: By phrase - grouping specification:
  - `()` empty list
  - `False` (0b) for no grouping, `True` (1b) for distinct
  - `False` (0b) specifically indicates delete operation
  - symbol atom/list naming table columns
  - dictionary of group-by specifications
- **a**: Select phrase - column specifications:
  - `()` empty list
  - symbol atom (table column name)
  - parse tree
  - dictionary of select specifications (aggregations)


## colon()

### Disambiguation Strategy

**Check Arity**
- **1 arg**: Return statement
- **2 args**: Assignment

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Assignment** | 2 args: variable, value | Assigns value to variable | The assigned value | `colon(a, 2)` | `a = 2` |
| **Return** | 1 arg: value | Returns value from function | The return value | `colon(a)` | `return a` |

## :: (colon colon)

| Syntax | Semantics |
|--------|-----------|
| `v::select from t where a in b` | define a view |
| `global::42` | amend a global from within a lambda |
| `::` | Identity |
| `::` | Null |

## underscore()

### Disambiguation Strategy

**Check argument patterns:**
- If arg1 is list of integers (non-decreasing) and arg2 is list/table → **Cut**
- If arg1 is single integer and arg2 is list/dict → **Drop** (leading/trailing)
- If arg1 is list/dict and arg2 is index/key → **Drop** (selected items)
- If arg1 is symbol/list of symbols and arg2 is dict/table → **Drop** (keys/columns)

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Cut** | arg1 is list of integers (non-decreasing), arg2 is list/table | Cuts list/table at specified indices | List of sub-arrays | `underscore([2, 4, 9], data)` | Cut |
| **Drop Leading/Trailing** | arg1 is single integer, arg2 is list/dict | Removes first x (positive) or last x (negative) items | Shortened list/dict | `underscore(5, data)` or `underscore(-5, data)` | Drop |
| **Drop Selected** | arg1 is list/dict, arg2 is index/key | Removes items at specified positions | Modified collection | `underscore(data, index)` | Drop |
| **Drop Keys** | arg1 is symbol/list of symbols, arg2 is dict/table | Removes specified keys/columns | Modified dict/table | `underscore(["a", "b"], table)` | Drop |


## query()

### Disambiguation Strategy

**Step 1: Check Arity**
- **2 args**: Find, Roll, Deal, Permute, or Enum Extend
- **3 args**: Vector Conditional or Simple Exec
- **4 args**: Select/Exec
- **5 args**: Select with limit
- **6 args**: Select with limit and sort

**Step 2: For 2 args, check arg1 pattern**
- String/list + arg2 is searchable → **Find**
- Positive integer + arg2 is range → **Roll**
- Negative integer + arg2 is range → **Deal**
- `0N` (null) + arg2 is list → **Permute**
- Enumeration domain + values → **Enum Extend**

**Step 3: For 3+ args, check if arg1 is table**
- arg1 is table → **Functional qSQL** (Simple Exec, Select, etc.)
- arg1 is boolean list → **Vector Conditional**

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Find** | 2 args: searchable, search_items | Finds positions of items in collection | Index list | `query("abcdef", "cab")` | Find |
| **Roll** | 2 args: positive int, range | Random sampling with replacement | Random values | `query(10, 1000)` | Roll |
| **Deal** | 2 args: negative int, range | Random sampling without replacement | Unique random values | `query(-10, 1000)` | Deal |
| **Permute** | 2 args: `0N` (null), list | Random permutation | Shuffled list | `query(null(), data)` | Permute |
| **Enum Extend** | 2 args: enumeration domain, values | Extends enumeration mapping | Extended enum | `query(enum_domain, values)` | Enum Extend |
| **Vector Conditional** | 3 args: boolean list, true_vals, false_vals | Element-wise conditional selection | Result list | `query([True,False,True], "black", "white")` | Vector Conditional |
| **Simple Exec** | 3 args: table, indices, parse_tree | Executes expression on table rows | Computed values | `query(table, [0,1,2], parse_tree)` | Simple Exec |
| **Select/Exec** | 4 args: table, conditions, groupby, aggregations | SQL-like query operation | Table or values | `query(table, conditions, groupby, select)` | Select/Exec |
| **Select Limited** | 5 args: + limit | Select with row limit | Limited table | `query(table, conditions, groupby, select, n)` | Select |
| **Select Sorted** | 6 args: + sort spec | Select with limit and sorting | Sorted limited table | `query(table, conditions, groupby, select, n, sort)` | Select |

**Functional qSQL Parameters (for 3+ args with table):**
- **t**: table or table name
- **c**: conditions list (where clause) - same as bang()
- **b**: groupby specification - same as bang()  
- **a**: aggregations/select specification - same as bang()
- **i**: indices list (Simple Exec only)
- **p**: parse tree (Simple Exec only)
- **n**: row limit (5+ args)
- **g,cn**: sort function and column (6 args)

## dollar()

### Disambiguation Strategy

**Step 1: Check Arity**
- **3 args**: `dollar(condition, true_value, false_value)` → **Conditional**

**Step 2: For 2 args, analyze arg1 pattern**

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Conditional** | 3 arguments | Conditional evaluation | Value from true or false branch | `dollar(x > 10, y, z)` | `y if (x > 10) else z` |
| **Cast** | arg1 is type indicator: String `"h"`, `"f"`, `"i"` / Symbol `` `short`` / Type code `5h`, `6i`, `9f` | Converts value to specified datatype | Converted value | `dollar("i", value)` | Cast |
| **Tok** | arg1 is parse indicator: Uppercase `"H"`, `"F"`, `"I"` / Negative code `-5h`, `-6i` | Interprets string as data of specified type | Parsed value | `dollar("I", "123")` | Tok |  
| **Enumerate** | arg1 is symbol vector/list | Creates enumeration from symbols | Enumerated values | `dollar(symbols, values)` | Enumerate |
| **Pad** | arg1 is positive integer, arg2 is string | Pads string to specified width | Padded string | `dollar(10, "abc")` | Pad |
| **Matrix Ops** | Both args are nested lists of floats (type `f`) | Matrix/vector multiplication, dot product | Result matrix/vector | `dollar(matrix1, matrix2)` | Matrix Ops |

### Q Type System Reference (for Cast/Tok)
```
n   c   name      literal   Cast    Tok
5   h   short     0h        "h"$    "H"$ or -5h$
6   i   int       0i        "i"$    "I"$ or -6i$ 
7   j   long      0j        "j"$    "J"$ or -7j$
9   f   float     0.0       "f"$    "F"$ or -9f$
11  s   symbol    `         "s"$    "S"$ or -11h$
```

## hash()

### Disambiguation Strategy

**Check arg1 type:**
- **Integer/vector**: Take operation
- **Symbol atom**: Set Attribute operation

### Variants and Recognition Patterns

| Variant | Pattern Recognition | What It Does | Returns | Intermediate Form | Qython Target |
|---------|-------------------|--------------|---------|------------------|---------------|
| **Take** | arg1 is int/vector, arg2 is list/dict/table | Takes items from collection: positive=first n, negative=last n, vector=multi-dimensional, symbol vector=named entries/columns. Treats source as circular if needed. | Selected items/reshaped array | `hash(5, data)` or `hash([2, 3], data)` | Take |
| **Set Attribute** | arg1 is symbol (`s`, `u`, `p`, `g`, or `` ` ``), arg2 is list/dict/table | Sets or removes attribute on collection | Collection with attribute | `hash(symbol("s"), data)` | Set Attribute |

**Take Patterns:**
- **Positive int**: Takes first n items
- **Negative int**: Takes last n items  
- **Vector**: Creates multi-dimensional array
- **Symbol vector + dict/table**: Selects named entries/columns

**Set Attribute Symbols:**
- **`s`**: Sorted attribute
- **`u`**: Unique attribute
- **`p`**: Parted attribute
- **`g`**: Grouped attribute
- **`` ` ``** (null symbol): Removes all attributes

## slash()

**IMPORTANT:** `slash()` is always a functional - it takes a function and returns another function. This creates a three-level arity analysis:

1. **Arity of `slash()` itself**: Always 1 (takes one function as input)
2. **Arity of the input function `f`**: Determines which variant of slash is used
3. **Arity of the output function `slash(f)`**: Varies depending on the variant

### Disambiguation Strategy

**Step 1: Determine the arity of the input function `f` in `slash(f)`**

**Step 2: Use input function arity to determine slash variant:**
- If `f` has arity 1 → Could be **Converge**, **Do**, or **While** (need more context)  
- If `f` has arity >1 → Must be **Reduce**

**Step 3: For arity-1 input functions, check usage context:**
- Used with 1 argument → **Converge**
- Used with 2 arguments → **Do** or **While** (check if second arg is condition vs count)

### Variants and Recognition Patterns

| Variant | Input Function Arity | Output Function Arity | Pattern Recognition | What It Does | Intermediate Form | Qython Target |
|---------|---------------------|----------------------|-------------------|--------------|------------------|---------------|
| **Converge** | 1 (unary function) | 1 | `slash(f)` used with 1 arg | Repeatedly applies `f` until result converges (stops changing) | `slash(unary_func)(start_value)` | Converge |
| **Do** | 1 (unary function) | 2 | `slash(f)` used with 2 args, second arg is integer count | Applies `f` exactly `n` times | `slash(unary_func)(count, start_value)` | Do |
| **While** | 1 (unary function) | 2 | `slash(f)` used with 2 args, second arg is condition/test | Applies `f` repeatedly while condition is true | `slash(unary_func)(condition, start_value)` | While |
| **Reduce** | >1 (multi-arg function) | Variable | `slash(f)` where `f` takes multiple arguments | Reduces a list using the multi-argument function `f` | `slash(binary_func)(list)` | Reduce |

### Detailed Examples

**Converge Example:**
```python
# Input: f has arity 1, slash(f) used with 1 argument
temp1 = slash(sqrt)(16.0)
# Disambiguation: slash(unary_function) called with 1 arg → Converge
# sqrt has arity 1, so slash(sqrt) has arity 1
temp1 = converge(sqrt)(16.0)
```

**Do Example:**  
```python
# Input: f has arity 1, slash(f) used with 2 arguments, second is integer
temp2 = slash(increment)(5, start_val)
# Disambiguation: slash(unary_function) called with 2 args, second is count → Do
# increment has arity 1, so slash(increment) has arity 2  
temp2 = do(increment)(5, start_val)
```

**Reduce Example:**
```python
# Input: f has arity 2, slash(f) used with 1 argument (a list)
temp3 = slash(add)(numbers_list)
# Disambiguation: slash(binary_function) → Reduce (variable arity)
# add has arity 2, so slash(add) has variable arity
temp3 = reduce(add)(numbers_list)
```

**Key Points for Disambiguation:**
- **Always check the arity of the input function first**
- **Then check how the resulting `slash(f)` is being used**
- **Converge**: `slash(unary_func)` + 1 usage arg = repeatedly apply until stable
- **Do**: `slash(unary_func)` + 2 usage args (count, value) = apply exactly n times  
- **While**: `slash(unary_func)` + 2 usage args (condition, value) = apply while condition holds
- **Reduce**: `slash(multi_arg_func)` = fold/reduce operation over collection




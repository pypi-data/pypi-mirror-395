# Qython programming language: like Python, compiles to q/kdb+
-vectorized: lists, tuples, iterators, np.arrays, pd.Series all equivalent
-limited subset of functions from numpy pre-imported as np always available
-functional: partial from functools pre-imported and always available
-kdb tables as first-class objects
-if asked to use Qython, use Qython whenever possible and avoid using the q tool
-only Latin-1 character encoding supported; avoid UTF-8 characters

## Important: Do not use import
-Numpy as np is already available
-Qython has no `import` statement and no concept of "modules"
-To run code from another file: `run_script('myfile.q')` - executes the file contents (typically function definitions for libraries)
-All definitions from `run_script()` are added to the global namespace

## Only supports following Python built-ins:
-keywords: while, if
-functions: len sorted ord chr string_to_md5_string enumerate round type isinstance filter try_except
-type casts: int float str String Char
-ternary `x if cond else y` available
-assignment operators: `=` `+=` `-=` `*=` `/=` `|=` `&=` `@=`
-round(x): Round to nearest integer. Optional second parameter: round(x, 2)
-type(x): Returns specific type name as string (e.g., "Int64", "Float32", "DateTimeNS")
-isinstance(x, type): Check if x is of given type. Use with type names like `int`, `float`, `str`, `Date`, `DateTimeNS`, etc.
  - Recommended for type checking: `isinstance(x, int)` checks for any integer width
  - `type(x)` returns specific implementation: `"Int64"`, `"Int32"`, `"Int8"`, etc.

## Automatic Type Casting:
Type casts like `int()`, `float()`, `str()` work on both symbols (str) (e.g., `"hello"`) and String objects. Methods like `.split()` and `.join()` also work on symbols (str) - they automatically cast the symbol to String first, then apply the method. This means you can use `"hello".split()` and it will work as if you wrote `String("hello").split()`.

## Modern Python Syntax Support:
-✅ **Function type hints**: `def func(x: int, y: str) -> bool:` - type annotations are parsed but ignored during translation
-✅ **Triple-quoted strings (docstrings)**: `"""multiline text"""` or `'''multiline text'''` - automatically converted to String literals without warnings, commonly used for function documentation
-✅ **Slicing for reading**: `array[1:3]`, `array[:2]`, `array[2:]`, `array[::2]` all work
-❌ **Slice assignment (L-value)**: `array[1:3] = [10, 20]` not supported (q language limitation)
  - ✅ **Workaround**: Use index arrays: `array[range(1, 3)] = [10, 20]`
  - ✅ Works with steps: `array[range(0, 6, 2)] = [10, 20, 30]`
-negative indices for arrays or slicing:
  - ❌ `array[-1]` → ✅ `last(array)` or `array[len(array) - 1]`
  - ❌ `array[:-1]` → ✅ `array[:len(array) - 1]`
  - ❌ `array[::-1]` → ✅ `reverse(array)` (built-in reverse function)

## Error Handling:
-❌ `try/except/finally` blocks not supported directly → use `try_except()` function instead
-✅ `try_except(func, error_handler)` - execute function with error handling
  - `func`: zero-argument callable (use `lambda:` to wrap)
  - `error_handler`: function taking exception, returns fallback value
  - Example: `result = try_except(lambda: risky_compute(x), lambda e: default_value)`
  - Definition:
```python
def try_except(func, error_handler):
    try:
        return func()
    except Exception as e:
        return error_handler(e)
```

## Timers:
For asynchronous timer callbacks, read help on topic "timer"

## Data Engineering Patterns:
For updating global tables in-place from inside functions in data engineering workflows, read help on topic "data_engineering"

## NOT supported (will cause syntax errors):
-❌ for loops: `for item in iterable:` → use `map()` instead. Only use `while` or `repeat n:` if absolutely impossible with `map()`
-✅ list comprehensions: `[x for x in items]` and `[x for x in items if condition]` → single-for only, no nested loops
  - Multiple variables supported: `[i+x for i, x in enumerate(items)]`
-❌ dictionary comprehensions: `{k: v for k, v in items}`
-❌ sets: `set()`, `{1, 2, 3}` → use numpy set operations instead:
  - Unique elements: `np.unique(array)`
  - Intersection: `np.intersect1d(a, b)`
  - Set difference: `np.setdiff1d(a, b)`
  - Union: `np.union1d(a, b)`
  - Symmetric difference: `np.setxor1d(a, b)`
-❌ break/continue statements: → use early `return` instead, or nested lambda functions for complex cases
-❌ bit shift operators: `<<` and `>>` are not supported
-✅ **Element-wise logical operators** (for boolean arrays/vectors):
  - `&` → element-wise AND (works like numpy: `[True, False] & [True, True]` → `[True, False]`)
  - `|` → element-wise OR (works like numpy: `[True, False] | [False, False]` → `[True, False]`)
  - `^` → element-wise XOR (works like numpy: `[True, False] ^ [True, True]` → `[False, True]`)
  - Example: `valid = (x > 0) & (x < 10)` filters elements between 0 and 10
  - ⚠️ These are NOT bitwise operators on integers - use for boolean array operations only
-✅ supported list methods:
  - `.index(value)` → returns first index where value appears in list
    - `arr.index(30)` → returns index of first occurrence of 30
    - Raises `ValueError` if value not found (matching Python behavior)
    - Example: `arr.index(min(evens))` finds position of minimum value
  - `.pop(index)` → mutates list/dict by removing element at index, returns the modified list/dict
    - **⚠️ UNLIKE Python**: returns the modified list/dict (Python returns the removed element)
    - `result = my_list.pop(2)` → `my_list` is modified AND `result` is the same modified list
    - Works on both lists and dicts
-✅ supported dict methods:
  - `.get(key)` → returns dict[key]
  - `.get(key, default)` → returns default if key not found
  - `.get(key, default=value)` → keyword argument also supported
-✅ supported string methods:
  - `.split()` → splits on spaces
  - `.split(String(","))` → splits on comma (❌ NOT `.split(",")`)
  - `.split(String(", "))` → splits on comma+space
  - `.strip()` → trims whitespace from both ends
  - `.lstrip()` → trims whitespace from left (beginning)
  - `.rstrip()` → trims whitespace from right (end)
  - `.lower()` → converts to lowercase
  - `.upper()` → converts to uppercase
  - `.join(list)` → joins list elements with separator (always requires a parameter)
    - `String("").join(words)` → no separator (❌ NOT `"".join(words)`)
    - `String(",").join(items)` → comma separator
    - `String(", ").join(items)` → comma+space separator
  - `.replace(old, new)` → replaces ALL occurrences of substring with new substring (❌ NO count parameter)
    - `text.replace(String(","), String(";"))` → replace commas with semicolons
    - `text.replace(String("old"), String("new"))` → replace substring

## ⚠️ COMMON GOTCHAS - Read This First!

### Array/List Equality Trap
**CRITICAL**: `==` does **element-wise comparison** (like numpy arrays), NOT whole-object comparison!

-❌ `[1,2,3] == [1,2,3]` → `[True, True, True]` (boolean array, NOT `True`)
-✅ `[1,2,3] is [1,2,3]` → `True` (single boolean - whole-object equality)
-✅ `np.array_equal([1,2,3], [1,2,3])` → `True` (alternative to `is`)
-✅ `([1,2,3]==[1,2,3]).all()` → `True` (check if all elements match)

### String Comparison Trap
Same as arrays: `String() == String()` does **element-wise comparison**!

-❌ `String("abc") == String("abc")` → `[True, True, True]` (boolean array)
-✅ `String("abc") is String("abc")` → `True` (single boolean)
-✅ **Palindrome check**: `text is reverse(text)` (NOT `text == reverse(text)`)
-✅ **Whole-string equality**: Use `is` or `np.array_equal()`

### Reserved Words
**CRITICAL**: Many common names are reserved! Always check reserved names list below.
-❌ Parameter name `string` → ✅ Use `text`, `s`, etc.
-❌ Variable `count` → ✅ Use `n`, `num`, etc.

## New keywords:
-`repeat n:` repeat n times; same as `for _ in range(n):` but without access to iteration variable `_`

## New built-ins:
-get current date/time: now_date now_time_ms now_time_ns now_datetime_ns utc_date utc_time_ms utc_time_ns utc_datetime_ns
-functional programming: converge partial reduce accumulate map filter
  - `partial(func, arg1, arg2)` - partial function application with fixed arguments
  - `partial(func, ..., arg2)` - use ellipsis (`...`) to skip parameters and fix later ones
  - `filter(predicate, iterable)` - returns elements where predicate function returns True
    - Example: `filter(lambda x: x > 0, numbers)` → keeps only positive numbers
    - Example: `filter(is_even, data)` → keeps only even values
-error handling: try_except
  - `try_except(func, error_handler)` - execute function with error handling (see Error Handling section above)
-reverse(array): reverses the order of elements in array or string
-where(condition): returns indices where boolean condition is True
  - ✅ `x[where(x > 0)]` (correct boolean indexing)
  - ❌ `x[x > 0]` (direct boolean indexing not supported)
-string constants: string.ascii_lowercase, string.ascii_uppercase, string.digits, string.ascii_letters

## Dictionary iteration (differs from Python):
**IMPORTANT**: Qython iterates over dictionary VALUES (not keys) while automatically maintaining the key-value mapping:
-`map(func, dict)` → applies `func` to values, preserving keys
-`[expr for x in dict]` → evaluates `expr` on values, preserving keys
-Example: `[i+1 for i in {'a':1,'b':2}]` → `{"a": 2, "b": 3}`
-For Python-like behavior, use explicit `.keys()`, `.values()`, or `.items()`:
  - `map(func, dict.keys())` → iterate over keys only
  - `map(func, dict.values())` → iterate over values only (no key preservation)
  - `map(func, dict.items())` → iterate over (key, value) tuples

## String vs Symbol Types (Important!):
Qython has TWO string types, like Ruby's symbols vs strings:

-**Symbols (str)** (immutable): `"hello"` → q symbols (appear as `` `hello``)
  - Used for identifiers, comparison, lookup
  - ❌ No string operations (no `.join()`, `.replace()`, etc.)
  - ✅ Fast comparison, memory efficient

-**Strings/Characters** (mutable): `String("hello")`, `Char('a')`  
  - `String` is a list of `Char` objects
  - Used for text processing, building, manipulation
  - ✅ Support string operations
  - Use these for ALL string/character operations

## Rule: Always use String()/Char() for text processing
-✅ `char == Char(" ")` not `char == " "`
-✅ `String("hello").join(chars)` not `"hello".join(chars)`
-⚠️ **CRITICAL - String Comparison**: `==` does element-wise comparison (returns boolean array), use `is` for whole-string equality (returns single boolean). See "Common Gotchas" section above.
-✅ **Concatenation**: Use `np.concatenate()` for all concatenation:
  - Lists: `groups = np.concatenate([groups, [new_item]])` or `groups = np.concatenate([groups, new_item])`
  - Strings: `text = np.concatenate([text, [char]])` or `text = np.concatenate([text, char])`
  - Unlike numpy, both forms are legal in Qython
  - Use `+` only for numeric addition

## New built-in types:
-temporal types: Date Month TimeSecond TimeMinute TimeMS TimeNS DateTimeNS DateTimeMS_Float
-examples: Date('2020.01.01') Month('2023.01') TimeMS('12:30:45.123') DateTimeNS('2020.01.01T12:30:45.123456789')
-date and datetime types have properties: year year_month month week day day_of_the_week quarter
-time and datetime types have properties: hour minute second
-`print` is available but f-strings are not. Only use mutable strings:
  - ✅ `print(String("Result:"), result)`
  - ❌ `print("Result:", result)`

## Reserved names
You may not use any of the following names for a function, variable, or column: abs cor ej gtime like mins prev scov system wavg acos cos ema hclose lj ljf mmax prior sdev tables where aj aj0 count enlist hcount load mmin rand select tan while ajf ajf0 cov eval hdel log mmu rank set til within all cross except hopen lower mod ratios setenv trim wj wj1 and csv exec hsym lsq msum raze show type wsum any cut exit iasc ltime neg read0 signum uj ujf xasc asc delete exp idesc ltrim next read1 sin ungroup xbar asin deltas fby if mavg not reciprocal sqrt union xcol asof desc fills ij ijf max null reval ss update xcols atan dev first in maxs or reverse ssr upper xdesc attr differ fkeys insert mcount over rload string upsert xexp avg distinct flip inter md5 parse rotate sublist value xgroup avgs div floor inv mdev peach rsave sum var xkey bin binr do get key med pj rtrim sums view xlog ceiling dsave getenv keys meta prd save sv views xprev cols each group last min prds scan svar vs xrank

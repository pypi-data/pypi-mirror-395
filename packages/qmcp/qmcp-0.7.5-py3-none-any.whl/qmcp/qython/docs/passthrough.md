# Raw Q Code Passthrough (Advanced)

**⚠️ USE ONLY AS LAST RESORT**: `__q__()` is an escape hatch for Q features not yet supported in Qython.

## When to use `__q__()`

- ✅ Only when Qython doesn't support a specific Q feature you need
- ✅ For Q-specific system commands or advanced features
- ❌ **NOT** for features already available in Qython
- ❌ **NOT** for general Q code (use Qython instead)

## Syntax

```python
__q__("raw q code here")
```

## CRITICAL RESTRICTIONS

- ⚠️ **Must use string literal** - `__q__("code")` ✅, `__q__(variable)` ❌
- ⚠️ **Not a normal function** - it's a compiler directive that inserts raw Q code verbatim
- ⚠️ **No validation** - Q syntax errors won't be caught until runtime
- ⚠️ **Requires Q knowledge** - you must know Q/KDB+ to use this

## How it works

`__q__()` is similar to inline assembly in C/C++. The translator inserts your Q code directly into the output without any processing or validation. Think of it as a "compiler escape hatch."

## Examples

### System commands
```python
# Set system variables
__q__("system \"t 1000\"")
```

### Q-specific features
```python
# Define timer callback
__q__(".z.ts:{update_func[]}")

# Multiple Q statements
__q__("system \"t 1000\"; .z.ts:{[]}")
```

### Within Qython functions
```python
def setup():
    __q__("system \"t 1000\"")  # Raw Q code
    data = load_data()          # Normal Qython
    return data
```

### Semicolon handling

The translator automatically adds semicolons at the end of statements when needed:

```python
__q__("x:10")           # Becomes: x:10;
__q__("x:10;")          # Already has semicolon, unchanged: x:10;
__q__("x:10  / comment")  # Becomes: x:10; / comment
```

## Best Practice

**Try to implement your logic in Qython first.** Only use `__q__()` for Q-specific features that have no Qython equivalent.

If you find yourself using `__q__()` frequently, consider requesting that feature be added to Qython.

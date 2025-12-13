# Linear System Solving: np.linalg.lstsq vs np.linalg.lstsq_T

## Overview

Qython provides two functions for solving linear systems of equations:
- `np.linalg.lstsq(A, B)` - Solves **AX ≈ B** (unknown on right, NumPy convention)
- `np.linalg.lstsq_T(A_T, B_T)` - Solves **XA ≈ B** (unknown on left, Q-native format)

**Key difference**: The unknown matrix is on opposite sides of the equation!

## Quick Comparison

**np.linalg.lstsq(A, B)**
- Solves: **AX ≈ B** (unknown **X** on right)
- Solution: **X** = (**A**ᵀ**A**)⁻¹**A**ᵀ**B**
- Input types: Any numeric (int, float32, float64)
- Second param: Vector or matrix
- Return type: Matches input shape
- Performance: 3 extra transpose operations
- Use with tables: `.values`

**np.linalg.lstsq_T(A_T, B_T)**
- Solves: **XA ≈ B** (unknown **X** on left)
- Solution: **X** = **BA**ᵀ(**AA**ᵀ)⁻¹
- Input types: **Must be float64 only**
- Second param: **Must be matrix (2D array)**
- Return type: Always matrix
- Performance: Direct, no extra operations (fastest)
- Use with tables: `.values_T` (recommended)

## np.linalg.lstsq(A, B)

Standard NumPy-compatible function that solves **AX ≈ B** in the least-squares sense.

```python
# Works with any numeric types
A = [[1.0, 2.0], [3.0, 4.0]]
B = [[5.0], [11.0]]
X = np.linalg.lstsq(A, B)  # Returns X such that AX ≈ B

# Verify: AX should be close to B
result = np.dot(A, X)  # Should be close to [[5.0], [11.0]]
```

**Mathematical details:**
- Solves: **AX ≈ B** (unknown **X** on the right)
- Returns: **X** = (**A**ᵀ**A**)⁻¹**A**ᵀ**B**
- Minimizes: ||**AX** - **B**||²

**Note:** Internally performs 3 transpose operations to convert between NumPy's matrix convention and Q's native format. This makes it less efficient than `lstsq_T`.

## np.linalg.lstsq_T(A_T, B_T) - Performance-Critical Code

More efficient version that solves **XA ≈ B** in the least-squares sense (unknown on LEFT). Designed for Q's native table format. **Use this when performance matters.**

**Mathematical details:**
- Solves: **XA ≈ B** (unknown **X** on the left)
- Returns: **X** = **BA**ᵀ(**AA**ᵀ)⁻¹
- Minimizes: ||**XA** - **B**||²

### Requirements (Strict!)

1. **All entries must be float64** (Q's `float` type)
   - Convert with: `A.astype(float)` or explicit float literals
   - Integer types will cause errors

2. **Second parameter must be a matrix** (2D array)
   - ❌ Vector `[5.0, 11.0]` will fail
   - ✅ Matrix `[[5.0], [11.0]]` works
   - ✅ Matrix `[[5.0, 6.0], [11.0, 12.0]]` for multiple systems

3. **Return value is always a matrix**
   - Even when solving single system
   - Extract column if needed: `result[:, 0]`

### Example

```python
# CORRECT: float64 types, B is matrix
# Note: We pass transposed inputs because solve_T solves XA ≈ B
A = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]  # 3x2 matrix
B = [[7.0], [8.0], [9.0]]                  # 3x1 matrix

A_T = np.array(A).T  # Transpose A
B_T = np.array(B).T  # Transpose B

X = np.linalg.lstsq_T(A_T, B_T)  # Returns X such that XA ≈ B

# Verify: XA should be close to B
result = np.dot(X, A)  # Should be close to [[7.0], [8.0], [9.0]]

# INCORRECT: B is vector
B_vec = [7.0, 8.0, 9.0]
X = np.linalg.lstsq_T(A_T, B_vec)  # ERROR!

# INCORRECT: integer types
A_int = [[1, 2], [3, 4], [5, 6]]
X = np.linalg.lstsq_T(A_int.T, B_T)  # ERROR!
```

## Working with Q Tables

Q tables are column-oriented, meaning each column is stored as a contiguous array. This has important implications for extracting matrix data and which lstsq function to use.

### Understanding .values vs .values_T

When you have a table with columns representing features/variables:

```python
# Table with columns as features (common in data science)
features = Table({
    'intercept': [1.0, 1.0, 1.0],
    'x': [1.0, 2.0, 3.0],
    'x_squared': [1.0, 4.0, 9.0]
})

target = Table({
    'y': [2.1, 4.2, 6.3]
})
```

**Option 1: .values (NumPy/pandas convention - observations as rows)**
```python
# Matrix layout: each row is an observation/data point
# Row 0: [intercept=1.0, x=1.0, x_squared=1.0]
# Row 1: [intercept=1.0, x=2.0, x_squared=4.0]
# Row 2: [intercept=1.0, x=3.0, x_squared=9.0]
A = features.values
y = target.values

# Result: A is 3x3, y is 3x1
# To solve: Aβ ≈ y (standard regression formulation)
beta = np.linalg.lstsq(A, y)

# Requires 4 transposes internally (1 for .values extraction, 3 for solving) - INEFFICIENT
```

**Option 2: .values_T (Q table structure - features as rows)**
```python
# Matrix layout: each row is a feature (all observations for that feature)
# Row 0: [intercept across all obs] = [1.0, 1.0, 1.0]
# Row 1: [x across all obs] = [1.0, 2.0, 3.0]
# Row 2: [x_squared across all obs] = [1.0, 4.0, 9.0]
A_T = features.values_T
y_T = target.values_T

# Result: A_T is 3x3, y_T is 1x3 (row vector matrix)
# To solve: βA ≈ y (transposed formulation, but mathematically equivalent)
beta = np.linalg.lstsq_T(A_T, y_T)

# Important: In traditional linear regression, β and y are vectors
# But Q requires them to be matrices (specifically 1xn row-vector matrices)
# So both beta and y are here shape (1, 3), not (3,)

# No transposes needed - direct use of Q's table structure - EFFICIENT
```

### Why .values_T is Faster

Q tables store columns contiguously in memory. `.values_T` gives you the data exactly as stored:
- Table columns → Matrix rows
- No memory reorganization needed
- Direct access to Q's native format
- Perfect for `solve_T` which expects this layout

**Key insight**: When you use `.values_T`, you're solving **βA ≈ y** instead of **Aβ ≈ y**. The coefficient vector **β** is the same in both cases, but the matrix formulation is transposed. This matches Q's native column-oriented table structure perfectly.

### Real-World Example: Linear Regression

```python
# Feature table with n observations
features = Table({
    'intercept': [1.0, 1.0, 1.0, 1.0],
    'x': [1.0, 2.0, 3.0, 4.0],
    'x_squared': [1.0, 4.0, 9.0, 16.0]
})

# Target variable
y = [[2.1], [4.2], [6.1], [8.3]]

# INEFFICIENT: Using .values with lstsq
X = features.values  # Shape: (4, 3) - rows are observations
y = [[2.1], [4.2], [6.1], [8.3]]
coeffs = np.linalg.lstsq(X, y)[0]  # 3 extra transposes!

# EFFICIENT: Using .values_T with lstsq_T
X_T = features.values_T  # Shape: (3, 4) - rows are features
y_T = [[2.1, 4.2, 6.1, 8.3]]  # Shape: (1, 4) - row vector
coeffs = np.linalg.lstsq_T(X_T, y_T)[0]  # Direct computation, no transposes!
```

## When to Use Each Function

### Use np.linalg.lstsq when:
- Working with small systems (performance not critical)
- Prototyping or exploratory analysis
- Input data is not from Q tables
- Mixed numeric types (int, float32, float64)
- Second parameter might be vector or matrix

### Use np.linalg.lstsq_T when:
- Performance matters (large systems, repeated calls)
- Working with Q table data via `.values_T`
- Data is already float64 and matrix format
- Production code that runs frequently

## Common Patterns

### Pattern 1: Solving multiple systems efficiently
```python
# Solve Ax = b1 and Ax = b2 simultaneously
A = [[1.0, 2.0], [3.0, 4.0]]
B = [[5.0, 7.0], [11.0, 15.0]]  # Two right-hand sides
X = np.linalg.lstsq_T(A, B)
# Returns: [[1.0, 1.0], [2.0, 3.0]]
# First column is solution for b1, second for b2
```

### Pattern 2: Converting solve to solve_T
```python
# Before (using solve)
A = df.values
x = np.linalg.lstsq(A, b)

# After (using solve_T)
A_T = df.values_T
b_matrix = [[b[0]], [b[1]], ...]  # Convert vector to matrix if needed
x = np.linalg.lstsq_T(A_T, b_matrix)
```

### Pattern 3: Ensuring float64 type
```python
# If you have integer or mixed-type data
df_float = df.update(update_columns={
    'col1': 'col1.astype(float)',
    'col2': 'col2.astype(float)'
})
A = df_float.values_T
```

## Performance Tips

1. **Always use .values_T with solve_T** - This is the main performance benefit
2. **Reuse matrix decompositions** when solving multiple systems with same A
3. **Batch solve multiple right-hand sides** by stacking them as matrix columns
4. **Type conversion overhead**: Convert to float64 once, not per solve

## Summary

- `np.linalg.lstsq()` is convenient but does 3 extra transposes
- `np.linalg.lstsq_T()` is strict (float64, matrix only) but efficient
- Q tables → use `.values_T` with `solve_T` for best performance
- For performance-critical code, the extra strictness of `solve_T` is worth it

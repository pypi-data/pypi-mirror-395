# qmcp Utilities Documentation

qmcp provides utility functions in the `.qmcp` namespace to help with debugging and working with q via IPC.

## .qmcp.print - Debug Printing via IPC

Simple print function for debugging q code via IPC.

### Syntax
```q
.qmcp.print[val1; val2; val3]
```

All arguments are automatically converted to strings and joined with spaces on a single line (Python-like behavior).

### Behavior

The print function automatically adapts based on the connection context:

- **No IPC connection** (`.z.w=0`): Prints to console (stdout)
- **IPC connection exists AND `.qmcp.PRINT_TO_ASYNC` is true**: Sends output via async IPC (visible to Claude)
- **Otherwise**: Prints to console (stdout)

The `.qmcp.PRINT_TO_ASYNC` flag is automatically configured from your config file's `print_to_async` setting when you connect.

### Error Handling

Arguments are NOT wrapped in error handling - the function will fail fast if errors occur.

If a function call might fail, use `@[]` to catch errors:

```q
/ If f[x] might fail, replace .qmcp.print[f[x]] with:
.qmcp.print[@[f; x; ::]]  / returns null on error

/ Or provide a custom error message:
.qmcp.print[@[f; x; {"ERROR: ", x}]]
```

### Examples

```q
/ Simple value printing
.qmcp.print[42]

/ Multiple values on one line (space-separated, like Python)
.qmcp.print[x; y; z]

/ Print intermediate results in a function
myFunction:{[x]
  .qmcp.print["Input:"; x];
  result: x * 2;
  .qmcp.print["Result:"; result];
  result
  }
```

### Common Patterns for Large Objects

When working with large tables or complex objects that might be too large to send via IPC:

```q
/ Print only first few rows of a table
.qmcp.print[5#bigTable]

/ Print table metadata instead of data
.qmcp.print["Rows:"; count bigTable; "Cols:"; count cols bigTable]

/ Use console view for large objects
.qmcp.print[.Q.s bigTable]  / formatted console view
.qmcp.print[.Q.s1 bigTable] / single-line console view

/ Check object size before printing
.qmcp.print[$[100000 > -22!x; x; "Object too large: ", string count x]]
```

### Configuration

The `print_to_async` setting in your config file controls the default behavior:

```toml
[servers.default]
print_to_async = true   # Print sends async IPC messages (for Claude/LLM visibility)
                        # Set false if experiencing issues with async messages,
                        # writing IPC code, or using an IDE which also uses IPC
```

You can also toggle it manually in your q session:

```q
.qmcp.PRINT_TO_ASYNC: 1b  / Enable async IPC printing
.qmcp.PRINT_TO_ASYNC: 0b  / Disable (use console show)
```

### Debugging Strategies

**Interactive debugging via IPC:**

**IMPORTANT: Before using `.qmcp.print` in IPC mode, you must first load the qmcp namespace by using MultiTool with action `setup_qmcp_namespace`.**

- Good for line-by-line exploration and fixing errors
- Use `.qmcp.print` to see intermediate values
- qmcp automatically shows error traces
- **Important:** When using IPC, statements must be separated by semicolons (`;`), not newlines
- **Prefer `system` over backslash commands:** Use `system"l file.q"` instead of `\l file.q` in multi-statement IPC queries. Backslash commands like `\l` only work standalone or in script files, while `system` works everywhere
- **Avoid truncated output:** If print output is truncated, increase console width: `system"c 9999 9999"`
- **SQL support:** q can run SQL queries by prepending `s)` (e.g., `s)SELECT * FROM orders`). Note: SQL mode does not support multiple statements separated by `;`

**Running scripts standalone with `q filename.q`:**
- Much more token-efficient - doesn't re-execute queries
- Better for running complete scripts and unit tests
- Script files use newlines as statement separators (semicolons optional)
- **However:** errors don't show backtraces by default

**Using .qmcp.print in standalone scripts:**

To use `.qmcp.print` in your script files:

1. Export the qmcp namespace: use MultiTool with action `export_qmcp_namespace_file` with the `parameter` field set to the full path and filename where you want the file written (e.g., `/home/user/project/qmcp.q`)
2. Load it at the top of your script:

```q
system"l qmcp.q";

/ Now you can use .qmcp.print in your tests
.qmcp.print["Running test..."]
```

**Important for distributed source files:** If you're distributing q source files that use `.qmcp.print` or other qmcp namespace functions, you should include `qmcp.q` with your distribution. Export it using MultiTool with action `export_qmcp_namespace_file`, and always specify the full path and filename in the `parameter` field (e.g., `/home/user/myproject/lib/qmcp.q`). This ensures the file is written to the correct location in your project structure.

**Pattern for unit tests in standalone mode:**

First, define a simple assert helper (q doesn't have a built-in one):

```q
/ Assert function - raises error if condition is false
assert:{[bool; err]
  if[not bool; '`$err]
  };
```

Note: The cast to symbol `'`$err` avoids q's weird "stype" behavior for single-char error messages.

Then add error trapping with `.Q.trp` at the end of your test file:

```q
runTests:{
  .qmcp.print["Running test1..."];
  assert[(2+2)=4; "addition works"];
  .qmcp.print["Running test2..."];
  assert[(count til 5)=5; "til works"];
  show "All tests passed!";
  }

/ Execute with error trapping - shows backtrace on failure
.Q.trp[runTests; ::; {-1 "ERROR: ", x, "\nbacktrace:\n", .Q.sbt y; exit 1}];
exit 0  / Exit cleanly (prevents q from entering interactive mode)
```

This ensures you see the full backtrace when tests fail in standalone mode, and exits cleanly after running.

**Important:** Before running `q tests.q` or any standalone q script from the command line, if your script uses `.qmcp.print` or other qmcp namespace functions, you must first export the qmcp namespace file using MultiTool with action `export_qmcp_namespace_file` and the `parameter` field set to the full path and filename (e.g., `/home/user/project/qmcp.q`). Otherwise, the script will fail with undefined function errors.

**Best practice:** Use IPC for debugging, then run scripts standalone once they're working to save tokens.

### When Building IPC Servers

If you're building a q IPC server that needs to use `(neg .z.w)` to respond to clients, and you import libraries that use `.qmcp.print`, you should set:

```q
.qmcp.PRINT_TO_ASYNC: 0b  / After loading libraries
```

This prevents debug print statements from interfering with your server's client responses.

Future versions may use a handle whitelist approach (`.qmcp.handles`) to avoid this manual step.

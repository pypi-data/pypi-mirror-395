// qmcp utility functions for q/kdb+ MCP integration
// These functions help with debugging and working with q via IPC

// Future improvement: Instead of using a global PRINT_TO_ASYNC flag, qmcp could register
// its handle in .qmcp.handles on connect, and print could check (.z.w in .qmcp.handles).
// This would allow:
// - Multiple qmcp Claude sessions to debug simultaneously
// - Building/testing IPC servers without print() interfering with client responses
// - Automatic, correct behavior without manual flag toggling
//
// Challenges with this approach:
// - Need .z.pc handler to clean up handles on disconnect
// - If q session already has .z.pc handler, need to chain them
// - If handle IDs get reused after disconnect, could send to wrong connection
// For now, the global flag approach works for single-Claude debugging scenarios

.qmcp.stringify:{
  s: $[type[x]=10h; x; .Q.s x];
  / Strip trailing newlines added by .Q.s
  $["\r\n"~-2#s; -2_s;
    enlist["\n"]~-1#s; -1_s;
    s]
  };

.qmcp.print:{[x]
  / Simple print function for debugging via IPC
  / Usage: .qmcp.print[val1; val2; val3]
  /
  / All arguments are joined with spaces on a single line (Python-like behavior)
  /
  / Checks:
  / - If no IPC connection (.z.w=0), prints to console
  / - If .qmcp.PRINT_TO_ASYNC is false (default), prints to console
  / - If IPC exists AND .qmcp.PRINT_TO_ASYNC is true, sends via async IPC
  /
  / Arguments are NOT wrapped in error handling - will fail fast if errors occur
  / This makes debugging easier as you see real errors immediately

  msg: " " sv .qmcp.stringify each x;
  printToAsync: $[`PRINT_TO_ASYNC in key .qmcp; .qmcp.PRINT_TO_ASYNC; 0b];
  f: $[(.z.w=0) or not printToAsync; {1 x,"\n"}; {(neg .z.w)x,"\n"}];
  f msg;
  }enlist::;

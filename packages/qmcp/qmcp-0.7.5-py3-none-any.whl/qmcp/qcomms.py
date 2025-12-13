import platform, time, psutil, signal, threading, warnings
from typing import Optional
import pandas as pd
from sugar import spl

from . import qlib
from .util import getTimeoutsStr, find_process_by_port
from .qpython.qconnection import ListenerThread, MessageType, parse_raw_bytes
# Import display functionality - only available in full installation
from .config import detect_full_installation, is_cloud_enabled, get_output_format, get_config_creation_error, get_output_format_fallback_warning
if detect_full_installation():
    from .qpython.display import format_qython_value, format_qython_values_batch
else:
    # Cloud-only qython formatting for thin installations
    def format_qython_value(value=None, bare_strings=False, raw_bytes=None):
        # Qython formatting is a premium feature - require cloud services or full installation
        if not is_cloud_enabled():
            raise RuntimeError("Qython formatting requires cloud services or full installation. Enable cloud_enabled=true or switch to output_format='q' for raw q console output.")

        try:
            from .cloud_api import call_cloud
            # Send raw_bytes to cloud instead of parsed value
            response = call_cloud(method="format_qython_value", raw_bytes=raw_bytes, bare_strings=bare_strings)
            if response.get("success", False):
                return response["result"]
            else:
                raise RuntimeError(f"Cloud formatting service failed: {response.get('result', 'Unknown error')}")
        except Exception as e:
            raise RuntimeError(f"Qython formatting failed: {e}")

    def format_qython_values_batch(values_list=None, bare_strings=False, raw_bytes_list=None):
        # Qython formatting is a premium feature - require cloud services or full installation
        if not is_cloud_enabled():
            raise RuntimeError("Qython formatting requires cloud services or full installation. Enable cloud_enabled=true or switch to output_format='q' for raw q console output.")

        try:
            from .cloud_api import call_cloud
            # Send batch of raw_bytes to cloud
            response = call_cloud(method="format_qython_values_batch", raw_bytes_list=raw_bytes_list, bare_strings=bare_strings)
            if response.get("success", False):
                return response["results"]  # Note: plural "results" for batch
            else:
                raise RuntimeError(f"Cloud batch formatting service failed: {response.get('result', 'Unknown error')}")
        except Exception as e:
            raise RuntimeError(f"Qython batch formatting failed: {e}")

# Translation dictionary for q types to Python types
translationDict = {i:j for i, j in zip(" bg xhijefcspmdznuvts", ',bool,Guid,,Int8,Int16,Int32,Int64,Float32,Float64,Char,str,DateTimeNS,Month,Date,DateTimeMS_Float,TimeNS,TimeMinute,TimeSecond,TimeMS'.split(',')) if i != ' '}
translationDict = {**translationDict, **{i.upper():f'List[{j}]' for i, j in translationDict.items()}}
translationDict['C'] = 'String'

# Global connection state
_q_connection = None
_listener_thread = None
_connection_port = None
_q_process_pid = None  # Store q process PID for safe interruption
_n_printed = 0  # Track number of async messages already processed (to avoid re-processing when collecting output)

# Timeout configuration
_switch_to_async_timeout = 1     # seconds before switching to async mode
# Set interrupt timeout to None on Windows (SIGINT not supported)
_interrupt_timeout = None if platform.system() == 'Windows' else 10  # seconds before sending SIGINT to q process
_connection_timeout = 2          # seconds to wait for connection to establish

# Async task management
_current_async_task = None       # Single async task: {"thread": Thread, "status": str, "command": str, "started": float, "result_container": dict}

# Last query result storage
_last_query_result = None        # Store raw result from query_with_console for later access

# Debug mode
_DEBUG = False

# Error information dictionary for common q errors
error_info = {
    'type': 'Type mismatch -- function expected different input type or multiple parameters of a function need to match one another',
    'nyi': 'Not yet implemented -- you tried to do something outside the confines of the language as documented.',
}

def _process_q_result_triplet(raw_bytes, include_async_output=False, is_print=False):
    """
    Process raw bytes from q and return formatted result and q console view

    Args:
        raw_bytes: Raw bytes from q server containing result triplet
        include_async_output: Whether to collect and prepend async messages
        is_print: True for print statements, False for queries

    Returns:
        tuple: (formatted_result, q_console_view, r)
            - formatted_result: The final formatted result or error message
            - q_console_view: Always r[2].str (q console output)
            - r: The parsed triplet structure for further processing
    """
    # Parse raw bytes to get the triplet structure
    r = parse_raw_bytes(raw_bytes)
    # Q console view is always available
    q_console_view = r[2].str

    # Collect async output first (before any early returns)
    async_output = ""
    if include_async_output:
        async_output = _collect_async_output()

    # When using q output format, size check doesn't apply (q has its own limits)
    using_q_format = get_output_format() == "q"

    # Check 1: Size too large (skip for q format)
    if not using_q_format and not r[0]:
        if is_print:
            error_msg = "Print output too large (>20KB); consider printing smaller objects; if printing a table, try printing only the first few rows instead"
        else:
            error_msg = "Result too large (>20KB); if you're returning a table, try only returning the first few rows instead; if failing repeatedly, you may use the q console view tool as a last resort"
        if async_output:
            error_msg = f"{async_output}\n{error_msg}"
        return error_msg, q_console_view, r

    # Check 2: Execution error
    if not r[1][0][0]:
        error = r[1][1].str
        error_msg = f'Error: {error}'
        if error in error_info:
            error_msg += f'\nError info: {error_info[error]}'
        if r[1][2].str:  # has trace
            error_msg += f'\nTrace:\n{r[1][2].str}'
        if async_output:
            error_msg = f"{async_output}\n{error_msg}"
        return error_msg, q_console_view, r

    # Success case
    if using_q_format:
        result = q_console_view  # Use q console output
    else:
        bare_strings = is_print  # Use bare strings for print, formatted for queries
        # Call with both parameters - cloud uses raw_bytes, full installation uses value
        result = format_qython_value(raw_bytes=raw_bytes, value=r[1][1], bare_strings=bare_strings)

    # Add async output if collected
    if async_output:
        result = f"{async_output}\n{result}"

    return result, q_console_view, r

def _join_print_parts(parts):
    """Join print output parts intelligently - only add space if previous doesn't end with newline"""
    result = ""
    for part in parts:
        if result and not result.endswith("\n") and not result.endswith("\r\n"):
            result += " "
        result += part
    return result

# Actually used to print inside MCP server
def _collect_async_output():
    """Collect all async messages (print statements) as a string"""
    global _listener_thread, _n_printed

    if not _listener_thread:
        return ""

    # Phase 1: Collect all print raw_bytes (for batching)
    print_raw_bytes = []
    while _n_printed < len(_listener_thread.messages):
        message = _listener_thread.messages[_n_printed]
        if message.type == MessageType.ASYNC:  # type 0 - print statements
            print_raw_bytes.append(message.data)
        elif message.type == MessageType.RESPONSE:  # type 2 - stop collecting
            break
        _n_printed += 1

    if not print_raw_bytes:
        return ""

    # Phase 2: Check output format
    using_q_format = get_output_format() == "q"

    if using_q_format:
        # Q format: Just extract console view from each
        output_parts = []
        for raw_bytes in print_raw_bytes:
            r = parse_raw_bytes(raw_bytes)
            # Check if it's the complex qython structure vs plain string from .qmcp.print
            # Complex structure: (size_ok_bool; ((success_bool;`);result); console_view_string)
            try:
                if (hasattr(r, '__len__') and len(r) == 3 and
                    hasattr(r[2], 'str')):
                    # Complex qython structure - extract console view
                    output_parts.append(r[2].str)
                else:
                    # Plain string from .qmcp.print - access .str property
                    output_parts.append(r.str)
            except (TypeError, IndexError, AttributeError):
                # If structure check fails, treat as plain string
                output_parts.append(r.str if hasattr(r, 'str') else str(r))

        return _join_print_parts(output_parts)
    else:
        # Qython format: Batch format all prints in ONE call
        # Parse all raw_bytes to extract values
        parsed_values = []
        for raw_bytes in print_raw_bytes:
            r = parse_raw_bytes(raw_bytes)
            # Check if it's the complex qython structure vs plain string from .qmcp.print
            try:
                if (hasattr(r, '__len__') and len(r) == 3 and
                    hasattr(r[2], 'str')):
                    # Complex qython structure - check for errors
                    if not r[0]:  # Size too large
                        parsed_values.append(None)  # Mark for error handling
                    elif not r[1][0][0]:  # Execution error
                        parsed_values.append(None)  # Mark for error handling
                    else:
                        parsed_values.append(r[1][1])  # Extract actual value
                else:
                    # Plain string from .qmcp.print - use as-is
                    parsed_values.append(r)
            except (TypeError, IndexError, AttributeError):
                # If structure check fails, treat as plain value
                parsed_values.append(r)

        # Batch format all values at once
        # In thin mode: 1 cloud API call for all prints!
        # In full mode: 1 function call that processes all
        formatted_results = format_qython_values_batch(values_list=parsed_values, bare_strings=True, raw_bytes_list=print_raw_bytes)

        return _join_print_parts(formatted_results)

def connect_to_q(host: Optional[str] = None) -> str:
    """
    Connect to q server with config-based connection management

    Args:
        host: Connection specification with multiple modes:
            - None/omitted: Load servers.default from qmcp config file
            - Port number: Load servers.default, override port (e.g., "5002")
            - Server name: Load servers.{name} from config (e.g., "prod")
            - Connection string: Use as-is if contains ':' (e.g., "host:5001:user:pass")

    Returns:
        Connection status and timeout settings
    """
    global _q_connection, _listener_thread, _connection_port, _q_process_pid
    global _switch_to_async_timeout, _interrupt_timeout, _connection_timeout

    from .config import get_server_config_with_defaults, build_connection_string

    try:
        # Determine connection mode and build connection string
        server_config = None
        connection_string = None

        if host is None:
            # Mode 1: Use default server config with operational defaults
            server_config = get_server_config_with_defaults("default")
            connection_string = build_connection_string(server_config)

        elif str(host).isdigit():
            # Mode 2: Port number - use default config but override port
            server_config = get_server_config_with_defaults("default")
            server_config["port"] = int(host)
            connection_string = build_connection_string(server_config)

        elif ':' in str(host):
            # Mode 4: Connection string with colons - use as-is
            connection_string = host
            # No server_config available - use global operational defaults
            from .config import get_operational_defaults
            server_config = get_operational_defaults()

        else:
            # Mode 3: Server name - load named config with operational defaults
            server_config = get_server_config_with_defaults(str(host))
            if server_config.get("host") is None:
                # Server not found in config, try as hostname with default port
                from .config import get_operational_defaults
                operational_defaults = get_operational_defaults()
                server_config = {**operational_defaults, "host": str(host), "port": 5001}
            connection_string = build_connection_string(server_config)

        # Apply timeout settings from config
        _connection_timeout = server_config.get("connection_timeout", 2)
        _switch_to_async_timeout = server_config.get("async_timeout", 1)
        _interrupt_timeout = server_config.get("interrupt_timeout", 10)

        # Set interrupt_timeout to None on Windows
        if platform.system() == 'Windows':
            _interrupt_timeout = None

        # Connect using the resolved connection string
        _q_connection = qlib.connect_to_q(connection_string, _connection_timeout)

        # Create and start listener thread for async response handling
        _listener_thread = ListenerThread(_q_connection.q, raw=True)
        _listener_thread.daemon = True
        _listener_thread.start()

        # Extract and store port for process management
        if ':' in connection_string:
            parts = connection_string.split(':')
            _connection_port = int(parts[1]) if len(parts) > 1 else None
        else:
            _connection_port = None

        # Find and store q process PID
        _q_process_pid = find_process_by_port(_connection_port)

        # Auto-configure print mode and console settings from server config
        if server_config:
            # Set print mode for both qython and qmcp namespaces
            if "print_to_async" in server_config:
                print_to_async = server_config["print_to_async"]
                _query_q(f".qython.PRINT_TO_ASYNC: {'1b' if print_to_async else '0b'}")
                _query_q(f".qmcp.PRINT_TO_ASYNC: {'1b' if print_to_async else '0b'}")

            # Set console view dimensions if configured
            console_size = server_config.get("console_size", [])
            if console_size and len(console_size) == 2:
                rows, cols = console_size
                _query_q(f'system"c {rows} {cols}"')

        # Build status message
        pid_status = ""
        is_windows = platform.system() == 'Windows'
        if _connection_port and (_q_process_pid is None or is_windows):
            if is_windows:
                pid_status = " Warning: Windows detected - interrupt functionality disabled."
            else:
                pid_status = " Warning: Failed to find q process PID - interrupt functionality disabled. If q server is running across WSL-Windows divide, this is expected."

        # Show which config was used
        config_info = ""
        if server_config:
            server_name = host if host and not str(host).isdigit() and ':' not in str(host) else "default"
            config_info = f" Using server config: '{server_name}'."

        result = f"Connected to q server.{config_info} {getTimeoutsStr(_switch_to_async_timeout, _interrupt_timeout, _connection_timeout)}){pid_status}"

        # Check for config creation errors and warn user
        config_error = get_config_creation_error()
        if config_error:
            result += f"\n⚠️  {config_error}"
            result += f"\n💡 To enable cloud services and full functionality, please allow this config file to be created."

        # Check for output format fallback and warn user
        format_warning = get_output_format_fallback_warning()
        if format_warning:
            result += f"\n{format_warning}"

        return f"[connect_to_q] {result}" if _DEBUG else result

    except Exception as e:
        _q_connection = None
        _listener_thread = None
        _connection_port = None
        _q_process_pid = None
        error_msg = f"Connection failed: {str(e)}. {getTimeoutsStr(_switch_to_async_timeout, _interrupt_timeout, _connection_timeout)}"
        raise ValueError(f"[connect_to_q] {error_msg}" if _DEBUG else error_msg)


def query_q(command: str) -> str:
    """
    Execute q command using stored connection with async timeout switching

    Args:
        command: q/kdb+ query or command to execute

    Returns:
        Query result (if fast) or async task ID (if slow)
        - Fast queries return console-formatted output (what you'd see in q console)
        - Slow queries switch to async mode and return task ID
        - Raw result data is stored for later access via get_last_query_raw_result
        - Error message string if query fails

    Note: This uses q IPC (inter-process communication). When sending multiple statements,
          they must be separated by semicolons (;) not newlines.
    """
    return _query_q(command)

def _query_q(command: str, low_level = False, expr = None) -> str:
    """
    Execute q command using ListenerThread with async timeout switching

    Args:
        command: q/kdb+ query or command to execute

    Returns:
        Query result (if fast) or async task ID (if slow)
        - Fast queries return console-formatted output (what you'd see in q console)
        - Slow queries switch to async mode and return task ID
        - Raw result data is stored in _last_query_result for later access
        - Error message string if query fails
    """
    global _q_connection, _listener_thread, _current_async_task, _last_query_result, _n_printed
    
    if _q_connection is None or _listener_thread is None:
        result = "No active connection. Use connect_to_q first."
        return result

    # Check for existing async task and auto-retrieve if completed
    previous_result = None
    if _current_async_task and _current_async_task.get("status") == "Running":
        # Check if the task has actually completed by looking for a response message
        if _listener_thread.messages and _listener_thread.messages[-1].type == MessageType.RESPONSE:
            # Task completed - retrieve and clear it
            response = _listener_thread.messages[-1]
            raw_bytes = response.data
            task = _current_async_task
            elapsed = time.time() - task["started"]

            # Process the result
            result_msg, _last_query_result, r = _process_q_result_triplet(raw_bytes, include_async_output=True, is_print=False)

            # Check if it was an error or success
            if not r[1][0][0] or (get_output_format() != "q" and not r[0]):  # error or size issue
                previous_result = f"[Previous query completed after {elapsed:.1f}s with ERROR]\n{result_msg}"
            else:
                previous_result = f"[Previous query completed after {elapsed:.1f}s]\n{result_msg}"

            # Clear the task so new query can proceed
            _current_async_task = None
        else:
            # Still actually running
            elapsed = time.time() - _current_async_task["started"]
            result = f"Another query is already running ({elapsed:.1f}s elapsed). Use MultiTool check_task to wait for completion."
            return result
    
    if low_level: 
        return _q_connection(command) if expr is None else _q_connection(command, expr)
    
    # Use the new ListenerThread approach
    try:
        # Reset print counter for new query
        _n_printed = 0

        # Sanitize command for IPC latin-1 encoding
        # Encode to latin-1, replacing unencodable characters with '?'
        command = command.encode('latin-1', errors='replace').decode('latin-1')

        # Prepare the query wrapper
        query_wrapper = '''{v:$[`trp in key .Q; .Q.trp[{( (1b;`) ;value x)};x;{((0b;`);x;$[3<count y; .Q.sbt -3 _ y; ""])}]; ((1b;`);value x)]; a:20480>@[-22!;v;{0}]; (a;$[a;v;0b];.Q.s v 1)}''' if get_output_format() == "qython" else '''{v:$[`trp in key .Q; .Q.trp[{( (1b;`) ;value x)};x;{((0b;`);x;$[3<count y; .Q.sbt -3 _ y; ""])}]; ((1b;`);value x)]; (1b; $[v[0][0];@[v;1;:;()];v]; .Q.s v 1)}'''

        # Send the query using sendSyncDetached with raw=True to get raw bytes
        _q_connection.q.sendSyncDetached(query_wrapper, command, raw=True)
        
        # Print any immediate async messages (prints)
        # _print_new_async_messages()
        
        # Wait for response using our new wait_for_response method
        if _listener_thread.wait_for_response(_switch_to_async_timeout):
            # Print any more async messages that came during execution
            # _print_new_async_messages()

            # Fast path - got response quickly
            response = _listener_thread.messages[-1]
            raw_bytes = response.data

            # Use helper function to process the result triplet from raw bytes
            result, _last_query_result, r = _process_q_result_triplet(raw_bytes, include_async_output=True, is_print=False)

            # Prepend previous result if exists
            if previous_result:
                result = f"{previous_result}\n\n[Latest query result]\n{result}"

            return result
        else:
            # Check if listener thread died vs normal timeout
            if not _listener_thread.is_alive():
                # Collect any final async output before reporting connection loss
                async_output = _collect_async_output()
                result = "Connection lost (listener thread died). Use connect_to_q() to reconnect."
                if async_output:
                    result = f"{async_output}\n{result}"
                # Prepend previous result if exists
                if previous_result:
                    result = f"{previous_result}\n{result}"
                return result

            # Slow path - switch to async mode
            _current_async_task = {
                "status": "Running",
                "command": command,
                "started": time.time(),
                "query_wrapper": query_wrapper
            }
            
            # Start the interrupt monitor thread if timeout is configured AND we have PID AND not on Windows
            def monitor_and_interrupt():
                """Monitor task and send SIGINT if it exceeds interrupt timeout"""
                if not _interrupt_timeout:
                    return
                    
                time.sleep(_interrupt_timeout)
                
                # Check if task is still running (no response received yet)
                if (_current_async_task and 
                    _current_async_task.get("status") == "Running" and 
                    _q_process_pid and
                    (not _listener_thread.messages or _listener_thread.messages[-1].type != 2)):
                    
                    try:
                        # Verify the stored PID still matches the process on our port
                        current_pid = find_process_by_port(_connection_port)
                        
                        # Only send SIGINT if it's the same q process we connected to
                        if current_pid == _q_process_pid:
                            # Collect any async messages before interrupting
                            async_output = _collect_async_output()
                            proc = psutil.Process(_q_process_pid)
                            proc.send_signal(signal.SIGINT)
                            error_msg = f"Query interrupted after {_interrupt_timeout}s timeout"
                            if async_output:
                                error_msg = f"{async_output}\n{error_msg}"
                            _current_async_task["error"] = error_msg
                            _current_async_task["status"] = "Timed out"
                        # If PIDs don't match, the q process we connected to is gone
                            
                    except Exception as e:
                        # If SIGINT fails, at least mark the task as timed out
                        if _current_async_task and _current_async_task.get("status") == "Running":
                            # Collect any async messages before marking as failed
                            async_output = _collect_async_output()
                            error_msg = f"Query timed out after {_interrupt_timeout}s (SIGINT failed: {e})"
                            if async_output:
                                error_msg = f"{async_output}\n{error_msg}"
                            _current_async_task["error"] = error_msg
                            _current_async_task["status"] = "Failed to time out"
            
            if _interrupt_timeout and _q_process_pid and platform.system() != 'Windows':
                interrupt_thread = threading.Thread(target=monitor_and_interrupt, daemon=True)
                interrupt_thread.start()
            
            interrupt_msg = ""
            if _interrupt_timeout and _q_process_pid and platform.system() != 'Windows':
                interrupt_msg = f" Will auto-interrupt after {_interrupt_timeout}s."
            elif _interrupt_timeout and platform.system() == 'Windows':
                interrupt_msg = " (Auto-interrupt disabled on Windows)"
            elif _interrupt_timeout and not _q_process_pid:
                interrupt_msg = " (Auto-interrupt disabled - no process PID)"
            
            # Collect any async output that occurred during the initial timeout period
            async_output = _collect_async_output()
            result = f"Query taking longer than {_switch_to_async_timeout}s, switched to async mode.{interrupt_msg} Use MultiTool check_task to wait for completion."
            if async_output:
                result = f"{async_output}\n{result}"
            # Prepend previous result if exists
            if previous_result:
                result = f"{previous_result}\n\n[Latest query result]\n{result}"

            return result
            
    except Exception as e:
        import traceback
        error_details = f"{str(e)}\nTraceback:\n{traceback.format_exc()}"
        result = f"Query failed: {error_details}"
        # Prepend previous result if exists
        if previous_result:
            result = f"{previous_result}\n\n[Latest query result]\n{result}"
        return result



def interrupt_current_query() -> str:
    """
    Send SIGINT to interrupt the currently running query
    
    Returns:
        Status message indicating success or failure
    """
    global _current_async_task, _q_process_pid, _connection_port
    
    if not _current_async_task:
        result = "No async task running to interrupt"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
    
    if platform.system() == 'Windows':
        result = "Cannot interrupt: interrupt functionality disabled on Windows"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
    
    if not _q_process_pid:
        result = "Cannot interrupt: no process PID available"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
        
    if not _connection_port:
        result = "Cannot interrupt: no connection port available"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
    
    task = _current_async_task
    
    # Check if task is already completed
    if task.get("status") != "Running":
        if task.get("error"):
            if task["status"] == "Timed out":
                result = f"Query already timed out: {task['error']}"
            else:
                result = f"Query already failed: {task['error']}"
        else:
            result = "Query already completed successfully, nothing to interrupt"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
    
    try:
        # Verify the stored PID still matches the process on our port
        current_pid = find_process_by_port(_connection_port)
        
        if current_pid != _q_process_pid:
            raise ValueError(f"Process PID mismatch: stored PID {_q_process_pid} but port {_connection_port} has PID {current_pid}. The q process may have been restarted.")
        
        # Collect any async messages before interrupting
        async_output = _collect_async_output()
        
        # Send SIGINT to interrupt the query
        proc = psutil.Process(_q_process_pid)
        proc.send_signal(signal.SIGINT)
        
        # Mark task as interrupted
        task["error"] = "Query manually interrupted"
        task["status"] = "Interrupted"
        
        elapsed = time.time() - task["started"]
        result = f"Query interrupted after {elapsed:.1f}s"
        if async_output:
            result = f"{async_output}\n{result}"
        return f"[interrupt_current_query] {result}" if _DEBUG else result
        
    except ValueError as e:
        # Re-raise PID mismatch errors
        raise e
    except Exception as e:
        result = f"Failed to interrupt query: {str(e)}"
        return f"[interrupt_current_query] {result}" if _DEBUG else result


def get_current_task_result(wait_seconds: int = None) -> str:
    """
    Get result of current/completed async task, optionally waiting for completion

    Args:
        wait_seconds: Max seconds to wait for completion (default: async_switch_timeout)

    Returns:
        Task result or status message
    """
    global _current_async_task, _listener_thread, _last_query_result

    if not _current_async_task:
        result = "No async task to get result from"
        return result

    # Set default wait time to async switch timeout
    if wait_seconds is None:
        wait_seconds = _switch_to_async_timeout or 0

    task = _current_async_task
    start_wait = time.time()
    listener_died = False

    # Wait for completion or timeout
    while time.time() - start_wait < wait_seconds:
        elapsed = time.time() - task["started"]

        # Check if listener thread died - stop waiting immediately
        if not _listener_thread.is_alive():
            listener_died = True
            break

        # Check if task completed by checking for response message
        if _listener_thread.messages and _listener_thread.messages[-1].type == MessageType.RESPONSE:
            response = _listener_thread.messages[-1]
            raw_bytes = response.data

            # Use helper function to check result status from raw bytes
            error_msg, _last_query_result, r = _process_q_result_triplet(raw_bytes, include_async_output=True, is_print=False)

            # Check if it's an error (helper returns error message for non-success cases)
            if not r[1][0][0] or (get_output_format() != "q" and not r[0]):  # query failed or size error
                # If already timed out, preserve the interrupt timing info and append q error
                if task.get("status") == "Timed out":
                    error_msg = f"{task['error']}\nq raised error: {error_msg}"

                # Clear task and return error
                _current_async_task = None
                result = f"Query FAILED after {elapsed:.1f}s. Error: {error_msg}"
                return result
            else:  # succeeded
                # Clear task and return result with elapsed time
                _current_async_task = None
                result = f"[Query completed after {elapsed:.1f}s]\n{error_msg}"
                return result

        # Small polling interval to avoid busy waiting
        time.sleep(0.1)

    # If we get here, either timed out or listener died
    elapsed = time.time() - task["started"]

    # Check if task failed due to existing error
    if task.get("error"):
        _current_async_task = None
        result = f"Query failed: {task['error']}"
        if listener_died:
            result += "\nNote: Connection lost (listener thread died)"
        return result

    # Still running - either because of timeout or dead listener
    if listener_died:
        # Collect any final async output before reporting connection loss
        async_output = _collect_async_output()
        _current_async_task = None
        result = f"Query incomplete after {elapsed:.1f}s - connection lost (listener thread died)"
        if async_output:
            result = f"{async_output}\n{result}"
        return result
    else:
        # Normal timeout
        result = f"Query still running ({elapsed:.1f}s elapsed). Query has not completed yet."
        return result




def get_last_query_result_q_view() -> str:
    """
    Get the q console view of the last query result
    
    Returns the formatted text representation (.Q.s output) that was
    stored from the last query execution. This gives the same view
    as you would see in a q console.
    
    Returns:
        String representation of the q console view or status message
    """
    global _last_query_result
    
    if _last_query_result is None:
        result = "No query result stored. Execute a query first."
        return f"[get_last_query_result_q_view] {result}" if _DEBUG else result
    
    # _last_query_result now stores the formatted text result (r[2].str)
    # which is already the q console view, so just return it directly
    result = _last_query_result
    return f"[get_last_query_result_q_view] {result}" if _DEBUG else result




def list_tables() -> str:
    """
    List all tables with metadata including type, row count, columns, and partition field
    
    Requires an active q connection.
    
    Returns:
        Table listing with metadata or error message
    """
    # Execute the complex query to get table metadata using the new async-capable method
    query = '''`table`table_type`n_rows`n_columns xcols update n_rows: (count get@)each table from ({$[`pf in key `.Q; update partition_field: .Q.pf from x where table_type=`partitioned; x]} (update 
    table_type: {x:.Q.qp get x; $[x~0;`normal;x;`partitioned;`splayed]} each table, 
    n_columns: (count cols get@) each table 
        from ([]table:tables[]))) where table_type<>`partitioned'''
    
    result = _query_q(query)
    return f"[list_tables] {result}" if _DEBUG else result

def describe_table(table: str) -> str:
    """
    Get column names and types for a given table
    
    Args:
        table: Name of the table to describe
    
    Returns:
        DataFrame with column names and Python types or error message
    """
    # Get table metadata using the new async-capable method
    query = f'`column`col_type xcol 0!meta {table}'
    if get_output_format()=='qython': query = 'update qython_col_type: ((-1_.Q.t)!``bool`Guid``Int8`Int16`Int32`Int64`Float32`Float64`Char`str`DateTimeNS`Month`Date`DateTimeMS_Float`TimeNS`TimeMinute`TimeSecond`TimeMS)col_type from '+query
    result = _query_q(query)
    
    # Check if query failed
    if result.startswith("No active connection") or result.startswith("Query failed"):
        return f"[describe_table] {result}" if _DEBUG else result
    
    # For successful queries, we need to parse the result and apply type mapping
    # This is more complex since we can't directly access the raw data like before
    # For now, return the formatted result - type mapping would need to be done in q
    return f"[describe_table] {result}" if _DEBUG else result




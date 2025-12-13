import os
from . import qcomms
from .config import detect_full_installation, is_cloud_enabled


def check_uses_qython_namespace(q_code):
    """
    Check if Q code contains references to .qython namespace.

    Args:
        q_code: String containing translated Q code

    Returns:
        Boolean indicating if .qython. is found in the code
    """
    return '.qython.' in q_code


def prepend_qython_load_if_needed(q_code):
    """
    Prepend 'system"l qython.q";' to Q code if it uses .qython namespace and doesn't already have the load.

    Args:
        q_code: String containing translated Q code

    Returns:
        String with 'system"l qython.q";' prepended if needed, otherwise unchanged
    """
    # Check if code uses .qython namespace
    if not check_uses_qython_namespace(q_code):
        return q_code

    # Check if already has qython.q load (avoid duplication)
    if '\\l qython.q' in q_code or 'system"l qython.q"' in q_code:
        return q_code

    # Prepend the load statement
    return 'system"l qython.q";\n' + q_code


def resolve_dependencies_recursive(qy_file_path, needs_qython_tracker=None, visited=None, stack=None, skip_root_file=False):
    """
    Recursively resolve and translate Qython dependencies.

    This function:
    1. Translates the file (getting both q_code and dependencies)
    2. Writes the q_code to .q file (unless skip_root_file=True for root)
    3. For each dependency:
       - Strips .q/.qy extensions
       - Looks for <dep>.qy in same directory (relative/absolute paths supported)
       - If found, translates it recursively
       - If not found but original had .qy extension, raises error
       - Otherwise ignores (assumes .q exists)
    4. Detects circular dependencies and raises error

    Args:
        qy_file_path: Path to the .qy file to process
        needs_qython_tracker: Optional list to track if qython.q is needed (modified in place)
        visited: Set of already-processed absolute file paths (for cycle detection)
        stack: List of currently-processing file paths (for cycle detection and error messages)
        skip_root_file: If True, don't create .q file for the root file (only for dependencies)

    Returns:
        None (files are translated as side effect)

    Raises:
        ValueError: If circular dependency detected or missing .qy file explicitly requested
    """
    if visited is None:
        visited = set()
    if stack is None:
        stack = []

    # Convert to absolute path for consistent tracking
    qy_file_path = os.path.abspath(qy_file_path)

    # Check for circular dependency
    if qy_file_path in stack:
        cycle_path = ' -> '.join(stack + [qy_file_path])
        raise ValueError(f"Circular dependency detected: {cycle_path}")

    # Skip if already processed
    if qy_file_path in visited:
        return

    # Mark as being processed
    stack.append(qy_file_path)
    visited.add(qy_file_path)

    # Is this the root call?
    is_root = len(stack) == 1

    try:
        # Read and translate the file, getting dependencies in one call
        with open(qy_file_path, 'r', encoding='utf-8') as f:
            qy_code = f.read()

        q_code, dependency_paths = translate_qython_to_q(qy_code, return_run_script_calls=True)

        # Check if this file needs qython.q
        if check_uses_qython_namespace(q_code):
            if needs_qython_tracker is not None:
                needs_qython_tracker[0] = True
            # Prepend load statement for qython.q when writing to file
            q_code = prepend_qython_load_if_needed(q_code)

        # Write the translated file (unless this is root and skip_root_file is True)
        if not (is_root and skip_root_file):
            q_file_path = os.path.splitext(qy_file_path)[0] + '.q'
            with open(q_file_path, 'w', encoding='utf-8') as f:
                f.write(q_code)

        # Get directory of current file for relative path resolution
        qy_dir = os.path.dirname(qy_file_path)

        # Process each dependency recursively
        for dep_path in dependency_paths:
            original_had_qy_extension = dep_path.endswith('.qy')

            # Strip .q or .qy extension
            if dep_path.endswith('.qy') or dep_path.endswith('.q'):
                dep_path = os.path.splitext(dep_path)[0]

            # Resolve relative to current file's directory
            if not os.path.isabs(dep_path):
                dep_path = os.path.join(qy_dir, dep_path)

            # Look for .qy file
            dep_qy_path = dep_path + '.qy'

            if os.path.exists(dep_qy_path):
                # Found .qy file - translate it recursively
                resolve_dependencies_recursive(dep_qy_path, needs_qython_tracker, visited, stack)
            elif original_had_qy_extension:
                # User explicitly requested .qy file but it doesn't exist
                raise ValueError(
                    f"File not found: {dep_qy_path}\n"
                    f"Required by: {qy_file_path}\n"
                    f"Note: run_script(\"{os.path.basename(dep_qy_path)}\") explicitly requests a .qy file."
                )
            # else: .qy not found and wasn't explicitly requested - assume .q exists, ignore

    finally:
        # Remove from processing stack
        stack.pop()


def translate_qython_to_q(qython_code: str, return_run_script_calls: bool = False):
    """
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Translate Qython code to q.
    If writing its output to file, inform user of qython namespace dependencies and existence of export_qython_namespace tool.

    Args:
        qython_code: Qython source code to translate
        return_run_script_calls: If True, also return list of run_script() paths found in code

    Returns:
        If return_run_script_calls is False: translated Q code (str)
        If return_run_script_calls is True: tuple of (translated Q code, list of run_script paths)
    """
    # Priority 1: If full installation available, always use local processing
    if detect_full_installation():
        from .qython.translate import translate_qython_code_to_q
        return translate_qython_code_to_q(qython_code, return_run_script_calls=return_run_script_calls)

    # Priority 2: If cloud enabled, use cloud translation
    elif is_cloud_enabled():
        from .cloud_api import call_cloud
        response = call_cloud(
            method="translate_qython_to_q",
            code=qython_code,
            return_run_script_calls=return_run_script_calls
        )
        if not response.get("success", False):
            raise RuntimeError(response.get("result", "Cloud translation failed"))

        if return_run_script_calls:
            return (response["result"], response.get("run_script_calls", []))
        return response["result"]

    else:  # thin-no-cloud
        raise RuntimeError("Qython translation not available. Either enable cloud mode (cloud_enabled=true) or install the full package.")

def translate_q_to_qython(q_code: str) -> str:
    """
    You MUST call qython_help tool before first calling this tool.
    Translate q code to Qython.
    PREREQUISITE: Must connect to q server first using connect_to_q tool.
    """
    try:
        from .parseq import translate
        assert qcomms._q_connection is not None, "Must connect to q server first using connect_to_q tool"
        return translate(q_code, qcomms)
    except Exception as e:
        return f"Translation failed: {str(e)}. Note: This tool requires the configured LLM (Claude or Copilot) to be installed and available in PATH."

def translate_and_run_qython(qython_code: str) -> str:
    """
    You MUST call connect_to_q before using this tool.
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Translate Qython code to q and execute it.
    Returns: Combined translation and execution result
    If writing translation to file, inform user of qython namespace dependencies and existence of export_qython_namespace tool.
    """
    if qcomms._q_connection is None:
        return "No active connection. Use connect_to_q first."
    
    try:
        # Get the translation
        q_code = translate_qython_to_q(qython_code)
        
        # Try to execute the Q code, but show translation even if execution fails
        try:
            execution_result = qcomms._query_q(q_code)
        except Exception as exec_e:
            execution_result = f"Execution failed: {str(exec_e)}"
        
        # Combine the results
        result = f"TRANSLATION:\n{q_code}\n\nEXECUTION RESULT:\n{execution_result}"
        return result
        
    except Exception as e:
        return f"Failed to translate Qython code: {str(e)}"


def translate_qython_file_to_q_file(qython_file_path: str, q_file_path: str) -> str:
    """
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Translate Qython code from a file to q and write to output file.
    Automatically resolves and translates all dependencies recursively.
    Returns: Status message with translation info
    If writing translation to file, inform user of qython namespace dependencies and existence of export_qython_namespace tool.
    """
    try:
        # Resolve and translate dependencies recursively (creates .q files for dependencies)
        _resolve_and_translate_dependencies(qython_file_path)

        # Read the qython file
        with open(qython_file_path, 'r', encoding='utf-8') as f:
            qython_code = f.read()

        # Translate
        q_code = translate_qython_to_q(qython_code)

        # Prepend \l qython.q if needed when writing to file
        if check_uses_qython_namespace(q_code):
            q_code = prepend_qython_load_if_needed(q_code)

        # Write to q file (for the main file)
        with open(q_file_path, 'w', encoding='utf-8') as f:
            f.write(q_code)

        return f"Successfully translated {qython_file_path} to {q_file_path}"

    except Exception as e:
        return f"Failed to translate file: {str(e)}"


def _resolve_and_translate_dependencies(qy_file_path, check_main_file=True):
    """
    Resolve and translate all dependencies of a .qy file recursively.

    This function creates .q files for all dependencies but does NOT
    create a .q file for the main file itself.

    If any translated file (including main) needs qython.q, exports it to the same directory.

    Works in both full installation and cloud mode.

    Args:
        qy_file_path: Path to the main .qy file
        check_main_file: Whether to also check if main file needs qython.q (default True)

    Returns:
        None (dependencies are written to .q files as side effect)
    """
    # Dependency resolution requires the dependency_resolution module
    # which is only available in full installation (not thin-no-cloud)
    if detect_full_installation() or is_cloud_enabled():
        # Get absolute path
        qy_abs_path = os.path.abspath(qy_file_path)

        # Track if any file needs qython.q (using list for mutability)
        needs_qython = [False]

        # Resolve dependencies (this will translate all .qy dependencies found)
        # This creates .q files for all dependencies but NOT for the main file
        resolve_dependencies_recursive(qy_abs_path, needs_qython, skip_root_file=True)

        # Also check if main file needs qython.q (by translating in-memory)
        if check_main_file:
            with open(qy_abs_path, 'r', encoding='utf-8') as f:
                main_qython_code = f.read()
            main_q_code = translate_qython_to_q(main_qython_code)
            if '\\l qython.q' in main_q_code or 'system"l qython.q"' in main_q_code:
                needs_qython[0] = True

        # If any file needed qython.q, export it to the same directory as the main file
        if needs_qython[0]:
            qy_dir = os.path.dirname(qy_abs_path) or '.'
            qython_q_path = os.path.join(qy_dir, 'qython.q')

            # Only export if it doesn't already exist
            if not os.path.exists(qython_q_path):
                from .qython.q_utils import get_q_qython_namespace_code
                q_code = get_q_qython_namespace_code()

                with open(qython_q_path, 'w', encoding='utf-8') as f:
                    f.write(q_code)
    # else: thin-no-cloud mode - no dependency resolution available


def translate_qython_to_q_file(qython_code: str, q_file_path: str) -> str:
    """
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Translate Qython code to q and write to output file.
    Returns: Status message with translation info
    If writing translation to file, inform user of qython namespace dependencies and existence of export_qython_namespace tool.
    """
    try:
        # Translate
        q_code = translate_qython_to_q(qython_code)

        # Prepend \l qython.q if needed when writing to file
        if check_uses_qython_namespace(q_code):
            q_code = prepend_qython_load_if_needed(q_code)

        # Write to q file
        with open(q_file_path, 'w', encoding='utf-8') as f:
            f.write(q_code)

        return f"Successfully translated Qython code to {q_file_path}"

    except Exception as e:
        return f"Failed to translate and write file: {str(e)}"


def translate_qython_file_to_q(qython_file_path: str) -> str:
    """
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Translate Qython code from a file to q.
    Returns: Translated q code
    If writing translation to file, inform user of qython namespace dependencies and existence of export_qython_namespace tool.
    """
    try:
        # Read the qython file
        with open(qython_file_path, 'r', encoding='utf-8') as f:
            qython_code = f.read()

        # Translate
        q_code = translate_qython_to_q(qython_code)

        return q_code

    except Exception as e:
        return f"Failed to translate file: {str(e)}"


def run_qython_file_via_IPC(qython_file_path: str) -> str:
    """
    You MUST call connect_to_q before using this tool.
    You MUST call qython_help tool before first calling this tool.
    You MUST call setup_qython_namespace tool before first calling this tool.
    Read Qython code from file, translate to q, and execute via IPC.
    Automatically resolves and translates dependencies recursively.
    Returns: Combined translation and execution result
    """
    if qcomms._q_connection is None:
        return "No active connection. Use connect_to_q first."

    try:
        # Resolve and translate dependencies recursively (creates .q files for dependencies)
        _resolve_and_translate_dependencies(qython_file_path)

        # Translate the main file IN-MEMORY (no .q file created for main)
        with open(qython_file_path, 'r', encoding='utf-8') as f:
            qython_code = f.read()
        q_code = translate_qython_to_q(qython_code)

        # Try to execute the Q code, but show translation even if execution fails
        try:
            execution_result = qcomms._query_q(q_code)
        except Exception as exec_e:
            execution_result = f"Execution failed: {str(exec_e)}"

        # Combine the results
        # result = f"TRANSLATION:\n{q_code}\n\nEXECUTION RESULT:\n{execution_result}"
        result = execution_result
        return result

    except Exception as e:
        return f"Failed to run Qython file: {str(e)}"


def run_q_file_via_IPC(q_file_path: str) -> str:
    """
    You MUST call connect_to_q before using this tool.
    Read q code from file and execute via IPC.
    Returns: Execution result
    """
    if qcomms._q_connection is None:
        return "No active connection. Use connect_to_q first."

    try:
        # Read the q file
        with open(q_file_path, 'r', encoding='utf-8') as f:
            q_code = f.read()

        # Execute the Q code
        try:
            execution_result = qcomms._query_q(q_code)
        except Exception as exec_e:
            execution_result = f"Execution failed: {str(exec_e)}"

        return execution_result

    except Exception as e:
        return f"Failed to run q file: {str(e)}"


def setup_qython_namespace() -> str:
    """
    Setup Qython namespace in q session by loading Qython runtime utilities.
    PREREQUISITE: Must connect to q server first using connect_to_q tool
    """
    if qcomms._q_connection is None:
        return "No active connection. Use connect_to_q first."
    
    try:
        # Import and get the qython namespace code
        from .qython.q_utils import get_q_qython_namespace_code
        q_code = get_q_qython_namespace_code()
        
        # Execute the Q code to setup the namespace
        qcomms.query_q(q_code)
        return "Qython namespace successfully loaded into q session"
        
    except Exception as e:
        return f"Failed to setup Qython namespace: {str(e)}"


def export_qython_namespace(file_path: str) -> str:
    """
    Export Qython namespace code with Qython q dependencies to a file.
    Args: file_path: Full path to the file to write (recommended extension: .q)
    Returns: Confirmation of success or failure
    """
    try:
        # Import and get the qython namespace code
        from .qython.q_utils import get_q_qython_namespace_code
        q_code = get_q_qython_namespace_code()
        
        # Write the Q code to the specified file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(q_code)
        
        return f"Qython namespace successfully exported to {file_path}"
        
    except Exception as e:
        return f"Failed to export Qython namespace: {str(e)}"


# # @mcp.tool()
# def ask_claude(question: str) -> str:
#     """
#     Ask Claude a question
#     """
#     try:
#         from parseq import ask_claude as parseq_ask_claude
#         result = parseq_ask_claude(question)
#         return result
#     except Exception as e:
#         import traceback
#         return f"Error in ask_claude: {str(e)}\nTraceback: {traceback.format_exc()}"
    
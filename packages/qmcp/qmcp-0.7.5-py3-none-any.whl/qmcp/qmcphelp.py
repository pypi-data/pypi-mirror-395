import os
from pathlib import Path
from . import qcomms

def get_qmcp_docs_path() -> Path:
    """Get the path to the qmcp documentation directory"""
    return Path(__file__).parent / "docs"

def get_qmcp_namespace_path() -> Path:
    """Get the path to the qmcp.q namespace file"""
    return Path(__file__).parent / "qmcp.q"

def export_qmcp_namespace(file_path: str = "qmcp.q") -> str:
    """
    Export qmcp namespace code to a file.

    Args:
        file_path: Path to the file to write (default: qmcp.q)

    Returns:
        Confirmation of success or failure
    """
    try:
        qmcp_source = get_qmcp_namespace_path()

        if not qmcp_source.exists():
            return f"❌ qmcp namespace file not found at {qmcp_source}"

        # Read the qmcp namespace code
        with open(qmcp_source, 'r', encoding='utf-8') as f:
            q_code = f.read()

        # Write to the specified file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(q_code)

        return f"✅ qmcp namespace successfully exported to {file_path}"

    except Exception as e:
        return f"❌ Failed to export qmcp namespace: {str(e)}"

def setup_qmcp_namespace() -> str:
    """
    Setup qmcp namespace in q session by loading qmcp runtime utilities.
    PREREQUISITE: Must connect to q server first using connect_to_q tool
    """
    if qcomms._q_connection is None:
        return "No active connection. Use connect_to_q first."

    try:
        qmcp_source = get_qmcp_namespace_path()

        if not qmcp_source.exists():
            return f"❌ qmcp namespace file not found at {qmcp_source}"

        # Read the qmcp namespace code
        with open(qmcp_source, 'r', encoding='utf-8') as f:
            q_code = f.read()

        # Execute the Q code to setup the namespace
        qcomms.query_q(q_code)
        return "✅ qmcp namespace successfully loaded into q session"

    except Exception as e:
        return f"❌ Failed to setup qmcp namespace: {str(e)}"

def qmcp_help(topic: str = "home") -> str:
    """Get qmcp documentation by topic

    Args:
        topic: Documentation topic filename (without extension)

    Returns:
        Markdown documentation content
    """
    # Security: prevent path traversal
    if ".." in topic or "/" in topic or "\\" in topic:
        raise ValueError(f"Invalid topic name: {topic}")

    # Only allow alphanumeric and basic characters
    if not topic.replace("_", "").replace("-", "").isalnum():
        raise ValueError(f"Invalid topic name: {topic}")

    docs_path = get_qmcp_docs_path()
    md_file = docs_path / f"{topic}.md"

    if not md_file.exists():
        # List available topics
        available = [f.stem for f in docs_path.glob("*.md")]
        raise FileNotFoundError(f"qmcp documentation topic '{topic}' not found. Available: {', '.join(available)}")

    # Ensure the resolved path is still within the docs directory (extra security)
    if not str(md_file.resolve()).startswith(str(docs_path.resolve())):
        raise ValueError(f"Invalid topic path: {topic}")

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            return f.read()
    except OSError as e:
        raise ValueError(f"Could not read documentation file '{topic}': {e}")

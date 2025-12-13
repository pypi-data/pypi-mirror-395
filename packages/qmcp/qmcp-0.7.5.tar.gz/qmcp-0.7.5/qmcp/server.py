#!/usr/bin/env python3
"""
qmcp Server - MCP Server for q/kdb+ integration

A Model Context Protocol server that provides q/kdb+ connectivity
with flexible connection management and query execution.
"""

from mcp.server.fastmcp import FastMCP
import os
import sys
from typing import Literal, Optional

from . import qcomms
from . import translate
from . import qythonhelp
from . import qmcphelp
from . import auth
from .config import get_config_path, load_config, get_config

# Initialize the MCP server
mcp = FastMCP("qmcp")

@mcp.tool(structured_output=False)
def MultiTool(
    action: Literal[
        "get_config_file_path", "reload_config",
        "interrupt_current_query", "check_task", "get_last_result_console_view",
        "setup_qython_namespace", "setup_qmcp_namespace",
        "export_qython_namespace_file", "export_qmcp_namespace_file",
        "request_api_key", "qython_help", "qmcp_help",
        "list_tables", "describe_table"
    ],
    parameter = None
) -> str:
    """Admin, help, and introspection utilities. The following utilities require a parameter:
-request_api_key: email address
-export_qython_namespace_file: output file path, default "qython.q"
-export_qmcp_namespace_file: output file path, default "qmcp.q"
-qython_help: Qython help page, default "home". You should run this when asked to code in the Qython language
-qmcp_help: qmcp help page, default "home". You should run this before running any q queries
-describe_table: table name
-check_task: optional seconds to wait (default: immediate check). Returns result if ready, status if still running
Use reload_config tool after a change to the config file to apply the new changes.
Before running Qython code, you must use the setup_qython_namespace tool.
Before using .qmcp utilities in q queries, you should use the setup_qmcp_namespace tool."""

    if action == "get_config_file_path":
        return str(get_config_path())

    elif action == "reload_config":
        try:
            import qmcp.config
            qmcp.config._config = None
            load_config()
            return "✅ Configuration reloaded successfully"
        except Exception as e:
            return f"❌ Failed to reload configuration: {e}"

    elif action == "interrupt_current_query":
        return qcomms.interrupt_current_query()

    elif action == "check_task":
        wait_secs = float(parameter) if parameter is not None else None
        return qcomms.get_current_task_result(wait_seconds=wait_secs)

    elif action == "get_last_result_console_view":
        return qcomms.get_last_query_result_q_view()

    elif action == "setup_qython_namespace":
        return translate.setup_qython_namespace()

    elif action == "setup_qmcp_namespace":
        return qmcphelp.setup_qmcp_namespace()

    elif action == "export_qython_namespace_file":
        return translate.export_qython_namespace(file_path=parameter or 'qython.q')

    elif action == "export_qmcp_namespace_file":
        return qmcphelp.export_qmcp_namespace(file_path=parameter or 'qmcp.q')

    elif action == "request_api_key":
        if not parameter:
            return "❌ email address required for request_api_key action"
        return auth.request_api_key(email=parameter)

    elif action == "qython_help":
        return qythonhelp.qython_help(topic=parameter or 'home')

    elif action == "qmcp_help":
        return qmcphelp.qmcp_help(topic=parameter or 'home')

    elif action == "list_tables":
        return qcomms.list_tables()

    elif action == "describe_table":
        if not parameter:
            return "❌ table name required for describe_table action"
        return qcomms.describe_table(table=parameter)

    else:
        return f"❌ Unknown action: {action}"

# Q connection and query tools
connect_to_q = mcp.tool(structured_output=False)(qcomms.connect_to_q)
query_q = mcp.tool(structured_output=False)(qcomms.query_q)

# Translation tools
translate_qython_to_q = mcp.tool(structured_output=False)(translate.translate_qython_to_q)
translate_q_to_qython = mcp.tool(structured_output=False)(translate.translate_q_to_qython)
translate_and_run_qython = mcp.tool(structured_output=False)(translate.translate_and_run_qython)
translate_qython_file_to_q_file = mcp.tool(structured_output=False)(translate.translate_qython_file_to_q_file)
translate_qython_to_q_file = mcp.tool(structured_output=False)(translate.translate_qython_to_q_file)
translate_qython_file_to_q = mcp.tool(structured_output=False)(translate.translate_qython_file_to_q)
run_qython_file_via_IPC = mcp.tool(structured_output=False)(translate.run_qython_file_via_IPC)
run_q_file_via_IPC = mcp.tool(structured_output=False)(translate.run_q_file_via_IPC)

def main():
    """Main entry point for the MCP server"""
    # Fix Windows console encoding to support UTF-8/emojis
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except AttributeError:
            # Python < 3.7 doesn't have reconfigure
            pass

    # Load config early to apply any fallbacks and set warnings
    get_config()
    mcp.run()


if __name__ == "__main__":
    main()
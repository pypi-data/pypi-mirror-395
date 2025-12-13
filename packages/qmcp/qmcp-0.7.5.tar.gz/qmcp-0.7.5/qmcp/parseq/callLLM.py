import os
import subprocess
import tempfile
import uuid
from ..config import get_config

def ask_claude(question: str, timeout = 30) -> str:
    """
    Ask Claude a question by creating a temp directory and running claude -p
    Returns Claude's response as a string.
    """
    # Create a unique subdirectory name
    subdir_name = f"claude_session_{uuid.uuid4().hex[:8]}"
    subdir_path = os.path.join(os.getcwd(), subdir_name)
    
    # Create the subdirectory
    os.makedirs(subdir_path, exist_ok=True)
    
    # Change to the subdirectory
    original_cwd = os.getcwd()
    os.chdir(subdir_path)
    
    try:
        # Run claude -p with the question (properly quoted)
        # Use setsid and clean environment to avoid deadlocks when called from MCP server
        clean_env = {
            'PATH': os.environ.get('PATH'),
            # 'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY'),
            'HOME': os.environ.get('HOME', '/tmp'),
        }
        
        result = subprocess.run(
            ['setsid'] + '''claude --disallowedTools Agent,Bash,Edit,Glob,Grep,LS,MultiEdit,NotebookEdit,NotebookRead,Read,Task,TodoRead,TodoWrite,WebFetch,WebSearch,Write --strict-mcp-config --mcp-config {"mcpServers":{}} -p'''.split()+[question],
            #['claude', '-p', question],
            capture_output=True,
            text=True,
            timeout=timeout,  # timeout seconds timeout
            env=clean_env,
            stdin=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "Error: Claude request timed out"
    except FileNotFoundError:
        return "Error: 'claude' command not found"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Change back to original directory
        os.chdir(original_cwd)

def ask_copilot(question: str, timeout = 30) -> str:
    """
    Ask GitHub Copilot a question by running copilot -p
    Returns Copilot's response as a string.
    Note: Unlike Claude, Copilot doesn't use directory-based session separation.
    """
    try:
        # Run copilot -p with the question, denying all tools for safety
        # Use setsid and clean environment to avoid deadlocks when called from MCP server
        clean_env = {
            'PATH': os.environ.get('PATH'),
            'HOME': os.environ.get('HOME', '/tmp'),
        }

        result = subprocess.run(
            ['setsid', 'copilot', '-p', question, '--deny-tool', 'shell', '--deny-tool', 'write', '--deny-tool', 'read'],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=clean_env,
            stdin=subprocess.DEVNULL
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "Error: Copilot request timed out"
    except FileNotFoundError:
        return "Error: 'copilot' command not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_llm_setting():
    """Get LLM setting from config, defaulting to 'claude'"""
    config = get_config()
    return config.get("default", {}).get("LLM", "claude").lower()

def call_llm(question: str, timeout = 30) -> str:
    """
    Call the configured LLM (Claude or Copilot) based on config.toml LLM setting
    Returns the LLM's response as a string.
    """
    llm = get_llm_setting()

    if llm == "copilot":
        return ask_copilot(question, timeout)
    elif llm == "claude":
        return ask_claude(question, timeout)
    else:
        return f"Error: Unknown LLM '{llm}'. Supported options: 'claude', 'copilot'"
"""
Configuration management for qmcp
"""
import os
import shutil
import sys
from pathlib import Path
from platformdirs import user_config_dir
import datetime

# Handle tomllib for different Python versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Global config cache
_config = None
_config_creation_failed = False
_config_creation_error = None
_is_full_installation = None
_output_format_fallback_warning = None

# Debug logging control
DEBUG = False

def _log_debug(message):
    """Log debug messages to file for tracking config loading"""
    if not DEBUG:
        return
    try:
        with open('/tmp/qmcp_config_debug.log', 'a') as f:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')
            f.write(f'[{timestamp}] {message}\n')
            f.flush()
    except:
        pass  # Ignore logging errors

def detect_full_installation():
    """Detect if this is a full installation (has qython and enhanced qpython)"""
    global _is_full_installation
    _log_debug(f"detect_full_installation() called, cached: {_is_full_installation}")
    if _is_full_installation is None:
        try:
            # Test for environment variable simulation
            import os
            if os.getenv('QMCP_SIMULATE_THIN'):
                raise ImportError("Simulating thin package")

            # Test for the key missing piece in thin builds - qpython.display
            from .qpython import display
            _is_full_installation = True
        except ImportError:
            _is_full_installation = False

    _log_debug(f"detect_full_installation() result: {_is_full_installation}")
    return _is_full_installation

def get_config_path():
    """
    Get the path to the config file using standard tool config pattern.

    Priority order:
    1. ./qmcp.toml or ./.qmcp.toml (project-specific config)
    2. ~/.config/qmcp/config.toml (user default)

    This follows standard tool patterns (git, docker, aws, etc.)
    Config is independent of virtual environments.
    """
    # 1. Project-local config (current working directory)
    cwd = Path.cwd()
    for config_name in ['qmcp.toml', '.qmcp.toml']:
        project_config = cwd / config_name
        if project_config.exists():
            return project_config

    # 2. User config directory (default)
    config_dir = Path(user_config_dir("qmcp"))
    return config_dir / "config.toml"

def ensure_config():
    """Ensure config file exists, create from template if needed"""
    global _config_creation_failed, _config_creation_error
    config_path = get_config_path()

    if not config_path.exists():
        try:
            # Create config directory
            config_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy template (content only, no permissions)
            template_path = Path(__file__).parent / "config_template.toml"
            shutil.copyfile(template_path, config_path)

            print(f"✅ Created qmcp config at: {config_path}")
            print("💡 Edit this file to customize your setup")
        except Exception as e:
            _config_creation_failed = True
            _config_creation_error = f"Failed to create config at {config_path}: {e}"
            print(f"❌ {_config_creation_error}")

    return config_path

def load_config():
    """Load configuration from file with automatic fallbacks"""
    global _output_format_fallback_warning
    _log_debug("load_config() called")
    _output_format_fallback_warning = None  # Clear any previous warning
    config_path = ensure_config()

    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
    except Exception as e:
        print(f"❌ Error loading config from {config_path}: {e}")
        print("💡 Using default configuration")
        config = get_default_config()

    # Check for incompatible qython + thin + no-cloud combination
    output_format = config.get("default", {}).get("output_format", "qython")
    cloud_enabled = config.get("default", {}).get("cloud_enabled", False)
    full_installation = detect_full_installation()

    _log_debug(f"Config check: output_format={output_format}, cloud_enabled={cloud_enabled}, full_installation={full_installation}")

    if output_format == "qython" and not full_installation and not cloud_enabled:
        _output_format_fallback_warning = "⚠️  Qython formatting requires cloud services or full installation. Switched to raw q output. Enable cloud_enabled=true or install full version for enhanced formatting."
        # Override the config to use q format
        if "default" not in config:
            config["default"] = {}
        config["default"]["output_format"] = "q"
        _log_debug(f"Applied fallback: warning set, config overridden to q format")
    else:
        _log_debug(f"No fallback needed")

    _log_debug(f"load_config() returning, warning={_output_format_fallback_warning is not None}")
    return config

def get_default_config():
    """Get default configuration when config file is unavailable"""
    return {
        "default": {
            "output_format": "qython",
            "cloud_enabled": False
        },
        "servers": {
            "default": {
                "host": "localhost",
                "port": 5001
            }
        }
    }

def get_config():
    """Get global configuration (cached)"""
    global _config
    _log_debug(f"get_config() called, cached: {_config is not None}")
    if _config is None:
        _config = load_config()
    return _config

def is_cloud_enabled():
    """Check if cloud translation is enabled"""
    config = get_config()
    return config.get("default", {}).get("cloud_enabled", False)


def get_config_creation_error():
    """Get config creation error message if it failed"""
    return _config_creation_error if _config_creation_failed else None

def get_output_format_fallback_warning():
    """Get output format fallback warning if it occurred"""
    _log_debug(f"get_output_format_fallback_warning() called, warning: {_output_format_fallback_warning is not None}")
    return _output_format_fallback_warning

def get_output_format():
    """Get output format setting"""
    config = get_config()
    return config.get("default", {}).get("output_format", "qython")

def get_server_config(server_name="default"):
    """Get configuration for a specific server"""
    config = get_config()
    servers = config.get("servers", {})
    return servers.get(server_name, servers.get("default", {
        "host": "localhost",
        "port": 5001
    }))

def get_operational_defaults():
    """
    Get operational defaults from [default] section

    These settings can be overridden per-server but provide global defaults
    for timeouts, print behavior, and console settings.

    Returns:
        Dict with operational settings
    """
    config = get_config()
    defaults = config.get("default", {})

    return {
        "connection_timeout": defaults.get("connection_timeout", 2),
        "async_timeout": defaults.get("async_timeout", 1),
        "interrupt_timeout": defaults.get("interrupt_timeout", 10),
        "print_to_async": defaults.get("print_to_async", True),
        "console_size": defaults.get("console_size", []),  # Empty array = don't change
    }

def get_server_config_with_defaults(server_name="default"):
    """
    Get server configuration merged with operational defaults

    Args:
        server_name: Name of server configuration to load

    Returns:
        Dict with merged config (operational defaults + server specifics)
        Server-specific settings override operational defaults
    """
    # Get operational defaults
    operational_defaults = get_operational_defaults()

    # Get server-specific config
    server_config = get_server_config(server_name)

    # Merge: operational defaults + server config
    # Server config overrides defaults
    return {**operational_defaults, **server_config}

def build_connection_string(server_config):
    """
    Build q connection string from server config

    Args:
        server_config: Dict with host, port, optional user/password

    Returns:
        Connection string in format: host:port or host:port:user:password
    """
    host = server_config.get("host", "localhost")
    port = server_config.get("port", 5001)
    user = server_config.get("user", "")
    password = server_config.get("password", "")

    # Basic connection string
    conn_str = f"{host}:{port}"

    # Add authentication if provided
    if user and password:
        conn_str = f"{conn_str}:{user}:{password}"

    return conn_str
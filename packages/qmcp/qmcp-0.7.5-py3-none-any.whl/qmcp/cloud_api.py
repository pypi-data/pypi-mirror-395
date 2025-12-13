"""
Cloud API client for qmcp
Provides secure communication with qmcp cloud services via HTTPS + API keys

PRIVACY NOTICE: This module communicates with external cloud services.
All functions assert that cloud_enabled=True in configuration before
making any external network calls.
"""

import requests
import time
from .config import is_cloud_enabled, get_config

# Server configuration
import os
if os.getenv("QMCP_LOCAL_SERVER"):
    BASE_URL = "http://127.0.0.1:8080"  # Local testing
else:
    BASE_URL = "https://qython.dev"  # Production

class _CloudClient:
    """Internal cloud client - not exposed to users"""

    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 3  # 3 second timeout

    def _get_api_key(self):
        """Get API key from config"""
        config = get_config()
        cloud_config = config.get("cloud", {})
        api_key = cloud_config.get("api_key", "")

        # Check if API key is set (not default value)
        if not api_key or api_key == "your-key-here":
            return None
        return api_key
    
    def call_cloud(self, **kwargs):
        """Make authenticated call to cloud server via HTTPS"""
        # Privacy safeguard: This assertion provides an auditable guarantee that
        # external network communication only occurs when explicitly enabled by user configuration
        assert is_cloud_enabled(), "External communication attempted while cloud_enabled=false. This assertion ensures user privacy protection."

        # Debug: Print method being called
        method = kwargs.get('method', 'unknown')
        if method == 'format_qython_values_batch':
            batch_size = len(kwargs.get('raw_bytes_list', []))
            print(f"[cloud_api] Calling {method} with {batch_size} items")
        else:
            print(f"[cloud_api] Calling {method}")

        try:
            # Get API key from config
            api_key = self._get_api_key()
            if not api_key:
                raise RuntimeError(
                    "API key required for cloud translation.\n"
                    "Use the request_api_key tool to get one, then add it to your config.\n"
                    "Run: request_api_key(email='your@email.com')"
                )

            # Add timestamp to kwargs
            kwargs["timestamp"] = time.time()

            # Pack data with msgpack (supports binary data)
            import msgpack
            packed_data = msgpack.dumps(kwargs)

            # Prepare headers with API key
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/msgpack"
            }

            # Send to server (msgpack body over HTTPS)
            response = self.session.post(
                f"{BASE_URL}/translate",
                data=packed_data,
                headers=headers,
                timeout=3
            )

            # Handle authentication errors
            if response.status_code == 401:
                error_detail = response.json().get("detail", "Invalid API key")
                raise RuntimeError(
                    f"Authentication failed: {error_detail}\n"
                    "Use request_api_key tool to get a new API key."
                )

            response.raise_for_status()

            # Parse msgpack response
            return msgpack.loads(response.content)

        except requests.exceptions.ConnectTimeout:
            raise ConnectionError(f"Cloud timeout: Could not connect within 3 seconds")
        except requests.exceptions.ReadTimeout:
            raise ConnectionError(f"Cloud timeout: Server did not respond within 3 seconds")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Cloud connection failed: {e}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # Already handled above
                raise
            raise ConnectionError(f"Cloud HTTP error: {e} (status: {e.response.status_code})")
        except RuntimeError:
            # Re-raise our auth errors
            raise
        except Exception as e:
            raise RuntimeError(f"Cloud call failed: {type(e).__name__}: {e}")

# Global client instance
_client = _CloudClient()

def call_cloud(**kwargs):
    """
    Make authenticated call to qmcp cloud server via HTTPS using MessagePack

    Requires cloud_enabled=true and a valid API key in config.
    Use request_api_key tool to obtain an API key.

    Args:
        **kwargs: Keyword arguments to send to cloud (supports binary data)

    Returns:
        Cloud server response (decoded from MessagePack)

    Raises:
        AssertionError: If cloud_enabled=false (privacy safeguard)
        RuntimeError: Missing/invalid API key or cloud processing errors
        ConnectionError: Network or timeout issues

    Examples:
        # Qython translation
        call_cloud(method="qython_to_q", code="print(2+2)")

        # Q object with binary data
        call_cloud(method="format_output", q_result=binary_q_object)
    """
    return _client.call_cloud(**kwargs)
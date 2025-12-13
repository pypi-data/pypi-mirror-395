#!/usr/bin/env python3
"""
Authentication tools for qmcp cloud services
"""
import requests
from .config import get_config

# Cloud server URL
CLOUD_SERVER_URL = "https://qython.dev"


def request_api_key(email: str) -> str:
    """
    Request an API key for cloud translation services.

    An API key enables cloud-based Qython translation (Python-like syntax → q code).
    The API key will be emailed to you.

    Args:
        email: Your email address

    Returns:
        Status message indicating success or instructions for next steps

    Example:
        >>> request_api_key("user@example.com")
        "✅ API key sent to user@example.com. Check your inbox (and spam folder)."
    """
    try:
        # Call the cloud server endpoint
        response = requests.post(
            f"{CLOUD_SERVER_URL}/api/request-key",
            json={"email": email},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return f"✅ {data.get('message')}\n\nOnce you receive the email, add the API key to your config by telling your AI assistant or manually editing the config file."
            else:
                return f"❌ {data.get('message', 'Unknown error')}"
        else:
            # Try to parse error message
            try:
                error_data = response.json()
                error_msg = error_data.get("detail", response.text)
            except:
                error_msg = response.text

            return f"❌ Request failed (HTTP {response.status_code}): {error_msg}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please check your internet connection and try again."
    except requests.exceptions.ConnectionError:
        return f"❌ Could not connect to {CLOUD_SERVER_URL}. Please check your internet connection."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

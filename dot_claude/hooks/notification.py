"""
Notification hook example for claude-hooks.
This hook responds to various Claude Code notifications.
Includes Home Assistant integration and macOS notifications.
"""

import os
import socket
import subprocess
import urllib.request
import urllib.error
import json
import logging
from claude_hooks import run_hooks

# Set up logger for this module
logger = logging.getLogger(__name__)

HOMEASSISTANT_URL = "https://ha.zarek.cc/api/services/notify/mobile_app_pixel_9_pro_xl"
DEFAULT_TITLE = "Claude Code"


def send_macos_notification(message: str, title: str = DEFAULT_TITLE) -> tuple[bool, str]:
    """Send a macOS notification using terminal-notifier."""
    try:
        result = subprocess.run(
            ["terminal-notifier", "-message", message, "-title", title],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return True, "macOS notification sent successfully"
        else:
            return False, f"terminal-notifier failed (code {result.returncode}): {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return False, "macOS notification timed out"
    except Exception as e:
        return False, f"macOS notification exception: {str(e)}"


def send_home_assistant_notification(
    message: str, title: str = DEFAULT_TITLE
) -> tuple[bool, str]:
    token = os.getenv("HOMEASSISTANT_TOKEN")
    if not token:
        return False, "HOMEASSISTANT_TOKEN environment variable not set"

    payload = json.dumps(
        {"message": message, "title": title, "data": {"ttl": 0, "priority": "high"}}
    ).encode("utf-8")
    req = urllib.request.Request(
        HOMEASSISTANT_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10):
            return True, "Notification sent successfully"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()}"
    except (urllib.error.URLError, OSError) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def notify_ha(event):
    hostname = socket.gethostname()
    message = f"{hostname}: {event.message}"
    
    success, error_msg = send_home_assistant_notification(message)
    
    if not success:
        logger.error(f"Failed to send Home Assistant notification: {error_msg}")
    else:
        logger.info("Home Assistant notification sent successfully")
    
    return event.undefined()


def notify_macos(event):
    hostname = socket.gethostname()
    message = f"{hostname}: {event.message}"
    
    success, error_msg = send_macos_notification(message)
    if not success:
        logger.error(f"Failed to send macOS notification: {error_msg}")
    
    return event.undefined()


if __name__ == "__main__":
    run_hooks(notify_ha, notify_macos)

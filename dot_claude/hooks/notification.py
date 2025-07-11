"""
Notification hook example for claude-hooks.
This hook responds to various Claude Code notifications.
Includes Home Assistant integration.
"""

import os
import socket
import urllib.request
import urllib.parse
import json
from claude_hooks import run_hooks

HOMEASSISTANT_URL = "https://ha.zarek.cc/api/services/notify/mobile_app_pixel_9_pro_xl"
DEFAULT_TITLE = "Claude Code"


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
        print(f"Failed to send Home Assistant notification: {error_msg}")
    
    return event.undefined()


if __name__ == "__main__":
    run_hooks(notify_ha)

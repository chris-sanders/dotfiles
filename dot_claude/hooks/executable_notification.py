#!/usr/bin/env python3
"""
Notification Hook - Home Assistant Integration
Requires HOMEASSISTANT_TOKEN environment variable
"""
import os
import socket
import urllib.request
import urllib.parse
import json

from hook_utils import HookContext, run_hooks, NotificationHook, neutral

# Configuration
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
        with urllib.request.urlopen(req, timeout=10) as response:
            return True, "Notification sent successfully"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()}"
    except (urllib.error.URLError, OSError) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def notify_ha(ctx: HookContext):
    import logging

    hook = NotificationHook(ctx)
    hostname = socket.gethostname()
    message = (
        f"{hook.message} on {hostname}"
        if hook.message
        else f"Notification on {hostname}"
    )

    success, error_msg = send_home_assistant_notification(message)

    if success:
        logging.info(f"Notification sent: {message}")
    else:
        logging.error(f"Failed to send notification: {error_msg}")

    return neutral()


if __name__ == "__main__":
    run_hooks(notify_ha)

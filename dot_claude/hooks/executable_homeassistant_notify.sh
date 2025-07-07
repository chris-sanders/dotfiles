#!/bin/bash

# Home Assistant notification hook for Claude Code
# This script sends notifications to Home Assistant when Claude Code events occur

# Check if HOMEASSISTANT_TOKEN is set
if [ -z "$HOMEASSISTANT_TOKEN" ]; then
    echo "Error: HOMEASSISTANT_TOKEN environment variable not set"
    exit 1
fi

# Default message and title
MESSAGE="${1:-Claude Code notification}"
TITLE="${2:-Claude Code}"

# Home Assistant API endpoint
URL="https://ha.zarek.cc/api/services/notify/mobile_app_pixel_9_pro_xl"

# Send notification
curl -X POST \
  -H "Authorization: Bearer $HOMEASSISTANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$MESSAGE\", \"title\": \"$TITLE\"}" \
  "$URL" \
  --silent --show-error

echo "Notification sent to Home Assistant"
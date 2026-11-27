#!/usr/bin/env bash
# Enable only on Linux with a running user systemd manager. Never invoke sudo.
set -u
[[ "$(uname -s)" == Linux ]] || exit 0
if [[ ! -x /usr/bin/python3 ]] || ! command -v systemctl >/dev/null 2>&1; then
    echo "go-cache-maintenance: python3 or systemctl missing; skipping"
    exit 0
fi
if ! systemctl --user daemon-reload; then
    echo "go-cache-maintenance: user systemd unavailable; retry on next apply"
    exit 0
fi
systemctl --user enable --now go-cache-maintenance.timer

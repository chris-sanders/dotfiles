"""
Pre-compact hook example for claude-hooks.
This hook runs before conversation compaction.
"""

from claude_hooks import run_hooks


def log_event(event):
    return event.undefined()


if __name__ == "__main__":
    run_hooks(log_event)

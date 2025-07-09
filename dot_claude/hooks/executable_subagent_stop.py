#!/usr/bin/env python3
"""
SubagentStop Hook - Logging hook to capture when a Claude subagent finishes
"""
from hook_utils import HookContext, run_hooks, neutral


def subagent_stop(ctx: HookContext):
    """Log when subagent finishes - raw payload logged automatically by run_hooks"""
    return neutral()


if __name__ == "__main__":
    run_hooks(subagent_stop)

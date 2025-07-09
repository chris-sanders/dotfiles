#!/usr/bin/env python3
"""
PostToolUse Hook - Logging hook to capture all tool results after execution
"""
from hook_utils import HookContext, run_hooks, neutral


def post_tool_use(ctx: HookContext):
    """Log tool results after execution - raw payload logged automatically by run_hooks"""
    return neutral()


if __name__ == "__main__":
    run_hooks(post_tool_use)

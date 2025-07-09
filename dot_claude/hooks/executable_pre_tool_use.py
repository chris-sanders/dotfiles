#!/usr/bin/env python3
"""
PreToolUse Hook - Logging hook to capture all tool calls before execution
"""
from hook_utils import HookContext, run_hooks, neutral


def pre_tool_use(ctx: HookContext):
    """Log tool calls before execution - raw payload logged automatically by run_hooks"""
    return neutral()


if __name__ == "__main__":
    run_hooks(pre_tool_use)

#!/usr/bin/env python3
"""
Stop Hook - Logging hook to capture when Claude finishes a session
"""
from hook_utils import HookContext, run_hooks, neutral


def stop(ctx: HookContext):
    """Log when Claude finishes - raw payload logged automatically by run_hooks"""
    return neutral()


if __name__ == "__main__":
    run_hooks(stop)

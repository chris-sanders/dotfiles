"""
Pre-tool-use hook to enforce uv for Python commands.
This hook blocks direct python commands and redirects to uv.
"""

from claude_hooks import run_hooks


def check_python_command(event):
    if event.tool_name == "Bash":
        command = event.tool_input.get("command", "")
        if command.strip().startswith("python"):
            return event.block("All python commands must be run with uv. `uv run python ...`")
    
    return event.undefined()


if __name__ == "__main__":
    run_hooks(check_python_command)

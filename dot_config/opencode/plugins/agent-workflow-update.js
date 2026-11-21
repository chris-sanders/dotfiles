// Refresh the shared agent-workflow checkout (skills + global AGENTS.md) when OpenCode
// starts. Same script as the Claude Code and Codex SessionStart hooks; it is silent,
// rate-limited (one refresh per 15 minutes across all harnesses) and returns immediately.
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const script = join(homedir(), "src", "agent-workflow", "scripts", "session-start.sh");

export default {
  id: "agent-workflow.update",
  setup: async () => {
    if (existsSync(script)) spawn("bash", [script], { detached: true, stdio: "ignore" }).unref();
  },
};

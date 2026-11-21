// Refresh the shared agent-workflow checkout (skills + global AGENTS.md) when OpenCode
// loads the plugin (server start; a long-lived server serving later sessions does not
// re-run it). Same script as the Claude Code and Codex SessionStart hooks; it is silent,
// rate-limited (one refresh per 15 minutes across all harnesses) and returns immediately.
// Failures are ignored: a refresh must never break OpenCode startup.
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const script = join(homedir(), "src", "agent-workflow", "scripts", "session-start.sh");

export default {
  id: "agent-workflow.update",
  setup: async () => {
    if (!existsSync(script)) return;
    try {
      const child = spawn("bash", [script], { detached: true, stdio: "ignore" });
      child.on("error", () => {});
      child.unref();
    } catch {}
  },
};

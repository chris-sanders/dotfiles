#!/bin/bash
# Approve the agent-workflow session-start hook in Codex (Codex skips a user hook until it is
# approved, and asks again when the hook's declaration or fingerprint changes). Runs on every
# apply, after the bootstrap clone, so a missing helper or a failed run is retried next time; the
# helper is a no-op once the hook is trusted and gives up within 30 seconds if Codex stalls.
repo="$HOME/src/agent-workflow"
s="$repo/scripts/codex-trust-hooks.py"
# An older checkout predates the helper; on a Codex-only host nothing else would update it.
[ ! -f "$s" ] && [ -f "$repo/scripts/update.sh" ] && bash "$repo/scripts/update.sh" --update >/dev/null 2>&1
if [ -f "$s" ] && command -v python3 >/dev/null 2>&1; then
  python3 "$s" --install || true
else
  echo "agent-workflow: $s not found yet; Codex hook approval retries on the next chezmoi apply"
fi
exit 0

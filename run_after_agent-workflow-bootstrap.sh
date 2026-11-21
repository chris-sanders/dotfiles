#!/usr/bin/env bash
# Make sure the shared agent-workflow checkout exists, so the agent session-start hooks
# have something to refresh. Runs on every `chezmoi apply` and exits at once when the
# checkout is present; a failed clone (no GitHub SSH key yet) is retried on the next apply.
set -u
dest="$HOME/src/agent-workflow"
[ -e "$dest" ] && exit 0
command -v git >/dev/null 2>&1 || { echo "agent-workflow: git not installed; skipping clone"; exit 0; }
mkdir -p "$HOME/src"
if GIT_SSH_COMMAND="ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new" \
   git clone -q git@github.com:chris-sanders/agent-workflow.git "$dest"; then
  bash "$dest/scripts/install-user-skills.sh" --install >/dev/null 2>&1 ||
    echo "agent-workflow: installer reported conflicts; run: bash $dest/scripts/install-user-skills.sh --check"
else
  echo "agent-workflow: clone failed (GitHub SSH key?); the next chezmoi apply retries"
fi
exit 0

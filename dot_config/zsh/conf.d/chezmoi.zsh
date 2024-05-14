# Function to automate chezmoi git operations
chezmoi_sync() {
  local message=${1:-"Updated configuration"}
  chezmoi git add .
  chezmoi git commit -- -m "$message"
  chezmoi git push
}

alias cm_sync=chezmoi_sync


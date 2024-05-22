# Directory containing kubeconfig files
KUBECONFIG_DIR=~/.config/kube/configs.d/

# Function to load all kubeconfig files
load_kubeconfigs() {
  export KUBECONFIG=$(find "$KUBECONFIG_DIR" -type f | tr '\n' ':')
}

# Initially load all configs
load_kubeconfigs

# Function to set kubeconfig per shell by filename
set_kubeconfig() {
  local config_file="$KUBECONFIG_DIR$1"
  if [[ -f "$config_file" ]]; then
    export KUBECONFIG="$config_file"
    export KUBE_CONTEXT=$(kubectl config current-context)
  else
    echo "Kubeconfig file '$config_file' not found"
  fi
}

# Function to list all available kubeconfig files and indicate the active one
list_kubeconfigs() {
  for file in "$KUBECONFIG_DIR"*; do
    if [[ "$file" == "$KUBECONFIG" ]]; then
      echo "* $(basename "$file") (active)"
    else
      echo "  $(basename "$file")"
    fi
  done
}

# Powerlevel10k customization to show Kubernetes context
typeset -g POWERLEVEL9K_KUBECONTEXT_SHOW_ON_COMMAND='kubectl'
POWERLEVEL9K_KUBECONTEXT_CONTENT_EXPANSION='${KUBE_CONTEXT}'
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(kubecontext)

# Add kubectl completions and alias
if command -v kubectl > /dev/null 2>&1; then
  source <(kubectl completion zsh)
  alias k=kubectl
  compdef _kubectl k
fi

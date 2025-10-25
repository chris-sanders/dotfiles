#!/usr/bin/env bash
# ~/ansible/bin/container-exec.sh

# Calculate container name dynamically
ANSIBLE_CONTAINER_NAME="ansible-molecule-${MOLECULE_VM_ENVIRONMENT:-dev1}"

# Common function to execute a command in the container
function execute_in_container() {
  local command=$1
  shift
  
  # Get current directory and container mount information
  CURRENT_DIR=$(pwd)
  MOUNT_SOURCE=$(podman inspect --format '{{range .Mounts}}{{if eq .Destination "/workspace"}}{{.Source}}{{end}}{{end}}' $ANSIBLE_CONTAINER_NAME)

  # If the mounted directory is the current directory or a parent of it
  if [[ "$CURRENT_DIR" == "$MOUNT_SOURCE"* ]]; then
    # Calculate relative path
    RELATIVE_PATH="${CURRENT_DIR#$MOUNT_SOURCE}"
    
    # Handle the case where we're exactly at the mount point
    if [[ -z "$RELATIVE_PATH" ]]; then
      CONTAINER_PATH="/workspace"
    else
      CONTAINER_PATH="/workspace$RELATIVE_PATH"
    fi
    
    # Verify path exists before executing
    podman exec -it $ANSIBLE_CONTAINER_NAME mkdir -p "$CONTAINER_PATH"
    
    # Execute command in the correct directory
    podman exec -it -w "$CONTAINER_PATH" $ANSIBLE_CONTAINER_NAME $command "$@"
  else
    echo "Error: Current directory ($CURRENT_DIR) is not within the mounted path ($MOUNT_SOURCE)"
    exit 1
  fi
}

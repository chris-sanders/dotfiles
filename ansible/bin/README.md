# Ansible Container Scripts

Simple wrapper scripts for running ansible in containers with environment isolation.

## Usage

**Start containers:**
```bash
ac-start                           # Start dev1 (default)
MOLECULE_VM_ENVIRONMENT=dev2 ac-start  # Start dev2
MOLECULE_VM_ENVIRONMENT=ci ac-start    # Start ci
```

**Run commands:**
```bash
ac-run molecule test                        # Run in dev1
MOLECULE_VM_ENVIRONMENT=dev2 ac-run molecule converge  # Run in dev2
MOLECULE_VM_ENVIRONMENT=ci ac-run ansible-playbook ... # Run in ci
```

**Stop containers:**
```bash
ac-stop                           # Stop dev1
MOLECULE_VM_ENVIRONMENT=dev2 ac-stop  # Stop dev2
```

## Environments

- `dev1` (default)
- `dev2` 
- `ci`

Each environment runs in its own isolated container: `ansible-molecule-{env}`
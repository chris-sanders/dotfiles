# Go build cache maintenance (Linux / WSL)

Installed by chezmoi as a user-level systemd timer; requires Python 3 and a running systemd user manager. No root privileges, packages, or external services are installed. The timer is hourly with up to five minutes of jitter.

Defaults: 48-hour retention, a soft budget of the smaller of 100 GiB or 15% of the cache filesystem's usable capacity, and additional oldest-first eviction when disk usage reaches 80%, targeting 70%. Files used within six hours are never intentionally evicted, even under pressure. This is best effort, not a hard quota. An active build can race with external eviction and may need to rebuild/retry. The existing WSL virtual disk capacity limit is the hard host protection.

Go's normal cache uses modification timestamps to track reuse (see https://go.dev/src/cmd/go/internal/cache/cache.go). The script scans only the 256 standard Go build cache shards and removes matching regular artifact files owned by the current user. Symlinks, hardlinks, foreign files, fuzz inputs, directories (including cached executable directories in newer Go versions), module caches and all other developer/agent data are excluded. Thus budget measurements cover managed regular artifacts only, not every byte of the cache. If newer Go has native size limits, prefer those when available.

Check the actual cache location with `go env GOCACHE`. The default is `$XDG_CACHE_HOME/go-build` or `~/.cache/go-build`. For an explicitly configured custom cache path or budget, create an **unmanaged local** file at `~/.config/go-cache-maintenance.env`, for example:

```ini
GO_CACHE_MAX_GIB=60
GO_CACHE_MAX_PERCENT=10
# GO_CACHE_DIR=/home/chris/custom/go-build
```

The timer reads that file on every invocation. For a default-config dry run:

```sh
~/.local/bin/go-cache-maintenance --dry-run
systemctl --user list-timers go-cache-maintenance.timer
systemctl --user start go-cache-maintenance.service
journalctl --user -u go-cache-maintenance.service -n 20 --no-pager
```

To dry-run with overrides, pass the corresponding environment variables explicitly. On headless hosts, if needed, enable user lingering with `sudo loginctl enable-linger "$USER"`. This is a manual choice, not an automatic privilege escalation. On WSL, the user manager needs to be running; the timer does not keep the WSL VM alive.

Use existing system `fstrim.timer` and `systemd-tmpfiles-clean.timer` if available; check them separately. TRIM does not guarantee a non-sparse Windows VHDX will shrink, and enabling sparse VHDX or offline compaction is outside this portable user policy.

Disable: `systemctl --user disable --now go-cache-maintenance.timer`. Reapplying chezmoi will enable it again unless excluded locally. No broad cache cleaning, monitoring or notification system is included.

Run regression tests from the source repository:
```sh
python3 -m unittest discover -s tests -p 'test_go_cache_maintenance.py'
```

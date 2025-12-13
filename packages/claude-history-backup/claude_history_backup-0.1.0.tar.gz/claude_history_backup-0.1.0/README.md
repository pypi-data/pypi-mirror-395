# claude-history-backup

Backup and manage Claude Code session history.

## Install

```bash
make install
```

## Usage

```bash
# Show sync status
claude-history status

# Sync sessions to backup
claude-history sync

# Install daily cron job
claude-history cron-install

# Check if sync needed (for cron)
claude-history cron-check
```

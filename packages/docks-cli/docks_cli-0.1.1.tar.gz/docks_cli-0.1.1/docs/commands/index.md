# Commands Reference

Docks CLI provides commands organized into logical groups for managing evaluation runs, datasets, and prebaked images.

## Global Options

These options are available for all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--profile` | `-p` | Config profile to use (default: `default`) |
| `--verbose` | `-v` | Enable verbose output |
| `--debug` | | Enable debug output (includes HTTP requests) |
| `--version` | `-V` | Show version information |
| `--help` | | Show help message |

## Command Groups

### [auth](auth.md)
Authentication and credential management.

```bash
docks auth login      # Login with API token
docks auth logout     # Clear stored credentials
docks auth status     # Show current auth status
docks auth token      # Display current token
```

### [runs](runs.md)
Evaluation run management.

```bash
docks runs list       # List evaluation runs
docks runs get        # Get run details
docks runs harbor-list # List Harbor runs
docks runs trials     # List trials for a Harbor run
docks runs artifacts  # Download trial artifacts
```

### [datasets](datasets.md)
Dataset management.

```bash
docks datasets list   # List available datasets
docks datasets get    # Get dataset details
```

### [images](images.md)
Prebaked image management.

```bash
docks images list     # List prebaked images
docks images get      # Get image details
```

## Quick Commands

### `docks run`
Create and launch a new evaluation run.

```bash
docks run --dataset <dataset-id> --agent <agent-config>
```

### `docks status`
Show current configuration and authentication status.

```bash
docks status
```

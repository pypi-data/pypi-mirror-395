# runs - Run Management Commands

Manage evaluation runs, Harbor runs, and download artifacts.

## Commands

### `docks runs list`

List evaluation runs.

```bash
docks runs list [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of runs to return (default: 20)
- `--status TEXT`: Filter by status (pending, running, completed, failed)

**Example:**
```bash
docks runs list --limit 10 --status running
```

### `docks runs get`

Get details of a specific run.

```bash
docks runs get RUN_ID
```

**Example:**
```bash
docks runs get abc123-def456-ghi789
```

### `docks runs stop`

Stop a running evaluation.

```bash
docks runs stop RUN_ID
```

**Example:**
```bash
docks runs stop abc123-def456-ghi789
```

## Evaluation Commands

Evaluation commands for running benchmarks at scale.

### `docks runs eval-list`

List evaluation runs.

```bash
docks runs eval-list [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of runs to return (default: 20)

**Example:**
```bash
docks runs eval-list --limit 5
```

### `docks runs eval-get`

Get details of an evaluation run.

```bash
docks runs eval-get RUN_ID
```

**Example:**
```bash
docks runs eval-get abc123-def456-ghi789
```

### `docks runs trials`

List trials for an evaluation run.

```bash
docks runs trials RUN_ID [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of trials to return

**Example:**
```bash
docks runs trials abc123-def456-ghi789
```

### `docks runs trial`

Get detailed trial info including artifact URIs.

```bash
docks runs trial RUN_ID TRIAL_ID
```

**Example:**
```bash
docks runs trial abc123-def456-ghi789 trial-001
```

### `docks runs artifacts`

Download artifacts from completed evaluation trials.

```bash
docks runs artifacts RUN_ID [OPTIONS]
```

**Options:**
- `--trial, -t TEXT`: Specific trial ID (downloads all if not specified)
- `--output, -o PATH`: Output directory (default: current directory)
- `--type TEXT`: Artifact type to download (logs, trajectory, diff, result)

**Examples:**
```bash
# Download all artifacts from a run
docks runs artifacts abc123-def456-ghi789 --output ./artifacts

# Download only logs from a specific trial
docks runs artifacts abc123-def456-ghi789 --trial trial-001 --type logs

# Download trajectory files
docks runs artifacts abc123-def456-ghi789 --type trajectory
```

**Artifact Types:**
- `logs`: Execution logs from the agent run
- `trajectory`: Step-by-step trajectory of agent actions
- `diff`: Git diff of changes made by the agent
- `result`: Final evaluation results and metrics

## Run Statuses

| Status | Description |
|--------|-------------|
| `pending` | Run is queued and waiting to start |
| `provisioning` | Resources are being allocated |
| `running` | Run is actively executing |
| `completed` | Run finished successfully |
| `failed` | Run encountered an error |
| `cancelled` | Run was manually stopped |

## Examples

### Monitor a Run

```bash
# List recent runs
docks runs list --limit 5

# Watch a specific run
docks runs get abc123-def456-ghi789

# View trials for completed evaluation run
docks runs trials abc123-def456-ghi789

# Download results
docks runs artifacts abc123-def456-ghi789 --output ./results
```

### Batch Operations

```bash
# List failed runs
docks runs list --status failed

# Get details of each failed run
for run_id in $(docks runs list --status failed --format json | jq -r '.[].id'); do
    docks runs get $run_id
done
```

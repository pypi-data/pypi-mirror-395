# Docks CLI - Agent Instructions

This file provides structured instructions for AI agents to operate the Docks CLI for running evaluations, capturing diagnostics, and generating reports.

## Prerequisites

```bash
# Install the CLI
pip install docks-cli

# Authenticate (get token from your admin)
docks auth login --api-url https://api.docks.dev --token <your-token>

# Verify authentication
docks auth status
```

---

## Command Reference

### Authentication

| Command | Description |
|---------|-------------|
| `docks auth login --api-url <url> --token <token>` | Save credentials |
| `docks auth status` | Check authentication status |
| `docks auth logout` | Clear saved credentials |

### Datasets

| Command | Description |
|---------|-------------|
| `docks datasets list` | List all datasets |
| `docks datasets aliases` | List dataset aliases for eval-run |
| `docks datasets tasks <alias>` | List tasks in a dataset |
| `docks datasets resolve <alias>` | Get full GCS URI for alias |

### Runs

| Command | Description |
|---------|-------------|
| `docks runs eval-run [options]` | Create and start evaluation |
| `docks runs eval-start <run_id>` | Start a queued run |
| `docks runs eval-get <run_id>` | Get run details and status |
| `docks runs eval-list --limit N` | List recent runs |
| `docks runs eval-cancel <run_id>` | Cancel a running evaluation |
| `docks runs trials <run_id>` | List all trials in a run |
| `docks runs trial <run_id> <trial_id>` | Get detailed trial info |
| `docks runs artifacts <run_id> --output <dir>` | Download artifacts |

### Reports

| Command | Description |
|---------|-------------|
| `docks report html <run_id> --output <file>` | Generate HTML report |
| `docks report tui <run_id>` | Interactive TUI viewer |

### Sandbox (Interactive Debugging)

| Command | Description |
|---------|-------------|
| `docks sandbox create --name <name> --image <image>` | Create sandbox |
| `docks sandbox list` | List active sandboxes |
| `docks sandbox shell <sandbox_id>` | Connect via shell |
| `docks sandbox exec <sandbox_id> "<command>"` | Run command |
| `docks sandbox stop <sandbox_id>` | Terminate sandbox |

---

## Workflow 1: Run an Evaluation

### Step 1: Check available datasets
```bash
docks datasets aliases
```

Example output:
```
swebench-lite          gs://izumi-harbor-datasets/swebench-lite
terminal-bench-core    gs://izumi-harbor-datasets/terminal-bench-core-0.1.1
dev-docks-appsmith     gs://izumi-harbor-datasets/dev-docks-appsmith
```

### Step 2: List tasks in a dataset
```bash
docks datasets tasks swebench-lite
```

### Step 3: Create and start evaluation run
```bash
docks runs eval-run \
  --name "My Evaluation Run" \
  --dataset swebench-lite \
  --tasks "django__django-11039,astropy__astropy-12907" \
  --agent claude-code \
  --model claude-sonnet-4-20250514 \
  --start
```

Options:
- `--name`: Human-readable run name
- `--dataset`: Dataset alias or full GCS URI
- `--tasks`: Comma-separated task slugs (or omit for all tasks)
- `--agent`: Agent type (claude-code, custom)
- `--model`: Model to use
- `--start`: Auto-start (otherwise use eval-start later)
- `--attempts`: Attempts per task (default: 3)
- `--concurrent`: Max concurrent trials (default: 10)

### Step 4: Monitor progress
```bash
# Get run status
docks runs eval-get <run_id>

# List trials with status
docks runs trials <run_id>
```

Example trials output:
```
ID             Task                    Agent        Status    Passed   Artifacts
─────────────────────────────────────────────────────────────────────────────────
4cf9c4b0-b37   django__django-11039    claude-code  success   Yes      logs,diff
eb600eb8-2e9   astropy__astropy-12907  claude-code  running   -        -
```

### Step 5: Wait for completion
Poll until status is `completed` or `failed`:
```bash
# Check run status
docks runs eval-get <run_id> | grep "Status:"
```

---

## Workflow 2: Download Artifacts and Generate Reports

### Download all artifacts
```bash
docks runs artifacts <run_id> --output ./results/
```

Downloads to:
```
./results/
├── <trial_id>/
│   ├── logs.txt           # Agent execution logs
│   ├── trajectory.json    # Full conversation trajectory
│   ├── diff.patch         # Code changes made
│   └── result.json        # Test results
```

### Generate HTML report
```bash
docks report html <run_id> --output ./report.html
```

### View in TUI (interactive terminal)
```bash
docks report tui <run_id>
```

---

## Workflow 3: Get Diagnostics for Failed Trials

### Step 1: List trials and find failures
```bash
docks runs trials <run_id>
```

### Step 2: Get detailed trial info
```bash
docks runs trial <run_id> <trial_id>
```

Example output:
```
Trial: 4cf9c4b0-b37a-4563-81dc-331650e75b08
  Task:        django__django-11039
  Agent:       claude-code
  Status:      failed
  Duration:    45s
  Error:       Test assertion failed

  Artifacts:
    logs_uri:       gs://izumi-artifacts/trials/4cf9c4b0.../logs.txt
    trajectory_uri: gs://izumi-artifacts/trials/4cf9c4b0.../trajectory.json
    diff_uri:       gs://izumi-artifacts/trials/4cf9c4b0.../diff.patch
```

### Step 3: Download specific trial artifacts
```bash
# Download logs
gsutil cp gs://izumi-artifacts/trials/<trial_id>/logs.txt ./

# Or download all for this trial
docks runs artifacts <run_id> --trial <trial_id> --output ./debug/
```

---

## Workflow 4: Debug in Interactive Sandbox

### Step 1: Create sandbox with task image
```bash
docks sandbox create \
  --name "debug-session" \
  --image us-west2-docker.pkg.dev/izumi-479101/izumi-repo/swebench-django__django-11039:latest \
  --timeout 60
```

### Step 2: Connect and debug
```bash
docks sandbox shell <sandbox_id>
```

### Step 3: Run commands
```bash
docks sandbox exec <sandbox_id> "cd /testbed && python -m pytest tests/"
```

### Step 4: Cleanup
```bash
docks sandbox stop <sandbox_id>
```

---

## Common Patterns

### Run evaluation on all tasks in a dataset
```bash
docks runs eval-run \
  --dataset swebench-lite \
  --agent claude-code \
  --start
# Omit --tasks to run all
```

### Run with specific model configuration
```bash
docks runs eval-run \
  --dataset dev-docks-appsmith \
  --agent claude-code \
  --model claude-sonnet-4-20250514 \
  --tasks "appsmith__fix-auth-flow" \
  --attempts 5 \
  --concurrent 3 \
  --start
```

### Check if run is complete
```bash
STATUS=$(docks runs eval-get <run_id> 2>/dev/null | grep "Status:" | awk '{print $2}')
if [ "$STATUS" = "completed" ]; then
  echo "Run completed"
fi
```

### Get pass rate
```bash
docks runs eval-get <run_id> | grep -E "(Passed|Failed|Total)"
```

---

## Error Handling

### Authentication errors
```bash
# Check status
docks auth status

# Re-authenticate
docks auth logout
docks auth login --api-url <url> --token <token>
```

### Run stuck in "running" state
```bash
# Cancel the run
docks runs eval-cancel <run_id>

# Check for error in trials
docks runs trials <run_id>
```

### Dataset not found
```bash
# List available aliases
docks datasets aliases

# Use full GCS URI if alias doesn't exist
docks runs eval-run --dataset gs://bucket/path/to/dataset ...
```

### Debug mode (see HTTP requests)
```bash
docks --debug runs eval-get <run_id>
```

---

## Output Formats

### JSON output (for parsing)
```bash
# Most commands support JSON output via API
curl -s "$API_URL/tenants/$TENANT/harbor/runs/$RUN_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Trial status values
- `pending` - Waiting to start
- `running` - Currently executing
- `success` - Completed with passing tests
- `failed` - Completed with failing tests
- `error` - Execution error (check error_message)
- `cancelled` - Manually cancelled

### Run status values
- `queued` - Created but not started
- `running` - In progress
- `completed` - All trials finished
- `failed` - Run failed to start
- `cancelled` - Manually cancelled

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DOCKS_API_URL` | Override API URL |
| `DOCKS_TOKEN` | Override auth token |
| `DOCKS_PROFILE` | Config profile to use |

---

## Quick Reference

```bash
# Full evaluation workflow
docks datasets aliases                                    # 1. Find dataset
docks datasets tasks <alias>                              # 2. List tasks
docks runs eval-run --dataset <alias> --agent claude-code --start  # 3. Start
docks runs trials <run_id>                                # 4. Monitor
docks runs artifacts <run_id> --output ./results/         # 5. Download
docks report html <run_id> --output ./report.html         # 6. Report

# Diagnostics
docks runs eval-get <run_id>                              # Run summary
docks runs trial <run_id> <trial_id>                      # Trial details
docks --debug runs trials <run_id>                        # HTTP debug

# Sandbox debugging
docks sandbox create --name debug --image <image>         # Create
docks sandbox shell <sandbox_id>                          # Connect
docks sandbox stop <sandbox_id>                           # Cleanup
```

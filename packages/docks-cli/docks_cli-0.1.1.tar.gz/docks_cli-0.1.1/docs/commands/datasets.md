# datasets - Dataset Management Commands

Manage evaluation datasets and tasks.

## Commands

### `docks datasets list`

List all datasets.

```bash
docks datasets list [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of datasets to return

**Example:**
```bash
docks datasets list
```

### `docks datasets get`

Get details of a specific dataset.

```bash
docks datasets get DATASET_ID
```

**Example:**
```bash
docks datasets get swebench-lite-v1
```

### `docks datasets tasks`

List tasks in a dataset.

```bash
docks datasets tasks DATASET_ID [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of tasks to return
- `--difficulty TEXT`: Filter by difficulty (easy, medium, hard)

**Example:**
```bash
docks datasets tasks swebench-lite-v1 --difficulty medium
```

### `docks datasets create`

Create a new empty dataset.

```bash
docks datasets create NAME [OPTIONS]
```

**Options:**
- `--description TEXT`: Dataset description
- `--version TEXT`: Version string (default: "1.0.0")

**Example:**
```bash
docks datasets create my-custom-dataset --description "Custom evaluation tasks"
```

### `docks datasets sync`

Sync dataset from YAML manifest file.

```bash
docks datasets sync MANIFEST_FILE
```

**Example:**
```bash
docks datasets sync ./manifests/datasets/enterprise-swe-v1.yaml
```

## Dataset Manifest Format

Datasets can be defined in YAML manifests:

```yaml
name: enterprise-swe-v1
version: "1.0.0"
description: Enterprise SWE evaluation tasks

tasks:
  - slug: auth-fix-001
    repo: github.com/example/auth-service
    ref: main
    path: src/auth
    difficulty: medium
    rubric: |
      Fix the authentication bypass vulnerability.
      Tests must pass.

  - slug: api-optimize-002
    repo: github.com/example/api-gateway
    ref: v2.0
    path: src/handlers
    difficulty: hard
    rubric: |
      Optimize the rate limiting implementation.
      Latency should decrease by 50%.
```

## Task Properties

| Property | Description |
|----------|-------------|
| `slug` | Unique identifier for the task |
| `repo` | Repository URL |
| `ref` | Git ref (branch, tag, or commit) |
| `path` | Path within the repository |
| `difficulty` | Task difficulty (easy, medium, hard) |
| `rubric` | Evaluation criteria and instructions |

## SWE-bench Datasets

Docks includes support for SWE-bench evaluation datasets:

- **SWE-bench Lite**: 300 curated tasks from popular open-source projects
- **SWE-bench Full**: Complete set of 2,294 tasks

List available SWE-bench datasets:
```bash
docks datasets list | grep swebench
```

## Examples

### View Dataset Contents

```bash
# List all datasets
docks datasets list

# Get dataset details
docks datasets get swebench-lite-v1

# List tasks with difficulty filter
docks datasets tasks swebench-lite-v1 --difficulty easy --limit 10
```

### Create Custom Dataset

```bash
# Create empty dataset
docks datasets create my-dataset --description "My custom tasks"

# Sync from manifest
docks datasets sync ./my-tasks.yaml
```

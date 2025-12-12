# Docks CLI

**Docks** is a command-line interface for managing evaluation runs, datasets, and prebaked images for AI code agent benchmarking.

## Installation

```bash
pip install docks-cli
```

Or install from source:

```bash
git clone https://github.com/your-org/docks-cli.git
cd docks-cli
pip install -e .
```

## Quick Start

### 1. Authenticate

```bash
# Login with your API token
docks auth login

# Check your authentication status
docks auth status
```

### 2. List Runs

```bash
# List recent evaluation runs
docks runs list

# Get details of a specific run
docks runs get <run-id>
```

### 3. Work with Evaluation Runs

```bash
# List evaluation runs
docks runs eval-list

# View trials for a run
docks runs trials <run-id>

# Download artifacts from completed trials
docks runs artifacts <run-id> --output ./artifacts
```

## Features

- **Run Management**: Create, monitor, and manage evaluation runs
- **Evaluation Runs**: Work with benchmark evaluation runs and trials
- **Dataset Management**: List and manage evaluation datasets
- **Image Management**: Work with prebaked Docker images
- **Artifact Downloads**: Download logs, trajectories, and results from completed runs
- **Rich Terminal Output**: Beautiful tables and formatted output using Rich

## Configuration

Docks stores its configuration in `~/.docks/config.toml`:

```toml
[default]
api_url = "https://api.docks.example.com"
tenant_id = "your-tenant-id"
token = "your-api-token"
```

You can manage multiple profiles by adding sections:

```toml
[staging]
api_url = "https://staging-api.docks.example.com"
tenant_id = "staging-tenant-id"
token = "staging-token"
```

Use `--profile` to switch between configurations:

```bash
docks --profile staging runs list
```

## Commands

See the [Commands](commands/index.md) section for detailed documentation of all available commands.

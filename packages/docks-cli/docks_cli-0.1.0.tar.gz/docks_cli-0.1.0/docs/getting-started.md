# Getting Started

This guide walks you through setting up Docks CLI and running your first evaluation.

## Prerequisites

- Python 3.9 or later
- pip or pipx for installation
- A Docks API account with tenant credentials

## Installation

### Using pip

```bash
pip install docks-cli
```

### Using pipx (recommended)

```bash
pipx install docks-cli
```

### From source

```bash
git clone https://github.com/contextlab/docks-cli
cd docks-cli
pip install -e .
```

## Configuration

### Login with credentials

```bash
docks auth login
```

You'll be prompted for:
- **API URL**: Your Docks API endpoint (e.g., `https://api.docks.example.com`)
- **Tenant ID**: Your organization's tenant identifier
- **Token**: Your API authentication token

### Environment variables

Alternatively, set credentials via environment variables:

```bash
export DOCKS_API_URL="https://api.docks.example.com"
export DOCKS_TENANT_ID="your-tenant-id"
export DOCKS_TOKEN="your-api-token"
```

### Verify setup

```bash
docks auth status
```

This will confirm your authentication is working.

## Quick Start

### List available datasets

```bash
docks datasets list
```

### View tasks in a dataset

```bash
docks datasets tasks swebench-lite-v1 --limit 10
```

### List evaluation runs

```bash
docks runs list
```

### View evaluation runs

```bash
docks runs eval-list
```

### Get run details

```bash
docks runs get <run-id>
```

### View trials for an evaluation run

```bash
docks runs trials <run-id>
```

### Download artifacts

```bash
docks runs artifacts <run-id> --output ./results
```

## Working with Prebaked Images

Prebaked images speed up evaluation runs by pre-installing dependencies.

### List available prebaked images

```bash
docks images list
```

### Build a prebaked image

```bash
docks images prebake astropy__astropy-12907
```

### Check build status

```bash
docks images status
```

### Validate an image

```bash
docks images validate astropy__astropy-12907
```

## Debugging

### Verbose output

Add `-v` or `--verbose` for detailed output:

```bash
docks -v runs list
```

### Debug mode

Add `--debug` to see HTTP requests and responses:

```bash
docks --debug runs eval-list
```

## Next Steps

- Read the [Commands Reference](commands/index.md) for detailed command documentation
- Learn about [Authentication](commands/auth.md) for multi-profile setup
- Explore [Evaluation Runs](commands/runs.md#evaluation-commands) for benchmark evaluations
- Manage [Prebaked Images](commands/images.md) for faster evaluations

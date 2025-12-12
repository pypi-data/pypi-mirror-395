# images - Prebaked Image Commands

Manage prebaked Docker images for evaluation environments.

## Overview

Prebaked images are Docker images with all dependencies pre-installed for faster evaluation runs. They are stored in Google Cloud Storage and built via Cloud Build.

## Commands

### `docks images list`

List prebaked images in GCS.

```bash
docks images list [OPTIONS]
```

**Options:**
- `--limit, -n INTEGER`: Number of images to return
- `--repo TEXT`: Filter by repository name

**Example:**
```bash
docks images list --repo astropy
```

### `docks images prebake`

Build prebaked images via Cloud Build.

```bash
docks images prebake INSTANCE_ID [OPTIONS]
```

**Options:**
- `--force`: Rebuild even if image exists
- `--async`: Don't wait for build to complete

**Example:**
```bash
# Build single image
docks images prebake astropy__astropy-12907

# Force rebuild
docks images prebake astropy__astropy-12907 --force

# Build without waiting
docks images prebake astropy__astropy-12907 --async
```

### `docks images status`

Check Cloud Build status.

```bash
docks images status [BUILD_ID]
```

**Example:**
```bash
# Check recent builds
docks images status

# Check specific build
docks images status abc123-def456
```

### `docks images validate`

Validate that a prebaked image has all prerequisites.

```bash
docks images validate INSTANCE_ID
```

Checks:
- Image exists in registry
- Required dependencies installed
- Test environment configured

**Example:**
```bash
docks images validate astropy__astropy-12907
```

### `docks images estimate`

Show cost estimate for prebaking all images.

```bash
docks images estimate [OPTIONS]
```

**Options:**
- `--dataset TEXT`: Dataset to estimate (default: swebench-lite)

**Example:**
```bash
docks images estimate --dataset swebench-lite
```

## Image Naming Convention

Prebaked images follow this naming pattern:
```
us-west2-docker.pkg.dev/PROJECT/REPO/swebench-INSTANCE_ID:latest
```

For example:
```
us-west2-docker.pkg.dev/izumi-479101/izumi-repo/swebench-astropy__astropy-12907:latest
```

## GCS Storage

Prebaked image configs and metadata are stored in GCS:
```
gs://izumi-harbor-datasets/swebench/
  ├── astropy__astropy-12907/
  │   ├── task.json
  │   └── Dockerfile
  ├── django__django-11099/
  │   ├── task.json
  │   └── Dockerfile
  ...
```

## Building Images in Batch

For building multiple images:

```bash
# Build images for a dataset
docks images prebake --dataset swebench-lite --async

# Monitor progress
docks images status
```

## Cost Considerations

| Resource | Cost |
|----------|------|
| Cloud Build (per minute) | ~$0.003 |
| GCS Storage (per GB/month) | ~$0.023 |
| Artifact Registry (per GB/month) | ~$0.10 |

**Typical costs:**
- Single image build: ~$0.05
- SWE-bench Lite (300 images): ~$15
- Storage (300 images): ~$7/month

## Examples

### Check Image Availability

```bash
# List available images
docks images list

# Validate specific image
docks images validate astropy__astropy-12907
```

### Build Missing Images

```bash
# Check what needs building
docks images estimate

# Build missing images
docks images prebake astropy__astropy-12907

# Check build status
docks images status
```

# auth - Authentication Commands

Manage authentication credentials for the Docks API.

## Commands

### `docks auth login`

Save authentication credentials to the config file.

```bash
docks auth login
```

This interactive command will prompt you for:
- **API URL**: The Docks API endpoint
- **Tenant ID**: Your organization's tenant identifier
- **Token**: Your API authentication token

Credentials are saved to `~/.docks/config.toml`.

### `docks auth status`

Show current authentication status.

```bash
docks auth status
```

Displays:
- Current profile
- API URL
- Tenant ID
- Token status (masked)
- Connection status

### `docks auth logout`

Clear saved authentication credentials.

```bash
docks auth logout
```

Removes the stored credentials for the current profile from the config file.

### `docks auth token`

Generate a development token (requires API access).

```bash
docks auth token
```

This is useful for creating tokens for automated scripts or CI/CD pipelines.

## Configuration File

Credentials are stored in `~/.docks/config.toml`:

```toml
[default]
api_url = "https://api.docks.example.com"
tenant_id = "your-tenant-id"
token = "your-api-token"
```

## Using Multiple Profiles

You can configure multiple profiles for different environments:

```toml
[default]
api_url = "https://api.docks.example.com"
tenant_id = "prod-tenant-id"
token = "prod-token"

[staging]
api_url = "https://staging-api.docks.example.com"
tenant_id = "staging-tenant-id"
token = "staging-token"
```

Switch between profiles using the `--profile` flag:

```bash
docks --profile staging auth status
docks --profile staging runs list
```

## Environment Variables

You can also set credentials via environment variables:

```bash
export DOCKS_API_URL="https://api.docks.example.com"
export DOCKS_TENANT_ID="your-tenant-id"
export DOCKS_TOKEN="your-api-token"
```

Environment variables take precedence over config file values.

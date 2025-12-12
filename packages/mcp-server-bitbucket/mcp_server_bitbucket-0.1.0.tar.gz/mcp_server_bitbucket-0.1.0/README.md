# Bitbucket MCP Server

MCP server for Bitbucket API operations. Works with Claude Code, Claude Desktop, and any MCP-compatible client.

## Features

- **Repositories**: get, create, delete, list
- **Pull Requests**: create, get, list, merge
- **Pipelines**: trigger, get status, list, view logs, stop
- **Branches**: list, get

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install with pipx (isolated environment)
pipx install mcp-server-bitbucket

# Or with pip
pip install mcp-server-bitbucket
```

### Option 2: From Source

```bash
git clone https://github.com/simplekyc/bitbucket-mcp.git
cd bitbucket-mcp
poetry install
```

## Configuration

Set environment variables for Bitbucket authentication:

```bash
export BITBUCKET_WORKSPACE=your-workspace
export BITBUCKET_EMAIL=your-email@example.com
export BITBUCKET_API_TOKEN=your-app-password
```

To create an app password:
1. Go to Bitbucket → Settings → App passwords
2. Create a new app password with these permissions:
   - Repositories: Read, Write, Admin, Delete
   - Pull Requests: Read, Write
   - Pipelines: Read, Write

## Usage with Claude Code

Add to your Claude Code MCP configuration (`~/.claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "bitbucket": {
      "command": "mcp-server-bitbucket",
      "env": {
        "BITBUCKET_WORKSPACE": "your-workspace",
        "BITBUCKET_EMAIL": "your-email@example.com",
        "BITBUCKET_API_TOKEN": "your-app-password"
      }
    }
  }
}
```

If installed from source:

```json
{
  "mcpServers": {
    "bitbucket": {
      "command": "poetry",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/bitbucket-mcp",
      "env": {
        "BITBUCKET_WORKSPACE": "your-workspace",
        "BITBUCKET_EMAIL": "your-email@example.com",
        "BITBUCKET_API_TOKEN": "your-app-password"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_repository` | Get repository info |
| `create_repository` | Create a new repository |
| `delete_repository` | Delete a repository |
| `list_repositories` | List repositories in workspace |
| `create_pull_request` | Create a pull request |
| `get_pull_request` | Get PR details |
| `list_pull_requests` | List PRs by state |
| `merge_pull_request` | Merge a PR |
| `trigger_pipeline` | Run a pipeline |
| `get_pipeline` | Get pipeline status |
| `list_pipelines` | List recent pipelines |
| `get_pipeline_logs` | View pipeline logs |
| `stop_pipeline` | Stop a running pipeline |
| `list_branches` | List branches |
| `get_branch` | Get branch info |

## HTTP Server (Cloud Run)

For deploying as an HTTP API:

```bash
# Run locally
poetry run uvicorn src.http_server:app --reload --port 8080

# Deploy to Cloud Run
gcloud run deploy bitbucket-mcp-service \
  --source . \
  --region australia-southeast1 \
  --set-secrets "BITBUCKET_EMAIL=bitbucket-email:latest,BITBUCKET_API_TOKEN=bitbucket-token:latest"
```

## License

MIT

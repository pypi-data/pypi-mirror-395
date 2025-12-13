# Hephaestus Docker Power

A Kiro Power for setting up and managing Hephaestus using Docker containers.

## Overview

This power provides MCP tools and steering guides for:
- Setting up Hephaestus development environment
- Managing Docker containers (Qdrant, MCP server)
- Initializing databases
- Troubleshooting common issues
- Production deployment best practices

## Installation

### Option 1: Install via Kiro Powers Panel

1. Open Kiro
2. Go to Powers panel
3. Add this repository URL

### Option 2: Manual MCP Configuration

Add to your `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "hephaestus-setup": {
      "command": "python",
      "args": ["/path/to/hephaestus-docker-power/src/setup_server.py"],
      "env": {
        "HEPHAESTUS_ROOT": "/path/to/Hephaestus",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `check_prerequisites` | Verify Python, tmux, git, docker, node, npm are installed |
| `check_services` | Check Docker daemon, Qdrant, MCP server status |
| `start_qdrant` | Start Qdrant vector database container |
| `stop_qdrant` | Stop Qdrant container (optionally remove volume) |
| `init_databases` | Initialize SQLite and Qdrant databases |
| `validate_env` | Check .env has required API keys |
| `configure_project` | Update hephaestus_config.yaml with project path |
| `health_check` | Comprehensive health check of all components |
| `view_logs` | View logs from server, monitor, or qdrant |
| `clean_reset` | Full reset (requires confirmation) |
| `quick_setup` | Complete setup in one command |

## Quick Start

```
# Complete setup in one command
quick_setup(project_path="/path/to/your/project")
```

Or step by step:

```
check_prerequisites()
validate_env()
start_qdrant()
init_databases()
configure_project("/path/to/project")
health_check()
```

## Steering Files

- `steering/getting-started.md` - Full setup walkthrough
- `steering/troubleshooting.md` - Common issues and solutions
- `steering/production.md` - Production deployment guide

## Requirements

- Python 3.10+
- Docker
- fastmcp (`pip install fastmcp`)
- pyyaml (`pip install pyyaml`)

## Environment Variables

- `HEPHAESTUS_ROOT` - Path to Hephaestus installation (defaults to current directory)
- `FASTMCP_LOG_LEVEL` - Log level for MCP server (default: ERROR)

## License

MIT

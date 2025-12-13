---
name: "hephaestus-docker"
displayName: "Hephaestus Docker Setup"
description: "Set up and manage Hephaestus using Docker containers for local development or production deployment"
keywords: ["docker", "hephaestus", "setup", "qdrant", "containers", "deployment", "docker-compose", "init", "agent", "workflow"]
author: "Hephaestus Community"
---

# Onboarding

Before proceeding, validate that the user has completed the following steps.

## Step 1: Clone Hephaestus

```bash
git clone https://github.com/Ido-Levi/Hephaestus.git
cd Hephaestus
```

## Step 2: Verify Prerequisites

Ensure the following tools are installed:
- **Python 3.10+**: `python --version`
- **Docker**: `docker --version`
- **tmux**: `tmux -V`
- **Node.js**: `node --version`
- **Git**: `git --version`

## Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY` (required for embeddings)
- `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` (optional)

## Step 4: Create Setup Hook

Create a hook at `.kiro/hooks/hephaestus-setup.kiro.hook`:

```json
{
  "enabled": true,
  "name": "Hephaestus Setup Helper",
  "description": "Helps with Hephaestus Docker setup and troubleshooting",
  "version": "1",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check the Hephaestus setup status: verify Docker is running, check if Qdrant container exists, and validate the .env file has required API keys."
  }
}
```

# Overview

Set up and manage Hephaestus using Docker containers for local development or production deployment.

Hephaestus is a semi-structured agentic framework for autonomous AI agent orchestration. It enables AI workflows to dynamically create and adapt their own task structures.

## When to Load Steering Files

- Setting up Hephaestus for the first time → `getting-started.md`
- Encountering errors or issues → `troubleshooting.md`
- Deploying to production → `production.md`

## Quick Setup Commands

### Start Qdrant Vector Database

```bash
docker run -d --name hephaestus-qdrant -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant:latest
```

Or using docker-compose:
```bash
docker-compose up -d qdrant
```

### Initialize Databases

```bash
python scripts/init_db.py
python scripts/init_qdrant.py
```

### Start Services

```bash
# MCP Server (port 8000)
python run_server.py

# Monitor (Guardian/Conductor)
python run_monitor.py

# Frontend (optional)
cd frontend && npm install && npm run dev
```

### Hephaestus Dev Mode

```bash
python run_hephaestus_dev.py --path /path/to/your/project
```

## Services

| Service | Port | Purpose |
|---------|------|---------|
| qdrant | 6333 | Vector database for RAG/embeddings |
| hephaestus-server | 8000 | MCP API server |
| hephaestus-monitor | - | Guardian/Conductor monitoring loop |
| frontend | 5173 | React dashboard (optional) |

## Configuration Files

- `.env` - API keys and secrets
- `hephaestus_config.yaml` - Main server configuration
- `config/agent_config.yaml` - Agent-specific settings

## Best Practices

### ✅ Do:
- Always start Qdrant before initializing databases
- Use environment variables for API keys
- Check Docker is running before starting containers
- Run health checks after setup
- Keep Qdrant data volume for persistence

### ❌ Don't:
- Commit `.env` file to version control
- Run init scripts without Qdrant running
- Use production API keys for development
- Skip the prerequisites check

## Troubleshooting

### Qdrant won't start
1. Check Docker is running: `docker info`
2. Check port 6333 is available: `netstat -an | grep 6333`
3. Remove existing container: `docker rm -f hephaestus-qdrant`

### Database initialization fails
1. Ensure Qdrant is healthy: `curl http://localhost:6333/health`
2. Check Python environment is activated
3. Verify all dependencies installed: `pip install -r requirements.txt`

### MCP server won't start
1. Check port 8000 is available
2. Verify `.env` has required API keys
3. Check database files exist

### Frontend build fails
1. Ensure Node.js 18+ installed
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Check for TypeScript errors: `npm run type-check`

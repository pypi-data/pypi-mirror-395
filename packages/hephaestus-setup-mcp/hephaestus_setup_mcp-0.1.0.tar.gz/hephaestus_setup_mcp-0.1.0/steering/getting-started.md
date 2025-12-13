# Getting Started with Hephaestus Docker

Step-by-step guide to run Hephaestus in Docker containers.

## Automated Setup (Recommended)

Use the `quick_setup` tool to perform all steps automatically:

```
quick_setup(project_path="/path/to/your/project")
```

This will:
1. Check prerequisites
2. Validate environment
3. Start Qdrant
4. Initialize databases
5. Configure project path
6. Run health checks

## Manual Setup

### Step 1: Clone and Navigate

```bash
git clone https://github.com/Ido-Levi/Hephaestus.git
cd Hephaestus
```

### Step 2: Check Prerequisites

Use the tool:
```
check_prerequisites()
```

Or manually verify: Python 3.10+, tmux, git, docker, node, npm

### Step 3: Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` with your API keys, then validate:
```
validate_env()
```

Required:
- `OPENAI_API_KEY` - For embeddings

Optional:
- `OPENROUTER_API_KEY` - For OpenRouter models
- `ANTHROPIC_API_KEY` - For Claude models

### Step 4: Start Qdrant

Use the tool:
```
start_qdrant()
```

Or manually:
```bash
docker-compose up -d qdrant
```

### Step 5: Initialize Databases

Use the tool:
```
init_databases()
```

Or manually:
```bash
python scripts/init_db.py
python scripts/init_qdrant.py
```

### Step 6: Configure Project

Use the tool:
```
configure_project(project_path="/path/to/your/project")
```

### Step 7: Verify Setup

Use the tool:
```
health_check()
```

Or check services:
```
check_services()
```

### Step 8: Start Services

```bash
# MCP Server
python run_server.py

# Monitor (optional)
python run_monitor.py

# Frontend (optional)
cd frontend && npm install && npm run dev
```

## Next Steps

1. Access frontend at http://localhost:5173
2. Or use Hephaestus Dev: `python run_hephaestus_dev.py --path /your/project`
3. Configure MCP in your AI tool (Claude Code, etc.)

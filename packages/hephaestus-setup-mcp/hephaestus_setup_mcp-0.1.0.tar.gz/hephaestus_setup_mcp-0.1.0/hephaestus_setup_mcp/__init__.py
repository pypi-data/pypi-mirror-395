"""
Hephaestus Setup MCP Server

Provides tools for setting up and managing Hephaestus Docker environment.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

__version__ = "0.1.0"

# Initialize FastMCP server
mcp = FastMCP("hephaestus-setup")

# Get the Hephaestus root directory - configurable via environment variable
HEPHAESTUS_ROOT = Path(os.environ.get("HEPHAESTUS_ROOT", Path.cwd())).resolve()


def run_command(cmd: list[str], cwd: Optional[Path] = None, timeout: int = 30) -> dict:
    """Run a shell command and return structured result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd or HEPHAESTUS_ROOT
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except FileNotFoundError as e:
        return {"success": False, "error": f"Command not found: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def check_prerequisites() -> dict:
    """Check if all required tools are installed for running Hephaestus."""
    tools = {
        "python": {"cmd": ["python", "--version"], "required": True},
        "tmux": {"cmd": ["tmux", "-V"], "required": True},
        "git": {"cmd": ["git", "--version"], "required": True},
        "docker": {"cmd": ["docker", "--version"], "required": True},
        "node": {"cmd": ["node", "--version"], "required": True},
        "npm": {"cmd": ["npm", "--version"], "required": True},
    }
    
    results = {}
    all_required_ok = True
    
    for tool_name, config in tools.items():
        exists = shutil.which(config["cmd"][0]) is not None
        version = None
        
        if exists:
            result = run_command(config["cmd"])
            if result["success"]:
                version = result["stdout"].split("\n")[0]
        
        status = "installed" if exists else "missing"
        if not exists and config["required"]:
            all_required_ok = False
            status = "MISSING (required)"
            
        results[tool_name] = {"installed": exists, "version": version, "status": status}
    
    return {
        "tools": results,
        "all_required_installed": all_required_ok,
        "message": "All required tools installed" if all_required_ok else "Some required tools are missing"
    }


@mcp.tool()
def check_services() -> dict:
    """Check the status of Docker daemon, Qdrant, and MCP server."""
    services = {}
    
    docker_result = run_command(["docker", "info"], timeout=5)
    services["docker_daemon"] = {"running": docker_result["success"]}
    
    qdrant_container = run_command(["docker", "ps", "--filter", "name=hephaestus-qdrant", "--format", "{{.Status}}"])
    services["qdrant"] = {"running": bool(qdrant_container["stdout"]), "status": qdrant_container["stdout"] or "not running"}
    
    return {"services": services}


@mcp.tool()
def start_qdrant() -> dict:
    """Start the Qdrant vector database container."""
    check = run_command(["docker", "ps", "--filter", "name=hephaestus-qdrant", "-q"])
    if check["stdout"]:
        return {"success": True, "message": "Qdrant container is already running"}
    
    stopped = run_command(["docker", "ps", "-a", "--filter", "name=hephaestus-qdrant", "-q"])
    if stopped["stdout"]:
        result = run_command(["docker", "start", "hephaestus-qdrant"])
    else:
        cmd = ["docker", "run", "-d", "--name", "hephaestus-qdrant", "-p", "6333:6333", 
               "-v", "qdrant_data:/qdrant/storage", "qdrant/qdrant:latest"]
        result = run_command(cmd, timeout=60)
    
    return {"success": result["success"], "message": "Qdrant started" if result["success"] else result.get("error")}


@mcp.tool()
def stop_qdrant(remove_volume: bool = False) -> dict:
    """Stop the Qdrant container."""
    run_command(["docker", "stop", "hephaestus-qdrant"], timeout=30)
    run_command(["docker", "rm", "hephaestus-qdrant"])
    
    if remove_volume:
        run_command(["docker", "volume", "rm", "qdrant_data"])
    
    return {"success": True, "message": "Qdrant stopped"}


@mcp.tool()
def validate_env() -> dict:
    """Validate the .env file has required API keys configured."""
    env_path = HEPHAESTUS_ROOT / ".env"
    
    if not env_path.exists():
        return {"success": False, "message": ".env file not found"}
    
    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    
    openai_key = env_vars.get("OPENAI_API_KEY", "")
    has_openai = bool(openai_key) and not openai_key.startswith("sk-...")
    
    return {"success": has_openai, "has_openai_key": has_openai, 
            "message": "API keys configured" if has_openai else "Missing OPENAI_API_KEY"}


@mcp.tool()
def health_check() -> dict:
    """Perform comprehensive health check of all Hephaestus services."""
    health = {}
    
    qdrant_result = run_command(["curl", "-s", "http://localhost:6333/health"], timeout=5)
    health["qdrant"] = {"healthy": qdrant_result["success"]}
    
    mcp_result = run_command(["curl", "-s", "http://localhost:8000/health"], timeout=5)
    health["mcp_server"] = {"healthy": mcp_result["success"]}
    
    db_path = HEPHAESTUS_ROOT / "hephaestus.db"
    health["database"] = {"healthy": db_path.exists()}
    
    all_healthy = all(h["healthy"] for h in health.values())
    return {"all_healthy": all_healthy, "components": health}


@mcp.tool()
def view_logs(service: str = "qdrant", lines: int = 50) -> dict:
    """View recent logs from a Hephaestus service (qdrant, server, or monitor)."""
    if service == "qdrant":
        result = run_command(["docker", "logs", "--tail", str(lines), "hephaestus-qdrant"])
        return {"success": result["success"], "logs": result.get("stdout", "") + result.get("stderr", "")}
    
    log_files = {"server": HEPHAESTUS_ROOT / "hephaestus_server.log",
                 "monitor": HEPHAESTUS_ROOT / "logs" / "monitor.log"}
    
    log_path = log_files.get(service)
    if not log_path or not log_path.exists():
        return {"success": False, "error": f"Log file not found for {service}"}
    
    with open(log_path) as f:
        all_lines = f.readlines()
        recent_lines = all_lines[-lines:]
    return {"success": True, "logs": "".join(recent_lines)}


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()

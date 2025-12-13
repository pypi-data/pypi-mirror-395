# Docker Troubleshooting Guide

Common issues and solutions when running Hephaestus with Docker.

## Diagnostic Tools

Start by checking overall status:
```
check_services()   # Check Docker, Qdrant, MCP server status
health_check()     # Comprehensive health check
view_logs("qdrant", lines=100)  # View recent logs
```

## Connection Issues

### Qdrant Connection Refused

**Symptom**: `ConnectionRefusedError: [Errno 111] Connection refused` to port 6333

**Diagnose**:
```
check_services()  # Check if Qdrant container is running
```

**Solutions**:
```
start_qdrant()    # Start or restart Qdrant
```

Or manually:
```bash
docker-compose restart qdrant
docker-compose logs qdrant
```

### MCP Server Not Responding

**Symptom**: Cannot connect to port 8000

**Diagnose**:
```
check_services()
view_logs("server", lines=50)
```

**Solutions**:
```bash
# Restart server
python run_server.py
```

## API Key Issues

### Invalid API Key Errors

**Symptom**: `AuthenticationError` or `Invalid API Key`

**Diagnose**:
```
validate_env()  # Check which keys are configured
```

**Solutions**:
1. Edit `.env` file with correct keys
2. Check for extra whitespace in key values
3. Ensure keys are not expired or revoked

## Database Issues

### SQLite Database Locked

**Symptom**: `database is locked` errors

**Solutions**:
```
clean_reset(confirm=True)  # WARNING: Deletes all data
init_databases()           # Reinitialize
```

### Qdrant Collection Errors

**Symptom**: Collection not found or corrupted

**Solutions**:
```
stop_qdrant(remove_volume=True)  # Remove corrupted data
start_qdrant()
init_databases()
```

## Port Conflicts

### Port Already in Use

**Symptom**: `Bind for 0.0.0.0:6333 failed: port is already allocated`

**Solutions**:
```bash
# Find what's using the port
lsof -i :6333
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

## Clean Slate Reset

When all else fails, use the reset tool:

```
clean_reset(confirm=True)
```

This will:
- Stop Qdrant container
- Remove Qdrant volume
- Delete SQLite database
- Clear log files

Then reinitialize:
```
start_qdrant()
init_databases()
```

Or use quick_setup for complete fresh start:
```
quick_setup(project_path="/path/to/project")
```

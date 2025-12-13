# Production Deployment Guide

Best practices for deploying Hephaestus with Docker in production.

## Security Considerations

### 1. Secure API Keys

Never commit `.env` files. Use secrets management:

```bash
# Use Docker secrets (Swarm mode)
echo "sk-your-key" | docker secret create openai_api_key -

# Or use environment variables from CI/CD
docker-compose --env-file /secure/path/.env up -d
```

### 2. Network Isolation

Create a dedicated network:

```yaml
# docker-compose.prod.yml
networks:
  hephaestus-net:
    driver: bridge
    internal: true  # No external access

services:
  qdrant:
    networks:
      - hephaestus-net
    # Remove port exposure in production
    # ports:
    #   - "6333:6333"
```

### 3. Enable Authentication

Set in `hephaestus_config.yaml`:
```yaml
mcp:
  auth_required: true
  session_timeout: 3600
```

## Resource Limits

Add resource constraints:

```yaml
services:
  hephaestus-server:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G
```

## Persistent Storage

Use named volumes for data persistence:

```yaml
volumes:
  qdrant_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/qdrant

  hephaestus_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/hephaestus
```

## Health Checks

Add health checks to services:

```yaml
services:
  hephaestus-server:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Logging

Configure centralized logging:

```yaml
services:
  hephaestus-server:
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"
```

## Backup Strategy

### Qdrant Snapshots

```bash
# Create snapshot
curl -X POST http://localhost:6333/collections/hephaestus_tasks/snapshots

# List snapshots
curl http://localhost:6333/collections/hephaestus_tasks/snapshots
```

### SQLite Backup

```bash
# Backup database
docker-compose exec hephaestus-server \
  sqlite3 /app/data/hephaestus.db ".backup '/app/data/backup.db'"
```

## Monitoring

Add Prometheus metrics endpoint (already included in Hephaestus):

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

## Scaling

For high availability, consider:
- Running multiple MCP server instances behind a load balancer
- Using Qdrant cluster mode for vector store redundancy
- Separating the monitoring loop to its own host

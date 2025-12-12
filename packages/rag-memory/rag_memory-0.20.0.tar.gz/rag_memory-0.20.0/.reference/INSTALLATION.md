# Installation

This guide covers setting up RAG Memory locally with Docker.

## Prerequisites

**Required Software**
- Docker Desktop (for Mac/Windows) or Docker Engine (for Linux)
- Git
- Python 3.11 or higher (for the setup script)

**Required Credentials**
- OpenAI API key (get from https://platform.openai.com/api-keys)

**System Requirements**
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- macOS, Linux, or Windows with WSL2

## Quick Start (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/rag-memory.git
cd rag-memory

# 2. Install dependencies (REQUIRED)
uv sync

# 3. Activate virtual environment (REQUIRED)
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows alternative

# 4. Run setup script
python scripts/setup.py
```

The setup script handles:
- Docker container startup (PostgreSQL + Neo4j)
- Database initialization
- System configuration
- CLI tool installation
- Health verification

## Detailed Setup Steps

### 1. Install Docker

**macOS**
```bash
# Download Docker Desktop from docker.com
# Or use Homebrew:
brew install --cask docker
```

**Linux**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

**Windows**
- Install Docker Desktop for Windows
- Enable WSL2 backend
- Restart system if prompted

### 2. Verify Docker

```bash
docker --version
docker ps
```

Should show Docker version and no errors.

### 3. Clone Repository

```bash
git clone https://github.com/yourusername/rag-memory.git
cd rag-memory
```

### 4. Activate Virtual Environment

```bash
# CRITICAL: This step is required for setup.py to work
source .venv/bin/activate

# Verify activation (prompt should show (.venv))
which python
```

### 5. Run Setup Script

```bash
python scripts/setup.py
```

**Setup Script Does:**
1. Checks Docker is installed and running
2. Checks for existing RAG Memory containers
3. **Prompts for OpenAI API key**
4. Finds available ports (54320 for PostgreSQL, 7474/7687 for Neo4j)
5. **Configures directory mounts** (for file ingestion access)
6. **Configures backup schedule** (daily backup time)
7. **Configures backup location** (where backups are stored)
8. **Configures backup retention** (how long to keep backups)
9. **Configures entity extraction quality** (standard vs enhanced)
10. Creates configuration files (config.yaml, .env, docker-compose.yml)
11. Builds MCP server Docker image
12. Starts all containers (PostgreSQL, Neo4j, MCP, backup)
13. Waits for health checks (all services ready)
14. Initializes Neo4j Graphiti indices (28 indexes/constraints)
15. Creates Neo4j vector indices (performance optimization)
16. Installs CLI tool globally (rag command)
17. Validates database schemas
18. Displays connection details and next steps

**Expected Output:**
```
================================================================================
RAG Memory Setup Script
================================================================================

STEP 1: Checking Docker Installation
✓ Docker is installed

STEP 2: Checking Docker Daemon
✓ Docker daemon is running

STEP 3: Checking for Existing RAG Memory Containers
ℹ No existing RAG Memory local containers found

STEP 4: OpenAI API Key
Enter your OpenAI API key (sk-...): sk-proj-...
✓ API key accepted: sk-proj-...***

STEP 5: Finding Available Ports
✓ postgres: 54320 (default)
✓ neo4j_http: 7474 (default)
✓ neo4j_bolt: 7687 (default)
✓ mcp: 18000 (default)

STEP 6: Configure Directory Access for File Ingestion
Mount home directory as read-only? (yes/no, default: yes): yes
✓ Added mount: /Users/you (read-only)

STEP 7: Configure Backup Schedule
Enter backup time in Local Time (HH:MM, default: 02:05): 02:05
✓ Backup schedule: Daily at 02:05

STEP 8: Configure Backup Location
Backup directory (default: ./backups):
✓ Backup location: ./backups

STEP 9: Configure Backup Retention
Keep backups for how many days? (default: 14): 14
✓ Backup retention: 14 days

STEP 10: Entity Extraction Quality (Optional)
Enter choice (0-2, default: 0): 0
✓ Using standard quality (fast, cost-effective)

STEP 11: Creating Configuration Files
✓ Configuration created: /Users/you/Library/Application Support/rag-memory/config.yaml
✓ Environment file created: deploy/docker/compose/.env
✓ Docker Compose configuration created: deploy/docker/compose/docker-compose.yml

STEP 12: Building and Starting Containers
✓ MCP image built (fresh build)
✓ Containers started (fresh recreate)

STEP 13: Waiting for Services to Be Ready
✓ PostgreSQL is ready and accepting connections
✓ Neo4j is ready and accepting connections
✓ MCP server is running and responding on port 18000

STEP 14: Initializing Neo4j Indices
✓ Neo4j indices initialized successfully

STEP 14.5: Creating Neo4j Vector Indices
✓ Entity.name_embedding vector index created
✓ RELATES_TO.fact_embedding vector index created

STEP 15: Installing CLI Tool
✓ CLI tool installed successfully

STEP 16: Validating Database Schemas
✓ PostgreSQL schema validated (4 tables found)
✓ Neo4j is accessible

✨ Setup Complete!
```

## Verify Installation

### Check Services

```bash
# Check Docker containers
docker ps

# Should show:
# - rag-memory-postgres-local (port 54320)
# - rag-memory-neo4j-local (ports 7474, 7687)
# - rag-memory-mcp-local (port 18000)
# - rag-memory-backup-local
```

### Check CLI Tool

```bash
# CLI should be available globally
rag status

# Expected output:
# ✓ PostgreSQL: healthy
# ✓ Neo4j: healthy
```

### Test Basic Functionality

```bash
# Create collection
rag collection create test-docs \
  --description "Test collection" \
  --domain "Testing" \
  --domain-scope "Setup verification"

# Ingest text
rag ingest text "PostgreSQL enables semantic search" \
  --collection test-docs

# Search
rag search "semantic search" --collection test-docs

# Should return the ingested text with similarity score
```

## Configuration Files

Setup creates configuration at:
- **macOS**: `~/Library/Application Support/rag-memory/config.yaml`
- **Linux**: `~/.config/rag-memory/config.yaml`
- **Windows**: `%APPDATA%\rag-memory\config.yaml`

Configuration contains:
- Database connection strings
- OpenAI API key
- Neo4j credentials
- Backup settings

See CONFIGURATION.md for details.

## Post-Installation

### Start Services

```bash
# Start containers (if stopped)
rag start

# Verify status
rag status
```

### Stop Services

```bash
# Stop containers (data persists)
rag stop
```

### View Logs

```bash
# View all service logs
rag logs

# View specific service
rag logs --service postgres
rag logs --service neo4j
```

## Database Access

**PostgreSQL**
```bash
# Connection string
postgresql://raguser:ragpassword@localhost:54320/rag_memory

# Connect via psql
psql postgresql://raguser:ragpassword@localhost:54320/rag_memory

# Or using docker exec
docker exec -it rag-memory-postgres-local psql -U raguser -d rag_memory
```

**Neo4j Browser**
- URL: http://localhost:7474
- Username: `neo4j`
- Password: `graphiti-password`

## Data Persistence

**Docker Volumes**
Data persists in Docker volumes even when containers are stopped:
- `postgres_data_local` - PostgreSQL data
- `neo4j_data_local` - Neo4j data
- `neo4j_logs_local` - Neo4j logs

**Backup**
```bash
# Manual backup
docker exec rag-memory-postgres-local pg_dump -U raguser rag_memory > backup.sql

# Restore
docker exec -i rag-memory-postgres-local psql -U raguser rag_memory < backup.sql
```

## Troubleshooting

See TROUBLESHOOTING.md for common issues and solutions.

**Quick Fixes:**

**Port Already in Use**
```bash
# Check what's using port 54320
lsof -i :54320

# Stop conflicting service or change RAG Memory port in config
```

**Docker Not Running**
```bash
# macOS: Start Docker Desktop app
# Linux: sudo systemctl start docker
# Windows: Start Docker Desktop
```

**Permission Denied**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

## Next Steps

- **CLI Usage** - See CLI_GUIDE.md for commands
- **MCP Setup** - See MCP_GUIDE.md for AI agent integration
- **Configuration** - See CONFIGURATION.md for advanced settings
- **Cloud Deployment** - See CLOUD_SETUP.md for production deployment

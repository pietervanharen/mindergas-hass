# Devcontainer Setup

This project includes a VS Code devcontainer configuration for streamlined development without polluting your local environment.

## What is a Devcontainer?

A devcontainer is a fully configured Docker environment that includes:
- Python 3.11 runtime
- Home Assistant development tools
- Code linting and formatting tools (pylint, black, flake8, ruff)
- Testing frameworks (pytest)
- Docker-in-Docker for running Home Assistant containers
- VS Code extensions pre-configured
- Automatic post-setup script execution

## Prerequisites

1. **Docker Desktop**
   - [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Ensure it's running before opening the devcontainer

2. **VS Code**
   - [Install Visual Studio Code](https://code.visualstudio.com/)
   - Install the "Dev Containers" extension (ms-vscode-remote.remote-containers)

3. **Git**
   - [Install Git](https://git-scm.com/)

## Getting Started

### Option 1: Automatic (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/pietervanharen/mindergas-hass.git
   cd mindergas-hass
   ```

2. Open in VS Code:
   ```bash
   code .
   ```

3. When prompted, click "Reopen in Container"
   - If not prompted, use Command Palette (⌘ Shift P or Ctrl Shift P)
   - Search for "Remote-Containers: Reopen in Container"

4. Wait for container build (first time takes 2-3 minutes)

5. The post-create script will automatically install all dependencies

### Option 2: Manual Setup

If automatic doesn't work:

1. Open the folder in VS Code
2. Command Palette → "Remote-Containers: Open Folder in Container"
3. Select the workspace folder
4. Wait for build to complete

## Development Workflow

### Code Formatting & Linting

```bash
# Format code with Black
black custom_components/mindergas

# Check formatting without changing
black custom_components/mindergas --check

# Lint code
pylint custom_components/mindergas

# Check with Ruff (fast Python linter)
ruff check custom_components/mindergas
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config_flow.py

# Run with coverage
pytest --cov=custom_components/mindergas

# Run with verbose output
pytest -vv
```

### Home Assistant Development

```bash
# Start Home Assistant (for direct testing, not recommended)
python -m homeassistant --open-ui

# Better: Use Docker for Home Assistant
./quick_start.sh
```

### Using Home Assistant with Docker

Even in the devcontainer, you can still use the docker-compose setup:

```bash
# Start Home Assistant (inside devcontainer)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Devcontainer Features

### VS Code Extensions (Auto-installed)

- **Python** - Core Python support
- **Pylance** - Advanced type checking
- **Pylint** - Code linting
- **Flake8** - Style guide enforcement
- **Black Formatter** - Code formatting
- **Ruff** - Fast Python linter
- **Makefile Tools** - Makefile support
- **GitHub Copilot** - AI assistance (optional, requires login)

### Settings Applied

- Python formatter: Black
- Auto-format on save: Enabled
- Import organization: Enabled
- Pylint: Enabled
- Type checking: Pylance

## Directory Structure in Container

```
/workspace/           # Your project root (mounted from host)
/config/             # Home Assistant config directory
├── custom_components/
│   └── mindergas/   # Your integration
└── ...              # Other HA config files
```

## Environment Variables

The devcontainer automatically sets:
- `PYTHONUNBUFFERED=1` - Real-time Python output
- `PYTHONDONTWRITEBYTECODE=1` - No .pyc files
- `PYTHONPATH=/workspace` - Project on path

## Port Forwarding

Port 8123 is automatically forwarded for Home Assistant access:
- Inside container: `http://localhost:8123`
- From host machine: `http://localhost:8123`

## Troubleshooting

### Container won't build
- Ensure Docker Desktop is running
- Check available disk space
- Try: Command Palette → "Dev Containers: Rebuild Container"

### Python modules not found
- The post-create script handles installation
- Manually run: `/bin/bash .devcontainer/post-create.sh`

### Can't access Docker
- Docker-in-Docker requires Docker socket to be mounted
- Verify Docker Desktop is running
- Check "Settings" → "Resources" → "File Sharing"

### Extensions not installed
- Wait for container to fully start
- Command Palette → "Extensions: Install Recommended Extensions"

### Port 8123 already in use
- Stop other Home Assistant instances
- Check: `lsof -i :8123`
- Kill process if needed: `kill -9 <PID>`

## Using Pre-commit Hooks (Optional)

Install pre-commit to automatically format before commits:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Bypass hooks (not recommended)
git commit --no-verify
```

## VS Code Tips & Tricks

### Command Palette Shortcuts

```
⌘ Shift P (Mac) / Ctrl Shift P (Windows/Linux)
```

- "Python: Run Linter" → Run pylint
- "Format Document" → Format with Black
- "Python: Run Tests" → Run pytest
- "Dev Containers: Rebuild Container" → Rebuild

### Keyboard Shortcuts

- Format file: Shift + Option + F (Mac) / Shift + Alt + F (Win/Linux)
- Open terminal: Control + ` (backtick)
- Go to definition: F12
- Find all references: Shift + Option + F12

### Debug with VS Code

1. Set breakpoint by clicking line number
2. Run Python file with debugging
3. Use Debug console for REPL

## Performance Tips

### Faster Container Builds

- Docker builds are cached, so subsequent starts are faster
- First build: 3-5 minutes
- Subsequent starts: 30-60 seconds

### Optimize Disk Usage

```bash
# Clean up old containers
docker container prune

# Clean up unused images
docker image prune

# Clean up volumes
docker volume prune
```

## Integration with Docker Compose

The devcontainer can control the Home Assistant container:

```bash
# Inside devcontainer
docker-compose ps          # Check status
docker-compose logs -f     # Watch logs
docker-compose restart     # Restart services
```

## Recommended Workflow

1. **Edit Code**: Work in VS Code editor
2. **Format**: Cmd+Shift+P → "Format Document" (on save auto)
3. **Lint**: Cmd+Shift+P → "Run Linter"
4. **Test**: Run pytest for unit tests
5. **Test Integration**: Use docker-compose for real Home Assistant
6. **Commit**: Git commits with pre-commit formatting

## Additional Resources

- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker Documentation](https://docs.docker.com/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Python Development in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

## Getting Help

- Check the [DOCKER_SETUP.md](DOCKER_SETUP.md) for Docker-specific issues
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an [issue on GitHub](https://github.com/pietervanharen/mindergas-hass/issues)
- Join the [Home Assistant Community](https://community.home-assistant.io/)

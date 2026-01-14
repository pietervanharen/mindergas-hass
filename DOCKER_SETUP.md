# Home Assistant Docker Setup Guide

This guide explains how to run Home Assistant in Docker on macOS to test the MinderGas integration.

## Prerequisites

- Docker Desktop installed on macOS
- Docker daemon running
- At least 2GB of free disk space
- Your MinderGas API key

## Quick Start

### 1. Start Home Assistant

From the project root directory:

```bash
docker compose up -d
```

This will:
- Pull the latest Home Assistant image (first time only)
- Create a `home_assistant_data` directory for configuration
- Start the container on `http://localhost:8123`
- Automatically mount the MinderGas integration

### 2. First Boot (takes 2-3 minutes)

Wait for Home Assistant to initialize. Check the logs:

```bash
docker compose logs -f home-assistant
```

You should see:
```
home-assistant | Starting Home Assistant
home-assistant | Loaded home assistant
```

### 3. Open Home Assistant

Visit: **http://localhost:8123**

You'll see the setup wizard. Complete these steps:
1. Create your Home Assistant account
2. Set location and language
3. Configure integrations

### 4. Add MinderGas Integration

Once Home Assistant is running:

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **Create Integration**
3. Search for "MinderGas"
4. Enter your API key and complete the configuration

## Management Commands

### View logs
```bash
docker compose logs -f home-assistant
```

### Restart Home Assistant
```bash
docker compose restart home-assistant
```

### Stop Home Assistant
```bash
docker compose down
```

### Remove everything (wipe data)
```bash
docker compose down -v
rm -rf home_assistant_data
```

### Clean up (free disk space)
```bash
docker system prune -a
```

## Integration Development Workflow

Since the integration is mounted directly from the project directory:

1. **Make code changes** to `custom_components/mindergas/`
2. **Restart Home Assistant**: `docker compose restart home-assistant`
3. **Reload integration**: Settings → Devices & Services → MinderGas → (three dots) → Reload
4. **Check logs**: `docker compose logs -f home-assistant` to see any errors

Changes to Python files require a restart. Changes to translations can often be reloaded.

## Troubleshooting

### Container won't start
```bash
# Check for port conflicts
lsof -i :8123

# Try removing the container
docker compose down
docker compose up -d
```

### Home Assistant not responding
```bash
# Check container status
docker compose ps

# View detailed logs
docker compose logs home-assistant
```

### Integration not appearing
1. Make sure the `custom_components/mindergas/` directory exists
2. Restart the container: `docker compose restart home-assistant`
3. Refresh the browser (Ctrl+Shift+R or Cmd+Shift+R)

### API key errors
1. Verify your API key in the configuration flow
2. Check logs for the actual error: `docker compose logs home-assistant | grep mindergas`

### Docker daemon issues
```bash
# Restart Docker daemon
open /Applications/Docker.app

# Or from terminal (might require sudo)
sudo killall com.docker.osx.HyperKit
```

## Performance Tips

### Free up resources
- Close unnecessary applications
- Home Assistant needs ~500MB RAM
- First startup can take 2-3 minutes

### Increase resources (optional)
Docker Desktop → Preferences → Resources:
- CPUs: 4+
- Memory: 4GB+

## Advanced: Persistent Data

The `home_assistant_data` directory contains:
- Configuration
- Automations
- Sensor history
- Logs

**Don't commit this to git!** It's already in `.gitignore`.

## Advanced: Multiple Instances

Want to test multiple configurations?

```bash
# Create a second instance
docker-compose -f docker-compose.yml -p mindergas-test2 up -d

# This creates a separate container and network
# Access on a different port (modify docker-compose.yml)
```

## Integration Reload Process

After code changes:

1. **Option A: Full Restart** (always works)
   ```bash
   docker compose restart home-assistant
   ```

2. **Option B: Reload Integration** (faster, not always reliable)
   - Go to Settings → Devices & Services
   - Find MinderGas
   - Click the three-dot menu → Reload

3. **Option C: Full Reload YAML** (for config file changes)
   - Developer Tools → YAML → Configuration Reloading → Reload Integrations

## Testing Checklist

After deploying the MinderGas integration:

- [ ] Integration appears in integrations list
- [ ] Configuration flow works (API key validation)
- [ ] Meter reading configuration step works
- [ ] Statistics update configuration step works
- [ ] Sensors are created (if stats enabled)
- [ ] No errors in logs
- [ ] Restart Home Assistant and verify persistence

## Useful Home Assistant Features

### Developer Tools
Settings → Developer Tools → States/Services/Templates
- View sensor states
- Test automations
- Debug issues

### Logs
Settings → System → Logs
- View error logs
- Filter by integration name
- Real-time log viewer

### Terminal
```bash
# Access Home Assistant Python shell
docker compose exec home-assistant python -c "import homeassistant; print(homeassistant.__version__)"

# Browse config directory
docker compose exec home-assistant ls -la /config
```

## Cleanup After Testing

When done testing:

```bash
# Stop but keep data
docker compose stop

# Stop and remove container
docker compose down

# Remove everything including data
docker compose down -v
rm -rf home_assistant_data
```

## Docker Compose Health Check

Monitor container health:

```bash
# Watch container status
watch docker compose ps

# Or one-time check
docker compose ps
```

## Next Steps

1. Start Home Assistant: `docker compose up -d`
2. Wait 2-3 minutes for startup
3. Open http://localhost:8123
4. Complete setup wizard
5. Go to TESTING.md for integration test guide

---

**Need help?**
- Home Assistant docs: https://www.home-assistant.io/docs/
- Docker docs: https://docs.docker.com/
- MinderGas integration: See METER_RESTRICTIONS.md

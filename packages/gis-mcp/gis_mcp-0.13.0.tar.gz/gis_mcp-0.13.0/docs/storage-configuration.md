## Storage Configuration

The GIS MCP Server uses a configurable storage directory for file operations (reading, writing, and downloading data). By default, files are stored in `~/.gis_mcp/data/`.

### Specifying a Custom Storage Folder

You can specify a custom storage folder using either:

1. **Command-line argument:**

   ```bash
   gis-mcp --storage-path /path/to/your/storage
   ```

2. **Environment variable:**

   ```bash
   export GIS_MCP_STORAGE_PATH=/path/to/your/storage
   gis-mcp
   ```

On Windows PowerShell:

```powershell
$env:GIS_MCP_STORAGE_PATH="C:\path\to\your\storage"
gis-mcp
```

### Default Storage Location

If no storage path is specified, the server uses the default location:

- **Default path:** `~/.gis_mcp/data/`
  - Linux/Mac: `/home/username/.gis_mcp/data/`
  - Windows: `C:\Users\username\.gis_mcp\data\`

The storage directory is automatically created if it doesn't exist.

### How Storage Works

- **File writes:** When you save files using tools like `write_file_gpd`, `write_raster`, or `save_results`, relative paths are resolved relative to the storage directory. Absolute paths are used as-is.
- **Data downloads:** Downloaded data (satellite imagery, climate data, movement networks, etc.) is saved to subdirectories within the storage folder:
  - `movement_data/` - Street networks
  - `land_products/` - Land cover data
  - `satellite_imagery/` - Satellite imagery
  - `ecology_data/` - Species occurrence data
  - `climate_data/` - Climate datasets
  - `administrative_boundaries/` - Administrative boundaries
  - `outputs/` - General output files

### Example Configuration for MCP Clients

For Claude Desktop or Cursor IDE, you can specify the storage path in your configuration.

**Claude Desktop / Cursor (JSON config):**

```json
{
  "mcpServers": {
    "gis-mcp": {
      "command": "/home/YourUsername/.venv/bin/gis-mcp",
      "args": ["--storage-path", "/custom/path/to/storage"]
    }
  }
}
```

On Windows, adjust the command path accordingly, for example:

```json
{
  "mcpServers": {
    "gis-mcp": {
      "command": "C:\\\\Users\\\\YourUsername\\\\.venv\\\\Scripts\\\\gis-mcp",
      "args": ["--storage-path", "C:\\\\custom\\\\path\\\\to\\\\storage"]
    }
  }
}
```

### Environment Variable Configuration

Instead of passing `--storage-path`, you can configure the environment variable in your shell profile:

```bash
export GIS_MCP_STORAGE_PATH=/custom/path/to/storage
```

Or in PowerShell:

```powershell
$env:GIS_MCP_STORAGE_PATH="C:\custom\path\to\storage"
```

This ensures all future `gis-mcp` runs use the specified storage directory by default.

### Docker: Persistent Storage with Volumes

When running GIS MCP Server in Docker, data inside containers is ephemeral by default. To persist your storage data, you need to mount a Docker volume.

#### Using Host Directory Mount

Mount a directory from your host machine to the container's storage path:

```bash
# Linux/Mac
docker run -p 9010:9010 \
  -v /home/user/gis-data:/app/.gis_mcp/data \
  gis-mcp

# Windows
docker run -p 9010:9010 \
  -v C:\gis-data:/app/.gis_mcp/data \
  gis-mcp
```

#### Using Named Docker Volumes

Named volumes are managed by Docker and provide better portability:

```bash
# Create a named volume
docker volume create gis-mcp-storage

# Run container with the named volume
docker run -p 9010:9010 \
  -v gis-mcp-storage:/app/.gis_mcp/data \
  gis-mcp
```

#### Custom Storage Path in Docker

You can use a custom storage path inside the container by combining volume mounting with environment variables:

```bash
docker run -p 9010:9010 \
  -v /host/path/to/storage:/container/storage \
  -e GIS_MCP_STORAGE_PATH=/container/storage \
  gis-mcp
```

Or with a named volume:

```bash
docker run -p 9010:9010 \
  -v gis-mcp-storage:/container/storage \
  -e GIS_MCP_STORAGE_PATH=/container/storage \
  gis-mcp
```

#### Docker Compose Example

For easier management, use `docker-compose.yml`:

```yaml
version: "3.8"

services:
  gis-mcp:
    image: gis-mcp:latest
    ports:
      - "9010:9010"
    volumes:
      # Option 1: Named volume (recommended)
      - gis-mcp-data:/app/.gis_mcp/data

      # Option 2: Host directory mount
      # - ./gis-data:/app/.gis_mcp/data

      # Option 3: Custom path with environment variable
      # - gis-mcp-data:/custom/storage
    environment:
      - GIS_MCP_TRANSPORT=http
      - GIS_MCP_HOST=0.0.0.0
      - GIS_MCP_PORT=9010
      # Uncomment if using custom storage path
      # - GIS_MCP_STORAGE_PATH=/custom/storage

volumes:
  gis-mcp-data:
    # Optional: Use a specific driver or external volume
    # driver: local
    # driver_opts:
    #   type: none
    #   o: bind
    #   device: /host/path/to/storage
```

#### Managing Docker Volumes

**List all volumes:**

```bash
docker volume ls
```

**Inspect a volume:**

```bash
docker volume inspect gis-mcp-storage
```

**Backup a volume:**

```bash
docker run --rm \
  -v gis-mcp-storage:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/gis-mcp-backup.tar.gz -C /data .
```

**Restore a volume:**

```bash
docker run --rm \
  -v gis-mcp-storage:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/gis-mcp-backup.tar.gz -C /data
```

**Remove a volume:**

```bash
docker volume rm gis-mcp-storage
```

#### Best Practices

- **Use named volumes** for production deployments as they're easier to manage and backup
- **Use host directory mounts** for development when you need direct file access
- **Set appropriate permissions** on host directories to ensure the container can write to them
- **Regular backups** of volumes are recommended, especially for production data
- **Document your volume strategy** in your deployment documentation

#### Default Storage Path in Docker

Inside Docker containers, the default storage path is `/app/.gis_mcp/data/`. When mounting volumes, ensure you mount to this path unless you're using a custom `GIS_MCP_STORAGE_PATH` environment variable.

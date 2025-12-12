# Configuration

This document describes the configuration options for the GIS MCP Server.

## Environment Variables

The server can be configured using the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| NOMINATIM_URL | https://nominatim.openstreetmap.org | Nominatim API URL |
| NOMINATIM_USER_AGENT | gis-mcp-server/1.0.0 | User agent |
| OSRM_URL | https://router.project-osrm.org | OSRM API URL |
| OSRM_PROFILE | driving | Default routing profile |
| PELIAS_URL | (empty) | Pelias geocoding URL |
| PELIAS_API_KEY | (empty) | Pelias API key |
| OPEN_ELEVATION_URL | https://api.open-elevation.com | Elevation API |
| GIS_DEFAULT_CRS | EPSG:4326 | Default CRS |
| GIS_TEMP_DIR | /tmp/gis-mcp | Temp directory |

## Nominatim Configuration

Nominatim is used for geocoding and reverse geocoding services.

### Using the Public Nominatim Service

The default configuration uses the public OpenStreetMap Nominatim service at `https://nominatim.openstreetmap.org`.

**Important Rate Limiting:**
- The public Nominatim service has a strict rate limit of **1 request per second**
- Exceeding this limit may result in your IP being blocked
- Always set an appropriate `NOMINATIM_USER_AGENT` to identify your application

### Self-Hosting Nominatim

For production environments or higher request volumes, consider self-hosting Nominatim:

1. Follow the [Nominatim installation guide](https://nominatim.org/release-docs/latest/admin/Installation/)
2. Set the `NOMINATIM_URL` environment variable to your self-hosted instance:
   ```bash
   export NOMINATIM_URL=https://your-nominatim-instance.com
   ```
3. Configure your own rate limits based on your server capacity

### User Agent Configuration

Always set a descriptive user agent to identify your application:

```bash
export NOMINATIM_USER_AGENT=my-application/1.0.0
```

## Pelias Configuration

Pelias is an alternative geocoding service that can be used alongside or instead of Nominatim.

### Using Pelias

To enable Pelias geocoding, configure the following environment variables:

```bash
export PELIAS_URL=https://api.geocode.earth/v1
export PELIAS_API_KEY=your-api-key-here
```

### Pelias Providers

Several commercial and self-hosted Pelias providers are available:

#### Geocode Earth
- Website: [https://geocode.earth](https://geocode.earth)
- Offers global geocoding coverage
- Provides API keys with various pricing tiers
- Configuration:
  ```bash
  export PELIAS_URL=https://api.geocode.earth/v1
  export PELIAS_API_KEY=your-geocode-earth-api-key
  ```

#### Self-Hosting Pelias
- Follow the [Pelias documentation](https://github.com/pelias/pelias) for self-hosting
- Configure your own URL:
  ```bash
  export PELIAS_URL=https://your-pelias-instance.com/v1
  ```
- No API key needed for self-hosted instances (unless you add authentication)

## OSRM Configuration

OSRM (Open Source Routing Machine) provides routing and navigation services.

### Routing Profiles

OSRM supports multiple routing profiles optimized for different transportation modes:

| Profile | Description |
|---------|-------------|
| driving | Car routing (default) |
| walking | Pedestrian routing |
| cycling | Bicycle routing |

### Configuration Examples

#### Using Default Profile (Driving)
```bash
export OSRM_URL=https://router.project-osrm.org
export OSRM_PROFILE=driving
```

#### Using Walking Profile
```bash
export OSRM_URL=https://router.project-osrm.org
export OSRM_PROFILE=walking
```

#### Using Cycling Profile
```bash
export OSRM_URL=https://router.project-osrm.org
export OSRM_PROFILE=cycling
```

### Self-Hosting OSRM

For production use or custom routing requirements:

1. Follow the [OSRM installation guide](https://github.com/Project-OSRM/osrm-backend)
2. Download and process OpenStreetMap data for your region
3. Configure the server URL:
   ```bash
   export OSRM_URL=https://your-osrm-instance.com
   ```

## Open-Elevation Configuration

Open-Elevation provides elevation data for geographic coordinates.

### Using the Public Service

The default configuration uses the public Open-Elevation API:

```bash
export OPEN_ELEVATION_URL=https://api.open-elevation.com
```

### Self-Hosting Open-Elevation

For production environments or custom elevation data:

1. Follow the [Open-Elevation setup guide](https://github.com/Jorl17/open-elevation)
2. Configure your instance URL:
   ```bash
   export OPEN_ELEVATION_URL=https://your-elevation-instance.com
   ```

### Alternative Elevation Services

You can also configure alternative elevation services that provide compatible APIs.

## Additional Configuration

### Coordinate Reference System (CRS)

The default CRS is WGS84 (EPSG:4326). To use a different default:

```bash
export GIS_DEFAULT_CRS=EPSG:3857  # Web Mercator
```

### Temporary Directory

Configure where temporary GIS files are stored:

```bash
export GIS_TEMP_DIR=/path/to/temp/directory
```

On Windows:
```bash
set GIS_TEMP_DIR=C:\temp\gis-mcp
```

## Configuration File Example

You can create a `.env` file in your project root with all configuration variables:

```env
# Nominatim Configuration
NOMINATIM_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=gis-mcp-server/1.0.0

# OSRM Configuration
OSRM_URL=https://router.project-osrm.org
OSRM_PROFILE=driving

# Pelias Configuration (optional)
PELIAS_URL=
PELIAS_API_KEY=

# Open-Elevation Configuration
OPEN_ELEVATION_URL=https://api.open-elevation.com

# General GIS Configuration
GIS_DEFAULT_CRS=EPSG:4326
GIS_TEMP_DIR=/tmp/gis-mcp
```

## Best Practices

1. **Production Deployments**: Always use self-hosted services for production to avoid rate limits and ensure reliability
2. **User Agents**: Always configure a descriptive user agent that includes contact information
3. **Rate Limiting**: Implement client-side rate limiting to respect service limits
4. **Error Handling**: Configure fallback services when primary services are unavailable
5. **Security**: Never commit API keys to version control; use environment variables or secret management systems

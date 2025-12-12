# Architecture

This document describes the architecture of the GIS MCP Server, including its structure, key components, and data flow.

## Project Structure

```
src/gis_mcp/
├── __init__.py        # Package init, version
├── server.py          # MCP server entry point (FastMCP)
├── config.py          # Configuration dataclasses
├── utils.py           # Common utilities
└── tools/
    ├── __init__.py    # Tool exports
    ├── geocoding.py   # geocode, reverse_geocode, batch_geocode
    ├── elevation.py   # get_elevation, get_elevation_profile
    ├── routing.py     # route, isochrone
    ├── geometry.py    # buffer, distance, spatial_query, transform_crs
    └── files.py       # read_file, write_file
```

## Key Components

### 1. MCP Server (server.py)

The MCP Server is the central component that orchestrates all GIS operations:

- **Framework**: Uses FastMCP from the mcp library to implement the Model Context Protocol
- **Tool Registration**: All tools are registered using the `@mcp.tool` decorator, making them discoverable by MCP clients
- **Entry Point**: The `main()` function initializes the server and starts listening for requests
- **Error Handling**: Implements comprehensive error handling and logging for all tool operations
- **Async Architecture**: Built on asynchronous Python to handle multiple concurrent requests efficiently

### 2. Configuration System (config.py)

The configuration system provides a flexible and type-safe way to manage service settings:

- **Dataclasses**: Each external service has its own configuration dataclass:
  - `NominatimConfig` - OpenStreetMap Nominatim geocoding service
  - `OSRMConfig` - Open Source Routing Machine configuration
  - `PeliasConfig` - Pelias geocoding service
  - `ElevationConfig` - Open-Elevation API configuration
- **Environment Variables**: Configuration is loaded from environment variables using `from_env()` class methods
- **Global Singleton**: A single `get_config()` function provides access to the global configuration instance
- **Validation**: Automatic validation of required settings and sensible defaults for optional parameters
- **Service URLs**: Configurable base URLs for all external services, allowing use of self-hosted instances

### 3. Utilities (utils.py)

Common utilities shared across all tools:

- **Response Formatting**:
  - `make_success_response()` - Standardized success response structure
  - `make_error_response()` - Standardized error response with details
- **Coordinate Validation**: Validates latitude/longitude values are within valid ranges
- **Distance/Duration Formatting**: Converts raw values into human-readable formats
- **Async Retry Decorator**: Automatically retries failed API calls with exponential backoff
- **Logging**: Centralized logging configuration for debugging and monitoring
- **Type Conversions**: Helper functions for converting between coordinate formats and units

### 4. External Services

The server integrates with several open-source GIS services:

#### Nominatim (OpenStreetMap)
- **Purpose**: Primary geocoding and reverse geocoding service
- **Features**: Address search, reverse geocoding, structured queries
- **Data Source**: OpenStreetMap collaborative database
- **Advantages**: Free, no API key required, comprehensive global coverage

#### Pelias
- **Purpose**: Alternative geocoding service
- **Features**: Fast autocomplete, multi-language support, customizable
- **Data Source**: Multiple sources (OpenStreetMap, OpenAddresses, Who's on First, etc.)
- **Advantages**: Better performance for autocomplete scenarios

#### OSRM (Open Source Routing Machine)
- **Purpose**: Routing and navigation
- **Features**: Point-to-point routing, isochrones, route optimization
- **Data Source**: OpenStreetMap road network
- **Advantages**: Fast routing calculations, support for multiple profiles (car, bike, foot)

#### Open-Elevation
- **Purpose**: Elevation data queries
- **Features**: Single point elevation, elevation profiles along paths
- **Data Source**: SRTM (Shuttle Radar Topography Mission) and other DEM sources
- **Advantages**: Free, no authentication required, global coverage

## Dependencies

The project relies on the following key Python libraries:

- **mcp (FastMCP)** - Implements the Model Context Protocol for AI agent integration
- **aiohttp** - Asynchronous HTTP client for making non-blocking API requests
- **shapely** - Geometry operations (buffer, distance, intersections, unions)
- **geopandas** - Geospatial data file I/O (GeoJSON, Shapefile, GeoPackage)
- **pyproj** - Coordinate reference system (CRS) transformations
- **geopy** - Distance calculations and geocoding utilities
- **pydantic** - Data validation and settings management (optional)

## Data Flow

The typical data flow through the system follows this pattern:

```
1. User Request
   ↓
   User or AI agent sends a request via MCP protocol
   Example: "Geocode the address '1600 Pennsylvania Avenue NW, Washington, DC'"

2. MCP Server
   ↓
   FastMCP server receives and validates the request
   Routes to appropriate tool handler based on tool name

3. Tool Handler
   ↓
   Tool function (e.g., geocode() in geocoding.py) processes request
   - Validates input parameters
   - Loads configuration for required service
   - Prepares API request

4. External API
   ↓
   Async HTTP request sent to external service (e.g., Nominatim)
   - Handles retries on transient failures
   - Respects rate limits
   - Manages timeouts

5. Response Processing
   ↓
   Tool handler processes API response
   - Parses JSON response
   - Extracts relevant data
   - Performs any necessary transformations

6. Response Formatting
   ↓
   Result formatted using utility functions
   - Standardized JSON structure
   - Error handling with descriptive messages
   - Includes metadata (source, timestamp, etc.)

7. User
   ↓
   Formatted response returned to user via MCP protocol
   Ready for display or further processing
```

### Example Flow: Geocoding Request

```
User: "Find coordinates for 'Eiffel Tower, Paris'"
  ↓
MCP Server: Receives geocode tool request
  ↓
geocoding.py: geocode() function called
  ↓
config.py: Load NominatimConfig
  ↓
aiohttp: HTTP GET to Nominatim API
  ↓
Nominatim: Returns JSON with coordinates and address details
  ↓
geocoding.py: Parse response, extract lat/lon
  ↓
utils.py: Format success response
  ↓
MCP Server: Return formatted response
  ↓
User: Receives {"latitude": 48.8584, "longitude": 2.2945, "address": "..."}
```

## Error Handling

The architecture implements multiple levels of error handling:

1. **Input Validation**: Parameter validation at tool entry points
2. **API Errors**: Graceful handling of external service failures
3. **Retry Logic**: Automatic retries with exponential backoff for transient errors
4. **Fallback Options**: Alternative services when primary service fails
5. **User-Friendly Messages**: Clear error messages with actionable information

## Extensibility

The modular architecture makes it easy to extend the server:

- **Adding New Tools**: Create new tool modules in the `tools/` directory
- **New Services**: Add new configuration classes and service integrations
- **Custom Utilities**: Extend `utils.py` with shared functionality
- **Alternative Implementations**: Swap external services by updating configuration

## Performance Considerations

- **Async/Await**: Non-blocking I/O for handling multiple concurrent requests
- **Connection Pooling**: Reused HTTP connections for better performance
- **Caching**: Optional caching layer for frequently requested data (future enhancement)
- **Rate Limiting**: Respects external service rate limits to avoid throttling

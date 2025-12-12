# GIS MCP Server

Welcome to the GIS MCP Server wiki! This documentation provides comprehensive guidance for using the server to enable AI agents with powerful geospatial capabilities.

## Overview

GIS MCP Server is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides geospatial tools for AI agents like Claude, GPT, and other Large Language Models. It bridges the gap between AI and Geographic Information Systems (GIS), enabling natural language interactions with spatial data, geocoding services, routing engines, and geospatial file formats.

The server exposes 13 specialized tools across five categories, allowing AI agents to perform complex geospatial operations through simple function calls.

## Key Features

### Geocoding Services
- **Address to Coordinates**: Convert human-readable addresses to precise latitude/longitude coordinates
- **Reverse Geocoding**: Transform coordinates back into human-readable addresses
- **Batch Processing**: Geocode up to 10 addresses simultaneously for efficient bulk operations
- **Multiple Providers**: Support for Nominatim/OpenStreetMap and Pelias geocoding engines

### Elevation Data
- **Point Elevation**: Get altitude/elevation data for any geographic point
- **Elevation Profiles**: Calculate elevation changes along paths and routes
- **Terrain Analysis**: Compute elevation statistics including min, max, gain, and loss

### Routing and Navigation
- **Route Calculation**: Compute optimal routes between points using OSRM (Open Source Routing Machine)
- **Multi-modal Routing**: Support for driving, walking, and cycling profiles
- **Isochrones**: Generate areas reachable within specified time limits
- **Detailed Instructions**: Get turn-by-turn directions with distance and duration

### Spatial Analysis
- **Distance Calculations**: Measure distances between points with multiple units (meters, kilometers, miles)
- **Buffer Operations**: Create buffer zones around geometries
- **Spatial Queries**: Perform intersection, union, contains, within, and other spatial operations
- **CRS Transformations**: Convert geometries between different coordinate reference systems

### File Operations
- **Multi-format Support**: Read and write Shapefiles, GeoJSON, and GeoPackage formats
- **Feature Management**: Load, analyze, and save geospatial features
- **Data Interoperability**: Seamless conversion between different GIS file formats

## Quick Start

### Installation

Install the server directly from PyPI:

```bash
pip install gis-mcp-server
```

For development or the latest features, install from source:

```bash
git clone https://github.com/matbel91765/gis-mcp-server.git
cd gis-mcp-server
pip install -e .
```

### Basic Configuration

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "gis": {
      "command": "uvx",
      "args": ["gis-mcp-server"]
    }
  }
}
```

For more details, see [[Installation]] and [[Configuration]].

## Documentation

### Getting Started
- [[Installation]] - Step-by-step installation guide for all platforms
- [[Getting-Started]] - Quick start tutorial with example usage
- [[Configuration]] - Environment variables and configuration options

### Tool Reference
- [[Geocoding-Tools]] - geocode, reverse_geocode, batch_geocode
- [[Elevation-Tools]] - get_elevation, get_elevation_profile
- [[Routing-Tools]] - route, isochrone
- [[Geometry-Tools]] - distance, buffer, spatial_query, transform_crs
- [[File-Tools]] - read_file, write_file

### Advanced Topics
- [[API-Reference]] - Complete API documentation
- [[Examples]] - Real-world usage examples and recipes
- [[Rate-Limits]] - Service rate limits and best practices
- [[Self-Hosting]] - Host your own geocoding and routing services
- [[Troubleshooting]] - Common issues and solutions

### Development
- [[Contributing]] - How to contribute to the project
- [[Development-Setup]] - Setting up development environment
- [[Testing]] - Running and writing tests
- [[Architecture]] - Server architecture and design

## Available Tools

| Category | Tool | Description |
|----------|------|-------------|
| **Geocoding** | `geocode` | Convert address to coordinates |
| | `reverse_geocode` | Convert coordinates to address |
| | `batch_geocode` | Geocode multiple addresses (max 10) |
| **Elevation** | `get_elevation` | Get altitude for a point |
| | `get_elevation_profile` | Get elevation along a path |
| **Routing** | `route` | Calculate route between points |
| | `isochrone` | Calculate reachable area by time |
| **Geometry** | `distance` | Calculate distance between points |
| | `buffer` | Create buffer zone around geometry |
| | `spatial_query` | Perform spatial operations |
| | `transform_crs` | Transform coordinate systems |
| **Files** | `read_file` | Read geospatial files |
| | `write_file` | Write geospatial files |

## Links

### Project Resources
- **PyPI Package**: [https://pypi.org/project/gis-mcp-server/](https://pypi.org/project/gis-mcp-server/)
- **GitHub Repository**: [https://github.com/matbel91765/gis-mcp-server](https://github.com/matbel91765/gis-mcp-server)
- **Issue Tracker**: [https://github.com/matbel91765/gis-mcp-server/issues](https://github.com/matbel91765/gis-mcp-server/issues)
- **Model Context Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

### External Services
- **Nominatim (Geocoding)**: [https://nominatim.org](https://nominatim.org)
- **OSRM (Routing)**: [http://project-osrm.org](http://project-osrm.org)
- **Pelias (Geocoding)**: [https://pelias.io](https://pelias.io)
- **Open-Elevation**: [https://open-elevation.com](https://open-elevation.com)

## Use Cases

### Urban Planning
- Geocode addresses for spatial analysis
- Calculate service area coverage using isochrones
- Analyze elevation profiles for infrastructure planning
- Buffer zones around facilities and points of interest

### Real Estate
- Reverse geocode property locations
- Calculate distances to amenities and services
- Generate drive-time polygons for market analysis
- Read and analyze property boundary shapefiles

### Environmental Analysis
- Calculate elevation changes for watershed analysis
- Create buffer zones around protected areas
- Perform spatial queries on environmental datasets
- Transform data between different coordinate systems

### Logistics and Transportation
- Calculate optimal routes for delivery planning
- Generate isochrones for service area definition
- Batch geocode customer addresses
- Analyze route elevation profiles for fuel estimation

## Requirements

- **Python**: 3.11 or higher
- **Operating Systems**: Windows, macOS, Linux
- **Internet Connection**: Required for geocoding, routing, and elevation services (unless self-hosted)

## License

GIS MCP Server is released under the [MIT License](https://opensource.org/licenses/MIT).

## Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/matbel91765/gis-mcp-server/issues)
- **Discussions**: Join community discussions on GitHub
- **Documentation**: Browse the wiki for detailed guides and examples

## Version

Current version: **1.0.0**

---

*Last updated: December 3, 2025*

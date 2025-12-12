# Getting Started

This guide will help you get up and running with the GIS MCP Server quickly.

## Quick Start with Claude Desktop

To use the GIS MCP Server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**Configuration File Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
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

After adding this configuration, restart Claude Desktop. The GIS MCP Server will be automatically started and available for use.

## Running the Server Directly

You can also run the server directly from the command line:

```bash
gis-mcp-server
```

This command starts the GIS MCP Server, which communicates via stdin/stdout using the MCP protocol. This is useful for:
- Testing the server independently
- Debugging issues
- Using the server with other MCP clients

## First Example: Geocoding an Address

Geocoding converts a textual address into geographic coordinates (latitude/longitude).

### Request

When using Claude Desktop with the GIS MCP Server configured, simply ask:

```
Can you geocode "Paris, France"?
```

Behind the scenes, this calls the `geocode` tool:

```json
{
  "method": "tools/call",
  "params": {
    "name": "geocode",
    "arguments": {
      "address": "Paris, France"
    }
  }
}
```

### Response

```json
{
  "success": true,
  "data": {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "display_name": "Paris, Île-de-France, France métropolitaine, France",
    "address": {
      "city": "Paris",
      "state": "Île-de-France",
      "country": "France",
      "country_code": "fr"
    },
    "boundingbox": ["48.8155755", "48.9021560", "2.2242990", "2.4699210"]
  },
  "metadata": {
    "provider": "nominatim",
    "timestamp": "2025-12-03T10:30:00Z"
  }
}
```

## Second Example: Calculating a Route Between Two Points

Route calculation finds the path between two geographic points.

### Request

When using Claude Desktop:

```
Calculate a route from Paris (48.8566, 2.3522) to the Eiffel Tower (48.8584, 2.2945)
```

Behind the scenes, this calls the `route` tool:

```json
{
  "method": "tools/call",
  "params": {
    "name": "route",
    "arguments": {
      "start": "48.8566,2.3522",
      "end": "48.8584,2.2945",
      "profile": "driving"
    }
  }
}
```

### Response

```json
{
  "success": true,
  "data": {
    "distance": 2350,
    "duration": 420,
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [2.3522, 48.8566],
        [2.3500, 48.8575],
        [2.3450, 48.8590],
        [2.2945, 48.8584]
      ]
    },
    "steps": [
      {
        "instruction": "Continue straight on Boulevard Saint-Germain",
        "distance": 850,
        "duration": 120
      },
      {
        "instruction": "Turn right onto Rue de Rivoli",
        "distance": 1500,
        "duration": 300
      }
    ]
  },
  "metadata": {
    "provider": "openrouteservice",
    "profile": "driving",
    "timestamp": "2025-12-03T10:35:00Z"
  }
}
```

## Understanding the Response Format

All responses from the GIS MCP Server follow a consistent structure:

### Basic Structure

```json
{
  "success": boolean,
  "data": object | null,
  "metadata": object | null,
  "error": string | null
}
```

### Response Fields

#### `success` (required)
- **Type**: `boolean`
- **Description**: Indicates whether the operation completed successfully
- `true`: Operation succeeded, data is available in `data`
- `false`: Operation failed, error message is in `error`

#### `data` (optional)
- **Type**: `object` or `null`
- **Description**: Contains the result data from the operation
- Structure varies depending on the operation type (geocoding, routing, etc.)
- `null` when an error occurs

#### `metadata` (optional)
- **Type**: `object` or `null`
- **Description**: Contextual information about the response
- Typically contains:
  - `provider`: The data provider used (e.g., "nominatim", "openrouteservice")
  - `timestamp`: ISO 8601 timestamp of when the request was processed
  - Other operation-specific information

#### `error` (optional)
- **Type**: `string` or `null`
- **Description**: Error message when the operation fails
- `null` on success
- Contains a descriptive error message to help with debugging

### Success Response Example

```json
{
  "success": true,
  "data": {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "display_name": "Paris, France"
  },
  "metadata": {
    "provider": "nominatim",
    "timestamp": "2025-12-03T10:30:00Z"
  },
  "error": null
}
```

### Error Response Example

```json
{
  "success": false,
  "data": null,
  "metadata": null,
  "error": "Address not found: the specified address could not be geocoded"
}
```

### Common Error Messages

- **"Address not found"**: The geocoding service couldn't find coordinates for the provided address
- **"Route calculation failed"**: Unable to calculate a route between the specified points
- **"Invalid coordinates"**: The provided coordinates are not valid (latitude must be -90 to 90, longitude -180 to 180)
- **"Service unavailable"**: The external GIS service is temporarily unavailable
- **"Rate limit exceeded"**: Too many requests sent to the service in a short time

## Next Steps

Now that you've configured the server and understand the basics, you can:

- **Explore All Tools**: Check the [Tools Reference](./Tools.md) to discover all available GIS operations
- **Advanced Examples**: See [Advanced Examples](./Examples.md) for more complex use cases
- **Development Guide**: Read the [Development Guide](./Development.md) if you want to contribute to the project
- **API Details**: Review the [API Reference](./API-Reference.md) for detailed technical specifications

## Tips for Success

- **Be specific with addresses**: Include city, state/region, and country for better geocoding accuracy
- **Coordinate format**: Use "latitude,longitude" format (e.g., "48.8566,2.3522")
- **Check for errors**: Always verify `success` is `true` before processing `data`
- **Use metadata**: Metadata helps with debugging and understanding which services were used
- **Rate limiting**: Be aware of rate limits from external geocoding and routing services

## Troubleshooting

### Server doesn't start
- Verify `uvx` is installed: `pip install uvx`
- Check that `gis-mcp-server` package is available
- Look for error messages in Claude Desktop logs

### Geocoding fails
- Verify the address is correctly formatted
- Try being more specific (include city, country)
- Check internet connectivity to geocoding services

### Routing fails
- Ensure coordinates are in valid ranges
- Check that both start and end points are accessible by the selected profile (driving, walking, cycling)
- Verify coordinates are in "latitude,longitude" format

## Support

If you need help:
- Check the [FAQ](./FAQ.md) for common questions
- Review the [Tools Reference](./Tools.md) for tool documentation
- Report issues on [GitHub Issues](https://github.com/yourusername/gis-mcp-server/issues)
- Join our community discussions

## What's Next?

Continue learning:
1. **[Tools Reference](./Tools.md)**: Complete list of all available GIS tools
2. **[Examples](./Examples.md)**: More complex real-world examples
3. **[Development](./Development.md)**: Contributing to the project
4. **[API Reference](./API-Reference.md)**: Detailed API documentation

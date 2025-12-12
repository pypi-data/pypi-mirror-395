# Frequently Asked Questions (FAQ)

## General Questions

**Q: What is MCP (Model Context Protocol)?**

A: MCP is Anthropic's protocol allowing AI models like Claude to use external tools. This server provides geospatial tools.

**Q: Which AI models can use this server?**

A: Any MCP-compatible client including Claude Desktop, and other LLM applications supporting MCP.

**Q: Is this free to use?**

A: Yes, MIT licensed. External services (Nominatim, OSRM) are also free but have rate limits.

## Technical Questions

**Q: Why am I getting rate limit errors?**

A: Nominatim allows only 1 request/second. The server handles this automatically, but batch operations may be slow.

**Q: Can I use my own geocoding/routing server?**

A: Yes! Set NOMINATIM_URL, OSRM_URL, or PELIAS_URL environment variables.

**Q: What coordinate format does the server use?**

A: WGS84 (EPSG:4326) - standard GPS coordinates. Latitude: -90 to 90, Longitude: -180 to 180.

**Q: Why are isochrones approximate?**

A: OSRM doesn't have native isochrone support. We sample points and create a hull. For production, use Valhalla.

## Troubleshooting

**Q: Claude Desktop doesn't see the GIS tools**

A: Check claude_desktop_config.json syntax, ensure uvx is installed, restart Claude Desktop.

**Q: "Network error" messages**

A: Check internet connection. External APIs may be temporarily unavailable.

**Q: File read/write fails**

A: Verify file path exists, check file permissions, ensure supported format.

## Feature Requests

**Q: Will you add [feature]?**

A: Check the roadmap in README. Open a GitHub issue for new requests.

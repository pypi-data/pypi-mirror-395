# Tools Reference

This document provides comprehensive documentation for all 13 tools available in the GIS MCP Server.

## Table of Contents

- [Geocoding Tools](#geocoding-tools)
  - [geocode](#geocode)
  - [reverse_geocode](#reverse_geocode)
  - [batch_geocode](#batch_geocode)
- [Elevation Tools](#elevation-tools)
  - [get_elevation](#get_elevation)
  - [get_elevation_profile](#get_elevation_profile)
- [Geometry Tools](#geometry-tools)
  - [distance](#distance)
  - [buffer](#buffer)
  - [spatial_query](#spatial_query)
  - [transform_crs](#transform_crs)
- [Routing Tools](#routing-tools)
  - [route](#route)
  - [isochrone](#isochrone)
- [File Tools](#file-tools)
  - [read_file](#read_file)
  - [write_file](#write_file)

---

## Geocoding Tools

### geocode

Convert an address or place name into geographic coordinates (latitude and longitude).

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `address` | string | Yes | - | The address or place name to geocode |
| `provider` | string | No | `"nominatim"` | Geocoding provider to use: `"nominatim"` or `"pelias"` |

**Returns:**

```json
{
  "lat": 48.8566,
  "lon": 2.3522,
  "display_name": "Paris, Île-de-France, France métropolitaine, France",
  "address": {
    "city": "Paris",
    "country": "France",
    "country_code": "fr",
    "state": "Île-de-France"
  },
  "confidence": 0.95
}
```

**Response Fields:**

- `lat` (float): Latitude in decimal degrees
- `lon` (float): Longitude in decimal degrees
- `display_name` (string): Human-readable formatted address
- `address` (object): Structured address components
- `confidence` (float): Confidence score (0-1)

**Example Usage:**

```json
{
  "address": "1600 Pennsylvania Avenue NW, Washington, DC",
  "provider": "nominatim"
}
```

---

### reverse_geocode

Convert geographic coordinates into a human-readable address.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lat` | float | Yes | - | Latitude in decimal degrees (-90 to 90) |
| `lon` | float | Yes | - | Longitude in decimal degrees (-180 to 180) |
| `provider` | string | No | `"nominatim"` | Geocoding provider: `"nominatim"` or `"pelias"` |

**Returns:**

```json
{
  "display_name": "Tour Eiffel, 5 Avenue Anatole France, Gros-Caillou, 7e, Paris, Île-de-France, France métropolitaine, 75007, France",
  "address": {
    "tourism": "Tour Eiffel",
    "road": "Avenue Anatole France",
    "neighbourhood": "Gros-Caillou",
    "suburb": "7e",
    "city": "Paris",
    "postcode": "75007",
    "country": "France",
    "country_code": "fr"
  }
}
```

**Response Fields:**

- `display_name` (string): Full formatted address
- `address` (object): Structured address components with various details

**Example Usage:**

```json
{
  "lat": 48.8584,
  "lon": 2.2945,
  "provider": "nominatim"
}
```

---

### batch_geocode

Geocode multiple addresses in a single request. Maximum 10 addresses per batch.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `addresses` | array[string] | Yes | - | Array of addresses to geocode (max 10) |
| `provider` | string | No | `"nominatim"` | Geocoding provider to use |

**Returns:**

```json
{
  "results": [
    {
      "address": "Paris, France",
      "success": true,
      "lat": 48.8566,
      "lon": 2.3522,
      "display_name": "Paris, Île-de-France, France",
      "confidence": 0.95
    },
    {
      "address": "London, UK",
      "success": true,
      "lat": 51.5074,
      "lon": -0.1278,
      "display_name": "London, Greater London, England, United Kingdom",
      "confidence": 0.92
    }
  ],
  "summary": {
    "total": 2,
    "successful": 2,
    "failed": 0
  }
}
```

**Response Fields:**

- `results` (array): Array of geocoding results for each address
  - `address` (string): Original input address
  - `success` (boolean): Whether geocoding was successful
  - `lat`, `lon` (float): Coordinates (if successful)
  - `display_name` (string): Formatted address (if successful)
  - `confidence` (float): Confidence score (if successful)
  - `error` (string): Error message (if failed)
- `summary` (object): Summary statistics
  - `total` (int): Total number of addresses
  - `successful` (int): Successfully geocoded
  - `failed` (int): Failed geocoding attempts

**Example Usage:**

```json
{
  "addresses": [
    "Paris, France",
    "London, UK",
    "Berlin, Germany"
  ]
}
```

---

## Elevation Tools

### get_elevation

Get the elevation (altitude) for a specific geographic point.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lat` | float | Yes | - | Latitude in decimal degrees (-90 to 90) |
| `lon` | float | Yes | - | Longitude in decimal degrees (-180 to 180) |

**Returns:**

```json
{
  "elevation_m": 347.5,
  "location": {
    "lat": 46.5197,
    "lon": 6.6323
  }
}
```

**Response Fields:**

- `elevation_m` (float): Elevation in meters above sea level
- `location` (object): Confirmed coordinates
  - `lat` (float): Latitude
  - `lon` (float): Longitude

**Example Usage:**

```json
{
  "lat": 46.5197,
  "lon": 6.6323
}
```

**Notes:**

- Uses Open-Elevation API or similar elevation service
- Returns elevation in meters (can be negative for below sea level)
- Accuracy depends on the underlying DEM (Digital Elevation Model)

---

### get_elevation_profile

Get elevation data along a path defined by multiple coordinate points.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coordinates` | array | Yes | - | Array of [lon, lat] coordinate pairs (2-100 points) |

**Coordinate Format:**

Each coordinate should be an array: `[longitude, latitude]`

**Returns:**

```json
{
  "profile": [
    {
      "distance_m": 0,
      "elevation_m": 100.5,
      "lat": 46.5197,
      "lon": 6.6323
    },
    {
      "distance_m": 1523.7,
      "elevation_m": 250.3,
      "lat": 46.5300,
      "lon": 6.6450
    }
  ],
  "stats": {
    "min_elevation_m": 100.5,
    "max_elevation_m": 350.8,
    "elevation_gain_m": 250.3,
    "elevation_loss_m": 0,
    "average_elevation_m": 225.6,
    "total_distance_m": 5430.2
  }
}
```

**Response Fields:**

- `profile` (array): Elevation data for each point
  - `distance_m` (float): Cumulative distance from start in meters
  - `elevation_m` (float): Elevation at this point
  - `lat`, `lon` (float): Coordinates of the point
- `stats` (object): Summary statistics
  - `min_elevation_m` (float): Lowest elevation along the path
  - `max_elevation_m` (float): Highest elevation along the path
  - `elevation_gain_m` (float): Total cumulative elevation gain
  - `elevation_loss_m` (float): Total cumulative elevation loss
  - `average_elevation_m` (float): Mean elevation
  - `total_distance_m` (float): Total path distance

**Example Usage:**

```json
{
  "coordinates": [
    [6.6323, 46.5197],
    [6.6450, 46.5300],
    [6.6580, 46.5400]
  ]
}
```

**Notes:**

- Minimum 2 points, maximum 100 points
- Coordinates must be in [longitude, latitude] order (GeoJSON format)
- Useful for hiking trails, cycling routes, or any path analysis

---

## Geometry Tools

### distance

Calculate the distance between two geographic points using different calculation methods.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lat1` | float | Yes | - | Latitude of first point (-90 to 90) |
| `lon1` | float | Yes | - | Longitude of first point (-180 to 180) |
| `lat2` | float | Yes | - | Latitude of second point (-90 to 90) |
| `lon2` | float | Yes | - | Longitude of second point (-180 to 180) |
| `method` | string | No | `"haversine"` | Calculation method: `"haversine"` or `"geodesic"` |

**Methods:**

- `haversine`: Fast approximation assuming spherical Earth (good for most purposes)
- `geodesic`: More accurate calculation accounting for Earth's ellipsoid shape

**Returns:**

```json
{
  "distance": {
    "meters": 5837.41,
    "kilometers": 5.84,
    "miles": 3.63,
    "feet": 19152.26
  },
  "method": "haversine"
}
```

**Response Fields:**

- `distance` (object): Distance in multiple units
  - `meters` (float): Distance in meters
  - `kilometers` (float): Distance in kilometers
  - `miles` (float): Distance in miles
  - `feet` (float): Distance in feet
- `method` (string): Calculation method used

**Example Usage:**

```json
{
  "lat1": 48.8566,
  "lon1": 2.3522,
  "lat2": 51.5074,
  "lon2": -0.1278,
  "method": "geodesic"
}
```

---

### buffer

Create a buffer zone (polygon) around a geometry at a specified distance.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geometry` | object | Yes | - | GeoJSON geometry (Point, LineString, Polygon, etc.) |
| `distance_meters` | float | Yes | - | Buffer distance in meters |
| `resolution` | int | No | `16` | Number of segments per quadrant (higher = smoother) |

**Supported Geometry Types:**

- Point
- LineString
- Polygon
- MultiPoint
- MultiLineString
- MultiPolygon

**Returns:**

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [2.3532, 48.8576],
        [2.3530, 48.8572],
        ...
      ]
    ]
  },
  "properties": {
    "buffer_distance_m": 100,
    "area_km2": 0.0314,
    "perimeter_km": 0.628
  }
}
```

**Response Fields:**

- `type` (string): Always "Feature"
- `geometry` (object): GeoJSON Polygon geometry representing the buffer zone
- `properties` (object): Buffer metadata
  - `buffer_distance_m` (float): Applied buffer distance
  - `area_km2` (float): Buffer area in square kilometers
  - `perimeter_km` (float): Buffer perimeter in kilometers

**Example Usage:**

```json
{
  "geometry": {
    "type": "Point",
    "coordinates": [2.3522, 48.8566]
  },
  "distance_meters": 100,
  "resolution": 16
}
```

**Notes:**

- Higher resolution values create smoother buffers but increase computation time
- Useful for creating proximity zones, service areas, or safety buffers

---

### spatial_query

Perform spatial operations between two geometries (intersections, unions, differences, etc.).

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geometry1` | object | Yes | - | First GeoJSON geometry |
| `geometry2` | object | Yes | - | Second GeoJSON geometry |
| `operation` | string | Yes | - | Spatial operation to perform |

**Supported Operations:**

| Operation | Type | Description | Return Type |
|-----------|------|-------------|-------------|
| `intersection` | Overlay | Returns the overlapping area | Geometry |
| `union` | Overlay | Combines both geometries | Geometry |
| `difference` | Overlay | Removes geometry2 from geometry1 | Geometry |
| `contains` | Predicate | Tests if geometry1 contains geometry2 | Boolean |
| `within` | Predicate | Tests if geometry1 is within geometry2 | Boolean |
| `intersects` | Predicate | Tests if geometries intersect | Boolean |
| `overlaps` | Predicate | Tests if geometries overlap | Boolean |

**Returns (Overlay Operations):**

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  },
  "properties": {
    "operation": "intersection",
    "area_km2": 1.25
  }
}
```

**Returns (Predicate Operations):**

```json
{
  "result": true,
  "operation": "contains"
}
```

**Example Usage (Overlay):**

```json
{
  "geometry1": {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
  },
  "geometry2": {
    "type": "Polygon",
    "coordinates": [[[5, 5], [15, 5], [15, 15], [5, 15], [5, 5]]]
  },
  "operation": "intersection"
}
```

**Example Usage (Predicate):**

```json
{
  "geometry1": {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
  },
  "geometry2": {
    "type": "Point",
    "coordinates": [5, 5]
  },
  "operation": "contains"
}
```

---

### transform_crs

Transform geometry coordinates from one Coordinate Reference System (CRS) to another.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geometry` | object | Yes | - | GeoJSON geometry to transform |
| `source_crs` | string | Yes | - | Source CRS in EPSG format (e.g., "EPSG:4326") |
| `target_crs` | string | Yes | - | Target CRS in EPSG format (e.g., "EPSG:3857") |

**Common CRS Codes:**

| EPSG Code | Name | Description | Usage |
|-----------|------|-------------|-------|
| EPSG:4326 | WGS84 | Latitude/Longitude in degrees | GPS, web services, global data |
| EPSG:3857 | Web Mercator | Projected coordinates in meters | Web maps (Google, OpenStreetMap) |
| EPSG:2154 | Lambert 93 | French national grid | France official mapping |
| EPSG:27700 | OSGB36 | British National Grid | UK official mapping |
| EPSG:32633 | UTM Zone 33N | Universal Transverse Mercator | Central Europe |

**Returns:**

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [261848.78, 6250566.72]
  },
  "properties": {
    "source_crs": "EPSG:4326",
    "target_crs": "EPSG:3857"
  }
}
```

**Response Fields:**

- `type` (string): Always "Feature"
- `geometry` (object): Transformed GeoJSON geometry
- `properties` (object): Transformation metadata
  - `source_crs` (string): Original CRS
  - `target_crs` (string): Target CRS

**Example Usage:**

```json
{
  "geometry": {
    "type": "Point",
    "coordinates": [2.3522, 48.8566]
  },
  "source_crs": "EPSG:4326",
  "target_crs": "EPSG:3857"
}
```

**Notes:**

- Essential for working with different mapping systems
- Use EPSG:4326 for GPS coordinates
- Use EPSG:3857 for web mapping applications
- Projected CRS (in meters) are better for distance/area calculations

---

## Routing Tools

### route

Calculate a route between two points with turn-by-turn directions.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_lat` | float | Yes | - | Starting point latitude |
| `start_lon` | float | Yes | - | Starting point longitude |
| `end_lat` | float | Yes | - | Destination point latitude |
| `end_lon` | float | Yes | - | Destination point longitude |
| `profile` | string | No | `"driving"` | Routing profile: `"driving"`, `"walking"`, or `"cycling"` |

**Routing Profiles:**

- `driving`: Car routing with road restrictions
- `walking`: Pedestrian routing including footpaths
- `cycling`: Bicycle routing with bike-friendly paths

**Returns:**

```json
{
  "distance": {
    "meters": 5423.7,
    "kilometers": 5.42,
    "miles": 3.37
  },
  "duration": {
    "seconds": 780,
    "minutes": 13,
    "formatted": "13 minutes"
  },
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [2.3522, 48.8566],
      [2.3530, 48.8570],
      ...
    ]
  },
  "steps": [
    {
      "distance_m": 234.5,
      "duration_s": 45,
      "instruction": "Head north on Rue de Rivoli",
      "name": "Rue de Rivoli"
    },
    {
      "distance_m": 567.8,
      "duration_s": 89,
      "instruction": "Turn right onto Avenue de l'Opéra",
      "name": "Avenue de l'Opéra"
    }
  ],
  "profile": "driving"
}
```

**Response Fields:**

- `distance` (object): Route distance in multiple units
- `duration` (object): Estimated travel time
- `geometry` (object): GeoJSON LineString of the route path
- `steps` (array): Turn-by-turn navigation instructions
  - `distance_m` (float): Distance of this step
  - `duration_s` (float): Duration of this step
  - `instruction` (string): Human-readable instruction
  - `name` (string): Road/path name
- `profile` (string): Routing profile used

**Example Usage:**

```json
{
  "start_lat": 48.8566,
  "start_lon": 2.3522,
  "end_lat": 48.8606,
  "end_lon": 2.3376,
  "profile": "walking"
}
```

**Notes:**

- Uses OpenRouteService or similar routing engine
- Respects road network and one-way restrictions
- Walking profile may include stairs and pedestrian-only paths

---

### isochrone

Generate an isochrone polygon showing the area reachable from a point within a specified time limit.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lat` | float | Yes | - | Starting point latitude |
| `lon` | float | Yes | - | Starting point longitude |
| `time_minutes` | int | Yes | - | Time limit in minutes (1-120) |
| `profile` | string | No | `"driving"` | Travel profile: `"driving"`, `"walking"`, or `"cycling"` |

**Time Limits:**

- Minimum: 1 minute
- Maximum: 120 minutes (2 hours)

**Returns:**

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [2.3522, 48.8566],
        [2.3650, 48.8580],
        ...
      ]
    ]
  },
  "properties": {
    "center": {
      "lat": 48.8566,
      "lon": 2.3522
    },
    "time_minutes": 15,
    "profile": "driving",
    "area_km2": 45.3
  }
}
```

**Response Fields:**

- `type` (string): Always "Feature"
- `geometry` (object): GeoJSON Polygon representing reachable area
- `properties` (object): Isochrone metadata
  - `center` (object): Starting point coordinates
  - `time_minutes` (int): Time limit used
  - `profile` (string): Travel profile used
  - `area_km2` (float): Area of the isochrone in square kilometers

**Example Usage:**

```json
{
  "lat": 48.8566,
  "lon": 2.3522,
  "time_minutes": 15,
  "profile": "driving"
}
```

**Use Cases:**

- Service area analysis (delivery zones)
- Accessibility mapping (where can customers reach in X minutes?)
- Emergency response planning (ambulance coverage areas)
- Real estate analysis (commute time zones)

**Notes:**

- Results account for actual road network and speed limits
- Walking profile considers pedestrian paths
- Cycling profile uses bike-friendly routes

---

## File Tools

### read_file

Read and parse geospatial data files in various formats.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_path` | string | Yes | - | Path to the geospatial file |
| `layer` | string | No | First layer | Specific layer name (for multi-layer formats) |
| `limit` | int | No | All features | Maximum number of features to return |

**Supported Formats:**

| Format | Extension | Description |
|--------|-----------|-------------|
| GeoJSON | `.geojson`, `.json` | JSON-based geospatial format |
| Shapefile | `.shp` | ESRI Shapefile (requires .shx, .dbf) |
| GeoPackage | `.gpkg` | SQLite-based geospatial format |
| KML | `.kml` | Keyhole Markup Language (Google Earth) |
| GML | `.gml` | Geography Markup Language |

**Returns:**

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [2.3522, 48.8566]
      },
      "properties": {
        "name": "Paris",
        "population": 2161000,
        "country": "France"
      }
    }
  ],
  "metadata": {
    "file_path": "/path/to/cities.geojson",
    "layer": "cities",
    "feature_count": 150,
    "returned_count": 150,
    "crs": "EPSG:4326",
    "bounds": {
      "minx": -180,
      "miny": -90,
      "maxx": 180,
      "maxy": 90
    }
  }
}
```

**Response Fields:**

- `type` (string): Always "FeatureCollection"
- `features` (array): Array of GeoJSON Feature objects
- `metadata` (object): File information
  - `file_path` (string): Path to the file
  - `layer` (string): Layer name (if applicable)
  - `feature_count` (int): Total features in file
  - `returned_count` (int): Number of features returned
  - `crs` (string): Coordinate Reference System
  - `bounds` (object): Spatial extent

**Example Usage:**

```json
{
  "file_path": "/data/world_cities.gpkg",
  "layer": "cities",
  "limit": 100
}
```

**Notes:**

- Shapefiles require accompanying .shx and .dbf files in the same directory
- GeoPackage files may contain multiple layers
- CRS is automatically detected and preserved
- Large files can be limited using the `limit` parameter

---

### write_file

Write geospatial features to a file in various formats.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `features` | object | Yes | - | GeoJSON FeatureCollection to write |
| `file_path` | string | Yes | - | Output file path |
| `driver` | string | No | Auto-detect | Output format driver |
| `crs` | string | No | EPSG:4326 | Coordinate Reference System |

**Supported Drivers:**

| Driver | Extension | Description |
|--------|-----------|-------------|
| `GeoJSON` | `.geojson`, `.json` | JSON-based geospatial format |
| `ESRI Shapefile` | `.shp` | ESRI Shapefile (creates .shx, .dbf, .prj) |
| `GPKG` | `.gpkg` | GeoPackage (SQLite-based) |

**Returns:**

```json
{
  "success": true,
  "file_path": "/output/data.geojson",
  "driver": "GeoJSON",
  "feature_count": 45,
  "file_size_bytes": 15234,
  "crs": "EPSG:4326"
}
```

**Response Fields:**

- `success` (boolean): Whether the write operation succeeded
- `file_path` (string): Path to the created file
- `driver` (string): Format driver used
- `feature_count` (int): Number of features written
- `file_size_bytes` (int): Size of the output file
- `crs` (string): Coordinate Reference System used

**Example Usage:**

```json
{
  "features": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [2.3522, 48.8566]
        },
        "properties": {
          "name": "Paris",
          "country": "France"
        }
      }
    ]
  },
  "file_path": "/output/cities.geojson",
  "driver": "GeoJSON",
  "crs": "EPSG:4326"
}
```

**Notes:**

- Driver is auto-detected from file extension if not specified
- Shapefiles automatically create accompanying files (.shx, .dbf, .prj)
- GeoPackage is recommended for complex data with multiple layers
- Existing files will be overwritten
- CRS defaults to EPSG:4326 (WGS84) if not specified

---

## Error Handling

All tools return errors in a consistent format:

```json
{
  "error": true,
  "message": "Description of what went wrong",
  "code": "ERROR_CODE",
  "details": {
    "additional": "context information"
  }
}
```

**Common Error Codes:**

- `INVALID_PARAMETER`: Invalid or missing required parameter
- `INVALID_COORDINATES`: Coordinates out of valid range
- `SERVICE_UNAVAILABLE`: External service (geocoding, routing) unavailable
- `FILE_NOT_FOUND`: Specified file does not exist
- `INVALID_FORMAT`: Unsupported file format or invalid GeoJSON
- `GEOMETRY_ERROR`: Invalid geometry or spatial operation
- `CRS_ERROR`: Invalid or unsupported CRS

---

## Best Practices

### Geocoding

- Always check the `confidence` score for geocoding results
- Use `batch_geocode` for multiple addresses to reduce API calls
- Respect rate limits for geocoding providers

### Elevation

- Use `get_elevation_profile` for analyzing terrain along paths
- Consider elevation data accuracy (typically ±10-30 meters)

### Geometry Operations

- Validate geometries before spatial operations
- Use `geodesic` distance method for accurate long-distance calculations
- Transform to projected CRS (e.g., EPSG:3857) for accurate area/distance calculations

### Routing

- Choose appropriate profile (driving/walking/cycling) for your use case
- Check `duration` estimates are reasonable (they depend on traffic assumptions)
- Isochrones are useful for accessibility analysis

### File Operations

- Use GeoPackage (.gpkg) for complex datasets with multiple layers
- Use GeoJSON for web applications and simple data exchange
- Use Shapefiles only when required for compatibility with older GIS software
- Always specify CRS explicitly when writing files

---

## Rate Limits and Quotas

Some tools rely on external services that may have rate limits:

- **Nominatim Geocoding**: 1 request per second
- **OpenRouteService**: Varies by account type (free tier: limited requests/day)
- **Open-Elevation**: No strict limits but avoid excessive requests

For production use, consider:
- Implementing caching for frequently used queries
- Using batch operations when available
- Respecting service rate limits
- Self-hosting services for high-volume usage

---

## Additional Resources

- [GeoJSON Specification](https://geojson.org/)
- [EPSG.io - CRS Reference](https://epsg.io/)
- [Nominatim Documentation](https://nominatim.org/release-docs/latest/)
- [OpenRouteService API](https://openrouteservice.org/dev/)
- [GDAL/OGR Documentation](https://gdal.org/)

---

*Last Updated: 2025-12-03*

# GIS MCP Server - Practical Examples

This guide provides real-world examples demonstrating how to use the GIS MCP Server for common geospatial tasks.

---

## Example 1: Find Nearby Points of Interest

**Scenario:** You want to find all restaurants within 1km of your office location.

### Step 1: Geocode the Office Location

**Request:**
```json
{
  "tool": "geocode",
  "arguments": {
    "address": "350 5th Ave, New York, NY 10118"
  }
}
```

**Response:**
```json
{
  "latitude": 40.748817,
  "longitude": -73.985428,
  "formatted_address": "350 5th Ave, New York, NY 10118, USA",
  "provider": "nominatim"
}
```

### Step 2: Create a 1km Buffer Zone

**Request:**
```json
{
  "tool": "buffer",
  "arguments": {
    "geometry": {
      "type": "Point",
      "coordinates": [-73.985428, 40.748817]
    },
    "distance": 1000,
    "unit": "meters"
  }
}
```

**Response:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-73.998468, 40.748817],
      [-73.997234, 40.743512],
      [-73.993876, 40.738567],
      // ... more coordinates forming a circle
      [-73.998468, 40.748817]
    ]
  ]
}
```

### Step 3: Use with External POI Data

Once you have the buffer polygon, you can:
- Query a restaurant database to find points within this polygon
- Use the `spatial_query` tool with your POI dataset
- Filter results by checking if each restaurant point is within the buffer using `within` predicate

**Use Case Applications:**
- Real estate: Find properties near schools or parks
- Retail: Analyze competitor locations
- Urban planning: Assess accessibility to services

---

## Example 2: Calculate Delivery Routes

**Scenario:** A delivery service needs to calculate the optimal route from a warehouse to three customer locations.

### Step 1: Batch Geocode All Addresses

**Request:**
```json
{
  "tool": "batch_geocode",
  "arguments": {
    "addresses": [
      "123 Main St, Boston, MA",
      "456 Oak Ave, Boston, MA",
      "789 Pine Rd, Boston, MA",
      "321 Elm St, Boston, MA"
    ]
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "address": "123 Main St, Boston, MA",
      "latitude": 42.3601,
      "longitude": -71.0589,
      "formatted_address": "123 Main St, Boston, MA 02129, USA"
    },
    {
      "address": "456 Oak Ave, Boston, MA",
      "latitude": 42.3550,
      "longitude": -71.0656,
      "formatted_address": "456 Oak Ave, Boston, MA 02114, USA"
    },
    {
      "address": "789 Pine Rd, Boston, MA",
      "latitude": 42.3520,
      "longitude": -71.0445,
      "formatted_address": "789 Pine Rd, Boston, MA 02127, USA"
    },
    {
      "address": "321 Elm St, Boston, MA",
      "latitude": 42.3645,
      "longitude": -71.0532,
      "formatted_address": "321 Elm St, Boston, MA 02113, USA"
    }
  ]
}
```

### Step 2: Calculate Route from Warehouse to First Stop

**Request:**
```json
{
  "tool": "route",
  "arguments": {
    "start": [-71.0589, 42.3601],
    "end": [-71.0656, 42.3550],
    "profile": "driving"
  }
}
```

**Response:**
```json
{
  "distance": 1247.5,
  "duration": 285.2,
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [-71.0589, 42.3601],
      [-71.0598, 42.3595],
      [-71.0612, 42.3585],
      // ... route coordinates
      [-71.0656, 42.3550]
    ]
  },
  "instructions": [
    "Head west on Main St",
    "Turn left onto Washington St",
    // ... turn-by-turn directions
    "Arrive at destination"
  ]
}
```

### Step 3: Calculate Remaining Routes and Sum Totals

Continue calculating routes between consecutive stops:
- Stop 1 to Stop 2
- Stop 2 to Stop 3
- Stop 3 back to Warehouse

**Total Calculation:**
```
Total Distance: 1247.5 + 875.3 + 1523.8 + 2105.4 = 5752 meters (5.75 km)
Total Duration: 285.2 + 198.5 + 342.1 + 475.8 = 1301.6 seconds (21.7 minutes)
```

**Use Case Applications:**
- Logistics planning and optimization
- Delivery time estimation
- Fuel cost calculation
- Driver schedule management

---

## Example 3: Elevation Analysis for Hiking Trail

**Scenario:** Analyze the elevation profile of a hiking trail to determine difficulty and total elevation gain.

### Step 1: Define Trail Coordinates

A trail from Mount Washington trailhead:

**Request:**
```json
{
  "tool": "elevation",
  "arguments": {
    "locations": [
      [-71.3032, 44.2706],
      [-71.3025, 44.2715],
      [-71.3015, 44.2728],
      [-71.3008, 44.2742],
      [-71.2998, 44.2755],
      [-71.2988, 44.2768],
      [-71.2980, 44.2780],
      [-71.2972, 44.2795]
    ]
  }
}
```

**Response:**
```json
{
  "elevations": [
    {
      "latitude": 44.2706,
      "longitude": -71.3032,
      "elevation": 582.3
    },
    {
      "latitude": 44.2715,
      "longitude": -71.3025,
      "elevation": 612.8
    },
    {
      "latitude": 44.2728,
      "longitude": -71.3015,
      "elevation": 658.4
    },
    {
      "latitude": 44.2742,
      "longitude": -71.3008,
      "elevation": 695.2
    },
    {
      "latitude": 44.2755,
      "longitude": -71.2998,
      "elevation": 742.6
    },
    {
      "latitude": 44.2768,
      "longitude": -71.2988,
      "elevation": 788.1
    },
    {
      "latitude": 44.2780,
      "longitude": -71.2980,
      "elevation": 825.7
    },
    {
      "latitude": 44.2795,
      "longitude": -71.2972,
      "elevation": 875.3
    }
  ]
}
```

### Step 2: Analyze Elevation Profile

**Elevation Gain Calculation:**
```
Point 1 to 2: +30.5m
Point 2 to 3: +45.6m
Point 3 to 4: +36.8m
Point 4 to 5: +47.4m
Point 5 to 6: +45.5m
Point 6 to 7: +37.6m
Point 7 to 8: +49.6m

Total Elevation Gain: 293.0 meters
```

**Trail Statistics:**
- Starting Elevation: 582.3m
- Ending Elevation: 875.3m
- Net Elevation Gain: 293.0m
- Average Grade: ~8.5% (moderate to difficult)

**Use Case Applications:**
- Hiking trail difficulty assessment
- Mountain biking route planning
- Running race course analysis
- Infrastructure planning (roads, pipelines)
- Flood risk assessment

---

## Example 4: Convert Shapefile to GeoJSON

**Scenario:** Convert a shapefile containing city boundaries to GeoJSON format for web mapping.

### Step 1: Read the Shapefile

**Request:**
```json
{
  "tool": "read_file",
  "arguments": {
    "file_path": "/data/shapefiles/city_boundaries.shp"
  }
}
```

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "city_name": "Boston",
        "population": 692600,
        "area_sqkm": 232.1
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-71.1912, 42.2279],
            [-71.1895, 42.3968],
            [-70.9286, 42.3968],
            [-70.9269, 42.2279],
            [-71.1912, 42.2279]
          ]
        ]
      }
    }
  ],
  "crs": {
    "type": "name",
    "properties": {
      "name": "EPSG:26986"
    }
  }
}
```

### Step 2: Transform CRS (if needed)

The shapefile is in Massachusetts State Plane (EPSG:26986). Convert to WGS84 (EPSG:4326) for web use:

**Request:**
```json
{
  "tool": "transform_crs",
  "arguments": {
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [239821.45, 899453.67],
          [240125.89, 918234.12],
          [267543.23, 918156.78],
          [267289.34, 899375.45],
          [239821.45, 899453.67]
        ]
      ]
    },
    "source_crs": "EPSG:26986",
    "target_crs": "EPSG:4326"
  }
}
```

**Response:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-71.1912, 42.2279],
      [-71.1895, 42.3968],
      [-70.9286, 42.3968],
      [-70.9269, 42.2279],
      [-71.1912, 42.2279]
    ]
  ]
}
```

### Step 3: Write to GeoJSON

**Request:**
```json
{
  "tool": "write_file",
  "arguments": {
    "file_path": "/output/city_boundaries.geojson",
    "data": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "city_name": "Boston",
            "population": 692600,
            "area_sqkm": 232.1
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [-71.1912, 42.2279],
                [-71.1895, 42.3968],
                [-70.9286, 42.3968],
                [-70.9269, 42.2279],
                [-71.1912, 42.2279]
              ]
            ]
          }
        }
      ]
    },
    "driver": "GeoJSON"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "File written successfully to /output/city_boundaries.geojson"
}
```

**Use Case Applications:**
- Data format conversion for web mapping
- Preparing GIS data for JavaScript libraries (Leaflet, Mapbox)
- Data sharing and interoperability
- Archive legacy spatial data in modern formats

---

## Example 5: Service Area Analysis (Isochrone)

**Scenario:** A real estate agent wants to show all areas within a 15-minute drive from a new development.

### Calculate 15-Minute Driving Isochrone

**Request:**
```json
{
  "tool": "isochrone",
  "arguments": {
    "location": [-122.4194, 37.7749],
    "time": 900,
    "profile": "driving"
  }
}
```

**Response:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-122.4194, 37.7749],
      [-122.4350, 37.7850],
      [-122.4520, 37.7820],
      [-122.4680, 37.7750],
      [-122.4720, 37.7620],
      [-122.4650, 37.7480],
      [-122.4520, 37.7380],
      [-122.4350, 37.7350],
      [-122.4180, 37.7400],
      [-122.4050, 37.7520],
      [-122.4020, 37.7650],
      [-122.4194, 37.7749]
    ]
  ],
  "time_seconds": 900,
  "profile": "driving"
}
```

### Visualization and Analysis

The returned polygon represents all areas reachable within 15 minutes by car. You can:

1. **Overlay on a map** to visualize the service area
2. **Calculate area** using geometric operations
3. **Find properties** within this polygon using spatial queries
4. **Compare** multiple time intervals (5, 10, 15 minutes)

**Use Case Applications:**

**Real Estate:**
- Show commute times from a property
- Market accessibility analysis
- "15-minute city" neighborhood planning

**Logistics:**
- Delivery service coverage areas
- Emergency response zones
- Service territory planning

**Retail:**
- Customer catchment analysis
- Store location optimization
- Competitive market analysis

**Healthcare:**
- Hospital service areas
- Ambulance response zones
- Healthcare accessibility studies

### Multi-Interval Analysis

Create multiple isochrones for 5, 10, and 15 minutes:

**5-Minute Isochrone:**
```json
{
  "tool": "isochrone",
  "arguments": {
    "location": [-122.4194, 37.7749],
    "time": 300,
    "profile": "driving"
  }
}
```

**10-Minute Isochrone:**
```json
{
  "tool": "isochrone",
  "arguments": {
    "location": [-122.4194, 37.7749],
    "time": 600,
    "profile": "driving"
  }
}
```

This creates concentric zones showing travel time gradients, useful for visualizing accessibility patterns.

---

## Example 6: Spatial Analysis - Find Overlapping Areas

**Scenario:** An urban planner needs to find where a proposed park (polygon) overlaps with existing flood zones.

### Step 1: Define the Two Geometries

**Proposed Park Boundary:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-71.0589, 42.3601],
      [-71.0589, 42.3650],
      [-71.0520, 42.3650],
      [-71.0520, 42.3601],
      [-71.0589, 42.3601]
    ]
  ]
}
```

**Flood Zone Boundary:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-71.0600, 42.3590],
      [-71.0600, 42.3630],
      [-71.0540, 42.3630],
      [-71.0540, 42.3590],
      [-71.0600, 42.3590]
    ]
  ]
}
```

### Step 2: Find Intersection Using Spatial Query

**Request:**
```json
{
  "tool": "spatial_query",
  "arguments": {
    "source_data": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "name": "Proposed Park"
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [-71.0589, 42.3601],
                [-71.0589, 42.3650],
                [-71.0520, 42.3650],
                [-71.0520, 42.3601],
                [-71.0589, 42.3601]
              ]
            ]
          }
        }
      ]
    },
    "query_geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [-71.0600, 42.3590],
          [-71.0600, 42.3630],
          [-71.0540, 42.3630],
          [-71.0540, 42.3590],
          [-71.0600, 42.3590]
        ]
      ]
    },
    "predicate": "intersects"
  }
}
```

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Proposed Park"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-71.0589, 42.3601],
            [-71.0589, 42.3650],
            [-71.0520, 42.3650],
            [-71.0520, 42.3601],
            [-71.0589, 42.3601]
          ]
        ]
      }
    }
  ],
  "matched_count": 1
}
```

### Step 3: Calculate Overlap Area

To get the exact overlapping area, use the `intersection` operation:

**Request:**
```json
{
  "tool": "geometry_operation",
  "arguments": {
    "operation": "intersection",
    "geometry_a": {
      "type": "Polygon",
      "coordinates": [
        [
          [-71.0589, 42.3601],
          [-71.0589, 42.3650],
          [-71.0520, 42.3650],
          [-71.0520, 42.3601],
          [-71.0589, 42.3601]
        ]
      ]
    },
    "geometry_b": {
      "type": "Polygon",
      "coordinates": [
        [
          [-71.0600, 42.3590],
          [-71.0600, 42.3630],
          [-71.0540, 42.3630],
          [-71.0540, 42.3590],
          [-71.0600, 42.3590]
        ]
      ]
    }
  }
}
```

**Response:**
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [-71.0589, 42.3601],
      [-71.0589, 42.3630],
      [-71.0540, 42.3630],
      [-71.0540, 42.3601],
      [-71.0589, 42.3601]
    ]
  ]
}
```

### Step 4: Calculate Area of Overlap

**Request:**
```json
{
  "tool": "area",
  "arguments": {
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [-71.0589, 42.3601],
          [-71.0589, 42.3630],
          [-71.0540, 42.3630],
          [-71.0540, 42.3601],
          [-71.0589, 42.3601]
        ]
      ]
    },
    "unit": "square_meters"
  }
}
```

**Response:**
```json
{
  "area": 18452.7,
  "unit": "square_meters"
}
```

### Analysis Results

- **Proposed Park Area:** 25,680 m²
- **Flood Zone Overlap:** 18,453 m²
- **Percentage in Flood Zone:** 71.8%

**Conclusion:** 71.8% of the proposed park lies within the flood zone, requiring special design considerations such as elevated structures, permeable surfaces, or flood-resistant landscaping.

**Use Case Applications:**

**Urban Planning:**
- Zoning compliance analysis
- Environmental impact assessment
- Land use conflict detection

**Environmental Analysis:**
- Habitat overlap studies
- Protected area management
- Contamination zone assessment

**Infrastructure:**
- Utility corridor planning
- Right-of-way analysis
- Easement conflict detection

**Emergency Management:**
- Evacuation zone planning
- Risk assessment
- Resource allocation

---

## Additional Spatial Predicates

The `spatial_query` tool supports various predicates for different analysis needs:

- **intersects**: Geometries share at least one point (most common)
- **within**: One geometry is completely inside another
- **contains**: One geometry completely contains another
- **touches**: Geometries touch at boundaries but don't overlap
- **crosses**: LineStrings or boundaries cross
- **overlaps**: Geometries overlap but neither contains the other
- **disjoint**: Geometries have no points in common

**Example - Find Properties Completely Within a Zone:**
```json
{
  "tool": "spatial_query",
  "arguments": {
    "source_data": { /* property features */ },
    "query_geometry": { /* zone polygon */ },
    "predicate": "within"
  }
}
```

---

## Best Practices

1. **Coordinate Order**: Always use [longitude, latitude] format (x, y)
2. **CRS Awareness**: Check and transform coordinate reference systems when needed
3. **Units**: Specify units explicitly in distance and area calculations
4. **Batch Operations**: Use batch_geocode for multiple addresses to reduce API calls
5. **Error Handling**: Check response status and handle geocoding failures gracefully
6. **Rate Limits**: Be mindful of external service rate limits (geocoding, routing)
7. **Data Validation**: Validate geometry types and coordinate formats before operations

---

## Next Steps

- Explore the [API Reference](./API-Reference.md) for complete tool documentation
- Check [Configuration Guide](./Configuration.md) for advanced settings
- See [Troubleshooting](./Troubleshooting.md) for common issues and solutions
- Visit [Use Cases](./Use-Cases.md) for industry-specific applications

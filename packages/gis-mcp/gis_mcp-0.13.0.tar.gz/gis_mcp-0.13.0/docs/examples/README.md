# Examples Overview

This section contains practical, step-by-step examples for using GIS MCP Server in real-world geospatial workflows. Each example includes prompts, actions, and video tutorials to help you get started quickly.

## Available Examples

- [**Example 1: Basic Spatial Analysis (Claude)**](basic_spatial_analysis_claude.md)

  - Perform buffer and intersection operations on shapefiles (e.g., park and building polygons).
  - Learn how to load shapefiles, buffer geometries, find intersections, and return results in WKT format.
  - Includes a video walkthrough.

- [**Example 2: CRS Check, Reprojection, Area & Distance Calculations**](crs_area_distance_analysis.md)

  - Check and transform the CRS of a parcel shapefile, calculate area by land use, and measure distances between centroids.
  - Useful for urban planning, cadastral management, and spatial QA.
  - Includes a video walkthrough.

- [**Example 3: Movement Analysis (OSMnx)**](movement_example.md)

  - Download and analyze street networks, calculate shortest paths between points, and visualize movement networks.
  - Useful for urban mobility, routing, and network analysis.
  - Includes a video walkthrough.

- [**Example 4: Climate Data Download & Analysis**](climate_data_example.md)

  - Download, visualize, and analyze climate raster data (e.g., Temperature) using GIS MCP Server & Claude Desktop.
  - Learn how to clip rasters, calculate zonal statistics, and export results for further analysis.

- [**Example 5: Build Your First GIS AI Agent**](../gis-ai-agent/README.md)

  - Create your own AI agent from scratch using the GIS MCP Server.
  - Available in two flavors:
    - **[LangChain (Python)](../gis-ai-agent/langchain.md)**: Step-by-step tutorial from zero to hero. Integrate with OpenRouter to access multiple AI models (DeepSeek, Gemini, GPT-4, Claude, etc.).
    - **[OpenAI (NodeJs)](../gis-ai-agent/openai-nodejs.md)**: Perfect for JavaScript/TypeScript developers using OpenAI's Agent SDK.
  - Learn how to build a complete agent that can perform geospatial operations through natural language.
  - No prior AI or GIS experience needed.

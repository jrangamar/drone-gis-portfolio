# Drone GIS Portfolio

A portfolio of GIS, photogrammetry, and geospatial web-publishing projects focused on drone imagery, spatial analysis, and reproducible technical workflows.

The projects progress from desktop GIS and cartographic analysis, through photogrammetry processing, to Python-based interactive publishing.

## Live Interactive Viewer

[Open the interactive geospatial viewer](https://jrangamar.github.io/drone-gis-portfolio/)

## Project Overview

### 01 — South Florida QGIS Map

A site-context mapping project centered on Arch Creek Park in Miami-Dade County.

The project demonstrates:

- QGIS project setup and layer management
- Coordinate reference system selection and reprojection
- Vector data preparation
- Site buffers and local context analysis
- Labeling and cartographic styling
- Final static map layout

Project directory:

```text
01_south_florida_qgis_map/
```

### 02 — Photogrammetry Case Studies

A WebODM-based photogrammetry project using two public drone-image datasets:

- Sand Key
- Helenenschacht

The project demonstrates:

- Docker-based WebODM operation
- Drone-image reconstruction
- Orthophoto and DSM generation
- Hillshade and contour creation in QGIS
- Slope and terrain-product review
- Point-cloud and 3D-output inspection
- Resource troubleshooting
- Recovery from an out-of-memory meshing failure
- Comparison of coastal and structural datasets

Project directory:

```text
02_photogrammetry/
```

### 03 — Interactive Geospatial Viewer

A Python-generated Folium and Leaflet viewer that publishes selected outputs from the earlier projects as a static website.

The project demonstrates:

- Python geospatial preprocessing
- GeoJSON project locations and area polygons
- Folium and Leaflet map generation
- Custom JavaScript interaction
- Popup image carousels and expanded previews
- Coordinated marker and polygon highlighting
- Responsive popup positioning
- Static-site packaging
- GitHub Pages deployment through GitHub Actions

Project directory:

```text
03_interactive_geospatial_viewer/
```

Live site:

[https://jrangamar.github.io/drone-gis-portfolio/](https://jrangamar.github.io/drone-gis-portfolio/)

## Portfolio Progression

```text
QGIS mapping
      ↓
Photogrammetry processing
      ↓
Python and web geospatial publishing
```

Together, these projects demonstrate a workflow that moves from spatial data preparation and analysis to imagery processing and public-facing presentation.

## Repository Structure

```text
GIS_portfolio/
├── 01_south_florida_qgis_map/
├── 02_photogrammetry/
├── 03_interactive_geospatial_viewer/
├── .github/
│   └── workflows/
├── .gitignore
└── README.md
```

Each project directory contains its own documentation, data organization, scripts, outputs, or supporting notes as appropriate.

## Tools and Technologies

- QGIS
- Python
- GeoPandas
- Folium
- Leaflet
- GeoJSON
- WebODM
- Docker
- Git
- GitHub
- GitHub Actions
- GitHub Pages

## Data and Storage Notes

Large raw drone-image datasets and full processing outputs are excluded where they are impractical for a public Git repository.

The repository emphasizes:

- Reproducible scripts
- Lightweight derived products
- Web-ready preview assets
- Project documentation
- Selected screenshots and outputs

Source datasets and external GIS layers are credited within the relevant project documentation.

## Current Scope

This repository currently focuses on:

- GIS mapping and cartography
- Drone photogrammetry
- Raster and vector output review
- Interactive geospatial publishing

Possible future work may explore remote-sensing analysis, point-cloud inspection, and 3D geospatial visualization.

## Author

Journey Rangamar
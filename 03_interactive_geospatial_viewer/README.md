# Interactive Geospatial Viewer for Drone Mapping Outputs

A browser-based geospatial portfolio viewer built with Python, Folium, GeoPandas, GeoJSON, and Leaflet.

This project publishes selected outputs from earlier GIS and photogrammetry work as an interactive static website. It combines project locations, mapped site boundaries, image previews, and short project summaries in a single interface that can be hosted through GitHub Pages.

## Live Demo

GitHub Pages deployment pending.

## Project Goals

The viewer demonstrates a lightweight geospatial publishing workflow:

1. Prepare project locations and boundaries as GeoJSON.
2. Generate the map with Python.
3. Add custom Leaflet interaction through Folium.
4. Package the result as static HTML, JavaScript, GeoJSON, and image assets.
5. Publish the viewer through GitHub Pages.

The project extends the earlier portfolio work:

- **Project 01:** QGIS site-context mapping
- **Project 02:** WebODM photogrammetry processing and raster/vector analysis
- **Project 03:** Python-based interactive geospatial publishing

## Included Projects

### Arch Creek Park

A QGIS site-context mapping project using local park and street data, projected analysis layers, buffers, labeling, and a final cartographic layout.

### Sand Key

A WebODM photogrammetry case study based on a coastal dataset. Outputs include an orthophoto, DSM-derived products, contours, slope analysis, and point-cloud previews.

### Helenenschacht

A WebODM photogrammetry case study based on an industrial structure dataset. The workflow included reconstruction, troubleshooting an out-of-memory failure during meshing, Docker resource adjustment, QGIS review, contours, hillshade, orthophoto, and point-cloud previews.

## Viewer Features

- Interactive project markers
- GeoJSON project-area polygons
- Coordinated marker and polygon hover behavior
- Active polygon highlighting while a popup is open
- Multiple basemap choices
- Project-area visibility controls
- Default-view reset control
- Popup image carousels
- Expanded image previews
- Automatic popup reset after closing
- Responsive popup panning within a 10% inset safe area
- Static output suitable for GitHub Pages

## Technical Workflow

The site is generated rather than manually authored as a single HTML file.

```text
GeoJSON project data
        +
preview images
        +
Python map configuration
        |
        v
Folium / Leaflet map generation
        |
        v
web/index.html
        +
web/data/previews/
        |
        v
static web hosting
```

Python handles preprocessing and map construction. Folium generates the Leaflet map, while custom JavaScript controls popup behavior, image expansion, carousel state, polygon highlighting, and viewport-safe panning.

The deployed website does not require a Python server. Python is used only to build the static site.

## Repository Structure

```text
03_interactive_geospatial_viewer/
├── data/
│   ├── geojson/
│   │   ├── project_areas.geojson
│   │   └── project_sites.geojson
│   └── previews/
├── scripts/
│   ├── build_map.py
│   └── build_project_areas.py
├── web/
│   ├── data/
│   │   └── previews/
│   └── index.html
├── requirements.txt
└── README.md
```

### Important Directories

- `data/geojson/` contains source project locations and project-area geometry.
- `data/previews/` contains the source preview images used by the map.
- `scripts/` contains the Python build scripts.
- `web/` contains the static website ready for local serving or deployment.

## Local Setup

From the repository root:

```bash
cd 03_interactive_geospatial_viewer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build the Viewer

```bash
python scripts/build_map.py
```

The generated map is written to:

```text
web/index.html
```

## Serve Locally

Use a local HTTP server rather than opening `index.html` directly:

```bash
python3 -m http.server 8001 --directory web
```

Then open:

```text
http://localhost:8001
```

Port `8001` is used because WebODM may already be running on `localhost:8000`.

Stop the local server with `Ctrl-C`.

## Rebuilding Project Areas

The project-area GeoJSON can be regenerated with:

```bash
python scripts/build_project_areas.py
```

Then rebuild the viewer:

```bash
python scripts/build_map.py
```

## Deployment

The publishable site is located in:

```text
03_interactive_geospatial_viewer/web/
```

Because this directory is nested inside the repository, GitHub Pages should be configured through a GitHub Actions workflow that uploads this folder as the Pages artifact.

After deployment, add the live URL near the top of this README.

## Data and Asset Notes

The repository includes lightweight project summaries, GeoJSON, screenshots, and web-ready preview images.

Large raw drone-image datasets and full WebODM processing outputs are not included. This keeps the repository practical to clone and separates portfolio presentation files from large source datasets.

Preview images inside `web/data/previews/` are copies used by the static website. The corresponding source images remain in `data/previews/`.

## Skills Demonstrated

- Python-based geospatial preprocessing
- GeoJSON creation and management
- Folium and Leaflet map generation
- Custom JavaScript interaction inside a Folium workflow
- Static web publishing
- Responsive popup and viewport behavior
- GIS and photogrammetry result communication
- Repository organization and reproducible project structure

## Limitations and Future Extensions

This project is intentionally a lightweight static viewer rather than a full web-GIS application.

Possible future extensions include:

- Raster tile pyramids for large orthophotos or elevation products
- Dedicated metadata panels
- Search and filtering
- React Leaflet migration
- Cloud-optimized raster delivery
- Embedded 3D or point-cloud previews

Full point-cloud inspection and 3D visualization are reserved for the next portfolio project.

## Related Portfolio Projects

- `01_south_florida_qgis_map`
- `02_photogrammetry`

## Possible Future Work

Future portfolio work may explore remote-sensing analysis, point-cloud inspection, and 3D geospatial visualization.

## Author

Journey Rangamar
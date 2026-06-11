# Helenenschacht Portfolio Dataset

## Dataset Information

- Dataset: Helenenschacht
- Images: 176
- Dataset Size: 2.46 GB
- Acquisition Platform: Autel Evo II Pro RTK
- CRS: WGS 84 / UTM Zone 33N (EPSG:32633)

## Purpose

Selected after completing the Sand Key learning run.

Goals:

- Work with a larger image set.
- Process a more varied environment.
- Incorporate Ground Control Points.
- Produce terrain products beyond basic hillshade and contours.
- Build a portfolio-quality photogrammetry case study.

## Dataset Components

Included:

- 176 RGB images
- Ground Control Point file (gcp_list.txt)
- RTK observation data

Processing used:

- RGB imagery
- Ground Control Point file

RTK observation files were retained but not used directly during processing.

## Processing Configuration

- Images: 176
- GCP File: gcp_list.txt
- Resize Images: No
- Processing Profile: Default
- Auto Boundary: Enabled
- DSM Generation: Enabled

## Processing Results

- Reconstruction completed successfully.
- Average GSD: 1.06 cm
- Area: 7,700.88 m²
- Points: 8,874,132
- Georeferencing: GPS/GCP

Generated:

- Orthophoto
- DSM
- Point cloud
- 3D model
- Quality report

## Terrain Analysis

Generated in QGIS:

- Hillshade raster
- 1 m contour lines
- 2 m contour lines
- Slope raster
- Aspect raster

### Contours

The 1 m contour interval provided the best balance between readability and terrain detail.

The 2 m contour interval simplified the terrain excessively and obscured gradual elevation changes visible along the road corridor.

### Slope

Slope analysis clearly highlighted:

- Road embankments
- Terrain transitions
- Vegetation boundaries
- Areas of rapid elevation change

Among the derived terrain products, slope provided the clearest visualization of terrain structure.

### Aspect

Aspect analysis was generated successfully and clearly distinguished the road corridor from surrounding vegetation. However, the DSM captured substantial canopy and vegetation detail, causing the aspect raster to report many small-scale directional changes. The result was technically correct but visually noisy, reducing its usefulness for interpreting broader terrain orientation.

For this dataset, hillshade, contours, and slope provided more actionable terrain information than aspect.

## Processing Challenge

Initial processing failed after 13 minutes 26 seconds.

Task output reported:

opendm.system.SubprocessException: Child returned 137

Investigation determined that Docker Desktop was limited to 7.75 GiB of RAM despite the host system containing 16 GB of unified memory.

The failure occurred during Screened Poisson Reconstruction (meshing).

Resolution:

- Increased Docker memory allocation to 12 GiB.
- Resumed processing from the Meshing stage.
- Processing completed successfully after approximately 5 additional minutes.

## Lessons Learned

- Docker memory limits can become the primary bottleneck during photogrammetry processing.
- WebODM task logs provide useful diagnostics for identifying failure stages.
- Resume checkpoints can prevent unnecessary reprocessing.
- GCP-enabled projects introduce additional workflow considerations beyond image-only processing.
- Slope and hillshade products often communicate terrain characteristics more effectively than contour lines alone.
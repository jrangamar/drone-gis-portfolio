# Helenenschacht Photogrammetry and Terrain Analysis Case Study

## Overview

This project explored a complete photogrammetry-to-GIS workflow using the Helenenschacht drone imagery dataset. The objective was to process aerial imagery into geospatial products using WebODM and perform terrain analysis within QGIS.

The project was completed after an introductory photogrammetry exercise using the Sand Key dataset and served as a more advanced case study involving a larger image set, Ground Control Points (GCPs), terrain analysis products, and troubleshooting of a processing failure.

---

## Objectives

- Process a larger and more complex photogrammetry dataset.
- Incorporate Ground Control Points into the workflow.
- Generate standard photogrammetry deliverables.
- Perform terrain analysis using QGIS.
- Practice troubleshooting and recovery procedures when processing failures occur.

---

## Dataset

**Dataset:** Helenenschacht

**Dataset Size:** 2.46 GB

**Images:** 176 RGB photographs

**Additional Data:**
- Ground Control Point (GCP) file
- RTK observation data

**Coordinate Reference System:**
- WGS 84 / UTM Zone 33N (EPSG:32633)

The imagery was captured using an Autel Evo II RTK platform and included supporting georeferencing information for improved spatial accuracy.

---

## Workflow

### Photogrammetry Processing

Imagery was processed using WebODM running in Docker on a local workstation.

Generated products included:

- Orthophoto
- Digital Surface Model (DSM)
- Point Cloud
- 3D Reconstruction
- Processing Report

The completed reconstruction produced:

- Average GSD: 1.06 cm
- Area Covered: 7,700.88 m²
- Point Count: 8,874,132
- Georeferencing Method: GPS/GCP

### GIS Analysis

Outputs were imported into QGIS for further analysis.

Terrain products generated from the DSM included:

- Hillshade
- 1 m Contours
- 2 m Contours
- Slope Raster
- Aspect Raster

These products were evaluated to determine which methods most effectively communicated terrain characteristics.

---

## Processing Challenge

The initial processing run failed approximately 13 minutes into reconstruction.

Reviewing the WebODM task logs revealed the following error:

> Child returned 137

Further investigation showed that Docker Desktop was configured with approximately 7.75 GB of available memory despite the workstation containing 16 GB of physical memory.

The failure occurred during mesh generation using Screened Poisson Reconstruction.

### Resolution

The Docker memory allocation was increased to 12 GB and processing was resumed from the Meshing stage rather than restarting the entire project.

The reconstruction completed successfully after approximately five additional minutes.

This experience demonstrated the value of reviewing task logs, understanding processing stages, and using available recovery checkpoints to avoid unnecessary reprocessing.

---

## Terrain Analysis Findings

### Hillshade

Hillshade provided a clear visualization of terrain structure and elevation changes throughout the study area.

The road corridor and surrounding terrain features were immediately recognizable and served as a useful foundation for subsequent analysis.

### Contours

Both 1 m and 2 m contour intervals were evaluated.

The 1 m interval provided the best balance between readability and terrain detail.

The 2 m interval simplified the landscape and obscured some of the more subtle elevation changes visible along the road corridor.

### Slope

Slope analysis proved to be one of the most informative derived products.

The slope raster clearly highlighted:

- Terrain transitions
- Road embankments
- Vegetation boundaries
- Areas of rapid elevation change

Among all terrain derivatives generated during the project, slope provided the clearest representation of the site's physical structure.

### Aspect

Aspect analysis was generated successfully and clearly distinguished the road corridor from surrounding vegetation.

However, because the Digital Surface Model included vegetation and canopy structure, the resulting raster contained many small-scale directional changes. While technically correct, these variations reduced its usefulness for interpreting broader terrain orientation.

The exercise demonstrated the difference between generating a valid analytical product and generating a product that effectively communicates information.

---

## Results

The project successfully produced a complete set of photogrammetry outputs and terrain-analysis products.

Deliverables included:

- Orthophoto
- DSM
- Point Cloud
- 3D Model
- Hillshade
- Contours
- Slope Raster
- Aspect Raster

The workflow also provided practical experience with data management, georeferencing concepts, terrain analysis, and troubleshooting of photogrammetry processing failures.

---

## Lessons Learned

Several important lessons emerged from this project:

- Docker resource allocation can become a critical bottleneck during photogrammetry processing.
- WebODM task logs provide valuable information for diagnosing failures.
- Processing checkpoints can significantly reduce recovery time after errors.
- Ground Control Points introduce additional workflow considerations beyond image-only reconstruction.
- Different terrain products communicate information differently.
- A technically correct output is not always the most useful output for interpretation or presentation.

Perhaps the most important lesson was that successful GIS and photogrammetry work involves not only generating outputs, but also evaluating which products best answer the question being asked.

---

## Future Work

Potential future extensions of this project include:

- Point cloud analysis using CloudCompare.
- Generation of cartographic map layouts.
- Comparison of DSM-derived products with bare-earth terrain models.
- Additional photogrammetry projects using larger or more topographically varied datasets.
- Exploration of drone-derived datasets within game engines and visualization environments.

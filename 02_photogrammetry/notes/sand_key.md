# Sand Key Learning Run

## Dataset Information

- Dataset: Sand Key
- Images: 100
- Dataset Size: ~1.1 GB
- Processing Platform: WebODM running in Docker
- Hardware: Apple Mac Mini (M4, 16 GB RAM)
- CRS: WGS 84 / UTM Zone 17N (EPSG:32617)

## Purpose

This dataset was processed as an introductory photogrammetry and GIS workflow exercise.

Goals:

- Validate WebODM installation.
- Learn the photogrammetry processing pipeline.
- Import outputs into QGIS.
- Generate basic terrain products.
- Establish a repeatable workflow for future projects.

## Processing Results

- Reconstruction completed successfully.
- Processing time: 12 minutes 59 seconds.
- Point cloud generated successfully.
- Orthophoto generated successfully.
- Digital Surface Model (DSM) generated successfully.
- Quality report exported.

## GIS Workflow

Imported orthophoto and DSM into QGIS.

Generated:

- Hillshade raster
- 0.25 m contour lines
- 1.0 m contour lines

## Observations

- Water produced noticeable reconstruction artifacts.
- Reconstruction edges contained increased noise.
- 0.25 m contours revealed subtle terrain variation but amplified reconstruction noise.
- 1.0 m contours showed that the beach surface is largely flat.
- Hillshade provided a clearer visualization of terrain variation than contours for this dataset.

## Lessons Learned

- Successfully deployed WebODM using Docker.
- Learned the relationship between orthophoto, point cloud, DSM, hillshade, and contours.
- Confirmed that CRS information is preserved and automatically recognized by QGIS.
- Demonstrated a complete drone imagery → photogrammetry → GIS workflow.

## Follow-on Work

- Completed a second photogrammetry case study using the Helenenschacht dataset.
- Plan to explore point cloud analysis in QGIS or CloudCompare.
- Plan to produce cartographic layouts and map products.
- Continue expanding the portfolio with additional terrain and vegetation datasets.
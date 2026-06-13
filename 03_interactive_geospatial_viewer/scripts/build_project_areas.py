from pathlib import Path
from typing import Optional

import geopandas as gpd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent

OUTPUT_GEOJSON = PROJECT_ROOT / "data" / "geojson" / "project_areas.geojson"

ARCH_CREEK_BUFFER = (
    REPO_ROOT
    / "01_south_florida_qgis_map"
    / "data_processed"
    / "arch_creek_250m_buffer.gpkg"
)

SAND_KEY_FOOTPRINT = (
    REPO_ROOT
    / "02_photogrammetry"
    / "data"
    / "processed"
    / "sand_key"
    / "sand_key_footprint.gpkg"
)

HELENENSCHACHT_FOOTPRINT = (
    REPO_ROOT
    / "02_photogrammetry"
    / "data"
    / "processed"
    / "helenenschacht"
    / "helenenschacht_footprint.gpkg"
)


def make_area_from_vector(path: Path, project_id: str, name: str, layer: Optional[str] = None) -> dict:
    """Create one project area feature from a vector polygon file."""

    if layer:
        gdf = gpd.read_file(path, layer=layer)
    else:
        gdf = gpd.read_file(path)

    if gdf.crs is None:
        raise ValueError(f"No CRS found for vector file: {path}")

    gdf = gdf.to_crs("EPSG:4326")
    geometry = gdf.geometry.union_all()

    return {
        "project_id": project_id,
        "name": name,
        "geometry": geometry,
    }


def main() -> None:
    """Build project area polygons from prior project outputs."""

    features = [
        make_area_from_vector(
            ARCH_CREEK_BUFFER,
            "arch_creek",
            "Arch Creek Park 250 m Buffer",
            layer="arch_creek_250m_buffer",
        ),
        make_area_from_vector(
            SAND_KEY_FOOTPRINT,
            "sand_key",
            "Sand Key Photogrammetry Footprint",
            layer="sand_key_footprint",
        ),
        make_area_from_vector(
            HELENENSCHACHT_FOOTPRINT,
            "helenenschacht",
            "Helenenschacht Photogrammetry Footprint",
            layer="helenenschacht_footprint",
        ),
    ]

    areas = gpd.GeoDataFrame(features, geometry="geometry", crs="EPSG:4326")

    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    areas.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

    print(f"Saved project areas to: {OUTPUT_GEOJSON}")


if __name__ == "__main__":
    main()
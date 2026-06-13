import ast
import json
import re
from pathlib import Path
from typing import Optional

import folium
import geopandas as gpd
from branca.element import MacroElement, Template


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "web" / "index.html"
SITES_GEOJSON = PROJECT_ROOT / "data" / "geojson" / "project_sites.geojson"
AREAS_GEOJSON = PROJECT_ROOT / "data" / "geojson" / "project_areas.geojson"


def make_link(text: str, url: str) -> str:
    """Return linked text when a URL exists; otherwise return plain text."""

    if url:
        return f'<a href="{url}" target="_blank">{text}</a>'

    return text


def make_preview_carousel(
    preview_images: list[dict],
    properties: dict,
    popup_id: str,
) -> tuple[str, str]:
    """Build carousel and expanded-preview HTML for popup images."""

    if not preview_images:
        return "", ""

    carousel_id = f"{popup_id}-carousel"
    counter_id = f"{popup_id}-carousel-counter"
    details_id = f"{popup_id}-details"
    expanded_id = f"{popup_id}-expanded"
    expanded_img_id = f"{popup_id}-expanded-img"

    slides_html = ""

    for index, image in enumerate(preview_images):
        display = "block" if index == 0 else "none"
        image_alt = image.get("alt", properties["name"])

        slides_html += f'''
        <img
            data-carousel-slide
            src="{image["src"]}"
            alt="{image_alt}"
            onclick="document.getElementById('{carousel_id}').style.display='none'; document.getElementById('{details_id}').style.display='none'; document.getElementById('{expanded_img_id}').src=this.src; document.getElementById('{expanded_img_id}').alt=this.alt; document.getElementById('{expanded_id}').style.display='block';"
            style="display: {display}; width: 100%; height: 220px; object-fit: contain; border-radius: 4px; background: #f4f4f4; cursor: pointer;"
        >
        '''

    controls_html = ""

    if len(preview_images) > 1:
        previous_script = (
            f"const carousel=document.getElementById('{carousel_id}');"
            "const slides=carousel.querySelectorAll('[data-carousel-slide]');"
            "let index=parseInt(carousel.dataset.index || '0');"
            "slides[index].style.display='none';"
            "index=(index-1+slides.length)%slides.length;"
            "slides[index].style.display='block';"
            "carousel.dataset.index=index;"
            f"document.getElementById('{counter_id}').textContent=(index+1)+' / '+slides.length;"
            "return false;"
        )
        next_script = (
            f"const carousel=document.getElementById('{carousel_id}');"
            "const slides=carousel.querySelectorAll('[data-carousel-slide]');"
            "let index=parseInt(carousel.dataset.index || '0');"
            "slides[index].style.display='none';"
            "index=(index+1)%slides.length;"
            "slides[index].style.display='block';"
            "carousel.dataset.index=index;"
            f"document.getElementById('{counter_id}').textContent=(index+1)+' / '+slides.length;"
            "return false;"
        )

        controls_html = f'''
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 6px;">
            <button
                type="button"
                onclick="{previous_script}"
                style="padding: 4px 8px; cursor: pointer;"
            >
                ← Previous
            </button>
            <span id="{counter_id}" style="font-size: 12px;">
                1 / {len(preview_images)}
            </span>
            <button
                type="button"
                onclick="{next_script}"
                style="padding: 4px 8px; cursor: pointer;"
            >
                Next →
            </button>
        </div>
        '''

    carousel_html = f'''
    <div id="{carousel_id}" data-index="0" style="margin: 8px 0;">
        {slides_html}
        {controls_html}
    </div>
    '''

    expanded_html = f'''
    <div id="{expanded_id}" style="display: none; margin: 8px 0;">
        <button
            type="button"
            onclick="document.getElementById('{expanded_id}').style.display='none'; document.getElementById('{carousel_id}').style.display='block'; document.getElementById('{details_id}').style.display='block';"
            style="margin-bottom: 6px; padding: 4px 8px; cursor: pointer;"
        >
            ← Back
        </button>
        <img
            id="{expanded_img_id}"
            src=""
            alt="Expanded preview"
            style="width: 100%; max-height: 420px; object-fit: contain; border-radius: 4px; background: #f4f4f4;"
        >
    </div>
    '''

    return carousel_html, expanded_html


def make_popup(
    properties: dict,
    project_bounds: Optional[list[list[float]]] = None,
    default_bounds: Optional[list[list[float]]] = None,
    map_name: str = "",
) -> str:
    """Build the marker popup from one GeoJSON feature's properties."""

    inputs = make_link(properties["inputs"], properties.get("input_url", ""))

    preview_images = properties.get("preview_images", [])

    if isinstance(preview_images, str):
        try:
            preview_images = ast.literal_eval(preview_images)
        except (SyntaxError, ValueError):
            preview_images = []

    if not preview_images and properties.get("preview_image", ""):
        preview_images = [
            {
                "src": properties["preview_image"],
                "alt": properties.get("preview_alt", properties["name"]),
            }
        ]

    popup_id = re.sub(r"[^a-z0-9]+", "-", properties["name"].lower()).strip("-")
    image_html, expanded_html = make_preview_carousel(
        preview_images,
        properties,
        popup_id,
    )

    repo = make_link(properties["repo_path"], properties.get("repo_url", ""))

    map_buttons_html = ""
    if project_bounds and default_bounds and map_name:
        project_bounds_json = json.dumps(project_bounds)
        default_bounds_json = json.dumps(default_bounds)
        map_buttons_html = f'''
            <div style="display: flex; gap: 6px; margin-top: 8px;">
                <button
                    type="button"
                    onclick="{map_name}.fitBounds({project_bounds_json}, {{padding: [30, 30]}}); return false;"
                    style="padding: 4px 8px; cursor: pointer;"
                >
                    Zoom to project area
                </button>
                <button
                    type="button"
                    onclick="{map_name}.fitBounds({default_bounds_json}, {{padding: [30, 30]}}); return false;"
                    style="padding: 4px 8px; cursor: pointer;"
                >
                    Reset map view
                </button>
            </div>
        '''

    return f"""
    <div style="width: 500px;">
        <h3 style="margin-bottom: 4px;">{properties["name"]}</h3>
        {image_html}
        {expanded_html}
        <div id="{popup_id}-details">
            <p style="margin: 2px 0;"><strong>{properties["project"]}</strong></p>
            <p style="margin: 2px 0;"><strong>Tools:</strong> {properties["tools"]}</p>
            <p style="margin: 2px 0;"><strong>Inputs:</strong> {inputs}</p>
            <p style="margin: 2px 0;"><strong>Outputs:</strong> {properties["outputs"]}</p>
            <p style="margin: 2px 0;"><strong>Repo:</strong> {repo}</p>
            {map_buttons_html}
        </div>
    </div>
    """


def load_sites() -> gpd.GeoDataFrame:
    """Load the project site locations from a GeoJSON file."""

    sites = gpd.read_file(SITES_GEOJSON)
    return sites


def load_areas() -> gpd.GeoDataFrame:
    """Load project area polygons when the project areas GeoJSON exists."""

    if not AREAS_GEOJSON.exists():
        return gpd.GeoDataFrame(columns=["project_id", "name", "geometry"], crs="EPSG:4326")

    areas = gpd.read_file(AREAS_GEOJSON)
    return areas


def add_project_areas(
    m: folium.Map,
    areas: gpd.GeoDataFrame,
) -> Optional[folium.GeoJson]:
    """Draw project area polygons on the map and return the layer."""

    if areas.empty:
        return None

    area_layer = folium.GeoJson(
        areas,
        name="Project areas",
        style_function=lambda feature: {
            "fillColor": "#3388ff",
            "color": "#3388ff",
            "weight": 2,
            "fillOpacity": 0.12,
        },
    )

    area_layer.add_to(m)
    return area_layer


# --- Inserted function: add_project_area_interactions ---
def add_project_area_interactions(
    m: folium.Map,
    area_layer: folium.GeoJson,
) -> None:
    """Manage polygon hover and persistent popup highlighting with shared state."""

    interaction_handler = MacroElement()
    interaction_handler._template = Template(
        """
        {% macro script(this, kwargs) %}
        window.{{ this.area_layer_name }}_active_project_id = null;

        window.{{ this.area_layer_name }}_highlight_project = function (projectId) {
            {{ this.area_layer_name }}.eachLayer(function (layer) {
                if (
                    layer.feature &&
                    layer.feature.properties.project_id === projectId
                ) {
                    layer.setStyle({
                        fillColor: '#B86B2B',
                        color: '#B86B2B',
                        weight: 3,
                        fillOpacity: 0.28
                    });
                }
            });
        };

        window.{{ this.area_layer_name }}_reset_project = function (projectId) {
            {{ this.area_layer_name }}.eachLayer(function (layer) {
                if (
                    layer.feature &&
                    layer.feature.properties.project_id === projectId
                ) {
                    {{ this.area_layer_name }}.resetStyle(layer);
                }
            });
        };

        {{ this.area_layer_name }}.eachLayer(function (layer) {
            if (!layer.feature) {
                return;
            }

            const projectId = layer.feature.properties.project_id;

            layer.on('mouseover', function () {
                window.{{ this.area_layer_name }}_highlight_project(projectId);
            });

            layer.on('mouseout', function () {
                if (
                    window.{{ this.area_layer_name }}_active_project_id !== projectId
                ) {
                    window.{{ this.area_layer_name }}_reset_project(projectId);
                }
            });
        });

        {{ this.map_name }}.on('zoomend moveend', function () {
            const activeProjectId =
                window.{{ this.area_layer_name }}_active_project_id;

            if (activeProjectId) {
                window.setTimeout(function () {
                    window.{{ this.area_layer_name }}_highlight_project(
                        activeProjectId
                    );
                }, 0);
            }
        });
        {% endmacro %}
        """
    )
    interaction_handler.area_layer_name = area_layer.get_name()
    interaction_handler.map_name = m.get_name()
    interaction_handler.add_to(m)


def add_marker_polygon_hover(
    m: folium.Map,
    marker: folium.Marker,
    area_layer: folium.GeoJson,
    project_id: str,
) -> None:
    """Connect marker hover and popup state to its project polygon."""

    hover_handler = MacroElement()
    hover_handler._template = Template(
        """
        {% macro script(this, kwargs) %}
        {{ this.marker_name }}.on('mouseover', function () {
            window.{{ this.area_layer_name }}_highlight_project(
                {{ this.project_id | tojson }}
            );
        });

        {{ this.marker_name }}.on('mouseout', function () {
            if (
                window.{{ this.area_layer_name }}_active_project_id !==
                {{ this.project_id | tojson }}
            ) {
                window.{{ this.area_layer_name }}_reset_project(
                    {{ this.project_id | tojson }}
                );
            }
        });

        {{ this.marker_name }}.on('popupopen', function () {
            window.{{ this.area_layer_name }}_active_project_id =
                {{ this.project_id | tojson }};

            window.{{ this.area_layer_name }}_highlight_project(
                {{ this.project_id | tojson }}
            );

            window.setTimeout(function () {
                const popup = {{ this.marker_name }}.getPopup();
                const popupElement = popup && popup.getElement();
                const mapElement = {{ this.map_name }}.getContainer();

                if (!popupElement || !mapElement) {
                    return;
                }

                popupElement.querySelectorAll('img').forEach(function (image) {
                    image.style.transition = 'none';
                    image.style.opacity = '1';
                });

                const popupRect = popupElement.getBoundingClientRect();
                const mapRect = mapElement.getBoundingClientRect();
                const insetX = mapRect.width * 0.10;
                const insetY = mapRect.height * 0.10;
                const safeLeft = mapRect.left + insetX;
                const safeRight = mapRect.right - insetX;
                const safeTop = mapRect.top + insetY;
                const safeBottom = mapRect.bottom - insetY;

                let panX = 0;
                let panY = 0;

                if (popupRect.left < safeLeft) {
                    panX = popupRect.left - safeLeft;
                } else if (popupRect.right > safeRight) {
                    panX = popupRect.right - safeRight;
                }

                if (popupRect.top < safeTop) {
                    panY = popupRect.top - safeTop;
                } else if (popupRect.bottom > safeBottom) {
                    panY = popupRect.bottom - safeBottom;
                }

                if (panX !== 0 || panY !== 0) {
                    {{ this.map_name }}.panBy([panX, panY]);
                }
            }, 50);
        });

        {{ this.marker_name }}.on('popupclose', function () {
            window.{{ this.area_layer_name }}_active_project_id = null;

            window.{{ this.area_layer_name }}_reset_project(
                {{ this.project_id | tojson }}
            );

            const popup = {{ this.marker_name }}.getPopup();
            const popupElement = popup && popup.getElement();

            if (popupElement) {
                popupElement.querySelectorAll('img').forEach(function (image) {
                    image.style.transition = 'opacity 50ms ease';
                    image.style.opacity = '0';
                });

                window.setTimeout(function () {
                    const expandedView = popupElement.querySelector(
                        '[id$="-expanded"]'
                    );
                    const carousel = popupElement.querySelector(
                        '[id$="-carousel"]'
                    );
                    const details = popupElement.querySelector(
                        '[id$="-details"]'
                    );

                    if (expandedView) {
                        expandedView.style.display = 'none';
                    }

                    if (carousel) {
                        carousel.style.display = 'block';
                        carousel.dataset.index = '0';

                        const slides = carousel.querySelectorAll(
                            '[data-carousel-slide]'
                        );

                        slides.forEach(function (slide, index) {
                            slide.style.display = index === 0 ? 'block' : 'none';
                        });

                        const counter = carousel.querySelector(
                            '[id$="-carousel-counter"]'
                        );

                        if (counter && slides.length > 0) {
                            counter.textContent = '1 / ' + slides.length;
                        }
                    }

                    if (details) {
                        details.style.display = 'block';
                    }
                }, 100);
            }
        });
        {% endmacro %}
        """
    )
    hover_handler.marker_name = marker.get_name()
    hover_handler.area_layer_name = area_layer.get_name()
    hover_handler.map_name = m.get_name()
    hover_handler.project_id = project_id
    hover_handler.add_to(m)


def get_project_bounds(
    project_id: str,
    areas: gpd.GeoDataFrame,
) -> Optional[list[list[float]]]:
    """Return Leaflet-style bounds for a matching project area."""

    if not project_id or areas.empty:
        return None

    matching_areas = areas[areas["project_id"] == project_id]

    if matching_areas.empty:
        return None

    minx, miny, maxx, maxy = matching_areas.total_bounds
    return [[miny, minx], [maxy, maxx]]


def get_default_bounds(
    areas: gpd.GeoDataFrame,
) -> Optional[list[list[float]]]:
    """Return Leaflet-style bounds containing all project areas."""

    if areas.empty:
        return None

    minx, miny, maxx, maxy = areas.total_bounds
    return [[miny, minx], [maxy, maxx]]


def get_marker_location(site: gpd.GeoSeries, areas: gpd.GeoDataFrame) -> list[float]:
    """Return marker coordinates from a matching area centroid, falling back to the site point."""

    project_id = site.get("project_id", "")

    if project_id and not areas.empty:
        matching_areas = areas[areas["project_id"] == project_id]

        if not matching_areas.empty:
            area_geometry = matching_areas.iloc[0].geometry
            centroid = area_geometry.centroid
            return [centroid.y, centroid.x]

    return [site.geometry.y, site.geometry.x]


def build_map() -> folium.Map:
    """Create the interactive Folium map from GeoJSON site data."""

    sites = load_sites()
    areas = load_areas()

    m = folium.Map(
        location=[27.5, -70.0],
        zoom_start=4,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    m.get_root().header.add_child(
        folium.Element(
            """
            <style>
                .leaflet-interactive:focus {
                    outline: none;
                }
            </style>
            """
        )
    )

    folium.TileLayer("CartoDB positron", name="Light basemap").add_to(m)
    folium.TileLayer("CartoDB dark_matter", name="Dark basemap").add_to(m)

    area_layer = add_project_areas(m, areas)

    if area_layer:
        add_project_area_interactions(m, area_layer)

    default_bounds = get_default_bounds(areas)

    if default_bounds:
        m.fit_bounds(default_bounds, padding=(30, 30))

    for _, site in sites.iterrows():
        properties = site.drop(labels="geometry").to_dict()

        marker_location = get_marker_location(site, areas)
        project_bounds = get_project_bounds(properties.get("project_id", ""), areas)

        marker = folium.Marker(
            location=marker_location,
            popup=folium.Popup(
                make_popup(
                    properties,
                    project_bounds,
                    default_bounds,
                    m.get_name(),
                ),
                max_width=540,
                auto_pan=False,
            ),
            tooltip=f'{properties["project"]}: {properties["name"]}',
        )
        marker.add_to(m)

        project_id = properties.get("project_id", "")
        if area_layer and project_id:
            add_marker_polygon_hover(
                m,
                marker,
                area_layer,
                project_id,
            )

    folium.LayerControl().add_to(m)

    return m


def main() -> None:
    """Build the map and save it as an HTML file."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    m = build_map()
    m.save(OUTPUT_PATH)

    print(f"Saved map to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
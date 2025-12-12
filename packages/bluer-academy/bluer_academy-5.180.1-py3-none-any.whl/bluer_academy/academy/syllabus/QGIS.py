from bluer_objects.README.consts import assets_url

from bluer_academy.academy.syllabus.consts import bluer_geo_blob
from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "QGIS",
    [
        "basic QGIS",
        "styling in QGIS",
        "templates in QGIS",
        "generating styled QGIS projects with algo",
        f"[@QGIS]({bluer_geo_blob}/QGIS)",
    ],
    duration=3,
    requires="geospatial",
    items={
        assets_url(
            "blue-geo/QGIS.png",
        ): f"{bluer_geo_blob}/QGIS"
    },
)

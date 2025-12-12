from bluer_objects.README.consts import assets_url

from bluer_academy.academy.syllabus.consts import bluer_geo_blob, bluer_geo_tree
from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "geospatial-sources",
    [
        f"[copernicus]({bluer_geo_blob}/catalog/copernicus): sentinels 1 & 2",
        f"[firms]({bluer_geo_blob}/catalog/firms): fire information",
        f"[global power plant]({bluer_geo_blob}/objects/md/global_power_plant_database.md): open source database of power plants around the world",
        f"[maxar open data]({bluer_geo_blob}/catalog/maxar_open_data): disaster management",
        f"[ukraine damage map]({bluer_geo_blob}/catalog/ukraine_timemap)",
    ],
    duration=6,
    requires="geospatial,QGIS",
    items={
        assets_url(
            suffix="blue-geo/Maxar-Open-Datacube.png"
        ): f"{bluer_geo_tree}/catalog/maxar_open_data"
    },
    capstone=True,
)

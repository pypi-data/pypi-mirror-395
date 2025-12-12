from bluer_objects.README.consts import assets_url

from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import vanwatch_root

topic = Topic(
    "city-watching",
    [
        f"[watching a city through traffic cameras]({vanwatch_root})",
    ],
    duration=3,
    requires="machine-vision,geospatial",
    items={
        assets_url(suffix="vanwatch/2024-01-06-20-39-46-73614-QGIS.gif"): vanwatch_root
    },
    capstone=True,
)

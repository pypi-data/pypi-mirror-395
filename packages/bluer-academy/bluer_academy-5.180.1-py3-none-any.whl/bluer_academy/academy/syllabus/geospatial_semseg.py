from bluer_objects.README.consts import assets_url

from bluer_academy.academy.syllabus.consts import palisades_blob
from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "geospatial-semseg",
    [
        f"[fire damage assessment in LA]({palisades_blob}/docs/damage-analytics.md)",
    ],
    duration=6,
    requires="geospatial,geospatial-sources,machine-vision",
    items={
        assets_url(
            suffix=f"palisades/palisades-analytics-2025-01-28-09-27-20-itglyy/{filename}"
        ): f"{palisades_blob}/docs/damage-analytics.md"
        for filename in [
            "thumbnail-039462-378510-palisades-analytics-2025-01-28-09-27-20-itglyy.gif",
            "Palisades.png",
        ]
    },
    cols=2,
    capstone=True,
)

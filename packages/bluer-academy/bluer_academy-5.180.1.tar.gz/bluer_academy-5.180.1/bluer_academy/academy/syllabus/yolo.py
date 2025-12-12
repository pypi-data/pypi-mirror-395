from bluer_objects.README.consts import assets_url


from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_ugv_blob

topic = Topic(
    "yolo",
    [
        f"[Yolo on a UGV]({bluer_ugv_blob}/docs/validations/village-3.md)",
    ],
    duration=3,
    requires="machine-vision,ugv",
    items={
        assets_url(
            "{object_name}/{object_name}.gif".format(
                object_name="swallow-debug-2025-09-25-13-16-59-rnm7jd"
            )
        ): f"{bluer_ugv_blob}/docs/validations/village-3.md"
    },
    capstone=True,
)

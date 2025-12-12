from bluer_objects.README.consts import assets_url

from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_algo_blob

topic = Topic(
    "machine-vision",
    [
        "opencv",
        "pytorch",
        f"[image classification]({bluer_algo_blob}/docs/image_classifier)",
        f"[target tracking]({bluer_algo_blob}/docs/tracker)",
        f"[yolo]({bluer_algo_blob}/docs/yolo)",
        "[semantic segmentation](https://github.com/kamangir/roofai)",
    ],
    duration=12,
    requires="python,bash",
    items={
        assets_url(
            "roofAI/predict-00009.png"
        ): "https://github.com/kamangir/roofai/tree/main/roofai/semseg"
    },
)

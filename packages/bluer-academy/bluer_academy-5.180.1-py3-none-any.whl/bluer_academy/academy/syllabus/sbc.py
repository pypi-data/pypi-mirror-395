from bluer_objects.README.consts import assets_url

from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_sbc_blob

topic = Topic(
    "sbc",
    [
        "single board computers",
        "raspberry pi",
        "[terraforming](https://github.com/kamangir/bluer-sbc)",
    ],
    duration=3,
    requires="linux,python,bash",
    items={
        assets_url(
            suffix="swallow/design/head-v1/01.jpg?raw=true",
            volume=2,
        ): f"{bluer_sbc_blob}/docs/swallow-head",
        assets_url(
            suffix="swallow/design/v5/01.jpg?raw=true",
            volume=2,
        ): f"{bluer_sbc_blob}/docs/swallow",
        "https://github.com/kamangir/blue-bracket/raw/main/images/chenar-grove-1.jpg": "https://github.com/kamangir/blue-bracket",
    },
)

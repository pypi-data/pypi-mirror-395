from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_ai_root

topic = Topic(
    "linux",
    [
        f"[setting up Linux on your machine]({bluer_ai_root})",
    ],
    duration=3,
    cost="a working mac, ubuntu (preferred) or windows machine",
    requires="math",
)

from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_ai_tree

topic = Topic(
    "pypi",
    [
        f"[publishing code on pypi]({bluer_ai_tree}/.abcli/plugins/pypi)",
    ],
    duration=3,
    requires="linux,python,github,bash",
)

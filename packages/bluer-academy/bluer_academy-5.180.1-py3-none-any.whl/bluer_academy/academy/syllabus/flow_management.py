from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "flow-management",
    [
        "[flow management basics](https://github.com/kamangir/bluer-flow)",
        "flow management on arvancloud",
    ],
    duration=2,
    requires="linux,bash,python,cloud",
    items={
        "https://github.com/kamangir/assets/raw/main/bluer_flow-localflow-hourglass/workflow.gif?raw=true": "https://github.com/kamangir/bluer-flow",
    },
)

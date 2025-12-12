from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "bash",
    [
        "basics of bash",
        "variables in bash",
        "functions in bash",
        "command substitution",
    ],
    duration=3,
    requires="linux,python,github",
)

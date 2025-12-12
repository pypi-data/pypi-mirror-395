from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "journal",
    [
        "[a private journal on github](https://github.com/kamangir/bluer-journal)",
    ],
    duration=3,
    requires="python,bash,github",
    items={
        "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true": "https://github.com/kamangir/bluer-journal",
    },
    capstone=True,
)

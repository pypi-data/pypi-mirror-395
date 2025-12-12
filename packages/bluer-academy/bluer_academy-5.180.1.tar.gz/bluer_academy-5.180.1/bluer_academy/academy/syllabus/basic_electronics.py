from bluer_objects.README.consts import assets_url

from bluer_academy.academy.classes.topic import Topic
from bluer_academy.academy.syllabus.consts import bluer_sbc_blob

topic = Topic(
    "basic-electronics",
    [
        "basic electronics",
        "[what is a PCB?](https://learn.sparkfun.com/tutorials/pcb-basics/all)",
        "power management",
        "voltage conversion",
        "soldiering, working with electronic parts",
        "sourcing electronic parts",
        "motor drivers and pwm",
        "wireless control",
    ],
    duration=6,
    items={
        assets_url(
            suffix="battery-bus/20251007_221902.jpg",
            volume=2,
        ): f"{bluer_sbc_blob}/docs/battery_bus",
        assets_url(
            suffix="adapter-bus/20251017_222911.jpg",
            volume=2,
        ): f"{bluer_sbc_blob}/docs/adapter-bus.md",
        assets_url(
            suffix="ultrasonic-sensor-tester/00.jpg?raw=true",
            volume=2,
        ): f"{bluer_sbc_blob}/docs/ultrasonic-sensor-tester.md",
    },
)

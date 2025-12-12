from bluer_academy.academy.syllabus.consts import bluer_options_blob
from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "testing",
    [
        f"[pylint]({bluer_options_blob}/.bash/pylint.sh)",
        f"[pytest]({bluer_options_blob}/.bash/pytest.sh)",
        f"[bashtest]({bluer_options_blob}/.bash/test.sh)",
    ],
    duration=6,
    requires="github,python,bash",
)

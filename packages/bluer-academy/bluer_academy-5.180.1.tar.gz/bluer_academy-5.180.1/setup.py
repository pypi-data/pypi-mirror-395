from blueness.pypi import setup

from bluer_academy import NAME, VERSION, DESCRIPTION, REPO_NAME

setup(
    filename=__file__,
    repo_name=REPO_NAME,
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[
        NAME,
        f"{NAME}.academy",
        f"{NAME}.academy.classes",
        f"{NAME}.academy.syllabus",
        f"{NAME}.ai4k",
        f"{NAME}.help",
    ],
    include_package_data=True,
    package_data={
        NAME: [
            ".abcli/**/*.sh",
        ],
    },
)

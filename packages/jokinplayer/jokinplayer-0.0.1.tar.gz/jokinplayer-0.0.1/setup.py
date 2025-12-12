import setuptools
from pathlib import Path

long_descrip = Path("README.md").read_text()

setuptools.setup(
    name= "jokinplayer",
    version="0.0.1",
    long_description = long_descrip,
    packages=setuptools.find_packages(
        exclude=["mocks","tests"]
    )
)
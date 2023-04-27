"""Install packages as defined in this file into the Python environment."""

from setuptools import setup, find_packages

# The version of this tool is based on the following steps:

# https://packaging.python.org/guides/single-sourcing-package-version/
from pathlib import Path

this_directory = Path(__file__).parent

long_description = (this_directory / "README.md").read_text()
VERSION = {}

with open("./swiftshadow/__init__.py") as fp:
    # pylint: disable=W0122

    exec(fp.read(), VERSION)

setup(
    name="swiftshadow",
    author="Sachin Sankar",
    author_email="mail.sachinsankar@gmail.com",
    url="https://github.com/sachin-sankar/swiftshadow",
    description="Free IP Proxy rotator for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION.get("__version__", "0.2.0"),
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
    ],
)

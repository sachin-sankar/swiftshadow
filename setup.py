"""Install packages as defined in this file into the Python environment."""

from setuptools import setup, find_packages

# The version of this tool is based on the following steps:

# https://packaging.python.org/guides/single-sourcing-package-version/

VERSION = {}

with open("./swiftshadow/__init__.py") as fp:
    # pylint: disable=W0122

    exec(fp.read(), VERSION)

setup(
    name="swiftshadow",
    author="Sachin Sankar",
    author_email="mail.sachinsankar@gmail.com",
    url="https://github.com/Chicken1Geek/swiftshadow",
    description="Free IP Proxy rotator for python",
    long_description="Swiftshadow is a proxy rotator that sources proxies for free and provides elegant pythonic API to manage proxies. Build for speed and performance in mind.",
    version=VERSION.get("__version__", "0.0.0"),
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
    ],
)

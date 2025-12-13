#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages, Command

if sys.version_info < (3, 8):
    raise NotImplementedError("""This tool does not support Python versions older than 3.6""")


version_file = os.path.abspath(os.path.join("unknowncli", "VERSION"))


def get_version():
    with open(version_file) as f:
        return f.readlines()[0].strip()


class BumpCommand(Command):
    description = "Version bump"
    user_options = [("which=", None, "Specify which part of the version to bump")]

    def initialize_options(self):
        self.which = None

    def finalize_options(self):
        assert self.which in (None, "major", "minor", "patch"), "Invalid bump pragma"

    def run(self):
        bump_version(self.which)


def bump_version(which):
    major, minor, patch = (0, 1, 0)
    old_version = get_version()
    major, minor, patch = old_version.split(".")

    if which == "major":
        major = int(major) + 1
        minor = 0
        patch = 0
    elif which == "minor":
        minor = int(minor) + 1
        patch = 0
    else:
        patch = int(patch.split("-")[0]) + 1

    new_version = "%s.%s.%s" % (major, minor, patch)

    with open(version_file, "w") as f:
        f.write(new_version)
    print(f"Version has been bumped from {old_version} to {new_version}")


with open("README.md", "r") as fh:
    long_description = fh.read()

version = get_version()

setup(
    name="unknown_cli",
    python_requires=">=3.6",
    version=version,
    license="MIT",
    author="",
    author_email="",
    description="Unknown Commandline Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(exclude=["tests"]),
    package_data={"": ["VERSION", "data/.p4ignore.txt"]},
    install_requires=[
        "typer",
        "click",
        "requests",
        "boto3",
        "psutil",
        "jsonpath-rw",
        "pyyaml",
        "pyjwt",
        "tabulate",
        "colorama",
        "shellingham",
        "boto3",
        "loguru",
        "P4Python",
        "rich",
        "pyuac",
        "pywin32"
    ],
    extras_require={},
    include_package_data=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    test_suite="tests",
    cmdclass={"bump": BumpCommand},
    entry_points={"console_scripts": ["unknown = unknowncli.__main__:app", "unk = unknowncli.__main__:app"]},
)

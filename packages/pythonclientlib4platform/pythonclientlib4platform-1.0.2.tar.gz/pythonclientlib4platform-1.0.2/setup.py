#!/usr/bin/env python

from os import path, walk
import sys
from setuptools import setup, find_packages

NAME = "pythonclientlib4platform"
VERSION = "1.0.2"

DESCRIPTION = "Python Implementation of the Platform utilities"
LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.md')).read()

LICENSE = "Apache v2.0"

KEYWORDS = (
    'Platform client services',
)

PACKAGES = find_packages()

REQUIRED_PACKAGES = ["paho-mqtt", "six", "requests"]

NAMESPACE_PACKAGES = ["lib4platform"]


if __name__ == '__main__':

    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        packages=PACKAGES,
        url="",
        install_requires=REQUIRED_PACKAGES,
        keywords=KEYWORDS,
        namespace_packages=NAMESPACE_PACKAGES,
        include_package_data=True,
        zip_safe=False,
    )

#!/usr/bin/env python
# ----------------------------------------------------------------------- #
# Copyright 2017, Gregor von Laszewski, Indiana University                #
#                                                                         #
# Licensed under the Apache License, Version 2.0 (the "License"); you may #
# not use this file except in compliance with the License. You may obtain #
# a copy of the License at                                                #
#                                                                         #
# http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
# See the License for the specific language governing permissions and     #
# limitations under the License.                                          #
# ------------------------------------------------------------------------#
"""
Cloudmesh CMD5 setup.
"""
import io
import sys
from setuptools import find_packages, setup
import os

def check_python():
    if not sys.version_info.major == 3 and \
        sys.version_info.minor == 6:
        print("This is an experimental version for 3.6, please upgrade if possible")

        print("You are using Python {}.{}."
              .format(sys.version_info.major,
                      sys.version_info.minor))


        sys.exit(1)
    elif not sys.version_info.major == 3 and \
        sys.version_info.minor >= 7:
        print("Python 3.7 or higher is required.")

        print("You are using Python {}.{}."
              .format(sys.version_info.major,
                      sys.version_info.minor))


check_python()

def readfile(filename):
    """
    Read a file
    :param filename: name of the file
    :return: returns the content of the file as string
    """
    with io.open(filename, encoding="utf-8") as stream:
        return stream.read()

requiers = """
pyyaml
docopt
requests
md_toc
""".splitlines()

requiers_cloudmesh = """
cloudmesh-common
""".splitlines()

if  "TESTING" not in os.environ:
    requiers = requiers + requiers_cloudmesh

version = readfile("VERSION").strip()

with open('README.md') as f:
    long_description = f.read()


NAME = "cloudmesh-cmd5"
DESCRIPTION = "A dynamic extensible CMD based command shell"
AUTHOR = "Gregor von Laszewski"
AUTHOR_EMAIL = "laszewski@gmail.com"
URL = "https://github.com/cloudmesh/cloudmesh-cmd5"

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    license="Apache 2.0",
    url=URL,
    packages=find_packages(
        exclude=("tests",
                 "deprecated",
                 "propose",
                 "examples",
                 "conda")),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Environment :: Plugins",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    install_requires=requiers,
    tests_require=[
        "flake8",
        "coverage",
    ],
    zip_safe=False,
    namespace_packages=['cloudmesh'],
    entry_points={
        'console_scripts': [
            'cms = cloudmesh.shell.shell:main',
        ],
    }
)

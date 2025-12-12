#!/usr/bin/env python
# This file is part of Ansible Lookup SysPass
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import codecs
import os.path

try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "This module could not be installed, probably because"
        " setuptools is not installed on this computer."
        "\nInstall ez_setup ([sudo] pip install ez_setup) and try again."
    )


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pre_version = get_version("ansible/plugins/lookup/syspass.py")

if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    if os.environ.get("CI_JOB_ID"):
        version = os.environ["CI_JOB_ID"]
    else:
        version = pre_version

with open("README.md") as f:
    long_description = f.read()

setup(
    name="digdeo-syspass-ansible-lookup",
    version=version,
    description="DigDeo Syspass Ansible Lookup",
    author="DigDeo",
    author_email="pierre-henry.muller@digdeo.fr",
    url="https://git.digdeo.fr/digdeo-system/digdeo-syspass-ansible-lookup",
    license="GPL-3.0-or-later",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    keywords="DigDeo Syspass Ansible Lookup",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    setup_requires=[
        "green",
        "wheel"
    ],
    install_requires=[
        "digdeo-syspass-client",
        "six",
        "colorama"
    ],
    py_modules=["ansible/plugins/lookup/syspass"],
)

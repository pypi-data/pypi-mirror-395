"""eea.dexterity.indicators Installer"""

import os
from os.path import join
from setuptools import setup, find_packages

NAME = "eea.dexterity.indicators"
PATH = NAME.split(".") + ["version.txt"]
with open(join(*PATH), "r", encoding="utf-8") as version_file:
    VERSION = version_file.read().strip()

with open("README.rst", "r", encoding="utf-8") as readme_file:
    with open(
        os.path.join("docs", "HISTORY.txt"), "r", encoding="utf-8"
    ) as history_file:
        LONG_DESCRIPTION = readme_file.read() + "\n" + history_file.read()

setup(
    name=NAME,
    version=VERSION,
    description="Dexterity Indicators",
    long_description_content_type="text/x-rst",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="EEA Add-ons Plone Zope",
    author="European Environment Agency: IDM2 A-Team",
    author_email="eea-edw-a-team-alerts@googlegroups.com",
    url="https://github.com/eea/eea.dexterity.indicators",
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["eea", "eea.dexterity"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.app.dexterity",
        "eea.api.layout",
        "eea.schema.slate",
        "eea.dexterity.themes",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

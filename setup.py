# This file is part of visier-sqllike-shell.
#
# visier-sqllike-shell is free software: you can redistribute it and/or modify
# it under the terms of the Apache License, Version 2.0 (the "License").
#
# visier-sqllike-shell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License, Version 2.0 for more details.
#
# You should have received a copy of the Apache License, Version 2.0
# along with visier-sqllike-shell. If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""
Visier SQL-like Read Eval Print Loop (REPL) Shell.
"""

import setuptools
from src import repl

VERSION = repl.__version__
REQUIRES = [
    "visier-connector",
]

print(setuptools.find_packages(include=["src", "src.*"]))
setuptools.setup(
    name="visier-sqllike-shell",
    version=VERSION,
    author="Visier Research & Development",
    author_email="info@visier.com",
    description="""Sample Command line utitlity for executing SQL-like
    queries against the Visier platform""",
    packages=setuptools.find_packages(include=["src", "src.*"]),
    include_package_data=True,
    install_requires=REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "vsql-shell=src.main:main",
        ],
    },
    python_requires=">=3.7",
)

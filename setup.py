#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages

with io.open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

with io.open("batteryhorse/version.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setup(
    name="BatteryHorse",
    version=version,
    packages=find_packages(),
    author="Chris Stranex",
    author_email="chris@stranex.com",
    description="Encode and decode binary data to English sentences",
    # include_package_data=True,
    package_data={
        "batteryhorse": ["nltk_data/corpora/wordnet/*"],
    },
    entry_points={
        "console_scripts": [
            "batteryhorse = batteryhorse:main"
        ],
    },
    install_requires=["nltk"],
    python_requires=">=3.4",
    license="Apache License, Version 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cstranex/batteryhorse",
    project_urls={
        "Source Code": "https://github.com/cstranex/batteryhorse",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

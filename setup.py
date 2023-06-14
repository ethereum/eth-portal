#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    "test": [
        "pytest>=7.0.0",
        "pytest-xdist>=2.4.0",
    ],
    "lint": [
        "black>=22.1,<23",
        "flake8==3.7.9",
        "isort>=5.10.1,<6",
        "mypy==0.770",
        "pydocstyle>=5.0.0,<6",
    ],
    "docs": [
        "sphinx>=6.0.0",
        "sphinx_rtd_theme>=1.0.0",
        "towncrier>=21,<22",
        "Jinja2<3",
        "MarkupSafe<2",
    ],
    "dev": [
        "bumpversion>=0.5.3",
        "pytest-watch>=4.1.0",
        "tox>=4.0.0",
        "build>=0.9.0",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]
    + extras_require["lint"]
    + extras_require["docs"]
)


with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="eth-portal",
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version="0.2.1",
    description="""eth-portal: A collection of utilities related to Ethereum's Portal Network""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Ethereum Foundation",
    author_email="snakecharmers@ethereum.org",
    url="https://github.com/ethereum/eth-portal",
    include_package_data=True,
    install_requires=[
        "web3>=5.30.0,<6",
        "py-evm==0.5.0-alpha.3",
        "ssz>=0.3.0,<0.4.0",
    ],
    python_requires=">=3.7, <4",
    extras_require=extras_require,
    py_modules=["eth_portal"],
    license="MIT",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"eth_portal": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)

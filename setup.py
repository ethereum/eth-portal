#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    "test": [
        "pytest>=6.2.5,<7",
        "pytest-xdist>=2.4.0,<3",
        "tox==3.14.6",
    ],
    "lint": [
        "black>=22.1,<23",
        "flake8==3.7.9",
        "isort>=5.10.1,<6",
        "mypy==0.770",
        "pydocstyle>=5.0.0,<6",
    ],
    "doc": [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9,<1",
        "towncrier>=21,<22",
        "Jinja2<3",
        "MarkupSafe<2",
    ],
    "dev": [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]
    + extras_require["lint"]
    + extras_require["doc"]
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
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)

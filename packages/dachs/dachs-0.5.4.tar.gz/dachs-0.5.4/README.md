# DACHS (v0.5.4)

[![PyPI Package latest release](https://img.shields.io/pypi/v/dachs.svg)](https://pypi.org/project/dachs)
[![Commits since latest release](https://img.shields.io/github/commits-since/BAMresearch/DACHS/v0.5.4.svg)](https://github.com/BAMresearch/DACHS/compare/v0.5.4...main)
[![License](https://img.shields.io/pypi/l/dachs.svg)](https://en.wikipedia.org/wiki/GPL-3.0-or-later)
[![Supported versions](https://img.shields.io/pypi/pyversions/dachs.svg)](https://pypi.org/project/dachs)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/dachs.svg)](https://pypi.org/project/dachs#files)
[![Weekly PyPI downloads](https://img.shields.io/pypi/dw/dachs.svg)](https://pypi.org/project/dachs/)
[![Continuous Integration and Deployment Status](https://github.com/BAMresearch/DACHS/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/BAMresearch/DACHS/actions/workflows/ci-cd.yml)
[![Coverage report](https://img.shields.io/endpoint?url=https://BAMresearch.github.io/DACHS/coverage-report/cov.json)](https://BAMresearch.github.io/DACHS/coverage-report/)

Database for Automation and Consistent Holistic Synthesis

## Installation

    pip install dachs

You can also install the in-development version with:

    pip install git+https://github.com/BAMresearch/DACHS.git@main

## Usage

To invoke the command line interface for processing experimental log files to the DACHS hierarchical structure and to HDF5 output, run the following to show the usage help:

    python -m dachs -h

## Documentation

https://BAMresearch.github.io/DACHS

## Development

### Testing

See which tests are available (arguments after `--` get passed to *pytest* which runs the tests):

    tox -e py -- --co

Run a specific test only:

    tox -e py -- -k <test_name from listing before>

For testing generation of the complete data structure in the local environment with stdout&stderr run:

    tox -e py -- -k test_integral

Run all tests with:

    tox -e py

### Package Version

Get the next version number and how the GIT history would be interpreted for that:

    pip install python-semantic-release
    semantic-release -v version --print

This prints its interpretation of the commits in detail. Make sure to supply the `--print`
argument to not raise the version number which is done automatically by the *release* job
of the GitHub Action Workflows.

### Project template

Update the project configuration from the *copier* template and make sure the required packages
are installed:

    pip install copier jinja2-time
    copier update --trust --skip-answered


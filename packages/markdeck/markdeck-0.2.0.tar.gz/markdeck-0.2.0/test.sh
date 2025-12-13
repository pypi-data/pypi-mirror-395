#!/usr/bin/env bash

set -e

# Unset custom index URLs to use public PyPI only
unset UV_INDEX_URL
unset UV_EXTRA_INDEX_URL
unset PIP_INDEX_URL
unset PIP_EXTRA_INDEX_URL

uv sync --extra dev

python -m unittest discover tests/ -v
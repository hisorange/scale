#!/bin/sh
pytest ./src/tests/test_deps.py --cov-config=.coveragerc --cov=./src/ --no-cov-on-fail
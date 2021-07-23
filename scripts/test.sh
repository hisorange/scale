#!/bin/sh
pytest ./src/tests/test_deps.py --cov-config=.coveragerc --cov=./src/ --cov-report=xml --no-cov-on-fail
#!/bin/sh
pytest ./src/tests/test_deps.py --cov-config=.coveragerc --cov=./src/ --cov-report=term-missing --no-cov-on-fail
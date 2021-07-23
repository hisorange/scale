#!/bin/sh
pytest ./src/tests/test_deps.py --cov=./src/ --cov-report=lcov --cov-report=xml
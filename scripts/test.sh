#!/bin/sh
pytest ./src/tests/test_vpn.py --cov=src/scale --cov-config=.coveragerc --no-cov-on-fail
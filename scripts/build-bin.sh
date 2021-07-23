#!/bin/sh
pyinstaller ./src/scale.py \
  --distpath ./dist \
  --workpath ./build \
  --onefile \
  --clean \
  --log-level="INFO" \
  --name="scale" \
  --strip
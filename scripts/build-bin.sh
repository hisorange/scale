#!/bin/sh
pyinstaller ./src/main.py \
  --distpath ./dist \
  --workpath ./build \
  --onefile \
  --clean \
  --log-level="INFO" \
  --name="scale" \
  --strip
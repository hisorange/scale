#!/bin/sh
pyinstaller src/main.py \
  --onefile \
  --distpath="./dist" \
  --workpath="./build" \
  --clean \
  --log-level="INFO" \
  --name="scale" \
  --strip
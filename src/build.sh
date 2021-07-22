#!/bin/sh
pyinstaller ./scale.py \
  --onefile \
  --clean \
  --log-level="INFO" \
  --name="scale" \
  --strip
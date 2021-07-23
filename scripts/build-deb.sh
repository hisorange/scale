#!/bin/sh
mkdir -p dist/debian
mkdir -p build/debian/scale/DEBIAN
mkdir -p build/debian/scale/usr/bin/
cp -rp debian/* build/debian/scale/DEBIAN
cp dist/scale build/debian/scale/usr/bin/scale

dpkg-deb --build build/debian/scale dist

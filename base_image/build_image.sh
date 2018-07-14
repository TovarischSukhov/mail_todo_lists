#!/usr/bin/env bash

VERSION=$1
cd ..
echo "Building python-tomita for version $VERSION"
docker build -t python-tomita:$VERSION -f base_image/Dockerfile.base .

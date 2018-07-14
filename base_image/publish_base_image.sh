#!/usr/bin/env bash

VERSION=$1
cd ..
echo "Building python-tomita for version $VERSION"
docker build -t eva-dock.sberned.ru/python-tomita:$VERSION -f base_image/Dockerfile.base .

echo "Publishing python-tomita version $VERSION"
docker push eva-dock.sberned.ru/python-tomita:$VERSION
#!/bin/bash

# This script handily initializes Tesseract container

cd tesseract

docker rm dev-tesseract
docker rmi img-dev-tesseract

docker build -t img-dev-tesseract .
docker create --publish 22:22 \
    --name dev-tesseract \
    --mount type=bind,source="$(pwd)",target=/home/ubuntu/tesseract \
    img-dev-tesseract
docker start dev-tesseract
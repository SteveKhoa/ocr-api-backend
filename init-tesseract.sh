#!/bin/bash

# This script handily initializes Tesseract container
# This script will delete the old container and the old image, and build all again. This means
# any data associated with the container would be lost during this rebuild. Please consider
# carefully while initiating this script
# 
# Only runs this script when major changes to the source code of `services/tesseract` happens

cd services/tesseract

# Remove the image and container, and build it again, so that changes are reflected immediately.
docker rm dev-tesseract
docker rmi img-dev-tesseract

docker build -t img-dev-tesseract .
docker create --publish 22:22 \
    --name dev-tesseract \
    --mount type=bind,source="$(pwd)",target=/home/ubuntu/tesseract \
    img-dev-tesseract

# Start the container
docker start dev-tesseract
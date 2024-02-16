# ocr-api-backend

This repository maintains the development of ocr-api backend facilities.

For now, `dev-tesseract` is the only container in development.

## Contributing

This project runs in Docker container.


### Tesseract-OCR `services/tesseract`

Follow one of the below instruction sets. Do not do both since Docker will build and start two separate containers.

#### Method 1: VSCode's Dev Container (Recommended)

Open `services/tesseract` via VSCode's Dev Container to get started.

#### Method 2: Manual

1. Copy this shell script and execute it to build and start the container with a builtin SSH server. 

This script will mount (using [bind mounts](https://docs.docker.com/storage/bind-mounts/)) the directory `services/tesseract` into the container and start an SSH server on port `22`.
```
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
```
2. Connect to the container via SSH `admin@localhost` with password `123`.
   - Type `ssh admin@localhost`, enter password `123`
   - IF `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, type `ssh-keygen -R localhost`, and connect to the container again
3. After SSH to the container, type `cd tesseract`
4. Type `python3.10 -m venv .venv` and `pip install -r requirements.txt`.
5. Done!

    To stop the container, type `docker stop dev-tesseract`.
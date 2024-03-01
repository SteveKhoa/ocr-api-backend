# Contributing Guidelines

## Setup

Contributing requires you to have Docker installed, at least `Docker version 20.10.16`.

### Initialize The Docker Container

##### Method 1: VSCode's Dev Container (Recommended)

Open this repository via VSCode's Dev Container to get started.

##### Method 2: Manual

*The instructions below may be platform-dependent. Please contact the maintainer of this repository for more info.*

1. Copy this shell script and execute it to build and start the container with a builtin SSH server. 

    This script will mount (using [bind mounts](https://docs.docker.com/storage/bind-mounts/)) this directory into the container and start an SSH server on port `22`.
```
#!/bin/bash

# This script handily initializes Tesseract container
# This script will delete the old container and the old image, and build all again. This means
# any data associated with the container would be lost during this rebuild. Please consider
# carefully while initiating this script

IMG_NAME="img-dev-ocr-api"
CTN_NAME="dev-ocr-api"

# Remove the image and container, and build it again, so that changes are reflected immediately.
docker rm $CTN_NAME
docker rmi $IMG_NAME

docker build -t $IMG_NAME .
docker create --publish 22:22 \
    --name $CTN_NAME \
    --mount type=bind,source="$(pwd)",target=/workspaces/$CTN_NAME \
    $IMG_NAME

# Start the container
docker start $CTN_NAME
```
2. Connect to the container via SSH `admin@localhost` with password `123`.
   
   Type `ssh admin@localhost`, enter password `123`
   
   IF `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, type `ssh-keygen -R localhost`, and connect to the container again.
3. After SSH to the container, type `cd /workspaces/dev-ocr-api`
4. Type `python3.10 -m venv .venv` and `pip install -r requirements.txt`.
5. Done!

    To stop the container, type `docker stop dev-ocr-api`.

### Install Python dependencies

##### Python Virtual Environment

Run `python -m venv .venv` to initialize Python's virtual environment.

##### Install requirements.txt

Type `pip install -r requirements/dev.txt`.

You also need to install commit hooks: `pre-commit install --hook-type commit-msg`.

It is also required to install `app/` directory as a Python package to allow global imports.  Type `pip install -e .`.

> Read this for more info on global imports:
> 
> https://stackoverflow.com/questions/72294299/multiple-top-level-packages-discovered-in-a-flat-layout

### Done!

You can start modifying the code now.

## Run FastAPI server

This application uses FastAPI to deliver its services.

Type `cd app`, then `uvicorn main:app --reload` to run `uvicorn` server.

## Run Tests
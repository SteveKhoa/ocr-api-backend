# ocr-api-backend

This repository maintains the development of ocr-api backend facilities.

For now, `dev-tesseract` is the only container in development.

## Contributing

This project runs in Docker container.

**TL;DR** 

1. For quick start, run the script `init.sh` to build, create and start container.
2. To stop the container, type `docker stop dev-tesseract`.
3. Source code is shared to the container using **bind mounts**, side effects could happen.
4. Connect to the container via SSH `admin@localhost` with password `123`.
5. Type `python -m venv .venv` and `pip install -r requirements.txt` before developing.

### Setting up

1. Download and Install Docker
2. Build the project's Docker image
```
cd tesseract

docker build -t img-dev-tesseract .
```
3. Create a container from the built image
```
docker create --publish 22:22 \
    --name dev-tesseract \
    --mount type=bind,source="$(pwd)",target=/home/ubuntu/tesseract \
    img-dev-tesseract
```

### Start and Stop the container
```
docker start dev-tesseract
```
```
docker stop dev-tesseract
```

### Working with the container
To start developing on the source code, you can either work directly on the repository (On-host), or connect remotely to the repository in the container (if you are using VSCode). This documentation describes On-host option only.

For **On-host** option, the `/tesseract` folder is shared between the container and the repository. Modifications on the repository reflect the changes to the container. However, the code needs to be executed within the container via SSH.

1. Connect to the container using SSH, ```ssh admin@localhost```, password `123`
2. Start modifying the source code on your local repository
3. To execute the code, run the command on the connected container's shell
- For example, in the SSH shell, type `python -m venv .venv` to initialize python virtual environment.

### Start developing
1. Open the connected container shell
2. Type `cd tesseract`
3. Type `python -m venv .venv` in SSH shell to initialize python virtual environment
4. Type `source .venv/bin/activate` to enter Python's virtual environment
5. Type `pip install -r requirements.txt` to install python dependencies
6. Good to go!
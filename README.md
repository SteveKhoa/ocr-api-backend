# ocr-api-backend

This repository maintains the development of ocr-api backend facilities.

For now, `dev-tesseract` is the only container in development.

## Contributing

This project runs in Docker container.


### Tesseract-OCR model `services/tesseract`

**Build and connected to the running container** 
1. Run the script `init-tesseract.sh` to build, create and start container.
2. To stop the container, type `docker stop dev-tesseract`.
3. Source code `services/tesseract` is shared to the container using **bind mounts**, side effects happens while modifying the contents inside `services/tesseract`.
4. Connect to the container via SSH `admin@localhost` with password `123`.
   - Type `ssh admin@localhost`, enter password `123`
   - IF `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, type `ssh-keygen -R localhost`, and connect to the container again
5. After SSH to the container, type `cd tesseract`
6. Type `python3.10 -m venv .venv` and `pip install -r requirements.txt`.

**Notes:** 
- The source code can be modified from outside the container (on local machine) or inside the container (by connecting to remote repository inside the container).
- Every code execution must be done within the container
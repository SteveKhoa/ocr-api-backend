# ocr-api-backend

This repository maintains the development of ocr-api backend facilities.

## Contributing

### Setting up
This project runs in Docker containers.

1. Download and Install Docker
2. Compose the neccessary services
```
docker compose up -d
```
3. When finish, decompose all the services
```
docker compose down
```

**Note:** at the moment, running `docker compose down` is not enough to stop all containers, you must continuously press `CTRL C` (MacOS). The reason is that tesseract daemon is kept running infinitely for current developing purposes.

### Run commands in containers
#### Interacting with Tesseract OCR
```
docker exec tesseract-ocr [tesseract-commands]
```

For examples, ```docker exec tesseract-ocr tesseract --help``` will display canonical help for tesseract CLI.
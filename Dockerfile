FROM python:3.10-bookworm as dev

# Core services
RUN apt -y update
RUN apt -y upgrade

# Environment variables
ENV ENVIRON=dev
ENV DB_URL="/workspaces/ocr-api-backend/database/apikey.db"

# Security environment variables
ENV SECRET_KEY=ecccbec8ba64fa75af46ae277aeabce459fbe29f753640ffc7e98f4ecb0cd42b

# Plugin services
RUN apt -y install tesseract-ocr

EXPOSE 22 8000
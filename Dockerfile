FROM python:3.10-bookworm as dev

# Core services
RUN apt -y update
RUN apt -y upgrade

# Environment variables
ENV ENVIRON=dev
ENV DB_URL="/workspaces/ocr-api-backend/database/shared.db"

# Security environment variables
ARG SERVER_SECRET
ENV SECRET_KEY=$SERVER_SECRET

# Plugin services
RUN apt -y install tesseract-ocr

EXPOSE 22 8000
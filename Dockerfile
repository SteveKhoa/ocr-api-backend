FROM python:3.10-bookworm as dev

# Core services
RUN apt -y update
RUN apt -y upgrade
RUN apt -y install sudo
RUN apt -y install openssh-server

# Environment variables
ENV TERM=xterm-256color
ENV ENVIRON=dev
ENV DB_URL="/workspaces/ocr-api-backend/app/db/database.db"

# Plugin services
RUN apt -y install tesseract-ocr

# Development-stage services
RUN apt -y install libx11-dev
RUN apt -y install python3-tk

# Create user `admin`  and set password to `123`
# (1) set default user directory to /home/ubuntu
# (2) set default shell to /bin/bash
# (3) set user group to `root`
# (4) set user id to 1000
# (5) set username to `admin`
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin

RUN echo 'admin:123' | chpasswd

# Start SSH service
RUN service ssh start

EXPOSE 22 8000

CMD ["/usr/sbin/sshd","-D"]
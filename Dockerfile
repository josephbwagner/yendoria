# Dockerfile for Yendoria Distribution
FROM python:3.11-slim

LABEL maintainer="Joseph Wagner <j.wagner1024@gmail.com>"
LABEL description="Yendoria - A Traditional Roguelike Game"
LABEL version="0.1.1"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Yendoria from GitHub release
RUN pip install --no-cache-dir \
    https://github.com/josephbwagner/yendoria/releases/download/v0.1.1/yendoria-0.1.1-py3-none-any.whl

# Create non-root user
RUN useradd -m -u 1000 player
USER player

# Set the entry point
CMD ["python", "-m", "yendoria"]

# Usage:
# docker build -t yendoria:0.1.1 .
# docker run -it yendoria:0.1.1

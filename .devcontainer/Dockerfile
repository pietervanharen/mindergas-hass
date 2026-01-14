# Dockerfile for devcontainer
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for docker-compose support)
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Set working directory
WORKDIR /workspace

# Create config directory for Home Assistant
RUN mkdir -p /config/custom_components

LABEL description="MinderGas Home Assistant Integration Development Container"

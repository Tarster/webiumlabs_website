#!/bin/bash
# Standardization: Auto-generated deploy script

# Requirements.txt check
if [ -f "requirements.txt" ]; then
    echo "Python project detected. Setting up venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Docker Compose check
if [ -f "compose.yaml" ]; then
    echo "Docker Compose (compose.yaml) detected. Starting services..."
    docker-compose up -d
elif [ -f "docker-compose.yml" ]; then
    echo "Docker Compose (docker-compose.yml) detected. Starting services..."
    docker-compose up -d
fi

# Node.js check
if [ -f "package.json" ]; then
    echo "Node.js project detected. Installing dependencies..."
    npm install
fi

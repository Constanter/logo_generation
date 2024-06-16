#!/bin/bash

# Set environment variables for sensitive information
export POSTGRES_USER="user"
export POSTGRES_PASSWORD="password"
export POSTGRES_DB="logo_storage"

# Build Docker images
sudo docker compose build

# Start containers
sudo docker compose up -d

# Wait for database to be ready
# while ! nc -z storage_db 5432; do sleep 1; done

# Apply any database migrations or initial data setup
# sudo python logo_generation/storage_service/src/db.py

# Expose application on public IP
# Assuming the static IP is 46.138.11.179
sudo ufw allow from 46.138.11.179 to any port 5000
sudo ufw allow from 46.138.11.179 to any port 7860

# Configure DNS to point to the static IP
# Update your domain registrar's DNS settings to point your domain to 46.138.11.179
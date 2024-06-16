#!/bin/bash

sudo docker compose build
sudo docker compose up -d
sudo ufw allow  5000
sudo ufw allow 7860

#!/bin/bash

# Update package lists
sudo apt-get update

# Install prerequisites
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

# Install Docker version 26.0.0
echo "Installing Docker 26.0.0..."
DOCKER_VERSION="26.0.0"
DOCKER_URL="https://download.docker.com/linux/ubuntu"
curl -fsSL "$DOCKER_URL/gpg" | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] $DOCKER_URL $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce=$DOCKER_VERSION~3-0~ubuntu
sudo apt-mark hold docker-ce
sudo systemctl enable docker
sudo systemctl start docker

# Install Python 3.10.12
echo "Installing Python 3.10.12..."
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev python3.10-distutils

# Install Node.js v12.22.9
echo "Installing Node.js v12.22.9..."
NODE_VERSION="12.22.9"
curl -fsSL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g npm@8.5.1

# Verify installations
echo "Verifying installations..."
docker --version
python3.10 --version
node -v
npm -v

echo "Installation complete!"

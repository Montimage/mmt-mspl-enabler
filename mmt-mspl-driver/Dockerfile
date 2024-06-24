# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompt during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    sudo && \
    apt-get clean

# Install Node.js v14.x
RUN curl -fsSL https://nodejs.org/dist/v14.17.0/node-v14.17.0-linux-x64.tar.xz -o node.tar.xz && \
    tar -xf node.tar.xz --directory /usr/local --strip-components=1 && \
    rm node.tar.xz
    
# Install npm 8.5.1
RUN npm install -g npm@8.5.1

# Clone the repository
RUN git clone https://github.com/Montimage/mmt-mspl-enabler.git

# Change working directory
WORKDIR /mmt-mspl-enabler/mmt-mspl-driver

# Run the node application
CMD ["sudo", "node", "index.js"]

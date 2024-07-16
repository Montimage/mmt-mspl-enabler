# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Atualizar o índice de pacotes e instalar pacotes necessários
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    && apt-get update && \
    apt-get install -y docker-ce-cli && \
    curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Verificar as instalações
RUN docker --version && docker-compose --version

# Definir o comando padrão
CMD [ "bash" ]


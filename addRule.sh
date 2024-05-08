#!/bin/bash

# This script is responsable for running mspl_mmt_agent (creates new mmt-probe.conf and new mmt-security rule)
# Send those files to mi_probe docker container
# Compile the new rule and restart the container

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPL='\033[0;35m'
NC='\033[0m'

echo -e "\n${PURPL}Running the script with the provided XML file...${NC}"
python3 mspl_mmt_agent.py inputs/pingofthedeath.xml

echo -e "\n${PURPL}Copying the new mmt-probe.conf file to the Docker container [Using only the new rule]...${NC}"
sudo docker cp new-mmt--probe.conf mi_probe:/opt/mmt/probe/mmt-probe.conf

echo -e "\n${PURPL}Copying the new rule XML file to the Docker container...${NC}"
sudo docker cp rules/new_rule.xml mi_probe:/opt/mmt/security/bin

echo -e "\n${PURPL}Compiling the new rule and generating the shared object file...${NC}"
sudo docker exec -it mi_probe ./opt/mmt/security/bin/compile_rule /opt/mmt/security/rules/104.new.so /opt/mmt/security/bin/new_rule.xml

echo -e "\n${PURPL}Restarting the MMT probe Docker container...${NC}"
sudo docker restart mi_probe

echo -e "\n${GREEN}Rule added with success!${NC}\n"
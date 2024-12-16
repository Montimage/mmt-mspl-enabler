import argparse
import subprocess
import requests
import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__author__ = "Gustavo Jodar Soares"
__copyright__ = "Copyright 2023, CERBERUS"
__credits__ = ["Antonio Skarmeta", "Alejandro Molina Zarca", "Gustavo jodar Soares", "Huu-Nghia Nguyen", "Emilio García de la Calera Molina"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Gustavo Jodar Soares"
__email__ = "gustavo.jodar@um.es"
__status__ = "Development"

# Define color escape codes
GREEN = '\033[92m'
PURPLE = '\033[95m'
RESET = '\033[0m'
RED = '\033[91m'


class MMTAgentDriver:

    def __init__(self, end_point_info):
        self.obtain_url(end_point_info)

    def obtain_url(self, end_point_info):

        self.mmtUri = f"{end_point_info['api'].uri}"

        logger.info("Istio credentials obtained successfully")

    # Function to execute a command
    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            print(f"{GREEN}{output}{RESET}\n")
            return output
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8')
            print(f"{RED}Error: {error_message}{RESET}")
            sys.exit(1)

    # Function to make an API request
    def make_api_request(self, method, endpoint, ip_address, headers=None, files=None, json_data=None):
        url = ip_address + endpoint
        try:
            if json_data:
                response = requests.request(method, url, headers=headers, json=json_data)
            else:
                response = requests.request(method, url, headers=headers, files=files)

            if response.status_code == 200:
                print(f"Success: {response.status_code}, {response.text}\n")
                return response.json() if response.headers.get('content-type') == 'application/json' else response.text
            else:
                print(f"Error: {response.status_code}, {response.text}")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {str(e)}")
            sys.exit(1)

    def enforce_conf(self, enabler_configuration):
        if len (mspl_confs):
            return
        enabler_configuration = mspl_confs[0]

        xml_file = enabler_configuration[0] if enabler_configuration[0] else None

        # Checking health of server
        print(f"{PURPLE}Checking health of server ... {RESET}")
        health_response = self.make_api_request('GET', '/healthcheck', self.mmtUri, headers={'accept': 'application/json'})
        print(f"{GREEN}IP address {self.mmtUri} is reachable {RESET}")

        if xml_file is not None:
            # Execute commands
            print(f"{PURPLE}Creating rule and config with plugin ...{RESET}")
            configs = enabler_configuration

            # Upload XML file
            print(f"{PURPLE}Uploading new rule to mmt-security at {self.mmtUri} ... {RESET}")
            xml_response = self.make_api_request(
                'PUT',
                '/xml-rule',
                self.mmtUri,
                headers={'accept': 'application/json'},
                json_data={'fileContent': xml_file}
            )

            # Upload MMT config file
            print(f"{PURPLE}Uploading new rule to mmt-probe.conf at {self.mmtUri} ... {RESET}")
            file_content = configs[0]  # Get the content of the file
            mmt_response = self.make_api_request(
                'PUT',
                '/mmt-config',
                self.mmtUri,
                headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                json_data={'fileContent': file_content}
            )

        else:
            # Upload default MMT config file
            print(f"{PURPLE}New rule not passed -> Uploading default mmt-probe.conf at {self.mmtUri} ... {RESET}")
            with open('mmt-confs/mmt-probe_original.conf', "r", encoding='utf-8') as conf_file:
                file_content = str(conf_file.read())
                mmt_response = self.make_api_request(
                    'PUT',
                    '/mmt-config',
                    self.mmtUri,
                    headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                    json_data={'fileContent': file_content}
                )

        # Restart Docker
        print(f"{PURPLE}Restarting docker containers at {self.mmtUri} ... {RESET}")
        restart_response = self.make_api_request('GET', 'restart-docker', self.mmtUri, headers={'accept': 'application/json'})

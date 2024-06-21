import subprocess
import requests
import sys

__author__ = "Gustavo Jodar Soares"
__copyright__ = "Copyright 2023, CERBERUS"
__credits__ = ["Antonio Skarmeta", "Alejandro Molina Zarca","Gustavo jodar Soares","Huu-Nghia Nguyen", "Emilio García de la Calera Molina"]
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

# IP address
IP_ADDRESS = '10.208.2.116' #'10.208.5.100'
PORT = 4000

# Function to execute a command
def execute_command(command):
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
def make_api_request(method, endpoint, headers=None, files=None):
    url = f'http://{IP_ADDRESS}:{PORT}/{endpoint}'
    try:
        response = requests.request(method, url, headers=headers, files=files)
        if response.status_code == 200:
            print(f"{GREEN}Success: {response.status_code}, {response.text}{RESET}\n")
            return response.json() if response.headers.get('content-type') == 'application/json' else response.text
        else:
            print(f"{RED}Error: {response.status_code}, {response.text}{RESET}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"{RED}Request Exception: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    
    xml_file = None
    if(len(sys.argv) > 1):
        xml_file = sys.argv[1]

    # Checking health of server
    print(f"{PURPLE}Checking health of server ... {RESET}")
    health_response = make_api_request('GET', 'healthcheck', headers={'accept': 'application/json'})
    print(f"{GREEN}IP address {IP_ADDRESS} is reachable on port {PORT}{RESET}")

    if(xml_file != None):
        # Execute commands
        print(f"{PURPLE}Creating rule and config with plugin ...{RESET}")
        plugin_output = execute_command("python3 mspl_mmt_plugin.py " + xml_file)

        # Upload XML file
        print(f"{PURPLE}Uploading new rule to mmt-security at {IP_ADDRESS} ... {RESET}")
        xml_file = {'file': open('rules/new_rule.xml', 'rb')}
        xml_response = make_api_request('PUT', 'xml-rule', headers={'accept': 'application/json'}, files=xml_file)


        # Upload MMT config file
        print(f"{PURPLE}Uploading new rule to mmt-probe.conf at {IP_ADDRESS} ... {RESET}")
        mmt_file = {'file': open('mmt-confs/new-mmt--probe.conf', 'rb')}
        mmt_response = make_api_request('PUT', 'mmt-config', headers={'accept': 'application/json'}, files=mmt_file)


    else:
        print(f"{PURPLE}New rule not passed -> Uploading default mmt-probe.conf at {IP_ADDRESS} ... {RESET}")
        mmt_file = {'file': open('mmt-confs/mmt-probe_original.conf', 'rb')}
        mmt_response = make_api_request('PUT', 'mmt-config', headers={'accept': 'application/json'}, files=mmt_file)

    # Restart Docker
    print(f"{PURPLE}Restarting docker containers at {IP_ADDRESS} ... {RESET}")
    restart_response = make_api_request('GET', 'restart-docker', headers={'accept': 'application/json'})

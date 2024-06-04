import subprocess
import requests
import sys

# IP address
IP_ADDRESS = '10.208.1.24'
PORT = 4000

# Function to execute a command
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        return output
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8')
        return error_message

# Function to make an API request
def make_api_request(method, endpoint, headers=None, files=None):
    url = f'http://{IP_ADDRESS}:{PORT}/{endpoint}'
    try:
        response = requests.request(method, url, headers=headers, files=files)
        if response.status_code == 200:
            return response.json() if response.headers.get('content-type') == 'application/json' else response.text
        else:
            return f'Error: {response.status_code}, {response.text}'
    except requests.exceptions.RequestException as e:
        return str(e)


if __name__ == "__main__":
    xml_file = sys.argv[1] 

    try:
        # Make a simple GET request
        response = requests.get(f"http://{IP_ADDRESS}:{PORT}/healthcheck")  # Replace with appropriate endpoint if needed
        
        response.raise_for_status()  # Raise an exception for non-200 status codes
        
        print(f"IP address {IP_ADDRESS} is reachable on port {PORT}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to {IP_ADDRESS}:{PORT}. {e} \n\nCheck if API is up!")
        exit(1)

    # Execute commands
    plugin_output = execute_command("python3 mspl_mmt_plugin.py " + xml_file)
    print("\n-> Plugin Output:", plugin_output)

    # Upload XML file
    xml_file = {'file': open('rules/new_rule.xml', 'rb')}
    xml_response = make_api_request('PUT', 'xml-rule', headers={'accept': 'application/json'}, files=xml_file)
    print("\n -> XML Upload Response:", xml_response)

    # Upload MMT config file
    mmt_file = {'file': open('mmt-confs/new-mmt--probe.conf', 'rb')}
    mmt_response = make_api_request('PUT', 'mmt-config', headers={'accept': 'application/json'}, files=mmt_file)
    print("\n -> MMT Config Upload Response:", mmt_response)

    # Restart Docker
    restart_response = make_api_request('GET', 'restart-docker', headers={'accept': 'application/json'})
    print("\n -> Docker Restart Response:", restart_response)

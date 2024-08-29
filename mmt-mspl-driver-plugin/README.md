
# mmt-mspl-drive-plugin

The mmt-mspl-enabler is a project designed to connect an mspl file to Montimage's mmt-tools. 

## Connecting to Bastion

For connecting to Bastion, refer the /Docker-MMT-Tools.README.md and use the file mmt-driver.py located in this folder

## Run Locally

Go to the project directory

```bash
  cd mmt-mspl-driver-plugin/
```
To generate a new mmt-security rule and a mmt-probe.conf 

```bash
python3 mmt-mspl-plugin [rule.xml]

```

Example pingofthedeath.xml input using default IP and defalut PORT (writen in the file program) 

```bash
  python3 mspl_mmt_plugin.py inputs/pingofthedeath.xml 
```
A variable with shape [string, string]  will be generated according to the Bastion (UMU's Orchastrator) requirements will be generated.

## Connecting mspl_mmt_plugin and mspl_mmt_driver using mmt-agent.py

The mmt-agent.py program runs the mspl_mmt_plugin, sends the respective files to the driver class and restarts the mmt-tools services in the desired server.

Example - Using mmt-agent.py to configure the mmt-tools to use the policies especified in pingofthedeath.xml file:

```bash
  python3 mmt_agent.py inputs/pingofthedeath.xml 
```
**Parameters for mmt-agent.py**

* -r, --rule -> Defines the rule.xml file to be sent to the mspl-enabler
* --host -> Defines the HOST's IP address of the API
* --port -> Defines the HOST's PORT address of the API

# Requires
 - Python 3

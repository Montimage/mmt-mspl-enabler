
# mmt-mspl-plugin

The mmt-mspl-plugin is a project designed to connect an mspl file to Montimage's mmt-tools. 



## Run Locally

Go to the project directory

```bash
  cd mmt-mspl-plugin/
```
To generate a new mmt-security rule and a mmt-probe.conf 

```bash
  python3 mspl_mmt_plugin.py <path/to/mspl_file.xml>
```

Example pingofthedeath.xml input

```bash
  python3 mspl_mmt_plugin.py inputs/pingofthedeath.xml 
```
Two files will be generated: rules/new_rule.xml and mmt-confs/newmmt-probe.conf .

## Connecting mspl_mmt_plugin and mspl_mmt_driver using mmt-agent.py

The mmt-agent.py program runs the mspl_mmt_plugin, sends the respective files to the driver and restarts the mmt-tools services.

Example - Using mmt-agent.py to configure the mmt-tools to use the policies especified in pingofthedeath.xml file:

```bash
  python3 mmt_agent.py inputs/pingofthedeath.xml 
```

# Requires
 - Python 3

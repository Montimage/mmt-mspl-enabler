# mmt-mspl-enabler

This project develops a plugin and a Driver to conect an MSPL Policy agent and the mmt-tools installed in a server, making it possible to use .xml policy files to generate new security rules to be used by the MMT-Tools.

Here is an overview of how this project works:
<img src="imgs/Cerberus-MMT%20Doc.jpg"/>

By passing a MSPL Policy File to the mmt-mspl-plugin you will generate two files: 
* a new mmt-security rule that uses the given policy 
* a mmt-probe.conf that applies only the new rule to be used by MMT-Security

After genrated, those files can be sent to the server running the mmt-tools by using the mmt-mspl-drive, it exposes and API documented by [Swagger](https://swagger.io/).

# mmt-tools

To set up the MMT-Tools check: [Docker-MMT-Tools](https://swagger.io/](https://github.com/Montimage/mmt-mspl-enabler/tree/main/mmt-mspl-driver/Docker-MMT-Tools)

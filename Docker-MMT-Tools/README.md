# Setting up MMT-TOOLS and API

For easily setting up multiple MMT-Probes using the same MMT-Operator the docker compose files only_probe.yml and operator_probe.yml were created.

<img src="../imgs/MultiProbes.jpg"/>

For Server 0 (The one that will host MMT-Operator and a MMT-Probe), run the following command:
Setting up the .env file to have the IP of Server 0 and the desired PORT for MMT-Operator.

```bash
  sudo docker compose -f operator_probe.yml -d
```

For setting up the other servers (with only MMT-Probe), run:
```bash
  sudo docker compose -f only_probe.yml up -d
```
For those servers, set the .env file using the IP of Server 0 (for OPERATOR_IP) and the MMT-Operator's PORT. Also, don't forget to change the PROBE_ID so it is possible to see their output in MMT-Operator. 

The API for remote configuration of MMT-Probe will be listening to port 4000, and it's responsible for making changes in the MMT-Probe docker.


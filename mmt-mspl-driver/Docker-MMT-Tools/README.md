# Setting up MMT-TOOLS 

For easily setting up multiple MMT-Probes using the same MMT-Operator the docker compose files only_probe.yml and operator_probe.yml were created.

<img src="../imgs/MultiProbes.jpg"/>

For Server 0 (The one that will host MMT-Operator and a MMT-Probe), run the following command:
Setting up the .env file to have the IP of Server 0 and the desired PORT for MMT-Operator.

```bash
  sudo docker compose -f operator_probe.yml -d
```

For setting up the other the other server, that will run only MMT-Probe, run:
```bash
  sudo docker compose -f only_probe.yml up -d
```
For those server, set the .env file using the IP of Server 0 and the MMT-Operator's PORT. Also, don't forget to change the PROBE_ID so it is possible to see their output in MMT-Operator. 



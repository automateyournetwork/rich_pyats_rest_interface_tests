# rich_pyats_rest_interface_tests
Various pyATS Interface Tests against IOS-XE YANG RESTCONF APIs using Rich Tables for reporting

# rich_pyats_rest_interface_tests
Examples of pyATS REST Connector with IOS-XE / NXOS YANG Model Interface level testing

## Ready to go with the Cisco CML

[CML Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/d6023d5d-e04f-4138-9f51-ff1dee9b0ad4)

[Always On IOS-XE Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/7b4d4209-a17c-4bc3-9b38-f15184e53a94?diagramType=Topology)

### Enable RESTCONF on the 2 IOS-XE Devices
Make sure to enable RESTCONF

```console
switch> enable
switch# conf t
switch(conf)# ip http secure-server
switch(conf)# restconf
```
## Installation

### Create a virtual environment
```console
$ python3 -m venv REST_Connector
$ source /REST_Connector/bin/activate
(REST_Connector) $
```

### Clone the repository 
```console
(REST_Connector) $ git clone https://github.com/automateyournetwork/rich_pyats_rest_interface_tests
(REST_Connector) $ cd rich_pyats_rest_interface_tests
```

### Install the required packages
```console
(REST_Connector) ~/rich_pyats_rest_interface_tests$ pip install pyats[full]
(REST_Connector) ~/rich_pyats_rest_interface_tests$ pip install rich
(REST_Connector) ~/rich_pyats_rest_interface_tests$ pip install rest.connector
```

## Run the code - using RESTCONF
```console
(REST_Connector) ~/rich_pyats_rest_interface_tests$
(REST_Connector) ~/rich_pyats_rest_interface_tests$ pyats run job rich_pyats_rest_interface_tests_job.py
```

### View the logs

```console
(REST_Connector) ~/
```
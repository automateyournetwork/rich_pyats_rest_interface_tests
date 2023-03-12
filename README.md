# brainiac
Examples of pyATS REST Connector with IOS-XE YANG Model Interface level testing using pyATS with chatGPT, Rich, and WebEx Integrations

## Ready to go with the Cisco CML

[Always On IOS-XE Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology)

## Installation

### Create a virtual environment
```console
$ python3 -m venv REST_Connector
$ source /REST_Connector/bin/activate
(REST_Connector) $
```

### Clone the repository 
```console
(REST_Connector) $ git clone https://github.com/automateyournetwork/brainiac
(REST_Connector) $ cd brainiac
```

### Install the required packages
```console
(REST_Connector) ~/brainiac$ pip install pyats[full]
(REST_Connector) ~/brainiac$ pip install rich
(REST_Connector) ~/brainiac$ pip install rest.connector
(REST_Connector) ~/brainiac$ pip install requests
(REST_Connector) ~/brainiac$ pip install python-dotenv
(REST_Connector) ~/brainiac$ pip install cairosvg
(REST_Connector) ~/brainiac$ pip install gtts
(REST_Connector) ~/brainiac$ pip install openai

```

## Run the code
```console
(REST_Connector) ~/brainiac$
(REST_Connector) ~/brainiac$ pyats run job brainiac_job.py
```

### View the logs

```console
(REST_Connector) ~/ pyats logs view
```

### SVG Output
If you are using VS Code you can install the SVG Preview Extension and view the per-test SVG Rich Table output of the results of each test in the IDE or you can view these files in a web browser to view the output without using the pyATS Logs Viewer
## WebEx
You can create a local.env file with a WebEx Room ID and WebEx Token and have the test results sent to that room

WEBEX_TOKEN=""
WEBEX_ROOMID=""


## ChatGPT
You can create a local.env file with an OpenAI API Key to get AI powered suggestions to fix failed tests

OPENAI_KEY=""

## API Coverage / Tests

### openconfig-interfaces:interfaces

Interface Admin State Matches Oper State

Interface Has A Description

Interface is Full Duplex

Input CRC Errors

Input Discards

Input Errors

Input FCS Errors

Input Fragment

Input Jabber

Input MAC Pause Frames

Input Oversize Frames

Input Unknown Protocols

Output Discards

Output Errors

Output Pause Frames

### Cisco-IOS-XE-interfaces-oper:interfaces

Interface Admin Status Matches Oper Status

Interface Has Description

Interface Flaps

Input CRC Errors

Input Discards

Input Discards 64

Input Errors

Input Errors 64

Input Unknown Protocols

Input Unknown Protocols 64

Output Discards

Output Errors

v4 Protocols Input Discarded Packets

v4 Protocols Input Error Packets

v4 Protocols Output Discarded Packets

v4 Protocols Output Error Packets

v6 Protocols Input Discarded Packets

v6 Protocols Input Error Packets

v6 Protocols Output Discarded Packets

v6 Protocols Output Error Packets

## ietf-interfaces:interfaces

Interface Description
## ietf-interfaces:interfaces-state

Interface Admin Status Matches Oper Status

Input Discards

Input Errors

Input Unknown Protocols

Output Discards

Output Errors

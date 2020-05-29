# Catalyst Wireless Data Retrieval Tool

This scripts in this file enables the retrieval of configuration data from IOS-XE based wireless controllers using RESTCONF.

## Requirements

* Python 3.6+
* requests
* pyyaml

## Getting Started

Clone this repository

```sh
git clone
```

Install the required packages

```
pip install -r requirements.txt
```

## Configuration

To customize the script for your environment, simply edit the `data.yaml` file in this directory. Specifically,
be sure to provide the connection details as shown below.

```yaml

# Set connection details for the controllers
controller: 10.255.131.125
port: 443
username: <YOUR USERNAME>
password: <YOUR PASSWORD>
```

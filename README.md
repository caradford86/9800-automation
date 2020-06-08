# Catalyst Wireless Data Retrieval Tool

The scripts in this repository enable the retrieval of configuration data from IOS-XE based wireless controllers using `RESTCONF`.

## Requirements

* Python 3.6+
* requests
* pyyaml

## Getting Started

Clone this repository

```sh
git clone https://github.com/caradford86/9800-automation.git
```

Install the required packages

```sh
cd 9800-automation
pip install -r requirements.txt
```

## Configuration

To customize the script for your environment, simply edit the `data.yaml` file in this directory. Specifically,
be sure to provide the connection details as shown below. The configuration that is retrieved depends on the endpoints that are configured in the `endpoints` section of the file.

```yaml

# Set connection details for the controllers
controller: 10.255.131.125
port: 443
username: <YOUR USERNAME>
password: <YOUR PASSWORD>

# ----------------- API ENDPOINTS --------------------------------

endpoints:
  interfaces: Cisco-IOS-XE-interfaces-oper:interfaces/interface
  vlans: Cisco-IOS-XE-vlan-oper:vlans/vlan
  wlan_profile: Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/wlan-cfg-entries/wlan-cfg-entry
  wlan_policy: Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/wlan-policies/wlan-policy
  policy_tags: Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/policy-list-entries/policy-list-entry
  ap_join_profiles: Cisco-IOS-XE-wireless-site-cfg:site-cfg-data/ap-cfg-profiles/ap-cfg-profile
  flex_profiles: Cisco-IOS-XE-wireless-flex-cfg:flex-cfg-data/flex-policy-entries/flex-policy-entry
  site_tags: Cisco-IOS-XE-wireless-site-cfg:site-cfg-data/site-tag-configs/site-tag-config
  rf_tag: Cisco-IOS-XE-wireless-rf-cfg:rf-cfg-data/rf-tags/rf-tag

```

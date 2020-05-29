from libpath import Path

import requests
import json
import re
import yaml

requests.packages.urllib3.disable_warnings()


data = yaml.safe_load(Path('data.yml').read_text())
HEADERS = {
    'content-type': 'application/yang-data+json',
    'accept': 'application/yang-data+json'
}


def _get(endpoint):
    host = data.get('controller')
    user = data.get('username')
    pw = data.get('password')
    port = data.get('port')

    url = f'https://{host}:{port}/restconf/data/{endpoint}'
    resp = requests.get(url, auth=(user, pw), headers=HEADERS)
    return resp


def write_to_file(key, content):
    filename = f'{key}.json'
    with open(filename, 'w') as out:
        out.write(out)


endpoints = data.get('endpoints')
for key, value in endpoints.items():
    print(f'retrieving data for {key}')
    r = _get(value)
    write_to_file(key, r.json())


#Interfaces
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('interfaces.json','wb') as f:
    f.write(response.content)


#VLANs
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-vlan-oper:vlans/vlan?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('vlans.json','wb') as f:
    f.write(response.content)



#WLAN Profiles
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/wlan-cfg-entries/wlan-cfg-entry?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('wlan-profiles.json','wb') as f:
    f.write(response.content)


#Open the WLAN Profile JSON File
fin = open("wlan-profiles.json", "r")
fout = open("wlan-profiles-2.json", "w")

for line in fin:
    fout.write(re.sub(r'-(?=.+\"\:)', r'_', line))

fin.close()
fout.close()



#Policy Profiles
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/wlan-policies/wlan-policy?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('policy-profiles.json','wb') as f:
    f.write(response.content)


#Open the Policy Profile JSON File
fin = open("policy-profiles.json", "r")
fout = open("policy-profiles-2.json", "w")

for line in fin:
    fout.write(re.sub(r'-(?=.+\"\:)', r'_', line))

fin.close()
fout.close()



#Policy Tags
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-wlan-cfg:wlan-cfg-data/policy-list-entries/policy-list-entry?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('policy-tags.json','wb') as f:
    f.write(response.content)



#AP Join Profiles
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-site-cfg:site-cfg-data/ap-cfg-profiles/ap-cfg-profile?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('ap-join-profiles.json','wb') as f:
    f.write(response.content)


#Open the AP Join Profile JSON File
fin = open("ap-join-profiles.json", "r")
fout = open("ap-join-profiles-2.json", "w")

for line in fin:
    fout.write(re.sub(r'-(?=.+\"\:)', r'_', line))

fin.close()
fout.close()



#Flex Profiles
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-flex-cfg:flex-cfg-data/flex-policy-entries/flex-policy-entry?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('flex-profiles.json','wb') as f:
    f.write(response.content)


#Open the Flex Profile JSON File
fin = open("flex-profiles.json", "r")
fout = open("flex-profiles-2.json", "w")

for line in fin:
    fout.write(re.sub(r'-(?=.+\"\:)', r'_', line))

fin.close()
fout.close()



#Site Tags
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-site-cfg:site-cfg-data/site-tag-configs/site-tag-config?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('site-tags.json','wb') as f:
    f.write(response.content)



#RF Profiles
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-rf-cfg:rf-cfg-data/rf-profiles/rf-profile?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)

with open('rf-profiles.json','wb') as f:
    f.write(response.content)


#Open the RF Profile JSON File
fin = open("rf-profiles.json", "r")
fout = open("rf-profiles-2.json", "w")

for line in fin:
    fout.write(re.sub(r'-(?=.+\"\:)', r'_', line))

fin.close()
fout.close()



#RF Tags
url = "https://10.1.1.111:443//restconf/data/Cisco-IOS-XE-wireless-rf-cfg:rf-cfg-data/rf-tags/rf-tag?with-defaults=report-all"
headers = {'content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}

response = requests.get(url, auth=("cradford", "P@22w0rd!@"), headers=headers, verify=False)



from pathlib import Path

import requests
import json
import re
import yaml

requests.packages.urllib3.disable_warnings()


# Global variables
OUTPUT_DIR = 'test'
HEADERS = {
    'content-type': 'application/yang-data+json',
    'accept': 'application/yang-data+json'
}


def get_url(url, auth=None, params={}, verify=False):
    """Wrapper function to make GET calls using requests

    Arguments:
        endpoint {url} -- url to target for the resource
        params {dict} -- key-value pairs to parameters to add to call

    Returns:
        JSON -- json response data for GET call
    """
    resp = requests.get(url, auth=auth, headers=HEADERS, params=params, verify=verify)
    if resp.ok:
        return resp.json()
    resp.raise_for_status()


def build_url(host, endpoint,  port=443):
    """ Simple function to build the URLs
    Arguments:
        host {str]} -- This is the hostname of IP address
        port {int} -- port number to connect to (default: 443)
        endpoint {endpoint} -- the specific endpoint for the resource

    Returns:
        str -- the fully built url to make the make
    """
    url = f'https://{host}:{port}/restconf/data/{endpoint}'
    return url


def write_to_file(stem, content):
    """Clean up and write content to file"""
    filename = f'{OUTPUT_DIR}/{stem}.json'

    with open(filename, 'w') as out:
        output_string = json.dumps(content, indent=2)

        # replace - with _ for Osiris compatibility
        formatted_output = re.sub(r'-(?=.+\"\:)', r'_', output_string)
        out.write(formatted_output)


def main():
    # load data from yaml file
    data = yaml.safe_load(Path('data.yaml').read_text())

    # set some variables for us to use
    endpoint_data = data.get('endpoints')
    host = data.get('controller')
    user = data.get('username')
    pw = data.get('password')
    port = data.get('port')

    params = {"with-defaults": "report-all"}

    # get the data for each endpoint defined in the data
    # for example: vlans: Cisco-IOS-XE-vlan-oper:vlans/vlan
    # in which case, ep_name = 'vlans' and ep_value = 'Cisco-IOS-XE-vlan-oper:vlans/vlan'
    combined_data = {}
    for ep_name, ep_value in endpoint_data.items():
        url = build_url(host, ep_value, port=port)

        print(f'retrieving data for: {ep_name}')
        json_data = get_url(url, auth=(user, pw), params=params)

        combined_data.update(json_data)

    print(f'saving data to file: {ep_name}')
    write_to_file('combined_output', json_data)


if __name__ == '__main__':
    main()

import requests
# import json
import re

requests.packages.urllib3.disable_warnings()


# Global variables
# OUTPUT_DIR = 'test'
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
    resp = requests.get(
        url,
        auth=auth,
        headers=HEADERS,
        params=params,
        verify=verify)
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


def write_to_file(stem, content, output_dir="."):
    """Clean up and write content to file"""
    filename = f'{output_dir}/{stem}.json'

    with open(filename, 'w') as out:
        out.write(content)


def format_output(input_string):
    return re.sub(r'-(?=.+\"\:)', r'_', input_string)

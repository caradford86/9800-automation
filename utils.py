import re
import socket
from time import time, sleep

from jinja2 import Template
import requests

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


def create_templates(jinja_template, data):
    with open(jinja_template) as f:
        template = Template(f.read())
        config_snippet = template.render(data)
    return config_snippet


def write_template_to_config(inputfile, config_snippet, rendered_config):
    with open(inputfile) as f:
        input_data = f.read()
    input_data += config_snippet
    with open(rendered_config, 'w') as f:
        f.write(input_data)


def socket_check(ip, port=22, socket_timeout=1, scan_timeout=400, retry=1, message_to_display=10):
    '''
    Socket Check

    This function will continually check an ip and port to see if it is
    responding.

    Args:
        ip(str): IP of the device
        port(int): Port to check. Default to 22.
        socket_timeout(int): Amount of time in seconds to wait for socket
                             to respond.
        scan_timeout(int): Amount of time in seconds to scan the device.
        retry(int): Amount of time in seconds to wait before trying to
                    scan the device again.
    Returns:
        Boolean. True if port becomes responsive during the scan_timeout.
                 False is scan_timeout is reached and device is still
                   unresponsive.

    Outputs:
        None
    '''
    end_time = time() + scan_timeout
    counter = 1
    while end_time > time():
        try:
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(socket_timeout)
            a_socket.connect((ip, port))
            return True
        except Exception as e:
            if counter == message_to_display:
                print("Waiting for device to respond")
                counter = 1
            else:
                counter += 1
            sleep(retry)
        finally:
            a_socket.close()
    return False


def http_check(
    url='',
    http_verb='get',
    headers='',
    params='',
    payload='',
    auth='',
    timeout=1,
    scan_timeout=480,
    retry=1,
    message_to_display=10
):
    ''''

    '''
    end_time = time() + scan_timeout
    counter = 1
    while end_time > time():
        try:
            response = requests.request(
                http_verb,
                url=url,
                headers=headers,
                params=params,
                json=payload,
                auth=auth,
                timeout=timeout,
                verify=False)
            response.raise_for_status()
            return response
        except Exception as e:
            scan_timeout = scan_timeout - retry
            if counter == message_to_display:
                print("Waiting for device to respond")
                counter = 1
            else:
                counter += 1
            sleep(retry)
    return None

import re
import socket
from time import time, sleep

from pathlib import Path
from pprint import pprint
import json

from jinja2 import Environment, FileSystemLoader
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
    '''
    Create Template

    This function will use jinja templating to create a config snippet.

    Args:
        jinja_template(str): Filename of the jinja template.
        data(dict): Dictionary that contains the data used by the jinja
                    template.

    Returns:
        String. This is the rendered template.
    '''
    # with open(jinja_template) as f:
    # stream = f.read()
    # print(stream)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(jinja_template)

    # template = Template(f.read())
    config_snippet = template.render(data)
    return config_snippet


def write_template_to_config(inputfile, config_snippet, rendered_config):
    '''
    Write Template

    This function will merge two files and create a new file.

    Args:
        inputfule(str): Filename of the original file.
        config_snippet(str): Rendered template.
        rendered_config(str): Filename of the merged file.

    Returns:
        None
    '''
    with open(inputfile) as f:
        input_data = f.read()
    input_data += config_snippet
    with open(rendered_config, 'w') as f:
        f.write(input_data)

def socket_check(
    ip,
    port=22,
    socket_timeout=1,
    scan_timeout=400,
    retry=1,
    message_to_display=10
):
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
        message_to_display(int): Only display the message to the screen once
                                 this number has been reached. This is to
                                 cut down on the verbosity of messages to
                                 screen.
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
    HTTP Check

    This function will continually check a URL for the status code. If the
    status code is non-200 it will continue to check until the website
    returns a 200 level status code, or the max time has been reached.

    Args:
        url(str): URL to check
        http_verb(str): URL ver (get, post, put, patch, delete, etc)
        headers(str): http headers to send
        params(str): http parameters
        payload(str): http payload
        auth(str): http authentication
        timeout(int): http timeout. Default to 1 second.
        scan_timeout(int): Amount of time in seconds to retry before
                           website is considered unresponsive.
        retry(int): Amount of time to wait before retrying.
        message_to_display(int): Only display the message to the screen once
                                 this number has been reached. This is to
                                 cut down on the verbosity of messages to
                                 screen.
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

def normalize(inputfile):
    # this code will format json data to make it easier to access in osiris

    # create a dictionary of various wlc data components
    wlcdata = {
        'acls': {},
        'snmp': {}
    }

    # read in json data to a string variable
    # combined_output_str = Path('combined_output.json').read_text()

    # load the string variable into json
    combined_output = inputfile

    # add a new key to the wlcdata nested dictionary and load the value with the data from combined_output 
    wlcdata['snmp']['community'] = combined_output['Cisco_IOS_XE_native:snmp_server']['Cisco_IOS_XE_snmp:community']
    wlcdata['snmp']['host_config'] = combined_output['Cisco_IOS_XE_native:snmp_server']['Cisco_IOS_XE_snmp:host_config']
    wlcdata['acls']['extacl'] = combined_output['Cisco_IOS_XE_native:access_list']['Cisco_IOS_XE_acl:extended']

    # add a new 'access_mode' key to the community dict with the value in wlcdata
    communities = wlcdata['snmp']['community']
    for community in communities:
        if community.get('RO'):
            community['access_mode'] = 'RO'
        elif community.get('RW'):
            community['access_mode'] = 'RW'

    # add a new 'type' key to the community dict with the value in wlcdata
    snmp_hosts = wlcdata['snmp']['host_config']['ip_community_port']
    for host in snmp_hosts:
        if host.get('informs'):
            host['type'] = 'informs'
        else:
            host['type'] = 'traps'

    # format acl data based on source address

    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('any'):
                    seq['source'] = 'any'
                    seq['source_mask'] = '0.0.0.0'
                elif seq['ace_rule'].get('host'):
                    seq['source'] = seq['ace_rule'].get('host')
                    seq['source_mask'] = '255.255.255.255'
                elif seq['ace_rule'].get('ipv4_address'):
                    seq['source'] = seq['ace_rule'].get('ipv4_address')
                    seq['source_mask'] = seq['ace_rule'].get('mask')

    # format acl data based on destination address
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('dst_any'):
                    seq['destination'] = 'any'
                    seq['dest_mask'] = '0.0.0.0'
                elif seq['ace_rule'].get('dst_host'):
                    seq['destination'] = seq['ace_rule'].get('dst_host')
                    seq['dest_mask'] = '255.255.255.255'
                elif seq['ace_rule'].get('dest_ipv4_address'):
                    seq['destination'] = seq['ace_rule'].get('dest_ipv4_address')
                    seq['dest_mask'] = seq['ace_rule'].get('dest_mask')

    # format acl data based on source port
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('src_eq'):
                    src_port = str(seq['ace_rule'].get('src_eq'))
                    seq['src_port'] = f'eq {src_port}'
                elif seq['ace_rule'].get('src_gt'):
                    seq['src_port'] = 'gt ' + str(seq['ace_rule'].get('src_gt'))
                elif seq['ace_rule'].get('src_lt'):
                    seq['src_port'] = 'lt ' + str(seq['ace_rule'].get('src_lt'))
                elif seq['ace_rule'].get('src_neq'):
                    seq['src_port'] = 'neq ' + str(seq['ace_rule'].get('src_neq'))
                elif seq['ace_rule'].get('src_range1'):
                    seq['src_port'] = str(seq['ace_rule'].get('src_range1')) + ' - ' + str(seq['ace_rule'].get('src_range2'))
                else:
                    seq['src_port'] = ' '

    # format acl data based on destination port
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('dst_eq'):
                    seq['dst_port'] = 'eq ' + str(seq['ace_rule'].get('dst_eq'))
                elif seq['ace_rule'].get('dst_gt'):
                    seq['dst_port'] = 'gt ' + str(seq['ace_rule'].get('dst_gt'))
                elif seq['ace_rule'].get('dst_lt'):
                    seq['dst_port'] = 'lt ' + str(seq['ace_rule'].get('dst_lt'))
                elif seq['ace_rule'].get('dst_neq'):
                    seq['dst_port'] = 'neq ' + str(seq['ace_rule'].get('dst_neq'))
                elif seq['ace_rule'].get('dst_range1'):
                    seq['dst_port'] = str(seq['ace_rule'].get('dst_range1')) + ' - ' + str(seq['ace_rule'].get('dst_range2'))
                else:
                    seq['dst_port'] = ' '

    # add key for dscp
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('dscp'):
                    seq['dscp'] = seq['ace_rule'].get('dscp')
                else:
                    seq['dscp'] = 'None'

    # add key for log
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('log'):
                    seq['log'] = 'Enabled'
                else:
                    seq['log'] = 'Disabled'

    # add key for action
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('action'):
                    seq['action'] = seq['ace_rule'].get('action')

    # add key for protocol
    for acl in wlcdata['acls']['extacl']:
        sequences = acl.get('access_list_seq_rule')
        if sequences is not None:
            for seq in sequences:
                if seq['ace_rule'].get('protocol'):
                    seq['protocol'] = seq['ace_rule'].get('protocol')

    # add wlcdata to combined_output variable for single file load into osiris
    combined_output.update(wlcdata)

    # write combined_output variable to normalized_output file
    with open('normalized_output.json', 'w') as outfile:
        json.dump(combined_output, outfile)

import argparse
# import time

from netmiko import ConnectHandler
from netmiko import file_transfer
import yaml

from documentation import document
from http_check import http_check
from socket_check import socket_check

DEVICEFILE = "data.yaml"


def reboot_device(conn):
    print('Reload initiated')
    output = conn.send_command_timing('reload', delay_factor=6)
    if "confirm" in output:
        output += conn.send_command_timing(
            "\n", strip_command=False, strip_prompt=False
        )
    else:
        print('Reloading')


def parse_cli():
    parser = argparse.ArgumentParser(description='Configure WLC')
    parser.add_argument('-c', '--config',
                        help='Path to staging WLC config file [config.yml]',
                        default=DEVICEFILE)
    parser.add_argument('-i', '--input-file',
                        help='Path to Translated_Config file [Translated_Config.cfg]',
                        default='input/Translated_Config.cfg')
    parser.add_argument('-d', '--dest-file',
                        help='Output filename',
                        default='initial.cfg')
    args = parser.parse_args()
    return args


def main():
    cli_args = parse_cli()
    devicefile = cli_args.config
    inputfile = cli_args.input_file
    destfile = cli_args.dest_file

    # load device file
    with open(devicefile) as f:
        data = yaml.safe_load(f.read())
        device = data.get('controller')

    # open SSH connection
    net_connect = ConnectHandler(**device)

    # enable SCP on the controller
    net_connect.send_config_set(['ip scp server enable'])

    # copy the configuration to flash
    print('Copying Translated_Config.cfg to flash')
    file_transfer(net_connect, source_file=inputfile, dest_file=destfile)

    # copy the file in flash to the startup-config and accept the prompt
    try:
        print('Copying flash:Translated_Config.cfg to startup-config')
        output = net_connect.send_command_timing('copy flash:initial.cfg startup-config')
        if "filename" in output:
            output += net_connect.send_command_timing(
                "\n", strip_command=False, strip_prompt=False
            )
        else:
            print('Translated_Config.cfg copied to startup-config successfully')
    except ValueError as error:
        if 'already exists' in str(error):
            print('File already present in controller flash, please move or rename and run the script again')
        else:
            raise error

    reboot_device(net_connect)
    net_connect.disconnect()

    port = data.get('api_port')
    protocol = 'https' if port == 443 else 'http'
    url = f"{protocol}://{device['host']}"
    endpoint = data.get('check_endpoint', '/restconf/data/ietf-yang-library:modules-state')
    headers = {
        'content-type': 'application/yang-data+json',
        'accept': 'application/yang-data+json'
    }
    username = device.get('username')
    pw = device.get('password')
    auth = (username, pw)

    nginx_is_up = http_check(
        url=f"{url}{endpoint}",
        headers=headers,
        auth=auth
    )
    netconf_is_up = socket_check(ip=device['host'], port=830)

    if nginx_is_up and netconf_is_up:
        print('Data collection initiated')
        document()
    else:
        print('Device did not come up before timeout expired')


if __name__ == "__main__":
    main()

import argparse

from netmiko import ConnectHandler
from netmiko import file_transfer
import yaml

from socket_check import socket_check
from documentation import document


DEVICEFILE = "config.yml"


def reboot_device(conn):
    print('reload initiated')
    output = conn.send_command_timing('reload', delay_factor=6)
    print(output)
    if "confirm" in output:
        print('sending new line')
        output += conn.send_command_timing(
            "\n", strip_command=False, strip_prompt=False
        )
    else:
        print('prompt not detected')


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
        device = yaml.safe_load(f.read())

    # open SSH connection
    net_connect = ConnectHandler(**device)

    # enable SCP on the controller
    net_connect.send_config_set(['ip scp server enable'])

    # copy the configuration to flash
    print('Transferring File')
    file_transfer(net_connect, source_file=inputfile, dest_file=destfile)

    # copy the file in flash to the startup-config and accept the prompt
    try:
        print('copying file to startup')
        output = net_connect.send_command_timing('copy flash:initial.cfg startup-config')
        print(output)
        if "filename" in output:
            print('sending new line')
            output += net_connect.send_command_timing(
                "\n", strip_command=False, strip_prompt=False
            )
        else:
            print('prompt not detected')
    except ValueError as error:
        if 'already exists' in str(error):
            print('File already exists, please move or rename and run the script again')
        else:
            raise error

    reboot_device(net_connect)
    net_connect.disconnect()

    port_is_open = socket_check(device['host'], port=22, scan_timeout=300)

    if port_is_open:
        print('Device is up')
        print('Verifying configuration')
        document()
    else:
        print('Device did not come up before timeout expired')


if __name__ == "__main__":
    main()

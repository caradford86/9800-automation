from netmiko import ConnectHandler
from netmiko import file_transfer
import logging
import yaml
import time
import socket


devicefile='homelab.yml'
timeout=300

def check_port(host, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result = a_socket.connect_ex(location)
    if result == 0:
        a_socket.close()
        return True
    return False


with open(devicefile) as f:
    device=yaml.safe_load(f.read())

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#open SSH connection
net_connect = ConnectHandler(**device)
#enable SCP on the controller
net_connect.send_config_set(['ip scp server enable'])
#copy the configuration to flash
print('Transferring File')
file_transfer(net_connect, source_file='input/Translated_Config-3.txt', dest_file='initial.cfg')
#copy the file in flash to the startup-config and accept the prompt
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

print('reload initiated')
output = net_connect.send_command_timing('reload')
print(output)
if "confirm" in output:
    print('sending new line')
    output += net_connect.send_command_timing(
        "\n", strip_command=False, strip_prompt=False
    )
else:
    print('prompt not detected')


#print(output)

net_connect.disconnect()

# while time < timeout
# attempt to connect on port 22
# if connection is unsuccessful continue
# else break and report success
counter = 0
while counter < timeout:
    is_open = check_port(device['host'], 22)
    print('checking port 22')
    if is_open:
        break
    counter +=1
    time.sleep(1)



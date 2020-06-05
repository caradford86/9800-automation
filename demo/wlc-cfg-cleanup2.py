from netmiko import ConnectHandler
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

with open('Translated_Config-3.txt') as f:
    commands = f.readlines()

net_connect = ConnectHandler(device_type='cisco_xe', host='10.1.1.111', username='cradford', password='P@22w0rd!@')

output = net_connect.send_command_timing('conf t')

for cmd in commands:    
    output += net_connect.send_command_timing(cmd, strip_command=False, strip_prompt=False)
    if 'you want to continue' in output:
        output += net_connect.send_command_timing('\n', strip_command=False, strip_prompt=False)

print(output)

net_connect.disconnect()
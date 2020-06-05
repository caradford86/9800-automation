from netmiko import ConnectHandler
import logging
import yaml
devicefile='homelab.yml'
with open(devicefile) as f:
    device=yaml.safe_load(f.read())

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

with open('input/Translated_Config-3.txt') as f:
    commands = f.readlines()

net_connect = ConnectHandler(**device)
try:
    output = net_connect.send_config_set(commands, strip_command=False, strip_prompt=False)
    if 'you want to continue' in output:
        output += net_connect.send_command_timing('\n', strip_command=False, strip_prompt=False)
except Exception:
    output += net_connect.send_command_timing('\n', strip_command=False, strip_prompt=False)

print(output)

net_connect.disconnect()
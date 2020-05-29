import re
import paramiko
import time
import cmd
import sys
 
fin = open("Translated_Config.cfg", "r")
fout = open("Translated_Config-2.cfg", "w")

for line in fin:
    fout.write(re.sub(r'^\s*!.*', r'', line))

fin.close()
fout.close()

with open("Translated_Config-2.cfg") as infile, open("Translated_Config-3.txt", "w") as outfile:
    for line in infile:
        if not line.strip(): continue
        outfile.write(line)


commands = open("Translated_Config-3.txt", "r")
buff = ''
resp = ''

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.255.131.125', username="admin", password="WWTwwt1!")
chan = client.invoke_shell()

chan.send('conf t\n')
time.sleep(1)
resp = chan.recv(9999)
output = resp.decode('ascii').split(',')

for line in commands:
    chan.send(line)
    chan.send('\n')
    time.sleep(1)
    resp = chan.recv(9999)
    output = resp.decode('ascii').split(',')

client.close()
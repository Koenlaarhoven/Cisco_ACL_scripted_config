#Before running this script, make sure there is an active PUTTY connection to the proxy server

import socks
import paramiko
import time
import sys

#Global variables
host = ''
port = 22
username = 'USER'
password = 'PASSWORD'

#User input servernumber
host_input = input('Please enter the switch you want to modify: 1, 2, 3, 4: ')

if host_input == '1':
    host = '100.100.2.' + host_input
    print('host is: ' + host)
elif host_input == '2':
    host = '100.100.2.' + host_input
    print('host is: ' + host)
elif host_input == '3':
    host = '100.100.2.' + host_input
    print('host is: ' + host)
elif host_input == '4':
    host = '100.100.2.' + host_input
    print('host is: ' + host)
else:
    print('You entered a false number, script has been terminated')
    sys.exit()

#User input for enabling or disabling the access lists
acl_onoff = input('Do you want to switch the access lists ON or OFF: ').upper()

#Socks proxy setup
sock=socks.socksocket()
sock.set_proxy(
    proxy_type=socks.SOCKS5,
    addr = '127.0.0.1',
    port = 8888,
)
sock.connect((host, port))

#SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('ignored without host key verification', username=username, password=password, sock=sock)
ssh_shell = ssh.invoke_shell()
time.sleep(0.1)

#Command function
def ssh_command(command):
    ssh_shell.send(command)
    time.sleep(0.1)

#Print function
def ssh_print(command):
    print((ssh.exec_command(command)[1]).read().decode())
    time.sleep(0.1)

#Print current access list state
print()
print('Current state of the access lists on the interfaces:')
ssh_print('Show run interface po202.100')
ssh_print('Show run interface po203.100')

#Commands to enable or disable the access lists
if acl_onoff == 'OFF':
    #Disable access lists
    ssh_command('conf t \n')
    ssh_command('Interface po100.100 \n')
    ssh_command('No ip access-group ACL-IN in \n')
    ssh_command('No ip access-group ACL-OUT out \n')
    ssh_command('exit \n')
    ssh_command('Interface po101.100 \n')
    ssh_command('No ip access-group ACL-IN in \n')
    ssh_command('No ip access-group ACL-OUT out \n')
    ssh_command('exit \n')
    ssh_command('exit \n')
    #Print intermediate results
    print('State of the access lists on the interfaces after disabling')
    ssh_print('Show run interface po100.100')
    ssh_print('Show run interface po101.100')

elif acl_onoff == 'ON':
    #Enable the access lists again
    ssh_command('conf t \n')
    ssh_command('Interface po100.100 \n')
    ssh_command('ip access-group ACL-IN in \n')
    ssh_command('ip access-group ACL-OUT out \n')
    ssh_command('exit \n')
    ssh_command('Interface po101.100 \n')
    ssh_command('ip access-group ACL-IN in \n')
    ssh_command('ip access-group ACL-OUT out \n')
    ssh_command('exit \n')
    ssh_command('exit \n')
    #Print with reactivated access lists
    print('State of the access lists on the interfaces after enabling')
    ssh_print('Show run interface po100.100')
    ssh_print('Show run interface po101.100')

else:
    print('You entered a false value for ON or OFF, script has been terminated')
    sys.exit()

print('The configuration script is finished')    
ssh.close()

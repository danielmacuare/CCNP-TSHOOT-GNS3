import paramiko
import time

ip_address = '192.168.236.128'
username = 'danielmac'
password = 'ccnplab'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username,
                   password=password)

print('Successful Connection to: ' + ip_address)

remote_connection = ssh_client.invoke_shell()

remote_connection.send('show version\n')


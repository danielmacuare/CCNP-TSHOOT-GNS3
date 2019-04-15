import netmiko

net_connect = ConnectHandler(
    device_type='cisco_ios_telnet',
    ip='192.168.236.128',
    username='danielmac',
    password='ccnplab',
    secret='ccnplab',
    global_delay_factor=2,
    banner_timeout=10,
    port=5003)

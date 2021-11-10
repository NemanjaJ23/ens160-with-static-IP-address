# Assuming static IP address for configuring local interface is an IPv4 address

import ipaddress
import subprocess
import threading

file_path = '/etc/network/interfaces'
ipv4_address = '192.168.20.20'
default_gateway = '192.168.20.1'
restart_command = '/etc/init.d/networking restart'

interface_config_template = '''
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto ens160
iface ens160 inet static
    address %(ipv4_address)s
    netmask %(ipv4_subnet_mask)s
    gateway %(ipv4_gateway)s
'''

ip_address = ipaddress.IPv4Network(ipv4_address)
network_interface_parameters = dict()
network_interface_parameters['ipv4_address'] = ipv4_address
network_interface_parameters['ipv4_subnet_mask'] = ip_address.netmask
network_interface_parameters['ipv4_gateway'] = default_gateway

ip_config = interface_config_template % network_interface_parameters

# lock would not be needed in this simple case, but needed if there could potentially be two or more threads that
# try to write to the file at the same time
lock = threading.Lock()

with lock:
    interfaces_file = open(file_path, mode='w')
    interfaces_file.write(ip_config)

# restarting the service for changes to apply
subprocess.call(restart_command, shell=True)

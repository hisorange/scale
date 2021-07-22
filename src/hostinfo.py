import socket

import netifaces


class HostInfo:
    def __init__(self, config):
        self.config = config
        self.host_name = socket.gethostname()
        self.network_interfaces = self.gather_interfaces()
        self.private_ip_addresses = self.get_private_ips()
        self.public_ip_addresses = self.get_public_ips()

    def get_host_info(self):
        host_info = {
            'host_name': self.host_name,
            'network_interfaces': self.network_interfaces,
            'private_ip_addresses': self.private_ip_addresses,
            'public_ip_addresses': self.public_ip_addresses
        }

        return host_info


    def gather_interfaces(self):
        network_interfaces = []
        for interface in netifaces.interfaces():
            try:
                network_interfaces.append(netifaces.ifaddresses(interface)[netifaces.AF_INET][0])
            except:
                pass

        return network_interfaces


    def get_private_ips(self):
        private_ip_addresses = []
        for iface in self.network_interfaces:
            if iface['addr'].startswith('10.') or iface['addr'].startswith('192.168.') or iface['addr'].startswith('172.'):
                private_ip_addresses.append(iface)

        return private_ip_addresses

    def get_public_ips(self):
        public_ip_addresses = []
        for iface in self.network_interfaces:
            if not iface['addr'].startswith('10.') and not iface['addr'].startswith('192.168.') and not iface['addr'].startswith('172.') and not iface['addr'] == '127.0.0.1':
                public_ip_addresses.append(iface)

        return public_ip_addresses

    def get_free_port(self):
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port


# port = find_free_port()
# print(port)
# s = connect_on_udp_port(port)
# #s.sendto(b'mysupersecretkey!', ('127.0.0.1',port))
# data,addr = s.recvfrom(1024)
# print({ "data": data, "addr": addr })
# s.detach()
# s.close()

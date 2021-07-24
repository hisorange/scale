from socket import gethostname

import netifaces

from scale.network.interface import Interface


class Host:
    def __init__(self, config):
        self.config = config
        self.hostname = gethostname()

    def gather_interfaces(self) -> list:
        interfaces = []
        for name in netifaces.interfaces():
            try:
                ip = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['addr']
                netmask = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['netmask']
                gate = netifaces.gateways()['default'][netifaces.AF_INET]

                if gate[1] == name:
                    gateway = gate[0]
                else:
                    gateway = None

                broadcast = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['broadcast']

                # Initialize into a local data structure
                interface = Interface(
                    name=name, ip=ip, netmask=netmask, gateway=gateway, broadcast=broadcast)

                # Push to the list of interfaces
                interfaces.append(interface)
            except:
                pass

        return interfaces

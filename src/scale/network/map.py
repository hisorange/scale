from scale.host import Host
from scale.logger import create_logger
from scale.network.node import Node
from scale.vpn import VPNManager


class Map:
    def __init__(self, config, vpn: VPNManager) -> None:
        self.logger = create_logger(self.__class__.__name__)
        self.config = config
        self.vpn = vpn
        self.host: Node = None
        self.nodes = {}
        self.is_joined = False
        pass

    def add_node(self, node: Node) -> None:
        if not node.hostname in self.nodes:
            self.nodes[node.hostname] = node

            if len(self.nodes) > 1:
                self.join()
        else:
            self.logger.warn(f"Node already exists [{node.hostname}]")

    def get_host(self) -> Node:
        return self.host

    def create_host(self) -> None:
        host = Host()
        node = Node(host.hostname)

        node.is_local = True
        node.set_public_key(self.config.network["publicKey"])

        for iface in host.gather_interfaces():
            node.add_interface(iface)

        self.host = node
        self.add_node(node)

    def join(self):
        if not self.is_joined:
            self.is_joined = True
            self.logger.info('Connection established, start the VPN')
            self.vpn.connect()

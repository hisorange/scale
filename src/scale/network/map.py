from scale.host import Host
from scale.logger import create_logger
from scale.network.node import Node


class Map:
    def __init__(self, config) -> None:
        self.logger = create_logger(self.__class__.__name__)
        self.config = config
        self.host: Node = None
        self.nodes = {}
        pass

    def add_node(self, node: Node) -> None:
        if not node.hostname in self.nodes:
            self.nodes[node.hostname] = node
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

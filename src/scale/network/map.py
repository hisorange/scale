from scale.network.node import Node
from src.scale.hostinfo import Host


class Map:
  def __init__(self, config) -> None:
    self.config = config
    self.nodes = {}
    pass

  def add_node(self, node: Node) -> None:
    self.nodes[node.hostname] = node

  def create_host_node(self):
    host = Host()
    node = Node(host.hostname)

    node.is_local = True
    node.set_public_key(self.config.network['publicKey'])

    for iface in host.gather_interfaces():
      node.add_interface(iface)

    self.add_node(node)


from time import time

from scale.network.interface import Interface

# Node is considered to be active if it was seen in the last 5 seconds
NETWORK_ALIVE_TIMEOUT = 5


class Node:
    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        self.publicKey: str = None
        self.interfaces: list[Interface] = []
        self.last_seen: float = None
        self.is_local: bool = False

    def add_interface(self, interface: Interface) -> None:
        if (interface.ip != "" and
            interface.ip != "127.0.0.1" and
            interface.ip != "::1" and
            interface.ip != "0.0.0.0" and
                interface.name != "lo"):
            self.interfaces.append(interface)

    def set_public_key(self, publicKey: str) -> None:
        self.publicKey = publicKey

    def is_alive(self) -> bool:
        if self.is_local:
            return True

        if self.last_seen is None:
            return False

        return (time() - self.last_seen) < NETWORK_ALIVE_TIMEOUT

    def is_dead(self) -> bool:
        return not self.is_alive()

    def to_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "publicKey": self.publicKey,
            "interfaces": [interface.to_dict() for interface in self.interfaces],
        }

    def from_dict(d: dict):
        node = Node(d['hostname'])
        node.set_public_key(d['publicKey'])
        for interface_dict in d['interfaces']:
            node.add_interface(Interface.from_dict(interface_dict))

        return node

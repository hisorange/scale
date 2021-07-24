from time import time

from scale.network.interface import Interface

# Node is considered to be active if it was seen in the last 5 seconds
NETWORK_ALIVE_TIMEOUT = 5


class Node:
    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        self.publicKey = None
        self.interfaces = []
        self.last_seen = None
        self.is_local = False

    def add_interface(self, interface: Interface) -> None:
        if interface.ip != "127.0.0.1" and interface.name != "lo":
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

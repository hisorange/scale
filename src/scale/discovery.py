import asyncio
import socket

from aioudp import UDPServer

from scale.logger import create_logger
from scale.network.map import Map
from scale.network.message import Message
from scale.udpserver import DiscoveryUDPServer


# TODO: use protobuf to serialize the message
# TODO: use zeromq to send the messages
# TODO: keep the UDP server running until for discovery
class Discovery:
    def __init__(self, config, loop: asyncio.AbstractEventLoop, network: Map):
        self.config = config
        self.loop = loop
        self.network = network
        self.logger = create_logger(self.__class__.__name__)

    async def run(self):
        self.logger.info('Starting discovery server')
        await self.start_udp_server()
        asyncio.ensure_future(self.run_discovery(), loop=self.loop)

    async def start_udp_server(self):
        udp_srv = UDPServer()
        udp_srv.run("0.0.0.0", int(
            self.config.network['discoveryPort']), loop=self.loop)
        # Allow to send to broadcast addresses
        udp_srv._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.server = DiscoveryUDPServer(
            server=udp_srv, loop=self.loop, config=self.config, network=self.network)

    async def run_discovery(self):
        while True:
            # First we check for entrypoints
            if len(self.config.entryPoints) > 0:
                await self.try_discovery_entrypoints()

            # Then we check for broadcast addresses
            await self.try_broadcast_addresses()

            self.logger.info('Discovery round finished')
            await asyncio.sleep(5)

    async def try_discovery_entrypoints(self):
        host = self.network.get_host()

        for entrypoint in self.config.entryPoints:
            if not self.is_known_node(entrypoint):
                await self.server.send_packet(entrypoint, Message('hello', host))

    def is_known_node(self, address: str):
        for node in self.network.nodes.values():
            for iface in node.interfaces:
                if iface.ip == address or iface.broadcast == address:
                    return True

    async def try_broadcast_addresses(self):
        host = self.network.get_host()

        for iface in host.interfaces:
            if not self.is_known_node(iface.broadcast):
                await self.server.send_packet(iface.broadcast, Message('hello', host))
                await asyncio.sleep(.5)

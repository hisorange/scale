import asyncio

from aioudp import UDPServer

from scale.logger import create_logger
from scale.udpserver import DiscoveryUDPServer


# TODO: Make this into context manager
class Discovery:
    def __init__(self, config, loop: asyncio.AbstractEventLoop):
        self.config = config
        self.loop = loop
        self.logger = create_logger(self.__class__.__name__)

    async def run(self):
        self.logger.info('Starting discovery server')
        await self.start_udp_server()

    async def start_udp_server(self):
        udp_srv = UDPServer(download_speed=100, upload_speed=100)
        udp_srv.run("0.0.0.0", int(
            self.config.network['discoveryPort']), loop=self.loop)

        self.server = DiscoveryUDPServer(
            server=udp_srv, loop=self.loop, config=self.config)

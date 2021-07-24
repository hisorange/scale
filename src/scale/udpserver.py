import asyncio

from aioudp.server import UDPServer

from scale.aes import AESCipher
from scale.logger import create_logger


class DiscoveryUDPServer:
    def __init__(self, server: UDPServer, loop, config):
        self.server = server
        self.loop = loop
        self.config = config
        self.logger = create_logger(self.__class__.__name__)
        self.create_network_key()

        # Subscribe for incoming udp packet event
        self.server.subscribe(self.handle_incoming)
        asyncio.ensure_future(self.send_discovery_packets(), loop=self.loop)

    def create_network_key(self):
        self.logger.info('Network key is calculated')
        crypter = AESCipher(self.config.network['passKey'])
        self.nkey = crypter.encrypt('hello')
        self.logger.info('Key is [{}]'.format(self.nkey))


    # Handle messages
    async def handle_incoming(self, data, addr):
        self.logger.info(f'Received from [{data}]: {addr}')

        data_str = str(data).replace('\n', '')

        # Check for valid key
        if data_str != self.nkey:
            self.logger.warning(f'Invalid key: [{data_str}]')
        else:
            self.logger.info(f'Valid key: [{data_str}]')

    async def send_discovery_packets(self):
        while True:
            for entry in self.config.entryPoints:
                await self.send_packet(entry)

    async def send_packet(self, ip):
        self.logger.debug('Sending discovery packet to [{}]'.format(ip))
        self.server.send(self.nkey, (ip, self.config.network['discoveryPort']))

        await asyncio.sleep(1)

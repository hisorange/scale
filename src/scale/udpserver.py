import asyncio

from aioudp.server import UDPServer

from scale.aes import AESCipher
from scale.logger import create_logger
from scale.network.map import Map
from scale.network.message import Message
from scale.network.node import Node


class DiscoveryUDPServer:
    def __init__(self, server: UDPServer, loop, config, network: Map):
        self.server = server
        self.loop = loop
        self.config = config
        self.network = network
        self.logger = create_logger(self.__class__.__name__)
        self.cipher = AESCipher(self.config.network['passKey'])

        # Subscribe for incoming udp packet event
        self.server.subscribe(self.handle_incoming_message)

    # Handle messages
    async def handle_incoming_message(self, data, addr):
        self.logger.info(f'New message arrived from [{addr}]')

        # Decrypt message
        data = (data)

        # Create message instance
        try:
            message: Message = Message.from_bytes(data)

            line = '-' * 80

            self.logger.debug(f'Message type: {message.type}')
            self.logger.debug(
                f'Message data:\n{line}\n{message.payload}\n{line}')

            if message.type == 'hello':
                self.logger.info(f'New [hello] message from [{addr}]')
                self.network.add_node(Node.from_dict(message.payload))

        except Exception as e:
            self.logger.error(f'Failed to parse message: {e}')

    async def send_packet(self, ip, message: Message):
        self.logger.debug(
            'Sending message [{}] to [{}]'.format(message.type, ip))

        # Address the message
        message.recipient = ip

        # Encrypt message
        payload = (message.to_bytes())

        self.server.send(payload, (ip, self.config.network['discoveryPort']))
        await asyncio.sleep(.1)
        pass

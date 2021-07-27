import asyncio

import zmq
import zmq.asyncio
from pymitter import EventEmitter


class Coordinator:
    def __init__(self, loop: asyncio.AbstractEventLoop, event_bus: EventEmitter):
        self.loop = loop
        self.event_bus = event_bus

    def connect(self):
        self.context = zmq.asyncio.Context.instance()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(self.address)

        self.subscribe()

    def subscribe(self):
        self.loop.ensure_futures(self.handle_incoming(), self.loop)
        self.loop.ensure_futures(self.publish(), self.loop)

    async def handle_incoming(self,):
        msg = await self.sock.recv_multipart()
        # Decode protobuf
        print(msg)
        # Dispatch to listeners
        self.event_bus.emit('message.message_type', msg)

    async def send(self, reply):
        # Encode protobuf
        await self.socket.send_multipart(reply)

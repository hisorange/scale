import uuid
from time import time

import msgpack
from scale.network.node import Node


class Message:
    def __init__(self, type: str, payload) -> None:
        self.id = str(uuid.uuid4())
        self.type = type
        self.recipient: str = None

        self.payload = payload

    def to_bytes(self) -> bytes:

        payload = self.payload

        if isinstance(payload, Node):
            payload = payload.to_dict()

        return msgpack.packb({
            "meta": {
                "id": self.id,
                "type": self.type,
                "recipient": self.recipient,
                "created": time()
            },
            "payload": payload,
        })

    def from_bytes(data: bytes):
        dict = msgpack.unpackb(data)
        msg = Message(dict["meta"]["type"], dict["payload"])

        msg.id = dict["meta"]["id"]
        msg.recipient = dict["meta"]["recipient"]

        return msg

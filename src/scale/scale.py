import asyncio

from scale.config import Config
from scale.dependencymanager import DependencyManager
from scale.discovery import Discovery
from scale.hostinfo import Host
from scale.logger import create_logger
from scale.network.map import Map
from scale.network.node import Node
from scale.vpn import VPN


async def start_scale(loop: asyncio.AbstractEventLoop):
    config = Config()
    config.load()

    DependencyManager().prepare_necessities()

    vpn = VPN(config)
    vpn.bootstrap()
    vpn.start()

    # Create the network map
    network = Map(config)
    network.create_host_node()

    # Start the discovery service
    discovery = Discovery(config, loop)
    await discovery.run()

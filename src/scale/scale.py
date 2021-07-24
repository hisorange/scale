import asyncio

from scale.config import Config
from scale.dependencymanager import DependencyManager
from scale.discovery import Discovery
from scale.network.map import Map
from scale.vpn import VPN


async def start_scale(loop: asyncio.AbstractEventLoop):
    config = Config()
    config.load()

    DependencyManager()

    vpn = VPN(config)
    vpn.bootstrap()
    vpn.start()

    # Create the network map
    network = Map(config)
    network.create_host()

    # Start the discovery service
    discovery = Discovery(config, loop, network=network)
    await discovery.run()

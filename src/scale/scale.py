import asyncio

from pymitter import EventEmitter

from scale.config import Config
from scale.dependencymanager import DependencyManager
from scale.discovery import Discovery
from scale.network.map import Map
from scale.vpn import VPNManager


async def start_scale(loop: asyncio.AbstractEventLoop):
    config = Config()
    config.load()

    event_bus = EventEmitter()

    DependencyManager()

    vpn = VPNManager(config)
    vpn.bootstrap()

    # Create the network map
    network = Map(config, vpn)
    network.create_host()

    # Start the discovery service
    discovery = Discovery(config, loop, network=network)
    await discovery.run()

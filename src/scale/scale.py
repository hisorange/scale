import asyncio

from scale.config import Config
from scale.dependencymanager import DependencyManager
from scale.discovery import Discovery
from scale.hostinfo import HostInfo
from scale.logger import create_logger
from scale.vpn import VPN


async def start_scale(loop: asyncio.AbstractEventLoop):
    logger = create_logger('Scale')

    config = Config()
    config.load()

    DependencyManager().prepare_necessities()


    vpn = VPN(config)
    vpn.bootstrap()

    logger.info('VPN is ready to start')

    host_info = HostInfo(config)
    # host_info_json = json.dumps(host_info.get_host_info(), sort_keys=True, indent=2);
    # logger.info('Host information {}'.format(host_info_json))

    vpn.start()

    disc = Discovery(config, loop)
    try:
        await disc.run()
    except KeyboardInterrupt:
        pass

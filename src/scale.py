import json

from config import Config
from hostinfo import HostInfo
from logger import create_logger
from vpn import VPN


def main():
    logger = create_logger('Scale')

    config = Config()
    config.load()

    vpn = VPN(config)
    vpn.bootstrap()

    logger.info('VPN is ready to start')

    host_info = HostInfo(config)
    host_info_json = json.dumps(host_info.get_host_info(), sort_keys=True, indent=2);

    logger.info('Host information {}'.format(host_info_json))

    vpn.start()


if __name__ == '__main__':
    main()

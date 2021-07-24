import os
import random
import string
from configparser import ConfigParser

from scale.logger import create_logger
from scale.network.node import Node


class VPNManager:
    def __init__(self, config):
        self.logger = create_logger('VPN')
        self.config = config
        self.nodes: list[Node] = []
        self.iface = self.config.network['interface']
        pass

    def bootstrap(self):
        # Check if the VPN is running
        if (len(self.config.network['passKey']) == 0):
            self.logger.info('No passkey found. Preparing one')
            self.config.network['passKey'] = self.generate_pass_key(32)
            self.config.save()

        if (len(self.config.network['publicKey']) < 1 or len(self.config.network['privateKey']) < 1):
            self.logger.info('No keys found. Generating...')
            self.generate_keys()

        self.generate_wg_config()

        self.logger.info('Bootstrapped VPN...')

    def check_if_wg_running(self):
        result = os.system('ip a | grep {}'.format(
            self.iface))

        if (result == 0):
            return True
        else:
            return False

    def generate_wg_config(self) -> None:
        config_path = os.path.join(
            '/etc/wireguard', '{}.conf'.format(self.iface))

        self.logger.info('Generating WG config [{}]'.format(config_path))

        with open(config_path, 'w') as f:
            iconfig = ConfigParser()
            iconfig.optionxform = str
            iconfig.add_section('Interface')
            iconfig.set('Interface', 'PrivateKey',
                        self.config.network['privateKey'])
            iconfig.set('Interface', 'Address ', '10.0.1.1/24')
            iconfig.set('Interface', 'ListenPort ', str(
                self.config.network['discoveryPort'] - 1))

            for node in self.nodes:
                iconfig.add_section('Interface')
                iconfig.set('Interface', 'PublicKey', node.public_key)

                # TODO: Add support for multiple interfaces~
                for iface in node.interfaces:
                    if iface.name == self.iface:
                        iconfig.set('Interface', 'Address', iface.ip)

            iconfig.write(f)

        pass

    def generate_pass_key(self, length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_keys(self):
        privateKey = os.popen('wg genkey').read().replace('\n', '')
        publicKey = os.popen('echo {} | wg pubkey'.format(
            privateKey)).read().replace('\n', '')

        self.config.network['privateKey'] = privateKey
        self.config.network['publicKey'] = publicKey

        self.logger.info('Private key: {}'.format(privateKey))
        self.logger.info('Public key: {}'.format(publicKey))

        self.config.save()

        pass

    def connect(self):
        # Restart with the new config
        if self.check_if_wg_running():
            self.stop()

        self.generate_wg_config()

        exit_code = os.system('wg-quick up {}'.format(self.iface))

        if (exit_code == 0):
            self.logger.info('WireGuard started')
        else:
            self.logger.fatal('WireGuard failed to start')

    def stop(self):
        exit_code = os.system(
            'wg-quick down {}'.format(self.iface))

        if (exit_code == 0):
            self.logger.info('WireGuard stopped')
        else:
            self.logger.fatal('WireGuard failed to stop')

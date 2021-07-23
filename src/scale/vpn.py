import os
import random
import string
from configparser import ConfigParser

from scale.logger import create_logger


class VPN:
    def __init__(self, config):
      self.logger = create_logger('VPN')
      self.config = config
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

    def generate_wg_config(self) -> None:
      config_path = os.path.join('/etc/wireguard', '{}.conf'.format(self.config.network['interface']))

      self.logger.info('Check for existing WG config [{}]'.format(config_path))

      if (os.path.isfile(config_path)):
        self.logger.info('WG config already exists. Skipping...')
      else:
        self.logger.info('Generating WG config [{}]'.format(config_path))

        with open(config_path, 'w') as f:
          iconfig = ConfigParser()
          iconfig.optionxform = str
          iconfig.add_section('Interface')
          iconfig.set('Interface', 'PrivateKey', self.config.network['privateKey'])
          iconfig.set('Interface', 'Address ', '10.0.1.1/24')
          iconfig.set('Interface', 'ListenPort ', str(self.config.network['discoveryPort'] - 1))

          iconfig.write(f)

      pass


    def generate_pass_key(self, length):
      return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_keys(self):
      privateKey = os.popen('wg genkey').read().replace('\n', '')
      publicKey = os.popen('echo {} | wg pubkey'.format(privateKey)).read().replace('\n', '')

      self.config.network['privateKey'] = privateKey
      self.config.network['publicKey'] = publicKey

      self.logger.info('Private key: {}'.format(privateKey))
      self.logger.info('Public key: {}'.format(publicKey))

      self.config.save()

      pass

    def start(self):
      exit_code = os.system('wg-quick up {}'.format(self.config.network['interface']))

      if (exit_code == 0):
        self.logger.info('WireGuard started')
      else:
        self.logger.fatal('WireGuard failed to start')


    def stop(self):
      exit_code = os.system('wg-quick down {}'.format(self.config.network['interface']))

      if (exit_code == 0):
        self.logger.info('WireGuard stopped')
      else:
        self.logger.fatal('WireGuard failed to stop')


    # def __del__(self):
    #   self.logger.info('Closing VPN')
    #   self.stop()
    #   pass

import json
import os

from scale.logger import create_logger


class Config:
  def __init__(self) -> None:
    self.logger = create_logger('Config')
    pass

  def check_local_path(self) -> bool:
    return os.path.exists(self.get_local_path())

  def get_local_path(self) -> str:
    return '/etc/scale/config.json'

  def load(self) -> None:
    self.logger.info('Loading config')

    if not self.check_local_path():
      self.create_config()

    with open(self.get_local_path(), 'r') as f:
      self.__dict__.update(json.load(f))

  def create_config(self)-> None:
    self.logger.info('Creating config')
    directory = os.path.dirname(self.get_local_path())

    if not os.path.exists(directory):
      os.makedirs(directory)

    with open(self.get_local_path(), 'w') as f:
      json.dump({
        "network": {
          "passKey": "",
          "publicKey": "",
          "privateKey": "",
          "interface": "wgscale",
          "discoveryPort": 56124
        },
        "entryPoints": [
          "192.168.56.101",
          "192.168.56.102",
          "192.168.56.103",
          "192.168.56.104",
        ]
      }, f, indent=2)

    pass

  def save(self) -> None:
    self.logger.info('Saving config')

    with open(self.get_local_path(), 'w') as f:
      json.dump({
        "network": self.network,
        "entryPoints": self.entryPoints,
      }, f, indent=2)

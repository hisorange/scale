import json
import os

from logger import create_logger


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
          "192.168.0.1:56124"
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

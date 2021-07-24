from logging import Logger

from scale.vpn import VPNManager


class MockConfig:
    def __init__(self, config):
        self.__dict__.update(config)


# should create the logger
def test_should_create_logger():
    assert isinstance(VPNManager(MockConfig({
        "network": {
            "interface": "wga"
        }
    })).logger, Logger)

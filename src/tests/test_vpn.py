from logging import Logger

from scale.vpn import VPNManager


# should create the logger
def test_should_create_logger():
    assert isinstance(VPNManager({}).logger, Logger)

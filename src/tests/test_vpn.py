from logging import Logger

from scale.vpn import VPN


# should create the logger
def test_should_create_logger():
    assert isinstance(VPN({}).logger, Logger)

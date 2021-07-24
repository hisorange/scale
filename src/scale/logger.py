import logging

import coloredlogs

fmt = '[%(asctime)s][%(levelname)8s] %(name)20s - %(message)s'
coloredlogs.install(level=logging.DEBUG, fmt=fmt)


def create_logger(name, level=logging.DEBUG, handler=None) -> logging.Logger:
    """
    Create a logger with the given name.
    """
    logger = logging.getLogger(name)
    if handler is None:
        handler = logging.StreamHandler()
    return logger

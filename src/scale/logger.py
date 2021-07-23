import logging


def create_logger(name, level=logging.DEBUG, handler=None) -> logging.Logger:
    """
    Create a logger with the given name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if handler is None:
        handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

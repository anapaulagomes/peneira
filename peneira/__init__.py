import logging


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(module)s: %(message)s"))
    logger.addHandler(stream_handler)
    return logger

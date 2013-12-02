import logging


def configure_logging(cfg):
    """
    Initialize the root logger from a HayrackConfiguration object
    """
    logger = logging.getLogger()
    logger.setLevel(cfg.logging.verbosity)

    if cfg.logging.logfile:
        logger.addHandler(logging.FileHandler(cfg.logging.logfile))
    if cfg.logging.console:
        logger.addHandler(logging.StreamHandler())

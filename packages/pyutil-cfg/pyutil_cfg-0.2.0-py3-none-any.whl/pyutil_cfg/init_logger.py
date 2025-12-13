# -*- coding: utf-8 -*-

import logging
import logging.config
from configparser import RawConfigParser

from .types import Config

from . import utils


def init_logger(name: str, config: Config) -> logging.Logger:
    logger = logging.getLogger(name)

    logger_config = {
        section: val for section, val in config.items()
        if utils.is_valid_logger_section(section)
    }

    if 'loggers' not in logger_config and 'formatters' not in logger_config and 'handlers' not in logger_config:  # noqa
        return logger

    logger_configparser = RawConfigParser()
    for section, val_by_section in logger_config.items():
        logger_configparser[section] = val_by_section

    # following logging.config.fileConfig default setting of disable_existing_loggers
    loggers: dict = logger_config.get('loggers', {})
    disable_existing_loggers = loggers.get('disable_existing_loggers', True)
    disable_existing_loggers = utils.val_to_json(disable_existing_loggers)

    try:
        logging.config.fileConfig(
            logger_configparser,
            disable_existing_loggers=disable_existing_loggers,
        )
    except Exception as e:
        logging.warning(f'unable to setup logger: e: {e}')

    return logger

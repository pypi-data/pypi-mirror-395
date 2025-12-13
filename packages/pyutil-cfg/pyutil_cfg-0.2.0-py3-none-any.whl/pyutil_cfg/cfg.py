# -*- coding: utf-8 -*-

from typing import Optional

import logging

from .types import Config
from .init_logger import init_logger
from .config_from_ini_file import config_from_ini_file
from .config_from_toml_file import config_from_toml_file
from .recursive_update import recursive_update


def init(
        name: str = '',
        filename: str = '',
        log_name: str = '',
        log_filename: str = '',
        default_params: Optional[dict] = None,
        extra_params: Optional[dict] = None,
        is_extra_params_in_file_ok: bool = True,
        is_skip_extra_params_in_file: bool = False,
        show_config: Optional[int] = None
) -> tuple[logging.Logger, Config]:
    '''
    init

    initialize the logger and config.

    Args:
        name: name to extract in the config file and as the logger name.
        filename: config filename. suffix with .toml or .ini

        log_name: opttional log-specific name
        log_filename: optional log-specific config filename.
        default_params: optional default parameters.
        extra_params: optional extra values not defined in the config filename.
                      usually from argparse.

        is_extra_params_in_file_ok:
            whether to raise error if extra_params already defined in the config file
            (as programmatically rewriting the settings from config file)
            default is ok.

        is_skip_extra_params_in_file:
            whether to skip extra_params if extra_params is in file.
            default to False as extra_params can overwrite the config in file.

        show_config: log-level in the config that shows config before return.
                     None means not showing the config.

    Return:
        logger, config
    '''
    if log_name == '':
        log_name = name
    if log_filename == '':
        log_filename = filename

    # logger
    config_from_log_file = _config_from_file(log_filename)
    logger = init_logger(log_name, config_from_log_file)

    # config
    config_from_file = _config_from_file(filename)
    config = _init_config(name, config_from_file)
    config = _post_init_config(
        name,
        config,
        default_params,
        extra_params,
        is_extra_params_in_file_ok,
        is_skip_extra_params_in_file,
        logger,
    )

    if show_config is not None:
        logger.log(show_config, f'pyutil_cfg.init: name: {name} logger-name: {log_name} config: {config}')   # noqa

    return logger, config


def _config_from_file(filename: str) -> tuple[Config]:
    if filename == '':
        return {}

    if filename.endswith('.toml'):
        config = config_from_toml_file(filename)
        return config
    elif filename.endswith('.ini'):
        config = config_from_ini_file(filename)
        return config
    else:
        raise Exception(f'not supported file type: filename: {filename}')


def _init_config(name: str, config_from_file: Config) -> dict:
    '''
    setup config from config_from_file[name]
    '''
    return config_from_file.get(name, {})


def _post_init_config(
        name: str,
        config: dict,
        default_params: Optional[dict],
        extra_params: Optional[dict],
        is_extra_params_in_file_ok: bool,
        is_skip_extra_params_in_file: bool,
        logger: logging.Logger,
) -> dict:
    '''
    add additional parameters into config
    '''

    if not default_params:
        default_params = {}

    config = recursive_update(name, default_params, config, logger, True, False)

    if not extra_params:
        return config

    config = recursive_update(
        name,
        config,
        extra_params,
        logger,
        is_extra_params_in_file_ok,
        is_skip_extra_params_in_file)

    return config

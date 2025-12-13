# -*- coding: utf-8 -*-

from typing import Any
from configparser import ConfigParser

from . import utils


def config_from_ini_file(filename: str) -> dict[str, Any]:
    '''
    get ini conf from section
    return: config: {key: val} val: json_loaded
    '''
    if not filename:
        return {}

    config_parser = ConfigParser()
    config_parser.read(filename)
    sections = config_parser.sections()

    return {section: _parse_options(config_parser, section) for section in sections}


def _parse_options(config_parser: ConfigParser, section: str) -> dict[str, Any]:
    options = config_parser.options(section)
    return {option: _parse_option(option, section, config_parser) for option in options}


def _parse_option(option: str, section: str, config_parser: ConfigParser) -> Any:
    '''
    '''
    # special treatment to logger sections (get raw values)
    if utils.is_valid_logger_section(section):
        return config_parser.get(section, option, raw=True)

    # json-formatted values for other sections.
    val = config_parser.get(section, option)
    return utils.val_to_json(val)

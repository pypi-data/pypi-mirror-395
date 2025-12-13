# -*- coding: utf-8 -*-

from typing import Any

import json


def is_valid_logger_section(section: str) -> bool:
    if section in ['loggers', 'handlers', 'formatters']:
        return True

    if section.startswith('logger_'):
        return True
    if section.startswith('handler_'):
        return True
    if section.startswith('formatter_'):
        return True

    return False


def val_to_json(val: Any) -> Any:
    '''
    try to do json load on value
    '''

    if not isinstance(val, str):
        return val

    orig_v = val
    try:
        val = json.loads(val)
    except:  # noqa
        val = orig_v

    return val

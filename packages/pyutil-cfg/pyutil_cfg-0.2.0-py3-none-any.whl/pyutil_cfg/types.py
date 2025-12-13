# -*- coding: utf-8 -*-

from enum import Enum
from typing import TypedDict

try:
    from typing import NotRequired
except:  # noqa for 3.10
    from typing_extensions import NotRequired


class FileType(Enum):
    ini = 1
    toml = 2

    def __str__(self):
        return self.name


class Loggers(TypedDict):
    keys: str
    disable_existing_loggers: NotRequired[bool]


class Logger(TypedDict):
    qualname: str
    handlers: str
    level: NotRequired[str]
    propagate: NotRequired[int | bool | str]


class Handlers(TypedDict):
    keys: str


Handler = TypedDict(
    'Handler',
    {
        'class': str,
        'args': NotRequired[str],
        'level': NotRequired[str],
        'formatter': NotRequired[str],
    }
)


class Formatters(TypedDict):
    keys: str


Formatter = TypedDict(
    'Formatter',
    {
        'format': NotRequired[str],
        'datefmt': NotRequired[str],
        'style': NotRequired[str],
        'validate': NotRequired[bool | str],
        'defaults': NotRequired[dict[str, float | int | bool | str]],
        'class': NotRequired[str],
    }
)


class Config(TypedDict):
    loggers: NotRequired[Loggers]
    handlers: NotRequired[Handlers]
    formatters: NotRequired[Formatters]

    '''
    logger_*: Logger
    '''

    '''
    handler_*: Handler
    '''

    '''
    formatter_*: Formatter
    '''

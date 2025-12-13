# -*- coding: utf-8 -*-

try:
    import tomllib
except:  # noqa for 3.10
    import tomli as tomllib

from .types import Config


def config_from_toml_file(filename: str) -> Config:
    with open(filename, 'rb') as f:
        return tomllib.load(f)

# -*- coding: utf-8 -*-

from typing import Any
import logging


def recursive_update(
        name: str,
        orig_params: Any,
        new_params: Any,
        logger: logging.Logger,
        is_new_params_in_orig_params_ok: bool,
        is_skip_new_params_in_orig_params: bool,
) -> Any:
    '''
    recursive_update

    Recursively update the values for list and dict.

    Args:
        name: config name, for log prompt purpose.
        orig_params: original parameters (from default or from file).
        new_params: new parameters (from file or from extra_params).
        logger: logger
        is_new_params_in_orig_params_ok: whether it is ok to have new params in original params
            (in dict).
        is_skip_new_params_in_orig_params: whether to skip new params if already exists in
            orig_params (in list and dict).

    Return:
        merged values of the parameters.
    '''
    if not isinstance(orig_params, type(new_params)):
        return orig_params if is_skip_new_params_in_orig_params else new_params

    if isinstance(new_params, dict):
        return _recursive_update_dict(
            name,
            orig_params,
            new_params,
            is_new_params_in_orig_params_ok,
            is_skip_new_params_in_orig_params,
            logger)

    if isinstance(new_params, list):
        return _recursive_update_list(
            name,
            orig_params,
            new_params,
            is_new_params_in_orig_params_ok,
            is_skip_new_params_in_orig_params,
            logger,
        )

    return orig_params if is_skip_new_params_in_orig_params else new_params


def _recursive_update_dict(
    name: str,
    orig_params: dict,
    new_params: dict,
    is_new_params_in_orig_params_ok: bool,
    is_skip_new_params_in_orig_params: bool,
    logger: logging.Logger,
):
    for key, val in new_params.items():
        if key not in orig_params:
            orig_params[key] = val
            continue

        if not is_new_params_in_orig_params_ok:
            logger.warning(f'config will be overwritten by extras ({name}.{key}): origin: {orig_params[key]} new: {val}')  # noqa

        orig_val = orig_params[key]
        new_val = recursive_update(
            f'{name}.{key}',
            orig_val,
            val,
            logger,
            is_new_params_in_orig_params_ok,
            is_skip_new_params_in_orig_params)
        orig_params[key] = new_val

    return orig_params


def _recursive_update_list(
    name: str,
    orig_params: list,
    new_params: list,
    is_new_params_in_orig_params_ok: bool,
    is_skip_new_params_in_orig_params: bool,
    logger: logging.Logger,
):
    orig_length = len(orig_params)
    orig_params = _extend_list(orig_params, new_params)
    if is_skip_new_params_in_orig_params:
        return orig_params

    for idx in range(orig_length):
        each = new_params[idx]
        new_val = recursive_update(
            f'{name}[{idx}]',
            orig_params[idx],
            each,
            logger,
            is_new_params_in_orig_params_ok,
            is_skip_new_params_in_orig_params)
        orig_params[idx] = new_val

    return orig_params


def _extend_list(orig_list: list, new_list: list):
    if len(orig_list) >= len(new_list):
        return orig_list

    the_new_list = new_list[len(orig_list):]

    return orig_list + the_new_list

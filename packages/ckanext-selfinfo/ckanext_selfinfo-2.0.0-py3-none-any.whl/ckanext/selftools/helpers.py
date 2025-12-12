from __future__ import annotations

from typing import Any

from ckanext.selftools import utils, config


def selftools_categories() -> list[Any]:
    return utils.get_selftools_categories()


def selftools_get_db_model_options() -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = utils.get_db_models()
    return [{"value": i.get("label"), "text": i.get("label")} for i in models]


def get_operations_limit() -> int:
    return config.selftools_get_operations_limit()


def check_operations_pwd_set() -> bool:
    return True if config.selftools_get_operations_pwd() else False

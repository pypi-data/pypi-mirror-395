"""Functions for working with projects"""

import re

import requests

from oocli import config

PATTERN = r"[\w\.\-]+"


def assert_valid(name: str):
    """Assert name is a valid project name"""
    if re.fullmatch(PATTERN, name) is None:
        raise ValueError(
            f"'{name}' is not a valid project name, only alphanumeric characters, "
            "'.', '-', and '_' are allowed"
        )


def get_name(name: str | None):
    """Get validated project name, if None, use project from config"""
    if name is None:
        name = config.CachedConfig().project
    assert_valid(name)
    return name


def read_all():
    """Retrieve all projects"""
    response = requests.get(
        f"{config.CachedConfig().apiurl}/projects",
        headers={"X-API-Key": config.CachedConfig().token},
    )
    response.raise_for_status()
    return response.json()

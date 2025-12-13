"""Functions for working with tags"""

import re

import requests

from oocli import config

PATTERN = r"[^\s/]+"


def assert_valid(name: str):
    """Assert name is a valid tag name"""
    if re.fullmatch(PATTERN, name) is None:
        raise ValueError(
            f"'{name}' is not a valid tag name, white space and '/' are not allowed"
        )


def create(name: str, run_sha: str, *, project: str):
    """Create or update a tag"""
    assert_valid(name)
    response = requests.put(
        f"{config.CachedConfig().apiurl}/tags/{project}/{name}",
        headers={"X-API-Key": config.CachedConfig().token},
        params={"sha": run_sha},
    )
    if response.status_code == 422:
        raise RuntimeError(response.text)
    response.raise_for_status()


def read_all(project: str):
    """Retreive all tags in the project"""
    response = requests.get(
        f"{config.CachedConfig().apiurl}/tags/{project}",
        headers={"X-API-Key": config.CachedConfig().token},
    )
    response.raise_for_status()
    return response.json()

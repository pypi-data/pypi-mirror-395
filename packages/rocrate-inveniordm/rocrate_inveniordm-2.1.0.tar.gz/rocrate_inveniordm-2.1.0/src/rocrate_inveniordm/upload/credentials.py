"""
    This file is used to define environment variables.

    :author: Philipp Beer
    :author: Milan Szente
    :author: Eli Chadwick
"""

import os


def get_api_key():
    api_key = os.getenv("INVENIORDM_API_KEY", None)
    if not api_key:
        raise ValueError("INVENIORDM_API_KEY environment variable not set")
    return api_key


def get_repository_base_url():
    repository_base_url = os.getenv("INVENIORDM_BASE_URL", None)
    if not repository_base_url:
        raise ValueError("INVENIORDM_BASE_URL environment variable not set")
    return repository_base_url

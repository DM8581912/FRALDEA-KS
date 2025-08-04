"""Configuration utilities for loading environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from getpass import getpass

from dotenv import load_dotenv


@dataclass
class Credentials:
    username: str
    password: str


def load_credentials(prefix: str) -> Credentials:
    """Load login credentials for a site.

    Parameters
    ----------
    prefix: str
        Prefix for the environment variables. For example, a prefix of
        ``"LEVER"`` will look for ``LEVER_USERNAME`` and ``LEVER_PASSWORD``.

    Returns
    -------
    Credentials
        The loaded username and password. If they are not found in the
        environment, the user is prompted for them.
    """
    load_dotenv()
    user_key = f"{prefix.upper()}_USERNAME"
    pass_key = f"{prefix.upper()}_PASSWORD"
    username = os.getenv(user_key)
    password = os.getenv(pass_key)

    if not username:
        username = input(f"Enter username for {prefix}: ")
    if not password:
        password = getpass(f"Enter password for {prefix}: ")

    return Credentials(username=username, password=password)

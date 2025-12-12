from __future__ import annotations

import os
from typing import Optional

DEFAULT_BASE_URL = "https://cad.milan-adhikari.com"

TOKEN_ENV_VAR = "OPTICLIENT_API_TOKEN"
BASE_URL_ENV_VAR = "OPTICLIENT_BASE_URL"


def get_default_api_token() -> Optional[str]:
    """
    Return the default API token from environment, if set.
    """
    return os.getenv(TOKEN_ENV_VAR)


def get_default_base_url() -> str:
    """
    Return the default base URL from environment or fall back
    to the hard-coded DEFAULT_BASE_URL.
    """
    return os.getenv(BASE_URL_ENV_VAR, DEFAULT_BASE_URL)

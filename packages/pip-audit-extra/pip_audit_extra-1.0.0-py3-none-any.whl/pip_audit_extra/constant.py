from pip_audit_extra.generic.path import get_cache_path

from typing import Final
from os.path import join
from os import environ


# Cache folder for generic purposes
DEFAULT_CACHE_DIR: Final[str] = join(get_cache_path(), "pip-audit-extra")
CACHE_DIR = environ.get("PAE_CACHE_DIR", DEFAULT_CACHE_DIR)

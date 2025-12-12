from zpy import EnvironmentKeys
from typing import Dict, List, Optional
from zpy.utils.collections import find
from zpy.utils import get_env as var
from re import search
import os

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


def get_schema(fn: str, env=None, schemas=None) -> str:
    """
    Get current schema according environment

    PD: You should be configured schemas list in repositories
    """
    real_env = os.getenv("env") if env is None else env
    if real_env is None:
        raise "Environment not configured"
    schema = find(schemas, lambda sc: sc["ENVIRONMENT"] == real_env)
    if schema:
        return "{}.{}".format(schema["value"], fn)
    raise "Not schema configured"


def get_schema_by(schemas: List[Dict], env=None) -> Optional[str]:
    """
    Get current schema according environment

    PD: You should be configured schemas list in repositories
    """
    real_env = os.getenv("ENVIRONMENT") if env is None else env
    if real_env is None:
        raise None
    schema = find(schemas, lambda sc: sc["ENVIRONMENT"] == real_env)
    if schema:
        return schema["value"]
    return None


def get_current_schema(schemas: List[Dict], local_emv: str = None, global_env: str = None):
    real_env = global_env if local_emv is None else local_emv
    external_env = var(str(EnvironmentKeys.ENVIRONMENT))
    real_env = external_env if real_env is None else real_env
    if real_env is not None:
        if schemas is not None:
            db_schema = get_schema_by(schemas, real_env)
            return db_schema
    return None


def displayable_message(raw_message: str, default: str = "") -> str:
    """
    Extract displayable message for emit to final client.
    The message must be wrapped by {}
    Ex: Failed {The customer provided doest exist.}
    @param raw_message: message
    @param default: if not found any message return this value.
    """
    if not raw_message:
        return default
    result = search('{(.*)}', raw_message)
    if not result:
        return default

    return result.group(1).strip()

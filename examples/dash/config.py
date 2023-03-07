from pathlib import Path
from os import getenv
from dotenv import load_dotenv, dotenv_values


def load_config(env_path=None):
    """
    Returns:
        returns a dict of env variables in dot file
    """
    if not env_path:
        env_path = Path(__file__).parent.joinpath('.env')
    load_dotenv(dotenv_path=env_path)
    return dotenv_values(dotenv_path=env_path)


def is_env_value(env_key, value):
    """
    Returns:
        True if value exists in a ENV variable
    """
    if getenv(env_key) and value in getenv(env_key).split(sep=','):
        return True
    return False


def is_enabled(feature):
    """
    Returns:
        Evaluates a string and returns a boolean
    """
    f = getenv(feature)
    if f and f in ['1','true','True','Yes','yes','y']:
        return True
    elif f and f in ['0','false','False','No','no','n']:
        return False
    # any value gives True
    elif f:
        return True
    return False
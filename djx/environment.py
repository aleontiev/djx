import os


def get_integer(key, default=0):
    """Return as an integer.

    Arguments:
        default: a default value used if the environment
            variable is undefined
    """
    value = os.environ.get(key)
    return int(value) if value else default


def get_boolean(key, default=False):
    """Return environment value as a boolean.

    Arguments:
        default: a default value used if the environment
            variable is undefined
    """
    value = os.environ.get(key)
    return value.lower() == 'true' if value else default


def get_string(key, default=''):
    """Return environment value as a string."""
    return os.environ.get(key, default)


def get_list(key, default=None, separator=','):
    """Return environment variable as a list."""
    value = os.environ.get(key)
    default = default or []
    return value.split(separator) if value else default

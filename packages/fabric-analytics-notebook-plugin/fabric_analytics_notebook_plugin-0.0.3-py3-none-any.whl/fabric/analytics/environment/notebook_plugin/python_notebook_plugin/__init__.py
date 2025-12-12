import os

from ..utils import is_pure_python_env


def in_context():
    return is_pure_python_env()

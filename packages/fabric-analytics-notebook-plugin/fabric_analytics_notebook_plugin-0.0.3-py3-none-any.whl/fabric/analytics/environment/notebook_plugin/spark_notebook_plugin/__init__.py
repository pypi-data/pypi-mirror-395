import os

from ..utils import is_fabric_spark


def in_context():
    return is_fabric_spark()

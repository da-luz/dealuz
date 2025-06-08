"""Concise package for implementing DEA"""


__all__ = [

    # definitions.py
    "DEAResult",

    # core.py
    "dea",
    "graphical_frontier",
]


import logging

from dealuz.definitions import *
from dealuz.core import *


# Silencing PuLP loggings, I hate those in production
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.WARNING)


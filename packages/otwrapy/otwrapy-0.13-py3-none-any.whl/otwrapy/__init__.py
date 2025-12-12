"""
General purpose OpenTURNS python wrapper tools
"""

# flake8: noqa

import os

__version__ = "0.13"

base_dir = os.path.dirname(__file__)

from ._otwrapy import *

__all__ = (_otwrapy.__all__)

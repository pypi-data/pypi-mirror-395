# Mock IoC Data SDK
# This module provides mock implementations to simulate the behavior of the real IoC SDK

from .core import BizContext, set_token, set_biz
from .infrastructure import *

__all__ = [
    "BizContext",
    "set_token",
    "set_biz"
]
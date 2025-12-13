from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FrameSizeRule(Enum):
    """
    Enum class representing frame size rules.

    """

    # Frame's height should be at least the value of the h attribute.
    AtLeast = 0
    # Frame's width or height should be exactly the value of the w or h attribute.
    Exact = 1
    #  Frame's width or height should be automatically.The w or h value is ignored.
    Auto = 2


from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextWrappingStyle(Enum):
    """
    Enum class to specify text wrapping style for an object.

    """

    # Inline text wrapping style
    Inline = 0
    # TopAndBottom text wrapping style
    TopAndBottom = 1
    # Square text wrapping style
    Square = 2
    # No text wrapping style
    InFrontOfText = 3
    # Tight text wrapping style
    Tight = 4
    # Through text wrapping style
    Through = 5
    # Behind text wrapping style
    Behind = 6
    # None
    none = -1


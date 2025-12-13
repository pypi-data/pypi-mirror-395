from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextWrappingType(Enum):
    """
    Enum class to specify text wrapping type for textbox.

    """

    # Wrap text both sides
    Both = 0
    # Wrap text left side
    Left = 1
    # Wrap text right side
    Right = 2
    # Wrap text largest
    Largest = 3


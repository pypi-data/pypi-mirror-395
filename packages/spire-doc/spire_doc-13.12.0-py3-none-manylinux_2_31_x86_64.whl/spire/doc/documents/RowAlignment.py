from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class RowAlignment(Enum):
    """
    Enum class for specifying the type of horizontal alignment.
    """

    # Specifies alignment to the left. 
    Left = 0
    # Specifies alignment to the center.
    Center = 1
    # Specifies alignment to the right. 
    Right = 2

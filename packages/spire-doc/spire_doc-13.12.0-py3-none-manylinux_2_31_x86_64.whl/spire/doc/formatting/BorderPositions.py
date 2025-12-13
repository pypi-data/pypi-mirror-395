from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class BorderPositions(Enum):
    """
    Enumerates the different types of borders that can be applied to elements.
    """

    #Represents no border being applied.
    none = -1
    #Represents a border at the bottom of the element.
    Bottom = 0
    #Represents a border at the left side of the element.
    Left = 1
    #Represents a border at the right side of the element.
    Right = 2
    #Represents a border at the top of the element.
    Top = 3
    #Represents a horizontal border spanning across the element (typically bottom or top).
    Horizontal = 4
    #Represents a vertical border spanning along the side of the element (typically left or right).
    Vertical = 5
    #Represents a diagonal border from the top-left to the bottom-right of the element.
    DiagonalDown = 6
    #Represents a diagonal border from the bottom-left to the top-right of the element.
    DiagonalUp = 7


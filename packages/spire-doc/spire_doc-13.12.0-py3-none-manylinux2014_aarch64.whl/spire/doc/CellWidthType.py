from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CellWidthType(Enum):
    """
    Specifies preferred width type
    """

    # No preferred width is specified.
    # The width is derived from other table measurements where a preferred size is specified, 
    # as well as from the size of the table contents, and the constraining size of the
    # container of the table.
    Auto = 1
    # Preferred table width specified in percentage
    Percentage = 2
    # Preferred table width specified in points
    Point = 3

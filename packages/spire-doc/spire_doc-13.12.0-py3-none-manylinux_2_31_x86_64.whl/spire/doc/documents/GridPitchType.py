from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class GridPitchType(Enum):
    """
    Enum class that defines how tall a grid unit is up/down.
    
    """

    # No doucment grid.
    NoGrid = 0
    # Line and Character Grid.
    CharsAndLine = 1
    # Line Grid Only.
    LinesOnly = 2
    # Character Grid Only.
    SnapToChars = 3

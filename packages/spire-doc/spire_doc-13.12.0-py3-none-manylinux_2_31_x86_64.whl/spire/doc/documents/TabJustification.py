from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TabJustification(Enum):
    """
    Enum class that specifies the tab justification.

    """

    # Left tab.
    Left = 0
    # Centered tab.
    Centered = 1
    # Right tab.
    Right = 2
    # Decimal tab.
    Decimal = 3
    # Bar.
    Bar = 4
    # List tab justification.
    List = 6
    # Clears any tab stop in this position.
    Clear = 7

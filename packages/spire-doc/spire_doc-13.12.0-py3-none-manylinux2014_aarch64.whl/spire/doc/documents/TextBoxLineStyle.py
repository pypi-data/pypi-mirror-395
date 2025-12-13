from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextBoxLineStyle(Enum):
    """
    Enum class to specify the line style of a TextBox object.
    
    """

    # Single line.
    Simple = 0
    # Double lines of equal width.
    Double = 1
    # Double lines, one thick, one thin.
    ThickThin = 2
    # Double lines, one thin, one thick.
    ThinThick = 3
    # Three lines, thin, thick, thin.
    Triple = 4

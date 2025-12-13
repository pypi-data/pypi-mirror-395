from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ShapeLineStyle(Enum):
    """
    Enum class for shape line styles.
    """

    # Single line.
    Single = 0
    # Single line.
    Double = 1
    # Double lines, one thick, one thin.
    ThickThin = 2
    # Double lines, one thin, one thick.
    ThinThick = 3
    # Three lines, thin, thick, thin.
    Triple = 4
    # Default value is <see cref="Single"/>.
    Default = 0


from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ShapeHorizontalAlignment(Enum):
    """
    Specifies horizontal alignment of a floating shape.
    """

    # The object is explicitly positioned using position properties.
    none = 0
    # The object is aligned to the left of the reference origin.
    Left = 1
    # The object is centered to the reference origin.
    Center = 2
    # The object is aligned to the right of the reference origin.
    Right = 3
    # Not documented.
    Inside = 4
    # Not documented.
    Outside = 5
    # Same as <see cref="None"/>.
    Default = 0

from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ShapeVerticalAlignment(Enum):
    """
    Specifies vertical alignment of a floating shape.
    """

    # Not documented.
    Inline = -1
    # The object is explicitly positioned using position properties.
    none = 0
    # The object is aligned to the top of the reference origin.
    Top = 1
    # The object is centered relative to the reference origin.
    Center = 2
    # The object is aligned to the bottom of the reference origin.
    Bottom = 3
    # Not documented.
    Inside = 4
    # Not documented.
    Outside = 5
    # Same as <see cref="None"/>.
    Default = 0

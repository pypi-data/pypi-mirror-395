from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HorizontalPosition(Enum):
    """
    Enum class for specifying the absolute horizontal position.
    
    """

    # Horizontal Position is null
    none = 0
    # The object is aligned to the left of the reference origin.
    Left = 1
    # The object is centered to the reference origin.
    Center = 2
    # The object is aligned to the right of the reference origin.
    Right = 3
    # "Inside" horizontal position.
    Inside = 4
    # "Outside" horizontal position.
    Outside = 5
    # Represents an inline horizontal position
    Inline = -1
    # Represents the default horizontal position
    Default = 0

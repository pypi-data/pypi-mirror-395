from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class GradientShadingVariant(Enum):
    """
    Enum class representing shading variants for background gradient.

    """
    
    # Shading in the upper part.
    ShadingUp = 0
    # Shading in the lower part.
    ShadingDown = 1
    # Shading in upper and lower parts.
    ShadingOut = 2
    # Shading in the middle.
    ShadingMiddle = 3

from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class GradientShadingStyle(Enum):
    """
    Enum class representing different gradient shading styles.
    """

    # Horizontal shading style.
    Horizontal = 0
    # Vertical shading style.
    Vertical = 1
    # Diagonal Up shading style.
    DiagonalUp = 2
    # Diagonal Down shading style.
    DiagonalDown = 3
    # FromCorner shading style.
    FromCorner = 4
    # From Center shading style.
    FromCenter = 5

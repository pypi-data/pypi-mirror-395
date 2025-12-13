from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class BackgroundType(Enum):
    """
    Enum class that specifies the type of background.
    """

    # No background fill effect.
    NoBackground = 0
    # Gradient fill effect.
    Gradient = 1
    # Picture fill effect.
    Picture = 2
    # Texture fill effect.
    Texture = 3
    # Color fill effect.
    Color = 4

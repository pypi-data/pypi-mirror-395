from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PictureColor(Enum):
    """
    Enum class representing different types of picture colors.

    """

    # Picture automatic color.
    Automatic = 0
    # Picture grayscale color.
    Grayscale = 1
    # Picture black and white color.
    BlackAndWhite = 2
    # Picture washout color.
    Washout = 3

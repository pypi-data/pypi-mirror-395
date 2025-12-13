from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CaptionPosition(Enum):
    """
    Enum class representing the position of Image Caption Numbering.
    
    """

    # Above the Image.
    AboveImage = 0
    # Above the Image.
    AfterImage = 1
    # Above the Image.
    AboveItem = 0
    # Above the Image.
    BelowItem = 1

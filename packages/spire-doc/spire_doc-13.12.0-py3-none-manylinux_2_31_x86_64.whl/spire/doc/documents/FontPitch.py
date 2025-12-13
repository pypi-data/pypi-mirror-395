from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FontPitch(Enum):
    """
    Enum class representing different font pitches.
    """

    # Specifies that no information is available about the pitch of a font.
    Default = 0
    # Specifies that this is a fixed width font.
    Fixed = 1
    # Specifies that this is a proportional width font.
    Variable = 2

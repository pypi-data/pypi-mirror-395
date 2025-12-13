from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextAlignment(Enum):
    """
    Enum class for specifying vertical font alignment for East Asian languages.

    """

    # This value specifies that characters are aligned based on the top of each character.
    Top = 0
    # This value specifies that characters are centered on the line.
    Center = 1
    # This value specifies that characters are aligned based on their baseline. 
    # This is how standard Latin text is displayed.
    Baseline = 2
    # This value specifies that characters are aligned based on the bottom of each character.
    Bottom = 3
    # This value specifies that alignment is automatically determined by the application.
    Auto = 4

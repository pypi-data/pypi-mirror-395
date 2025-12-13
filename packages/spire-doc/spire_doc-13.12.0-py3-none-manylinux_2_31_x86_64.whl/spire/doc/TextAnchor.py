from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextAnchor(Enum):
    """
    Specifies vertical alignment of a textbox.
    """

    # The object is aligned to the top of the reference origin.
    Top = 1
    # The object is centered relative to the reference origin.
    Center = 2
    # The object is aligned to the bottom of the reference origin.
    Bottom = 3

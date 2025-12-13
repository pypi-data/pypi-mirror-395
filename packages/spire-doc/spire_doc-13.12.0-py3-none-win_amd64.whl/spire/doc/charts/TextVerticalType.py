from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextVerticalType(Enum):
    """
    Specifies type of text direction.
    """

    #Horizontal type.
    Horizontal = 0
    #Vertical type.
    Vertical = 1
    #All text rot 90°.
    Vertical90 = 2
    #All text rot 270°.
    Vertical270 = 3
    #East Asian text vertical.
    EastAsianVertical = 4
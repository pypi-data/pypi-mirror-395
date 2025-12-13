from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisCategoryType(Enum):
    """
    Specifies type of a category axis.
    """
    #Specifies that type of a category axis is determined automatically based on data.
    Automatic = 0
    #Specifies an axis of an arbitrary set of categories.
    Category = 1
    #Specifies a time category axis.
    Time = 2


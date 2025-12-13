from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisScaleType(Enum):
    """
    Specifies the possible scale types for an axis.
    """
    #Linear scaling.
    Linear = 0
    #Logarithmic scaling.
    Logarithmic = 1


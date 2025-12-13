from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisCrosses(Enum):
    """
    Specifies the possible crossing points for an axis.
    """
    #The category axis crosses at the zero point of the value axis (if possible), or at the minimum value
    #if the minimum is greater than zero, or at the maximum if the maximum is less than zero.
    AutoZero = 0
    #A perpendicular axis crosses at the maximum value of the axis.
    Max = 1
    #A perpendicular axis crosses at the minimum value of the axis.
    Min = 2
    #A perpendicular axis crosses at the specified value of the axis.
    Custom = 3


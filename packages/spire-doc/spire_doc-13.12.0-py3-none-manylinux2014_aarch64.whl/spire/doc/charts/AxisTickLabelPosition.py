from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisTickLabelPosition(Enum):
    """
    Specifies the possible positions for tick labels.
    """
    #Specifies the axis labels shall be at the high end of the perpendicular axis.
    High = 0
    #Specifies the axis labels shall be at the low end of the perpendicular axis.
    Low = 1
    #Specifies the axis labels shall be next to the axis.
    NextTo = 2
    #Specifies the axis labels are not drawn.
    none = 3
    #Specifies default value of tick labels position.
    Default = 2


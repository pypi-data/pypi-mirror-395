from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisTickMark(Enum):
    """
    Specifies the possible positions for tick marks.
    """
    #Specifies that the tick marks shall cross the axis.
    Cross = 0
    #Specifies that the tick marks shall be inside the plot area.
    Inside = 1
    #Specifies that the tick marks shall be outside the plot area.
    Outside = 2
    #Specifies that there shall be no tick marks.
    none = 3


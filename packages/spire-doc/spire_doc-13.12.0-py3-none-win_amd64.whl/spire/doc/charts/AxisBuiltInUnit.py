from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisBuiltInUnit(Enum):
    """
    Specifies the display units for an axis.
    """
    #Specifies the values on the chart shall displayed as is.
    none = 0
    #Specifies the values on the chart shall be divided by a user-defined divisor. This value is not supported
    #by the new chart types of MS Office 2016.
    Custom = 1
    #Specifies the values on the chart shall be divided by 1,000,000,000.
    Billions = 2
    #Specifies the values on the chart shall be divided by 100,000,000.
    HundredMillions = 3
    #Specifies the values on the chart shall be divided by 100.
    Hundreds = 4
    #Specifies the values on the chart shall be divided by 100,000.
    HundredThousands = 5
    #Specifies the values on the chart shall be divided by 1,000,000.
    Millions = 6
    #Specifies the values on the chart shall be divided by 10,000,000.
    TenMillions = 7
    #Specifies the values on the chart shall be divided by 10,000.
    TenThousands = 8
    #Specifies the values on the chart shall be divided by 1,000.
    Thousands = 9
    #Specifies the values on the chart shall be divided by 1,000,000,000,0000.
    Trillions = 10
    #Specifies the values on the chart shall be divided by 0.01. This value is supported only by the new chart
    #types of MS Office 2016.
    Percentage = 11


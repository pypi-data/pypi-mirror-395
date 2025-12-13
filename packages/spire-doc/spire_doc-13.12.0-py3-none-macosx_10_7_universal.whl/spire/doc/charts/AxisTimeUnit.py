from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisTimeUnit(Enum):
    """
    pecifies the unit of time for axes.
    """
    #Specifies that unit was not set explicitly and default value should be used.
    Auto = 0
    # Specifies that the chart data shall be shown in days.
    Days = 1
    #Specifies that the chart data shall be shown in months.
    Months = 2
    #Specifies that the chart data shall be shown in years.
    Years = 3


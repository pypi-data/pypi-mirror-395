from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.charts import *
from spire.doc import *
from ctypes import *
import abc

class ChartAxisType(Enum):
    """
    Specifies the type for an axis.
    """

    #Category axis.
    Category = 0
    #Date axis.
    Date = 1
    #Series axis.
    Series = 2
    #Value axis.
    Value = 3


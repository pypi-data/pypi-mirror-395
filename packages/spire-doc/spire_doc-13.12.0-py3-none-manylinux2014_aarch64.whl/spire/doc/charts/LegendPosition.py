from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LegendPosition(Enum):
    """
    Specifies the possible positions for a chart legend.
    """

    #No legend will be shown for the chart.
    none = 0
    #Specifies that the legend shall be drawn at the bottom of the chart.
    Bottom = 1
    #Specifies that the legend shall be drawn at the left of the chart.
    Left = 2
    #Specifies that the legend shall be drawn at the right of the chart.
    Right = 3
    #Specifies that the legend shall be drawn at the top of the chart.
    Top = 4
    #Specifies that the legend shall be drawn at the top right of the chart.
    TopRight = 5


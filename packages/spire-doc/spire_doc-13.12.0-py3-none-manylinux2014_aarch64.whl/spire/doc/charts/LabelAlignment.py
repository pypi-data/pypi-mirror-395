from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LabelAlignment(Enum):
    """
    Specifies the possible alignment for the tick labels of chart axis.
    """

    #The labels alignment is not specified.
    Default = 0
    #Specifies that the labels are centered.
    Center = 1
    #Specifies that the labels are left justified.
    Left = 2
    #Specifies that the labels are right justified.
    Right = 3
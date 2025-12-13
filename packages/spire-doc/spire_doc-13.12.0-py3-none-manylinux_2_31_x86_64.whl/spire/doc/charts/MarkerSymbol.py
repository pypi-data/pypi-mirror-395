from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkerSymbol(Enum):
    """
    Specifies marker symbol style.
    """
    #Specifies a default marker symbol shall be drawn at each data point.
    Default = 0
    #Specifies a circle shall be drawn at each data point.
    Circle = 1
    #Specifies a dash shall be drawn at each data point.
    Dash = 2
    #Specifies a diamond shall be drawn at each data point.
    Diamond = 3
    #Specifies a dot shall be drawn at each data point.
    Dot = 4
    #Specifies nothing shall be drawn at each data point.
    none = 5
    #Specifies a picture shall be drawn at each data point.
    Picture = 6
    #Specifies a plus shall be drawn at each data point.
    Plus = 7
    #Specifies a square shall be drawn at each data point.
    Square = 8
    #Specifies a star shall be drawn at each data point.
    Star = 9
    #Specifies a triangle shall be drawn at each data point.
    Triangle = 10
    #Specifies an X shall be drawn at each data point.
    X = 11


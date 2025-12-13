from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartMarker (SpireObject) :
    """
    Represents a chart data marker.
    """
    @property

    def Symbol(self)->'MarkerSymbol':
        """
        Gets or sets chart marker symbol.
        """
        GetDllLibDoc().ChartMarker_get_Symbol.argtypes=[c_void_p]
        GetDllLibDoc().ChartMarker_get_Symbol.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartMarker_get_Symbol,self.Ptr)
        objwraped = MarkerSymbol(ret)
        return objwraped

    @Symbol.setter
    def Symbol(self, value:'MarkerSymbol'):
        GetDllLibDoc().ChartMarker_set_Symbol.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartMarker_set_Symbol,self.Ptr, value.value)

    @property
    def Size(self)->int:
        """
        Gets or sets chart marker size.
        Default value is 7.
        """
        GetDllLibDoc().ChartMarker_get_Size.argtypes=[c_void_p]
        GetDllLibDoc().ChartMarker_get_Size.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartMarker_get_Size,self.Ptr)
        return ret

    @Size.setter
    def Size(self, value:int):
        GetDllLibDoc().ChartMarker_set_Size.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartMarker_set_Size,self.Ptr, value)


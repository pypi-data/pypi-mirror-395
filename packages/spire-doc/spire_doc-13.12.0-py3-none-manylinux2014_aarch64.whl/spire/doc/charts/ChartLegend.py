from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartLegend (SpireObject) :
    """
    Represents a chart legend in a DML (Drawing Markup Language) document.
    """
    @property
    def Show(self)->bool:
        """
        Gets or sets a value indicating whether the legend is visible.
        """
        GetDllLibDoc().ChartLegend_get_Show.argtypes=[c_void_p]
        GetDllLibDoc().ChartLegend_get_Show.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartLegend_get_Show,self.Ptr)
        return ret

    @Show.setter
    def Show(self, value:bool):
        GetDllLibDoc().ChartLegend_set_Show.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartLegend_set_Show,self.Ptr, value)

    @property

    def Position(self)->'LegendPosition':
        """
        Gets or sets the position of the legend.
        """
        GetDllLibDoc().ChartLegend_get_Position.argtypes=[c_void_p]
        GetDllLibDoc().ChartLegend_get_Position.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartLegend_get_Position,self.Ptr)
        objwraped = LegendPosition(ret)
        return objwraped

    @Position.setter
    def Position(self, value:'LegendPosition'):
        GetDllLibDoc().ChartLegend_set_Position.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartLegend_set_Position,self.Ptr, value.value)

    @property
    def Overlay(self)->bool:
        """
        Gets or sets a value indicating whether show the legend with overlapping the chart.
        """
        GetDllLibDoc().ChartLegend_get_Overlay.argtypes=[c_void_p]
        GetDllLibDoc().ChartLegend_get_Overlay.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartLegend_get_Overlay,self.Ptr)
        return ret

    @Overlay.setter
    def Overlay(self, value:bool):
        GetDllLibDoc().ChartLegend_set_Overlay.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartLegend_set_Overlay,self.Ptr, value)

    @property

    def CharacterFormat(self)->'CharacterFormat':
        """
        Gets the font format for the text properties.

        returns: The font format.
        """
        GetDllLibDoc().ChartLegend_get_CharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartLegend_get_CharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartLegend_get_CharacterFormat,self.Ptr)
        from spire.doc.formatting.CharacterFormat import CharacterFormat
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret



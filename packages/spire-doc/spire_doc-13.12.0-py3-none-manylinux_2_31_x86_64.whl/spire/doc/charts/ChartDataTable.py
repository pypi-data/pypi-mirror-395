from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartDataTable (SpireObject) :
    """
    Represents a data table options associated with a chart.
    """
    @property
    def Show(self)->bool:
        """
        Gets or sets a value indicating whether the DataTable is visible.
        """
        GetDllLibDoc().ChartDataTable_get_Show.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_Show.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataTable_get_Show,self.Ptr)
        return ret

    @Show.setter
    def Show(self, value:bool):
        GetDllLibDoc().ChartDataTable_set_Show.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataTable_set_Show,self.Ptr, value)

    @property
    def ShowLegendKeys(self)->bool:
        """
        Gets or sets a value indicating whether to show legend keys.
        """
        GetDllLibDoc().ChartDataTable_get_ShowLegendKeys.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_ShowLegendKeys.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataTable_get_ShowLegendKeys,self.Ptr)
        return ret

    @ShowLegendKeys.setter
    def ShowLegendKeys(self, value:bool):
        GetDllLibDoc().ChartDataTable_set_ShowLegendKeys.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataTable_set_ShowLegendKeys,self.Ptr, value)

    @property
    def ShowHorizontalBorder(self)->bool:
        """
        Gets or sets a value indicating whether the horizontal border of the data table is shown.
        """
        GetDllLibDoc().ChartDataTable_get_ShowHorizontalBorder.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_ShowHorizontalBorder.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataTable_get_ShowHorizontalBorder,self.Ptr)
        return ret

    @ShowHorizontalBorder.setter
    def ShowHorizontalBorder(self, value:bool):
        GetDllLibDoc().ChartDataTable_set_ShowHorizontalBorder.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataTable_set_ShowHorizontalBorder,self.Ptr, value)

    @property
    def ShowVerticalBorder(self)->bool:
        """
        Gets or sets a value indicating whether the vertical border of the data table is shown.
        """
        GetDllLibDoc().ChartDataTable_get_ShowVerticalBorder.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_ShowVerticalBorder.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataTable_get_ShowVerticalBorder,self.Ptr)
        return ret

    @ShowVerticalBorder.setter
    def ShowVerticalBorder(self, value:bool):
        GetDllLibDoc().ChartDataTable_set_ShowVerticalBorder.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataTable_set_ShowVerticalBorder,self.Ptr, value)

    @property
    def ShowOutlineBorder(self)->bool:
        """
        Gets or sets a value indicating whether the outline border of the data table is shown.
        """
        GetDllLibDoc().ChartDataTable_get_ShowOutlineBorder.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_ShowOutlineBorder.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataTable_get_ShowOutlineBorder,self.Ptr)
        return ret

    @ShowOutlineBorder.setter
    def ShowOutlineBorder(self, value:bool):
        GetDllLibDoc().ChartDataTable_set_ShowOutlineBorder.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataTable_set_ShowOutlineBorder,self.Ptr, value)

    @property

    def CharacterFormat(self)->'CharacterFormat':
        """
        Gets the font format for the text properties.

        returns:
            The FontFormat object representing the font properties.
        """
        GetDllLibDoc().ChartDataTable_get_CharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataTable_get_CharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartDataTable_get_CharacterFormat,self.Ptr)
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret



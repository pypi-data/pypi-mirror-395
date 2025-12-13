from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartDataLabelCollection (  IEnumerable) :
    """
    Represent the data labels options for the chart series.
    """

    def get_Item(self ,index:int)->'ChartDataLabel':
        """
        Gets the ChartDataLabel at the specified index.
        """
        
        GetDllLibDoc().ChartDataLabelCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().ChartDataLabelCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_Item,self.Ptr, index)
        ret = None if intPtr==None else ChartDataLabel(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
        Gets the number of data labels in the collection.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_Count,self.Ptr)
        return ret

    @property
    def ShowCategoryName(self)->bool:
        """
        Gets or sets a value indicating whether the label contains the category name.

        true if the label contains the category name; otherwise, false.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowCategoryName.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowCategoryName.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowCategoryName,self.Ptr)
        return ret

    @ShowCategoryName.setter
    def ShowCategoryName(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowCategoryName.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowCategoryName,self.Ptr, value)

    @property
    def ShowBubbleSize(self)->bool:
        """

        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowBubbleSize.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowBubbleSize.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowBubbleSize,self.Ptr)
        return ret

    @ShowBubbleSize.setter
    def ShowBubbleSize(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowBubbleSize.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowBubbleSize,self.Ptr, value)

    @property
    def ShowLegendKey(self)->bool:
        """
        Gets or sets a value indicating whether the label contains the legend key.

        true if the label contains the legend key; otherwise, false.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowLegendKey.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowLegendKey.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowLegendKey,self.Ptr)
        return ret

    @ShowLegendKey.setter
    def ShowLegendKey(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowLegendKey.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowLegendKey,self.Ptr, value)

    @property
    def ShowPercentage(self)->bool:
        """

        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowPercentage.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowPercentage.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowPercentage,self.Ptr)
        return ret

    @ShowPercentage.setter
    def ShowPercentage(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowPercentage.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowPercentage,self.Ptr, value)

    @property
    def ShowSeriesName(self)->bool:
        """
        Gets or sets a value indicating whether the label contains the series name.

        true if the label contains the series name; otherwise, false.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowSeriesName.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowSeriesName.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowSeriesName,self.Ptr)
        return ret

    @ShowSeriesName.setter
    def ShowSeriesName(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowSeriesName.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowSeriesName,self.Ptr, value)

    @property
    def ShowValue(self)->bool:
        """
        Gets or sets a value indicating whether the label contains the value.

        true if the label contains the value; otherwise, false.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowValue.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowValue.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowValue,self.Ptr)
        return ret

    @ShowValue.setter
    def ShowValue(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowValue.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowValue,self.Ptr, value)

    @property
    def ShowLeaderLines(self)->bool:
        """
        Gets or sets a value indicating whether leader lines are shown for the label.

        true if leader lines are shown; otherwise, false.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowLeaderLines.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowLeaderLines.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowLeaderLines,self.Ptr)
        return ret

    @ShowLeaderLines.setter
    def ShowLeaderLines(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowLeaderLines.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowLeaderLines,self.Ptr, value)

    @property
    def ShowDataLabelsRange(self)->bool:
        """

        """
        GetDllLibDoc().ChartDataLabelCollection_get_ShowDataLabelsRange.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_ShowDataLabelsRange.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_ShowDataLabelsRange,self.Ptr)
        return ret

    @ShowDataLabelsRange.setter
    def ShowDataLabelsRange(self, value:bool):
        GetDllLibDoc().ChartDataLabelCollection_set_ShowDataLabelsRange.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_ShowDataLabelsRange,self.Ptr, value)

    @property

    def Separator(self)->str:
        """
        Gets or sets the separator used in the labels.

        returns: The separator string.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_Separator.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_Separator.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_Separator,self.Ptr))
        return ret


    @Separator.setter
    def Separator(self, value:str):
        valuePtr=StrToPtr(value)
        GetDllLibDoc().ChartDataLabelCollection_set_Separator.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().ChartDataLabelCollection_set_Separator,self.Ptr, valuePtr)

    @property

    def NumberFormat(self)->'ChartNumberFormat':
        """
        Gets the number format for the label.

        returns: The ChartNumberFormat object that represents the number format for the label.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_NumberFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_NumberFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_NumberFormat,self.Ptr)
        from spire.doc.charts.ChartNumberFormat import ChartNumberFormat
        ret = None if intPtr==None else ChartNumberFormat(intPtr)
        return ret


    @property

    def CharacterFormat(self)->'CharacterFormat':
        """
        Gets the font format for the data labels.

        returns: The FontFormat object representing the font properties.
        """
        GetDllLibDoc().ChartDataLabelCollection_get_CharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_get_CharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_get_CharacterFormat,self.Ptr)
        from spire.doc.formatting.CharacterFormat import CharacterFormat
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret



    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibDoc().ChartDataLabelCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibDoc().ChartDataLabelCollection_GetEnumerator.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartDataLabelCollection_GetEnumerator,self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret



from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisTickLabels (SpireObject) :
    """
    Represents a class to handle the options of axis tick labels in a chart.
    """
    @property
    def Spacing(self)->int:
        """
        Gets or sets the interval unit between labels on the axis.
        """
        GetDllLibDoc().AxisTickLabels_get_Spacing.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickLabels_get_Spacing.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickLabels_get_Spacing,self.Ptr)
        return ret

    @Spacing.setter
    def Spacing(self, value:int):
        GetDllLibDoc().AxisTickLabels_set_Spacing.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickLabels_set_Spacing,self.Ptr, value)

    @property
    def IsAutoSpacing(self)->bool:
        """
        Gets or sets a value indicating whether the interval between labels is automatically determined.
        """
        GetDllLibDoc().AxisTickLabels_get_IsAutoSpacing.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickLabels_get_IsAutoSpacing.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisTickLabels_get_IsAutoSpacing,self.Ptr)
        return ret

    @IsAutoSpacing.setter
    def IsAutoSpacing(self, value:bool):
        GetDllLibDoc().AxisTickLabels_set_IsAutoSpacing.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().AxisTickLabels_set_IsAutoSpacing,self.Ptr, value)

    @property
    def Offset(self)->int:
        """
        Gets or sets the distance from axis of the labels.
        """
        GetDllLibDoc().AxisTickLabels_get_Offset.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickLabels_get_Offset.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickLabels_get_Offset,self.Ptr)
        return ret

    @Offset.setter
    def Offset(self, value:int):
        GetDllLibDoc().AxisTickLabels_set_Offset.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickLabels_set_Offset,self.Ptr, value)

    @property

    def Position(self)->'AxisTickLabelPosition':
        """
        Gets or sets the position of the labels.
        """
        GetDllLibDoc().AxisTickLabels_get_Position.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickLabels_get_Position.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickLabels_get_Position,self.Ptr)
        objwraped = AxisTickLabelPosition(ret)
        return objwraped

    @Position.setter
    def Position(self, value:'AxisTickLabelPosition'):
        GetDllLibDoc().AxisTickLabels_set_Position.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickLabels_set_Position,self.Ptr, value.value)

    @property

    def Alignment(self)->'LabelAlignment':
        """
        Gets or sets the alignment of the labels.
        """
        GetDllLibDoc().AxisTickLabels_get_Alignment.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickLabels_get_Alignment.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickLabels_get_Alignment,self.Ptr)
        objwraped = LabelAlignment(ret)
        return objwraped

    @Alignment.setter
    def Alignment(self, value:'LabelAlignment'):
        GetDllLibDoc().AxisTickLabels_set_Alignment.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickLabels_set_Alignment,self.Ptr, value.value)


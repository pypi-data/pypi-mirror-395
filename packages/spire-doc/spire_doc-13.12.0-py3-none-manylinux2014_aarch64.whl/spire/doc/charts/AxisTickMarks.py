from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisTickMarks (SpireObject) :
    """
    Represents a class to handle the options of axis tick marks in a chart.
    """
    @property
    def Spacing(self)->int:
        """
        Gets or sets the interval between tick marks on the axis.
        """
        GetDllLibDoc().AxisTickMarks_get_Spacing.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickMarks_get_Spacing.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickMarks_get_Spacing,self.Ptr)
        return ret

    @Spacing.setter
    def Spacing(self, value:int):
        GetDllLibDoc().AxisTickMarks_set_Spacing.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickMarks_set_Spacing,self.Ptr, value)

    @property

    def Major(self)->'AxisTickMark':
        """
        Gets or sets the major type of the tick marks for the axis.
        """
        GetDllLibDoc().AxisTickMarks_get_Major.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickMarks_get_Major.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickMarks_get_Major,self.Ptr)
        objwraped = AxisTickMark(ret)
        return objwraped

    @Major.setter
    def Major(self, value:'AxisTickMark'):
        GetDllLibDoc().AxisTickMarks_set_Major.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickMarks_set_Major,self.Ptr, value.value)

    @property

    def Minor(self)->'AxisTickMark':
        """
        Gets or sets the minor type of the tick marks for the axis.
        """
        GetDllLibDoc().AxisTickMarks_get_Minor.argtypes=[c_void_p]
        GetDllLibDoc().AxisTickMarks_get_Minor.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisTickMarks_get_Minor,self.Ptr)
        objwraped = AxisTickMark(ret)
        return objwraped

    @Minor.setter
    def Minor(self, value:'AxisTickMark'):
        GetDllLibDoc().AxisTickMarks_set_Minor.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisTickMarks_set_Minor,self.Ptr, value.value)


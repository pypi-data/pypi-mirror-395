from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisBounds (SpireObject) :
    """
    Represents the bounds of an axis in a chart.
    """
    @property

    def Minimum(self)->'AxisBound':
        """
        Gets the minimum value of the axis.
        """
        GetDllLibDoc().AxisBounds_get_Minimum.argtypes=[c_void_p]
        GetDllLibDoc().AxisBounds_get_Minimum.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().AxisBounds_get_Minimum,self.Ptr)
        from spire.doc.charts.AxisBound import AxisBound
        ret = None if intPtr==None else AxisBound(intPtr)
        return ret


    @Minimum.setter
    def Minimum(self, value:'AxisBound'):
        """
        Sets the minimum value of the axis.
        """
        GetDllLibDoc().AxisBounds_set_Minimum.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().AxisBounds_set_Minimum,self.Ptr, value.Ptr)

    @property

    def Maximum(self)->'AxisBound':
        """
        Gets the maximum value of the axis.
        """
        GetDllLibDoc().AxisBounds_get_Maximum.argtypes=[c_void_p]
        GetDllLibDoc().AxisBounds_get_Maximum.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().AxisBounds_get_Maximum,self.Ptr)
        from spire.doc.charts.AxisBound import AxisBound
        ret = None if intPtr==None else AxisBound(intPtr)
        return ret


    @Maximum.setter
    def Maximum(self, value:'AxisBound'):
        """
        Sets the maximum value of the axis.
        """
        GetDllLibDoc().AxisBounds_set_Maximum.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().AxisBounds_set_Maximum,self.Ptr, value.Ptr)

    @property
    def LogBase(self)->float:
        """
        Gets the logarithmic scale base.
        """
        GetDllLibDoc().AxisBounds_get_LogBase.argtypes=[c_void_p]
        GetDllLibDoc().AxisBounds_get_LogBase.restype=c_double
        ret = CallCFunction(GetDllLibDoc().AxisBounds_get_LogBase,self.Ptr)
        return ret

    @LogBase.setter
    def LogBase(self, value:float):
        """
        Sets the logarithmic scale base.
        """
        GetDllLibDoc().AxisBounds_set_LogBase.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().AxisBounds_set_LogBase,self.Ptr, value)


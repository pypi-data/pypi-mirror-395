from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisBound (SpireObject) :

    @dispatch
    def __init__(self, value: float):
        """
        Initializes a new instance of the AxisBound class with the specified value.

        Args:
            value (float): The value to initialize the AxisBound with.
        """
        GetDllLibDoc().AxisBound_CreateAxisBoundV.argtypes=[c_float]
        GetDllLibDoc().AxisBound_CreateAxisBoundV.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().AxisBound_CreateAxisBoundV, value)
        super(AxisBound, self).__init__(intPtr)

    @dispatch
    def __init__(self, dateTime: DateTime):
        """
        Initializes a new instance of the axisBound class with the specified DateTime flag.

        Args:
            dateTime (DateTime): The DateTime value to initialize the AxisBound with.

        """
        intPtrdateTime:c_void_p = dateTime.Ptr

        GetDllLibDoc().AxisBound_CreateAxisBoundD.argtypes=[c_void_p]
        GetDllLibDoc().AxisBound_CreateAxisBoundD.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().AxisBound_CreateAxisBoundD, intPtrdateTime)
        super(AxisBound, self).__init__(intPtr)

    """
    Represents a class that defines the bound value for an <see cref="AxisBounds"/>.
    """
    @property
    def IsAuto(self)->bool:
        """
        Gets a value indicating whether the property is automatically managed.
        """
        GetDllLibDoc().AxisBound_get_IsAuto.argtypes=[c_void_p]
        GetDllLibDoc().AxisBound_get_IsAuto.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisBound_get_IsAuto,self.Ptr)
        return ret

    @property
    def Value(self)->float:
        """
        Gets the value.
        """
        GetDllLibDoc().AxisBound_get_Value.argtypes=[c_void_p]
        GetDllLibDoc().AxisBound_get_Value.restype=c_double
        ret = CallCFunction(GetDllLibDoc().AxisBound_get_Value,self.Ptr)
        return ret

    @property

    def ValueAsDate(self)->'DateTime':
        """
        Converts the stored OLE Automation date to a DateTime value.
        """
        GetDllLibDoc().AxisBound_get_ValueAsDate.argtypes=[c_void_p]
        GetDllLibDoc().AxisBound_get_ValueAsDate.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().AxisBound_get_ValueAsDate,self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret



    def Equals(self ,obj:'SpireObject')->bool:
        """

        """
        intPtrobj:c_void_p = obj.Ptr

        GetDllLibDoc().AxisBound_Equals.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().AxisBound_Equals.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisBound_Equals,self.Ptr, intPtrobj)
        return ret


    def ToString(self)->str:
        """

        """
        GetDllLibDoc().AxisBound_ToString.argtypes=[c_void_p]
        GetDllLibDoc().AxisBound_ToString.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().AxisBound_ToString,self.Ptr))
        return ret



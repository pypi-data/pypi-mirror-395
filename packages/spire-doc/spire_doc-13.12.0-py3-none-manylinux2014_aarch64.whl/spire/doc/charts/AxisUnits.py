from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisUnits (SpireObject) :
    """
    Represents the units for an axis in a chart.
    """
    @property
    def Major(self)->float:
        """
        Gets the major unit value of the axis.
        """
        GetDllLibDoc().AxisUnits_get_Major.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_Major.restype=c_double
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_Major,self.Ptr)
        return ret

    @Major.setter
    def Major(self, value:float):
        """
        Sets the major unit value of the axis.
        """
        GetDllLibDoc().AxisUnits_set_Major.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().AxisUnits_set_Major,self.Ptr, value)

    @property

    def MajorTimeUnit(self)->'AxisTimeUnit':
        """
        Gets the major time unit for the date axis.
        """
        GetDllLibDoc().AxisUnits_get_MajorTimeUnit.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_MajorTimeUnit.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_MajorTimeUnit,self.Ptr)
        from spire.doc.charts.AxisTimeUnit import AxisTimeUnit
        objwraped = AxisTimeUnit(ret)
        return objwraped

    @MajorTimeUnit.setter
    def MajorTimeUnit(self, value:'AxisTimeUnit'):
        """
        Sets the major time unit for the date axis.
        """
        GetDllLibDoc().AxisUnits_set_MajorTimeUnit.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisUnits_set_MajorTimeUnit,self.Ptr, value.value)

    @property
    def IsMajorAuto(self)->bool:
        """
        Gets a value indicating whether the major units on the axis are automatically determined.
        """
        GetDllLibDoc().AxisUnits_get_IsMajorAuto.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_IsMajorAuto.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_IsMajorAuto,self.Ptr)
        return ret

    @IsMajorAuto.setter
    def IsMajorAuto(self, value:bool):
        """
        Sets a value indicating whether the major units on the axis are automatically determined.
        """
        GetDllLibDoc().AxisUnits_set_IsMajorAuto.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().AxisUnits_set_IsMajorAuto,self.Ptr, value)

    @property
    def Minor(self)->float:
        """
        Gets the minor unit value of the axis.
        """
        GetDllLibDoc().AxisUnits_get_Minor.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_Minor.restype=c_double
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_Minor,self.Ptr)
        return ret

    @Minor.setter
    def Minor(self, value:float):
        """
        Sets the minor unit value of the axis.
        """
        GetDllLibDoc().AxisUnits_set_Minor.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().AxisUnits_set_Minor,self.Ptr, value)

    @property

    def MinorTimeUnit(self)->'AxisTimeUnit':
        """
        Gets the minor time unit of the date axis.
        """
        GetDllLibDoc().AxisUnits_get_MinorTimeUnit.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_MinorTimeUnit.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_MinorTimeUnit,self.Ptr)
        from spire.doc.charts.AxisTimeUnit import AxisTimeUnit
        objwraped = AxisTimeUnit(ret)
        return objwraped

    @MinorTimeUnit.setter
    def MinorTimeUnit(self, value:'AxisTimeUnit'):
        """
        Sets the minor time unit of the date axis.
        """
        GetDllLibDoc().AxisUnits_set_MinorTimeUnit.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisUnits_set_MinorTimeUnit,self.Ptr, value.value)

    @property
    def IsMinorAuto(self)->bool:
        """
        Gets a value indicating whether the minor units on the axis are automatically determined.
        """
        GetDllLibDoc().AxisUnits_get_IsMinorAuto.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_IsMinorAuto.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_IsMinorAuto,self.Ptr)
        return ret

    @IsMinorAuto.setter
    def IsMinorAuto(self, value:bool):
        """
        Sets a value indicating whether the minor units on the axis are automatically determined.
        """
        GetDllLibDoc().AxisUnits_set_IsMinorAuto.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().AxisUnits_set_IsMinorAuto,self.Ptr, value)

    @property

    def BaseTimeUnit(self)->'AxisTimeUnit':
        """
        Gets the base time unit of the axis.
        """
        GetDllLibDoc().AxisUnits_get_BaseTimeUnit.argtypes=[c_void_p]
        GetDllLibDoc().AxisUnits_get_BaseTimeUnit.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisUnits_get_BaseTimeUnit,self.Ptr)
        from spire.doc.charts.AxisTimeUnit import AxisTimeUnit
        objwraped = AxisTimeUnit(ret)
        return objwraped

    @BaseTimeUnit.setter
    def BaseTimeUnit(self, value:'AxisTimeUnit'):
        """
        Sets the base time unit of the axis.
        """
        GetDllLibDoc().AxisUnits_set_BaseTimeUnit.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisUnits_set_BaseTimeUnit,self.Ptr, value.value)


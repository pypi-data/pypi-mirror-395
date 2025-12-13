from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AxisDisplayUnits (SpireObject) :
    """
    Represents the display units for an axis in a chart.
    """
    @property

    def Unit(self)->'AxisBuiltInUnit':
        """
        Gets or sets the built-in unit of the axis display.

        returns:
            The built-in unit of the axis display.
        """
        GetDllLibDoc().AxisDisplayUnits_get_Unit.argtypes=[c_void_p]
        GetDllLibDoc().AxisDisplayUnits_get_Unit.restype=c_int
        ret = CallCFunction(GetDllLibDoc().AxisDisplayUnits_get_Unit,self.Ptr)
        objwraped = AxisBuiltInUnit(ret)
        return objwraped

    @Unit.setter
    def Unit(self, value:'AxisBuiltInUnit'):
        GetDllLibDoc().AxisDisplayUnits_set_Unit.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().AxisDisplayUnits_set_Unit,self.Ptr, value.value)

    @property
    def CustomUnit(self)->float:
        """
        Gets or sets the custom unit for the axis display units.
        """
        GetDllLibDoc().AxisDisplayUnits_get_CustomUnit.argtypes=[c_void_p]
        GetDllLibDoc().AxisDisplayUnits_get_CustomUnit.restype=c_double
        ret = CallCFunction(GetDllLibDoc().AxisDisplayUnits_get_CustomUnit,self.Ptr)
        return ret

    @CustomUnit.setter
    def CustomUnit(self, value:float):
        GetDllLibDoc().AxisDisplayUnits_set_CustomUnit.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().AxisDisplayUnits_set_CustomUnit,self.Ptr, value)

    @property
    def ShowLabel(self)->bool:
        """
        Gets or sets whether show display units label on the chart.

        true if the display units label is shown; otherwise, false.
        """
        GetDllLibDoc().AxisDisplayUnits_get_ShowLabel.argtypes=[c_void_p]
        GetDllLibDoc().AxisDisplayUnits_get_ShowLabel.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().AxisDisplayUnits_get_ShowLabel,self.Ptr)
        return ret

    @ShowLabel.setter
    def ShowLabel(self, value:bool):
        GetDllLibDoc().AxisDisplayUnits_set_ShowLabel.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().AxisDisplayUnits_set_ShowLabel,self.Ptr, value)


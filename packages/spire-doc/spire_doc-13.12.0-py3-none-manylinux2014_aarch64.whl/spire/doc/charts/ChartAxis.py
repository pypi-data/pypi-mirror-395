from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartAxis (SpireObject) :
    """
    Represents a chart axis in a chart.
    Implements interfaces for handling chart titles, extension lists, and number format providers.
    """
    @property

    def Type(self)->'ChartAxisType':
        """
        Gets the type of the chart axis.
        """
        GetDllLibDoc().ChartAxis_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_Type,self.Ptr)
        objwraped = ChartAxisType(ret)
        return objwraped

    @property

    def CategoryType(self)->'AxisCategoryType':
        """
        Gets or sets the type of the category axis.
        """
        GetDllLibDoc().ChartAxis_get_CategoryType.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_CategoryType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_CategoryType,self.Ptr)
        from spire.doc.charts.AxisCategoryType import AxisCategoryType
        objwraped = AxisCategoryType(ret)
        return objwraped

    @CategoryType.setter
    def CategoryType(self, value:'AxisCategoryType'):
        GetDllLibDoc().ChartAxis_set_CategoryType.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartAxis_set_CategoryType,self.Ptr, value.value)

    @property

    def Bounds(self)->'AxisBounds':
        """
        Gets the bounds for the axis
        """
        GetDllLibDoc().ChartAxis_get_Bounds.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Bounds.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_Bounds,self.Ptr)
        from spire.doc.charts.AxisBounds import AxisBounds
        ret = None if intPtr==None else AxisBounds(intPtr)
        return ret

    @property

    def Units(self)->'AxisUnits':
        """
        Gets the units for the axis
        """
        GetDllLibDoc().ChartAxis_get_Units.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Units.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_Units,self.Ptr)
        from spire.doc.charts.AxisUnits import AxisUnits
        ret = None if intPtr==None else AxisUnits(intPtr)
        return ret


    @property

    def Crosses(self)->'AxisCrosses':
        """
        Gets of sets the axis crosses.
        """
        GetDllLibDoc().ChartAxis_get_Crosses.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Crosses.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_Crosses,self.Ptr)
        from spire.doc.charts import AxisCrosses
        objwraped = AxisCrosses(ret)
        return objwraped

    @Crosses.setter
    def Crosses(self, value:'AxisCrosses'):
        GetDllLibDoc().ChartAxis_set_Crosses.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartAxis_set_Crosses,self.Ptr, value.value)

    @property
    def CrossesAt(self)->float:
        """
        Gets or sets the axis crosses value.
        """
        GetDllLibDoc().ChartAxis_get_CrossesAt.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_CrossesAt.restype=c_double
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_CrossesAt,self.Ptr)
        return ret

    @CrossesAt.setter
    def CrossesAt(self, value:float):
        GetDllLibDoc().ChartAxis_set_CrossesAt.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().ChartAxis_set_CrossesAt,self.Ptr, value)

    @property
    def AxisBetweenCategories(self)->bool:
        """
        Gets or sets a value indicating whether the axis is between tick marks.
        true: if the axis is between tick marks; otherwise, false.
        This property is applicable only when the axis type is either Category or Date.
        """
        GetDllLibDoc().ChartAxis_get_AxisBetweenCategories.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_AxisBetweenCategories.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_AxisBetweenCategories,self.Ptr)
        return ret

    @AxisBetweenCategories.setter
    def AxisBetweenCategories(self, value:bool):
        GetDllLibDoc().ChartAxis_set_AxisBetweenCategories.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxis_set_AxisBetweenCategories,self.Ptr, value)

    @property

    def DisplayUnits(self)->'AxisDisplayUnits':
        """
        Gets the display units for the axis.
        returns:The display units for the axis.
        """
        GetDllLibDoc().ChartAxis_get_DisplayUnits.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_DisplayUnits.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_DisplayUnits,self.Ptr)
        from spire.doc.charts.AxisDisplayUnits import AxisDisplayUnits
        ret = None if intPtr==None else AxisDisplayUnits(intPtr)
        return ret


    @property
    def ReverseOrder(self)->bool:
        """
        Gets or sets a value indicating whether the categories in reverse order.
        """
        GetDllLibDoc().ChartAxis_get_ReverseOrder.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_ReverseOrder.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_ReverseOrder,self.Ptr)
        return ret

    @ReverseOrder.setter
    def ReverseOrder(self, value:bool):
        GetDllLibDoc().ChartAxis_set_ReverseOrder.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxis_set_ReverseOrder,self.Ptr, value)

    @property

    def TickMarks(self)->'AxisTickMarks':
        """
        Gets the tick marks options for the axis.
        """
        GetDllLibDoc().ChartAxis_get_TickMarks.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_TickMarks.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_TickMarks,self.Ptr)
        from spire.doc.charts.AxisTickMarks import AxisTickMarks
        ret = None if intPtr==None else AxisTickMarks(intPtr)
        return ret


    @property

    def Labels(self)->'AxisTickLabels':
        """
        Gets the tick labels options for the axis.
        """
        GetDllLibDoc().ChartAxis_get_Labels.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Labels.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_Labels,self.Ptr)
        from spire.doc.charts.AxisTickLabels import AxisTickLabels
        ret = None if intPtr==None else AxisTickLabels(intPtr)
        return ret


    @property

    def NumberFormat(self)->'ChartNumberFormat':
        """
        Gets the number format for the axis.
        """
        GetDllLibDoc().ChartAxis_get_NumberFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_NumberFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_NumberFormat,self.Ptr)
        from spire.doc.charts.ChartNumberFormat import ChartNumberFormat
        ret = None if intPtr==None else ChartNumberFormat(intPtr)
        return ret


    @property
    def HasMajorGridlines(self)->bool:
        """
        Gets or sets a value indicating whether major gridlines are enabled.
        if major gridlines are enabled, true; otherwise, false.
        """
        GetDllLibDoc().ChartAxis_get_HasMajorGridlines.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_HasMajorGridlines.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_HasMajorGridlines,self.Ptr)
        return ret

    @HasMajorGridlines.setter
    def HasMajorGridlines(self, value:bool):
        GetDllLibDoc().ChartAxis_set_HasMajorGridlines.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxis_set_HasMajorGridlines,self.Ptr, value)

    @property
    def HasMinorGridlines(self)->bool:
        """
        Gets or sets a value indicating whether minor gridlines are enabled.
        true if minor gridlines are enabled; otherwise, false.
        """
        GetDllLibDoc().ChartAxis_get_HasMinorGridlines.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_HasMinorGridlines.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_HasMinorGridlines,self.Ptr)
        return ret

    @HasMinorGridlines.setter
    def HasMinorGridlines(self, value:bool):
        GetDllLibDoc().ChartAxis_set_HasMinorGridlines.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxis_set_HasMinorGridlines,self.Ptr, value)

    @property
    def Delete(self)->bool:
        """
        Gets or sets a value indicating whether the chart axis is hidden.
        true if the chart axis is hidden; otherwise, false.
        """
        GetDllLibDoc().ChartAxis_get_Delete.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Delete.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxis_get_Delete,self.Ptr)
        return ret

    @Delete.setter
    def Delete(self, value:bool):
        GetDllLibDoc().ChartAxis_set_Delete.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxis_set_Delete,self.Ptr, value)

    @property

    def Title(self)->'ChartAxisTitle':
        """
        Gets the title of the chart axis.

        returns:The <see cref="ChartAxisTitle"/> object representing the title of the chart axis.
        """
        GetDllLibDoc().ChartAxis_get_Title.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxis_get_Title.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxis_get_Title,self.Ptr)
        from spire.doc.charts.ChartAxisTitle import ChartAxisTitle
        ret = None if intPtr==None else ChartAxisTitle(intPtr)
        return ret

    @property
    def TextVerticalType(self):
        raise AttributeError("This property can only be set, not get!")

    @TextVerticalType.setter
    def TextVerticalType(self, value:'TextVerticalType'):
        GetDllLibDoc().ChartAxis_set_TextVerticalType.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ChartAxis_set_TextVerticalType,self.Ptr, value.value)


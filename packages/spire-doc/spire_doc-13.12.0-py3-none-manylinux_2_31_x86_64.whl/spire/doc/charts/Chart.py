from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from spire.doc.charts.ChartSeriesType import ChartSeriesType
from ctypes import *
import abc

class Chart (SpireObject) :
    """
    Provides access to the chart shape properties.
    """
    @property

    def Series(self)->'ChartSeriesCollection':
        """
        Provides access to series collection.
        """
        GetDllLibDoc().Chart_get_Series.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_Series.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_Series,self.Ptr)
        from spire.doc.charts.ChartSeriesCollection import ChartSeriesCollection
        ret = None if intPtr==None else ChartSeriesCollection(intPtr)
        return ret


    @Series.setter
    def Series(self, value:'ChartSeriesCollection'):
        GetDllLibDoc().Chart_set_Series.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().Chart_set_Series,self.Ptr, value.Ptr)

    @property

    def Title(self)->'ChartTitle':
        """
         Provides access to the chart title properties.
        """
        GetDllLibDoc().Chart_get_Title.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_Title.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_Title,self.Ptr)
        from spire.doc.charts.ChartTitle import ChartTitle
        ret = None if intPtr==None else ChartTitle(intPtr)
        return ret


    @property

    def Legend(self)->'ChartLegend':
        """
        Provides access to the chart legend properties.
        """
        GetDllLibDoc().Chart_get_Legend.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_Legend.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_Legend,self.Ptr)
        from spire.doc.charts.ChartLegend import ChartLegend
        ret = None if intPtr==None else ChartLegend(intPtr)
        return ret


    @property

    def AxisX(self)->'ChartAxis':
        """
        Provides access to properties of the X axis of the chart.
        """
        GetDllLibDoc().Chart_get_AxisX.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_AxisX.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_AxisX,self.Ptr)
        from spire.doc.charts.ChartAxis import ChartAxis
        ret = None if intPtr==None else ChartAxis(intPtr)
        return ret


    @property

    def AxisY(self)->'ChartAxis':
        """
        Provides access to properties of the Y axis of the chart.
        """
        GetDllLibDoc().Chart_get_AxisY.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_AxisY.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_AxisY,self.Ptr)
        from spire.doc.charts.ChartAxis import ChartAxis
        ret = None if intPtr==None else ChartAxis(intPtr)
        return ret


    @property

    def AxisZ(self)->'ChartAxis':
        """
        Provides access to properties of the Z axis of the chart.
        """
        GetDllLibDoc().Chart_get_AxisZ.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_AxisZ.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_AxisZ,self.Ptr)
        from spire.doc.charts.ChartAxis import ChartAxis
        ret = None if intPtr==None else ChartAxis(intPtr)
        return ret


    @property

    def Axes(self)->'ChartAxisCollection':
        """
		Gets the collection of axes for the chart.
        """
        GetDllLibDoc().Chart_get_Axes.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_Axes.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_Axes,self.Ptr)
        from spire.doc.charts.ChartAxisCollection import ChartAxisCollection
        ret = None if intPtr==None else ChartAxisCollection(intPtr)
        return ret


    @property

    def DataTable(self)->'ChartDataTable':
        """
		Gets the Data Table Options associated with the Chart.
        """
        GetDllLibDoc().Chart_get_DataTable.argtypes=[c_void_p]
        GetDllLibDoc().Chart_get_DataTable.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Chart_get_DataTable,self.Ptr)
        from spire.doc.charts.ChartDataTable import ChartDataTable
        ret = None if intPtr==None else ChartDataTable(intPtr)
        return ret



    def SaveToTemp(self ,fileName:str):
        """

        """
        fileNamePtr=StrToPtr(fileName)
        GetDllLibDoc().Chart_SaveToTemp.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().Chart_SaveToTemp,self.Ptr, fileNamePtr)


    def ChangeSeriesType(self ,seriesName:str,seriesType:'ChartSeriesType',showOnSecondaryAxis:bool):
        """
		Choose the chart type and axis for the data series.
        This method is intended for manipulating combo chart.
        """
        enumseriesType:c_int = seriesType.value
        seriesNamePtr=StrToPtr(seriesName)
        GetDllLibDoc().Chart_ChangeSeriesType.argtypes=[c_void_p ,c_char_p,c_int,c_bool]
        CallCFunction(GetDllLibDoc().Chart_ChangeSeriesType,self.Ptr, seriesNamePtr,enumseriesType,showOnSecondaryAxis)


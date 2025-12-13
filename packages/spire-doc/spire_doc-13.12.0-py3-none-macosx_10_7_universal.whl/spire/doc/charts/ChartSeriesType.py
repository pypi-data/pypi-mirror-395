from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.charts import *
from spire.doc import *
from ctypes import *
import abc

class ChartSeriesType(Enum):
    """
    Specifies type of a series.
    """

    # Area series. 
    Area = 0
    # Stacked Area series.
    AreaStacked = 1
    # 100% Stacked Area series.
    AreaPercentStacked = 2
    #3D Area chart.
    Area3D = 3
    # 3D Stacked Area series.
    Area3DStacked = 4
    # 3D 100% Stacked Area series.
    Area3DPercentStacked = 5
    #Bar series.
    Bar = 6
    # Stacked Bar series.
    BarStacked = 7
    # 100% Stacked Bar series.
    BarPercentStacked = 8
    #3D Bar series.
    Bar3D = 9
    # 3D Stacked Bar series.
    Bar3DStacked = 10
    # 3D 100% Stacked Bar series.
    Bar3DPercentStacked = 11
    # Bubble series.
    Bubble = 12
    # 3D Bubble series.
    Bubble3D = 13
    #Column series.
    Column = 14
    #Stacked Column series.
    ColumnStacked = 15
    #100% Stacked Column series.
    ColumnPercentStacked = 16
    #3D Column series.
    Column3D = 17
    #3D Stacked Column series.
    Column3DStacked = 18
    #3D 100% Stacked Column series.
    Column3DPercentStacked = 19
    #3D Clustered Column series.
    Column3DClustered = 20
    #Doughnut series.
    Doughnut = 21
    #Line series.
    Line = 22
    #Stacked Line series.
    LineStacked = 23
    #100% Stacked Line series.
    LinePercentStacked = 24
    #3D Line series.
    Line3D = 25
    #Pie series.
    Pie = 26
    #3D Pie series.
    Pie3D = 27
    #Pie of Bar series.
    PieOfBar = 28
    # Radar series.
    PieOfPie = 29
    #Scatter series.
    Radar = 30
    #Scatter series.
    Scatter = 31
    #Stock series.
    Stock = 32
    #Surface series.
    Surface = 33
    #3D Surface series.
    Surface3D = 34
    #Treemap series.
    Treemap = 35
    #Sunburst series.
    Sunburst = 36
    #Histogram series.
    Histogram = 37
    #Pareto series.
    Pareto = 38
    #ParetoLine series.
    ParetoLine = 39
    #BoxAndWhisker series.
    BoxAndWhisker = 40
    #Waterfall series.
    Waterfall = 41
    #Funnel series.
    Funnel = 42
    #RegionMap series.
    RegionMap = 43


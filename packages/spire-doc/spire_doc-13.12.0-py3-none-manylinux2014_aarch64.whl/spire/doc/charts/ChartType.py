from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.charts import *
from spire.doc import *
from ctypes import *
import abc

class ChartType(Enum):
    """
    Specifies type of a chart.
    """
    
   # Area chart. 
    Area = 0
    # Stacked Area chart.
    AreaStacked = 1
    # 100% Stacked Area chart.
    AreaPercentStacked = 2
    #3D Area chart.
    Area3D = 3
    # 3D Stacked Area chart.
    Area3DStacked = 4
    # 3D 100% Stacked Area chart.
    Area3DPercentStacked = 5
    #Bar chart.
    Bar = 6
    # Stacked Bar chart.
    BarStacked = 7
    # 100% Stacked Bar chart.
    BarPercentStacked = 8
    #3D Bar chart.
    Bar3D = 9
    # 3D Stacked Bar chart.
    Bar3DStacked = 10
    # 3D 100% Stacked Bar chart.
    Bar3DPercentStacked = 11
    # Bubble chart.
    Bubble = 12
    # 3D Bubble chart.
    Bubble3D = 13
    #Column chart.
    Column = 14
    #Stacked Column chart.
    ColumnStacked = 15
    #100% Stacked Column chart.
    ColumnPercentStacked = 16
    #3D Column chart.
    Column3D = 17
    #3D Stacked Column chart.
    Column3DStacked = 18
    #3D 100% Stacked Column chart.
    Column3DPercentStacked = 19
    #3D Clustered Column chart.
    Column3DClustered = 20
    #Doughnut chart.
    Doughnut = 21
    #Line chart.
    Line = 22
    #Stacked Line chart.
    LineStacked = 23
    #100% Stacked Line chart.
    LinePercentStacked = 24
    #3D Line chart.
    Line3D = 25
    #Pie chart.
    Pie = 26
    #3D Pie chart.
    Pie3D = 27
    #Pie of Bar chart.
    PieOfBar = 28
    # Radar chart.
    PieOfPie = 29
    #Scatter chart.
    Radar = 30
    #Scatter chart.
    Scatter = 31
    #Stock chart.
    Stock = 32
    #Surface chart.
    Surface = 33
    #3D Surface chart.
    Surface3D = 34
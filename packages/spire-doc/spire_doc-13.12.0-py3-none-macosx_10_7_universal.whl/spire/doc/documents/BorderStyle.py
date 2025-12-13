from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class BorderStyle(Enum):
    """
    Specifies style of the border line.
    """

    
    #No border is applied.
    none = 0
    #A single line border is applied.
    Single = 1
    #A thick line border is applied.
    Thick = 2
    #A double line border is applied.
    Double = 3
    #A hairline border is applied.
    Hairline = 5
    #A dotted border is applied.
    Dot = 6
    #A dashed border with large gaps is applied.
    DashLargeGap = 7
    #A dot-dash border is applied.
    DotDash = 8
    #A dot-dot-dash border is applied.
    DotDotDash = 9
    #A triple line border is applied.
    Triple = 10
    # A thin-thick line border with a small gap is applied.
    ThinThickSmallGap = 11
    # A thick-thin line border with a small gap is applied.
    ThickThinSmallGap = 12
    # A thick-thin line border with a small gap is applied.
    ThinThinSmallGap = 12
    # A thin-thin-thick line border with a small gap is applied.
    ThinThickThinSmallGap = 13
    # A thin-thick line border with a medium gap is applied.
    ThinThickMediumGap = 14
    # A thick-thin line border with a medium gap is applied.
    ThickThinMediumGap = 15
    # A thin-thick-thin line border with a medium gap is applied.
    ThinThickThinMediumGap = 16
    # A thick-thick-thin line border with a medium gap is applied.
    ThickThickThinMediumGap = 16
    # A thin-thick line border with a large gap is applied.
    ThinThickLargeGap = 17
    # A thick-thin line border with a large gap is applied.
    ThickThinLargeGap = 18
    # A thin-thick-thin line border with a large gap is applied.
    ThinThickThinLargeGap = 19
    # A wavy border is applied.
    Wave = 20
    # A double wave border is applied.
    DoubleWave = 21
    # A dashed border with small gaps is applied.
    DashSmallGap = 22
    # A dashed border with dot stroker effect is applied.
    DashDotStroker = 23
    # A border with emboss 3D effect is applied.
    Emboss3D = 24
    # A border with engrave 3D effect is applied.
    Engrave3D = 25
    # A border with outset effect is applied.
    Outset = 26
    # A border with inset effect is applied.
    Inset = 27
    # A twisted lines 1 border effect is applied.
    TwistedLines1 = 214
    """
    Codes 64 - 230 represent border art types and are used only for page borders.
    They are represented using the PageBorderArt enum.
    """
    # Represents a cleared border, indicating no border is applied.
    Cleared = 255

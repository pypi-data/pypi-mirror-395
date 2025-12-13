from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class UnderlineStyle(Enum):
    """
    Enum class that specifies the style of the underline.
    
    """

    # No underlining.
    none = 0
    # Normal single underline. 
    Single = 1
    # Underline words only.
    Words = 2
    # Double underline.
    Double = 3
    # Dotted underline.
    Dotted = 4
    DotDot = 4
    # Heavy underline.
    Thick = 6
    # Dashed underline.
    Dash = 7
    # Dot-dash underline.
    DotDash = 9
    # Dot-dot-dash underline.
    DotDotDash = 10
    # Wavy underline.
    Wavy = 11
    # Heavy dotted underline.
    DottedHeavy = 20
    # Heavy dashed underline.
    DashHeavy = 23
    # Heavy dot-dash underline.
    DotDashHeavy = 25
    # Heavy dot-dot-dash underline.
    DotDotDashHeavy = 26
    # Heavy wavy underline.
    WavyHeavy = 27
    # Long-dash underline.
    DashLong = 39
    # Wavy double underline.
    WavyDouble = 43
    # Heavy long-dash underline.
    DashLongHeavy = 55

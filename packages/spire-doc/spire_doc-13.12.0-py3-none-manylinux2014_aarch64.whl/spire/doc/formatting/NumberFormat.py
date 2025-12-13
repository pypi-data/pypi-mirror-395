from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class NumberFormat(Enum):
    """
    Enum class that defines different number formats.
    """

    # No formatting 
    none = 0
    # Format with while number.
    WholeNumber = 1
    # Format with floating point number.
    FloatingPoint = 2
    # Whole number in percents.
    WholeNumberPercent = 3
    # Floating point number in percents. 
    FloatingPointPercent = 4
    # Format which suits to "#?#0" Word format.
    WholeNumberWithSpace = 5
    # Format which suites to "#?#0,00" Word format.
    FloatingPointWithSpace = 6
    # Format which suites to "#?#0,00 $;(#?#0,00 $)" Word format.
    CurrencyFormat = 7

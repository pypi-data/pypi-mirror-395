from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LineSpacingRule(Enum):
    """
    Enum for paragraph line spacing rule.

    """

    # The line spacing can be greater than or equal to, but never less than,
    # the value specified in the LineSpacing property. 
    AtLeast = 0
    # The line spacing never changes from the value specified in the LineSpacing property, 
    # even if a larger font is used within the paragraph. 
    Exactly = 1
    # The line spacing is specified in the LineSpacing property as the number of lines. 
    # One line equals 12 points. 
    Multiple = 2

from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SectionBreakType(Enum):
    """
    Specifies type of the section break code.
    """

    # The section starts on the same page.
    NoBreak = 0
    # The section starts from a new column.
    NewColumn = 1
    # The section starts from a new page. 
    NewPage = 2
    # The section starts on a new even page. 
    EvenPage = 3
    # The section starts on a new odd page. 
    Oddpage = 4


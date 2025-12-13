from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HeaderType(Enum):
    """
    Enum class representing different types of headers and footers.
    """

    # Specifies InvalidValue.
    InvalidValue = -1
    # Header for even numbered pages.
    EvenHeader = 0
    # Header for odd numbered pages.
    OddHeader = 1
    # Footer for even numbered pages.
    EvenFooter = 2
    # Footer for odd numbered pages.
    OddFooter = 3
    # Header for the first page of the section.
    FirstPageHeader = 4
    # Footer for the first page of the section.
    FirstPageFooter = 5


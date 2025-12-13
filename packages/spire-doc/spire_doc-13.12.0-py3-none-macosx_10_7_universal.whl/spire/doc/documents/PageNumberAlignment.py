from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PageNumberAlignment(Enum):
    """
    Specifies PageNumber alignment.
    """

    # Aligns the page number to the left side of the page
    Left = 0
    # Centers the page number horizontally on the page
    Center = -4
    # Aligns the page number to the right side of the page
    Right = -8
    # Aligns the page to the inside margin of the page (useful for double-sided printing)
    Inside = -12
    # Aligns the page to the outside margin of the page (useful for double-sided printing)
    Outside = -16


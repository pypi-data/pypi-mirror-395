from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PageBorderOffsetFrom(Enum):
    """
    Specifies the position of page border.
    """

    # Page border is measured from text.
    Text = 0
    # Page border is measured from the edge of the page.
    PageEdge = 1


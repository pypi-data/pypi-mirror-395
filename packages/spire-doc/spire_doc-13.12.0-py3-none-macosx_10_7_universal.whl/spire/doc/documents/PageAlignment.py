from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PageAlignment(Enum):
    """
    Specifies alignment of the text on a page.
    """

    # Text is aligned at the top of the page.
    Top = 0
    # Text is aligned at the middle of the page.
    Middle = 1
    # Text is spanned to fill the page. 
    Justified = 2
    # Text is aligned at the bottom of the page.
    Bottom = 3

from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PageBordersApplyType(Enum):
    """
    Specifies on which pages border is applied.
    """

    # Page border applies to all pages.
    AllPages = 0
    # Page border applies only to first pages.
    FirstPage = 1
    # Page border applies to all pages except the first.
    AllExceptFirstPage = 2


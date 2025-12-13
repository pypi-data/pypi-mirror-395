from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HtmlExportListLabelsType(Enum):
    """
    Specifies type of the Header/Footer.

    """

    #Specifies Auto list labels type.
    Auto = 0
    #Specifies InlineText list labels type.
    InlineText = 1
    #Specifies HtmlTags list labels type.
    HtmlTags = 2


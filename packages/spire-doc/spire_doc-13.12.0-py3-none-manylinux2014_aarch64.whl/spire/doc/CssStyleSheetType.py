from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CssStyleSheetType(Enum):
    """
    Enum class representing the type of CSS style sheet.

    """

    # Specifies External sheet type.
    External = 0
    # Specifies Internal sheet type.
    Internal = 1

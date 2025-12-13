from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class AutoFitBehaviorType(Enum):
    """
    Specifies how Microsoft Word resizes a table when the AutoFit feature is used.
    """

    # The table is automatically sized to fit the content contained in the table.
    AutoFitToContents = 1
    # The table is automatically sized to the width of the active window.
    AutoFitToWindow = 2
    # The table is set to a fixed size, regardless of the content, and is not automatically sized.
    FixedColumnWidths = 0

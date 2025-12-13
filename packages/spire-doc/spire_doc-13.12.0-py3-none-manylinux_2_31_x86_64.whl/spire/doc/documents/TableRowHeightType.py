from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TableRowHeightType(Enum):
    """
    Specifies the table row height type.
    
    """

    # "At least" table row height type
    AtLeast = 0
    # " Exactly" table row height type
    Exactly = 1
    # The height will grow automatically to accommodate all text inside an object.
    Auto = 2

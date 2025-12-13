from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MoveRevisionType(Enum):
    """
    The type of move revision mark.
    """

    MoveFrom = 0,
    MoveTo = 1,
    none = 2


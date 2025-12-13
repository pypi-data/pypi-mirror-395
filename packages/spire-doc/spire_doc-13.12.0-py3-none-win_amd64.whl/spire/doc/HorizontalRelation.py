from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HorizontalRelation(Enum):
    """
    The enum defines the horizontal relation.

    """

    # The "Column" horizontal relation
    Column = 0
    # The "Margin" horizontal relation
    Margin = 1
    # The "Page" horizontal relation
    Page = 2

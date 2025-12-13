from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class GroupEventType(Enum):
    """
    Enum class representing different types of group events.
    """

    # The group start
    GroupStart = 0
    # The group end
    GroupEnd = 1
    # The table start
    TableStart = 2
    # The table end
    TableEnd = 3


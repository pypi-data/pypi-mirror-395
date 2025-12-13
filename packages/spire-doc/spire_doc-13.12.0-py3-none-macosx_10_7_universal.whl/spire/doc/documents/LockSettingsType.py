from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LockSettingsType(Enum):
    """
    Enum class representing different lock settings types.
    """

    # No locking.
    UnLocked = 0
    # Contents cannot be edited at runtime.
    ContentLocked = 1
    # Contents cannot be edited at runtime and SDT cannot be deleted.
    SDTContentLocked = 2
    # SDT cannot be deleted.
    SDTLocked = 3


from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class RtfTokenType(Enum):
    """
    Enum class representing the types of RTF tokens.
    """

    # A group start token (e.g., \{)
    GroupStart = 0
    # A group end token (e.g., \})
    GroupEnd = 1
    # A control word (e.g., \par, \b, \i)
    ControlWord = 2
    # A plain text token
    Text = 3
    # A table entry marker
    TableEntry = 4
    # Unknown type
    Unknown = 5

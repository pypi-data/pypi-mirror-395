from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class EndnotePosition(Enum):
    """
    Enum class representing the endnote position of the Document.

    """

    # Placed the Endnote on End of the section.
    DisplayEndOfSection = 0
    # Placed the Endnote on End of the section.
    DisplayEndOfDocument = 3

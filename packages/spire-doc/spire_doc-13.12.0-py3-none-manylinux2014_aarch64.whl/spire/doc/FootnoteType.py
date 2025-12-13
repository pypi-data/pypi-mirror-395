from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FootnoteType(Enum):
    """
    Specifies the Type of the FootNote.
    """

    # Specifies object is a footnote. 
    Footnote = 0
    # Specifies object is a endnote.
    Endnote = 1

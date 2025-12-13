from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class StyleType(Enum):
    """
    Enum class that specifies the type of the Style.
    
    """

    # The style is a paragraph style. 
    ParagraphStyle = 1
    # The style is a character style. 
    CharacterStyle = 2
    # The style is a table style.
    TableStyle = 3
    # The style is a list style.
    ListStyle = 4
    # The style is other kind of style. 
    OtherStyle = 4

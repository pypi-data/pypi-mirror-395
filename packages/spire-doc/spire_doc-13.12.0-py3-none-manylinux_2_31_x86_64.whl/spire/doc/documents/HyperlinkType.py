from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HyperlinkType(Enum):
    """
    Enum class that specifies the type of the hyperlink.

    """

    # No links. 
    none = 0
    # Links to another file.
    FileLink = 1
    # Links to a web page. 
    WebLink = 2
    # Link to e-mail.
    EMailLink = 3
    # Bookmark link.
    Bookmark = 4

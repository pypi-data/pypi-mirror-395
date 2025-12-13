from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CommentMarkType(Enum):
    """
    Defines types of comment mark.
    """

    # Comment start mark type.
    CommentStart = 0
    # Comment end mark type
    CommentEnd = 1


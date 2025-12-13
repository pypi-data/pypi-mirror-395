from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FollowCharacterType(Enum):
    """
    The type of character following the number text for the paragraph
    """

    # List levels number or bullet is followed by tab
    Tab = 0
    # List levels number or bullet is followed by space
    Space = 1
    # Follow character isn't used
    Nothing = 2

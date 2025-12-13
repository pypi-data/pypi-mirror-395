from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class Emphasis(Enum):
    """
    Specifies the emphasis mark type.

    """

    # No Emphasis Mark
    none = 0
    # Dot Emphasis Mark Above Characters
    Dot = 1
    # Comma Emphasis Mark Above Characters
    CommaAbove = 2
    # Circle Emphasis Mark Above Characters
    CircleAbove = 3
    # Dot Emphasis Mark Below Characters
    DotBelow = 4
    # Represents the default emphasis mark type.
    Default = 0

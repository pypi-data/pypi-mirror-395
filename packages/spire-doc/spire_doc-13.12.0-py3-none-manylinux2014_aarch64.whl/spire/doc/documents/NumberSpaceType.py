from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class NumberSpaceType(Enum):
    """
    Specifies the number spacing type.
    """

    # Apply the default number spacing.
    Default = 0
    # Apply the default number spacing.
    Proportional = 1
    # Apply the default number spacing.
    Tabular = 2


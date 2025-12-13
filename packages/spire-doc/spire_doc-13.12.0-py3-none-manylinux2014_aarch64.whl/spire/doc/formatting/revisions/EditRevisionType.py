from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class EditRevisionType(Enum):
    """
    Enum class representing types of edit revisions.
    """

    # Type of revision mark is insertion.
    Insertion = 0
    # Type of revision mark is Deletion.
    Deletion = 1


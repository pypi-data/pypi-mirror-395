from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SubSuperScript(Enum):
    """
    Specifies the type of the SubSuperScript.
    """

    # No sub- or superscript.
    none = 0
    # Specified superscript format.
    SuperScript = 1
    # Specified subscript format.
    SubScript = 2
    # Specified baseline format.
    BaseLine = 0

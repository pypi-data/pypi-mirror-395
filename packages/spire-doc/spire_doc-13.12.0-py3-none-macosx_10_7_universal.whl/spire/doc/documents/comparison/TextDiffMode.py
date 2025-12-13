from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc


class TextDiffMode(Enum):
    """
    Specifies types of comparison.
    """

    #Character level comparison.
    Char = 0
    #Word level comparison.
    Word = 1


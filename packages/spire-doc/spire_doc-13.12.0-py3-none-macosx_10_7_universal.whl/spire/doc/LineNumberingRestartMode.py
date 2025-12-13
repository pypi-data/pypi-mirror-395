from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LineNumberingRestartMode(Enum):
    """
    Specifies when line numbering is restarted. 

    """

    # Line numbering restarts at the start of every page
    RestartPage = 0
    # Line numbering restarts at the section start. 
    RestartSection = 1
    # Line numbering continuous from the previous section. 
    Continuous = 2
    # None.
    none = 255

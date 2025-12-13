from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FootnoteRestartRule(Enum):
    """
    Specifies the restart rule for footnotes.
    
    """

    # Numbering continuous throughout the document.
    DoNotRestart = 0
    # Numbering restarts at each section.
    RestartSection = 1
    # Numbering restarts at each page.
    RestartPage = 2
    # Equals <see cref="DoNotRestart"/>.
    Default = 0

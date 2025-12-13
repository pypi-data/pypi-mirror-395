from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentSecurity(Enum):
    """
    Enum class representing different document security options.
    """

    # Indicates that the document security level is none.
    none = 0
    # Indicates that the document security level is password protected.
    PasswordProtected = 1
    # Indicates that the document security level is recommended to be read-only.
    ReadOnlyRecommended = 2
    # Indicates that the document security level is forced to be read-only.
    ReadOnlyEnforced = 4
    # Indicates that the document security level is read-only, except for annotations.
    ReadOnlyExceptAnnotations = 8

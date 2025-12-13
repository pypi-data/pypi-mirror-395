from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ProtectionType(Enum):
    """
    Enum class representing the type of protection in the document.

    """

    # Only modify comments in the document. 
    AllowOnlyComments = 1
    # Only enter data in the form fields in the document. 
    AllowOnlyFormFields = 2
    # Only reading are allowed in the document. 
    AllowOnlyReading = 3
    # Only add revision marks to the document. 
    AllowOnlyRevisions = 0
    # Not protected
    NoProtection = -1


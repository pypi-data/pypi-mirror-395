from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfPermissionsFlags(Enum):
    """
    Specifies the available permissions set for the signature.
    """

    # Not all permissions
    none = 0
    # Default value is 2876. A common document contains all privileges
    Default = 2876
    # Print the document.
    Print = 4
    # Edit content.
    EditContent = 8
    # Copy content.
    CopyContent = 16
    # Add or modify text annotations, fill in interactive form fields.
    EditAnnotations = 32
    # Fill form fields. (Only for 128 bits key).
    FillFields = 256
    # Copy accessibility content.
    AccessibilityCopyContent = 512
    # Assemble document permission. (Only for 128 bits key).
    AssembleDocument = 1024
    # Full quality print.
    FullQualityPrint = 2244


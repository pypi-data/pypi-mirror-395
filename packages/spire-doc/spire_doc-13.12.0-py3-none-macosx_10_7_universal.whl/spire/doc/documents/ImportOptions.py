from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ImportOptions(Enum):
    """
    Enum class for import options.
    """

    # Keep the source document's formatting intact.
    KeepSourceFormatting = 0
    # Merge the source document's formatting with the destination document's styles.
    MergeFormatting = 1
    # Import only the text content, discarding all formatting.
    KeepTextOnly = 2
    # Use the destination document's styles for the imported content.
    UseDestinationStyles = 3


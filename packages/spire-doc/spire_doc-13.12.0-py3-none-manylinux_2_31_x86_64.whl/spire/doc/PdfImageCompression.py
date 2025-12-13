from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfImageCompression(Enum):
    """
    Indicates the compression method used for images within the PDF file.
    """

    #Automatically chooses the optimal compression method for each image.
    Auto = 0,
    #Jpeg compression.
    Jpeg = 1



from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc


class ImageType(Enum):
    """
    Specifies the image type.
    """

    # Represents a bitmap image format (e.g., BMP, PNG, JPEG).
    Bitmap = 0
    # Represents a metafile format (e.g., WMF, EMF).
    Metafile = 1


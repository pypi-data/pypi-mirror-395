from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfEncryptionKeySize(Enum):
    """
    Specifies length of the encryption key for encryption.
    """

    # The key is 40 bit long.
    Key40Bit = 1
    # The key is 128 bit long.
    Key128Bit = 2
    # The key is 256 bit long.
    Key256Bit = 3


from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfDigitalSignatureHashAlgorithm(Enum):
    """
    Represents the hash algorithms supported for digital signatures in PDF documents.
    """

    #SHA384 hash algorithm.
    Sha256 = 0
    #SHA384 hash algorithm.
    Sha384 = 1
    #SHA512 hash algorithm.
    Sha512 = 2
    #RIPEMD-160 is a cryptographic hash function that produces a 160-bit (20-byte) hash value. 
    #It is commonly used for data integrity checks and in various security applications.
    RipeMD160 = 3


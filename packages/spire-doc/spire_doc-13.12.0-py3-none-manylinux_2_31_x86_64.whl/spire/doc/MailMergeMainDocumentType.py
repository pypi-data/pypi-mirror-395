from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MailMergeMainDocumentType(Enum):
    """
    Enum class representing the types of mail merge main documents.
    """

    # This document is not a mail merge document.
    NotAMergeDocument = 0
    # Specifies that the mail merge source document is of the form letter type.
    FormLetters = 1
    # Specifies that the mail merge source document is of the mailing label type.
    MailingLabels = 2
    # Specifies that the mail merge source document is of the envelope type.
    Envelopes = 4
    # Specifies that the mail merge source document is of the catalog type.
    Catalog = 8
    # Specifies that the mail merge source document is of the e-mail message type.
    Email = 16
    # Specifies that the mail merge source document is of the fax type.
    Fax = 32
    #Equals to <see cref="NotAMergeDocument"/>
    Default = 0

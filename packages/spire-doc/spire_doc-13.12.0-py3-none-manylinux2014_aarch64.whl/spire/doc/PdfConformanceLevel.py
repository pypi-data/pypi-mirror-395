from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfConformanceLevel(Enum):
    """
    Specifies the Pdf document's Conformance-level.
    """

    #Specifies Default / No Conformance.
    none = 0
    #This PDF/A ISO standard [ISO 19005-1:2005] is based on Adobe PDF version 1.4
    #and This Level B conformance indicates minimal compliance to ensure that the 
    #rendered visual appearance of a conforming file is preservable over the long term.
    Pdf_A1B = 1
    #This PDF/X-1a:2001 ISO standard [ISO 15930-1] is based on Adobe PDF version 1.3
    #which uses only CMYK + Spot Color and this compliance to ensure that the 
    #contents will be reliably reproduced in the repress environment.
    Pdf_X1A2001 = 2
    #PDF/A-1a ensures the preservation of a document's logical structure and con-tent text stream in natural reading order. 
    Pdf_A1A = 3
    #PDF/A-2a standard,Only check the standard from the pdfaid:part and pdfaid:conformance node,And only check.
    Pdf_A2A = 4
    #PDF/A-2b standard,Only check the standard from the pdfaid:part and pdfaid:conformance node,And only check.
    Pdf_A2B = 5
    #PDF/A-3a standard,Only check the standard from the pdfaid:part and pdfaid:conformance node,And only check
    Pdf_A3A = 6
    #PDF/A-3b standard,Only check the standard from the pdfaid:part and pdfaid:conformance node,And only check
    Pdf_A3B = 7

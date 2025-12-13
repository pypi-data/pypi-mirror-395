from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FileFormat(Enum):
    """
    Enum class representing different types of file formats.
    """

    # Microsoft Word 97 - 2003 Binary Document. 
    Doc = 0
    # Microsoft Word 97 - 2003 Binary Document or Template.
    Dot = 5
    # Microsoft Word 2007 Document.
    Docx = 10
    # Microsoft Word 2010 Document
    Docx2010 = 11
    # Microsoft Word 2013 Document
    Docx2013 = 12
    # Microsoft Word 2016 Document
    Docx2016 = 13
    # Microsoft Word 2019 Document
    Docx2019 = 14
    # Microsoft Word 2007 Template format.
    Dotx = 20
    # Microsoft Word 2010 Template format.
    Dotx2010 = 21
    # Microsoft Word 2013 Template format.
    Dotx2013 = 22
    # Microsoft Word 2016 Template format.
    Dotx2016 = 23
    # Microsoft Word 2019 Template format.
    Dotx2019 = 24
    # Microsoft Word 2007 macro enabled file format.
    Docm = 30
    # Microsoft Word 2010 macro enabled file format.
    Docm2010 = 31
    #  Microsoft Word 2013 macro enabled file format.
    Docm2013 = 32
    #  Microsoft Word 2019 macro enabled file format.
    Docm2016 = 33
    #  Microsoft Word 2019 macro enabled file format.
    Docm2019 = 34
    # Microsoft Word 2007 macro enabled template format.
    Dotm = 40
    # Microsoft Word 2010 macro enabled template format.
    Dotm2010 = 41
    # Microsoft Word 2013 macro enabled template format.
    Dotm2013 = 42
    # Microsoft Word 2016 macro enabled template format.
    Dotm2016 = 43
    # Microsoft Word 2019 macro enabled template format.
    Dotm2019 = 44
    # Office Open Xml
    OOXML = 50
    # Word xml format for for word 2003
    WordML = 60
    # Word xml format for word 2007-2013
    WordXml = 70
    # OpenDocument format.
    Odt = 80
    #OpenDocument Template format
    Ott = 90
    # PDF format
    PDF = 100
    # Text file format.
    Txt = 110
    # Rtf format
    Rtf = 120
    # Scalable vector graphics format
    SVG = 130
    # Xml file format.
    Xml = 140
    # Mhtml format.
    Mhtml = 150
    # Html format.
    Html = 160
    # XPS format
    XPS = 170
    # EPub format
    EPub = 180
    # The document is in the Word 6 or Word 95 format. Spire.Doc does not currently support loading such documents. 
    DocPre97 = 190
    # PostScript (PS) format.
    PostScript = 200
    # Printer Command Language (PCL) format.
    PCL = 210
    #  Open Fixed-layout Document (OFD) format.
    OFD = 220
    #  Only for Spire Online editing.
    OnlineDoc = 230
    #  Word processing system format.
    Wps = 240
    #  Word processing technician format.
    Wpt = 250
    # Markdown format.
    Markdown = 260
    # Instructs Spire.Doc to recognize the format automatically. 
    Auto = 300
    
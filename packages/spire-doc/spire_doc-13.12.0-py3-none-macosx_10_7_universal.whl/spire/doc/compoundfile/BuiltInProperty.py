from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class BuiltInProperty(Enum):
    """
    Enum class representing built-in properties in a document.
    """

    #Title document property Id.
    Title = 2
    #Subject document property Id.
    Subject = 3
    #Author document property Id.
    Author = 4
    #Keywords document property Id.
    Keywords = 5
    #Comments document property Id.
    Comments = 6
    #Template document property Id.
    Template = 7
    #LastAuthor document property Id.
    LastAuthor = 8
    #Revnumber document property Id.
    RevisionNumber = 9
    #EditTime document property Id.
    EditTime = 10
    #LastPrinted document property Id.
    LastPrinted = 11
    #CreationDate document property Id.
    CreationDate = 12
    #LastSaveDate document property Id.
    LastSaveDate = 13
    #PageCount document property Id.
    PageCount = 14
    #WordCount document property Id.
    WordCount = 15
    #CharCount document property Id.
    CharCount = 16
    #Thumbnail document property Id.
    Thumbnail = 17
    #ApplicationName document property Id.
    ApplicationName = 18
    #Ssecurity document property Id.
    Security = 19
    #Category Id.
    Category = 1000
    #Target format for presentation (35mm, printer, video, and so on) id.
    PresentationTarget = 1001
    #ByteCount Id.
    ByteCount = 1002
    #LineCount Id.
    LineCount = 1003
    #ParCount Id.
    ParagraphCount = 1004
    #SlideCount Id.
    SlideCount = 1005
    #NoteCount Id.
    NoteCount = 1006
    #HiddenCount Id.
    HiddenCount = 1007
    #MmclipCount Id.
    MultimediaClipCount = 1008
    #ScaleCrop property Id.
    ScaleCrop = 1009
    #HeadingPair Id.
    HeadingPair = 1010
    #DocParts Id.
    DocParts = 1011
    #Manager Id.
    Manager = 1012
    #Company Id.
    Company = 1013
    #LinksDirty Id.
    LinksDirty = 1014
    #MUST be a VT_I4 TypedPropertyValue ([MS-OLEPS] section 2.15) property. The integer value of the 
    #property specifies an Eschertimate of the number of characters in the document including whitespace.
    CharactersWithSpaces = 1015
    #MUST be a VT_BOOL TypedPropertyValue ([MS-OLEPS] section 2.15) property. 
    #The property value MUST be FALSE (0x00000000).
    ShareDoc = 1016
    #MUST NOT be written (to built-in properties). The base URL property is persisted to the User Defined Property 
    #Set with the _PID_LINKBASE property name.
    LinkBase = 1017
    #MUST NOT be written (to built-in properties). The hyperlinks property is persisted to the User Defined Property 
    #Set with the _PID_HLINKS property name.
    Hyperlinks = 1018
    #MUST be a VT_BOOL TypedPropertyValue ([MS-OLEPS] section 2.15) property. The property value 
    #specifies TRUE (any value other than 0x00000000) if the _PID_HLINKS property in the User 
    #Defined Property Set has changed outside of the application, which would require hyperlink 
    #fix up on document load.
    HyperlinksChanged = 1019
    #Version of the application that created the document.
    #MUST be a VT_I4 TypedPropertyValue ([MS-OLEPS] section 2.15) property. The unsigned integer 
    #value of the property specifies the version of the application that wrote the property set storage. 
    #The two high order bytes specify an unsigned integer specifying the major version number. 
    #The two low order bytes specify an unsigned integer specifying the minor version number. 
    #The value MUST have the major version number set to a nonzero value, and the minor version 
    #number SHOULD always be 0x0000. The minor version number MAY be set to the minor version 
    #number of the application that wrote the property set storage.
    Version = 1020
    #Represents a digital signature in an Excel document, used to verify the integrity and authenticity of the file.
    ExcelDigitalSignature = 1021
     #MUST be a VtString property. VtString.stringValue specifies the content type of the file. 
    #MAY be absent.
    ContentType = 1022
    #MUST be a VtString property. VtString.stringValue specifies the document status. MAY be absent.
    ContentStatus = 1023
    #MUST be a VtString property. SHOULD be absent.
    Language = 1024
    #MUST be a VtString property. SHOULD be absent.
    DocVersion = 1025

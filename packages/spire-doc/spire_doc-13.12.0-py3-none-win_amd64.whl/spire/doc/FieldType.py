from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FieldType(Enum):
    """
    Enum class representing the type of fields.
    """

    # Field type is not specified or unknown.
    FieldNone = 0
    # Specifies that the field contains data created by an add-in. 
    FieldAddin = 81
    # Offset subsequent text within a line to the left, right, up or down. 
    FieldAdvance = 84
    # Prompt the user for text to assign to a bookmark. 
    FieldAsk = 38
    # The name of the document's author from Summary Info.
    FieldAuthor = 17
    # Insert an automatic number. 
    FieldAutoNum = 54
    # Insert an automatic number in legal format.
    FieldAutoNumLegal = 53
    # Insert an automatic number in outline format.
    FieldAutoNumOutline = 52
    # Insert an AutoText entry. 
    FieldAutoText = 79
    #  Insert text based on style. 
    FieldAutoTextList = 89
    # Insert a delivery point barcode. 
    FieldBarcode = 63
    # According to the citation style you choose, show an information about a particular source.
    FieldCitation = 1980
    # The comments from Summary Info.
    FieldComments = 19
    # Compares two values. 
    FieldCompare = 80
    # The date the document was created.
    FieldCreateDate = 21
    # Specifies data. 
    FieldData = 40
    # Insert data from an external database. 
    FieldDatabase = 78
    # Specified Today`s Date.
    FieldDate = 31
    # Specified Type as DDE.
    FieldDDE = 45
    # Specified Type as DDEAuto.
    FieldDDEAuto = 46
    #  Insert the value of the property
    FieldDocProperty = 85
    # Insert the value of the document variable. 
    FieldDocVariable = 64
    # The total document editing time. 
    FieldEditTime = 25
    # Specifies OLE embedded object.
    FieldEmbed = 58
    # Specified Empty Field.
    FieldEmpty = -1
    # Specifies Field Expression.
    FieldFormula = 34
    FieldExpression = 34
    #  The document's name.
    FieldFileName = 29
    # The size on disk of the active document. 
    FieldFileSize = 69
    #  Prompt the user for text to insert in the document.
    FieldFillIn = 39
    # Specifies Type as FootnoteRef.
    FieldFootnoteRef = 5
    # Specifies Check box control.
    FieldFormCheckBox = 71
    # Specifies Drop Down box control.
    FieldFormDropDown = 83
    # Specifies Text control.
    FieldFormTextInput = 70
    # The EQ field is used to display a mathematical equation
    FieldEquation = 49
    # Specifies FieldGlossary.
    FieldGlossary = 47
    # Specifies GoToButton control.
    FieldGoToButton = 50
    # Specifies HTMLActiveX control.
    FieldHTMLActiveX = 91
    # Specifies Hyperlink control.
    FieldHyperlink = 88
    # Evaluate arguments conditionally. 
    FieldIf = 7
    # Specifies Type as Import.
    FieldImport = 55
    # Specifies Type as Export.
    FieldInclude = 36
    # Insert a picture from a file. 
    FieldIncludePicture = 67
    # Insert text from a file.
    FieldIncludeText = 68
    # Create an index. 
    FieldIndex = 8
    # Mark an index entry. 
    FieldIndexEntry = 4
    # Data from Summary Info. 
    FieldInfo = 14
    # The keywords from Summary Info.
    FieldKeyWord = 18
    # Name of user who last saved the document. 
    FieldLastSavedBy = 20
    # Linked OLE2 object.
    FieldLink = 56
    # Insert an element in a list.
    FieldListNum = 90
    # Run a macro.
    FieldMacroButton = 51
    # Insert a mail merge field.
    FieldMergeField = 59
    # The number of the current merge record.
    FieldMergeRec = 44
    # Merge record sequence number. 
    FieldMergeSeq = 75
    # Go to the next record in a mail merge. 
    FieldNext = 41
    # Conditionally go to the next record in a mail merge. 
    FieldNextIf = 42
    # Insert the number of a footnote or endnote.
    FieldNoteRef = 72
    # The number of characters in the document. 
    FieldNumChars = 28
    #  The number of pages in the document. 
    FieldNumPages = 26
    # The number of words in the document. 
    FieldNumWords = 27
    # Represents an ActiveX control such as a command button etc.
    FieldOCX = 87
    # Insert the number of the current page.
    FieldPage = 33
    # Insert the number of the page containing the specified bookmark. 
    FieldPageRef = 37
    # Download commands to a printer. 
    FieldPrint = 48
    # The date the document was last printed.
    FieldPrintDate = 23
    # Stores data for documents converted from other file formats.
    FieldPrivate = 77
    # Insert literal text. 
    FieldQuote = 35
    # Insert the text marked by a bookmark. 
    FieldRef = 3
    # Create an index, table of contents, table of figures, and/or table of authorities by using multiple documents. 
    FieldRefDoc = 11
    # Insert the number of times the document has been saved. 
    FieldRevisionNum = 24
    # The date the document was last saved.
    FieldSaveDate = 22
    # Insert the number of the current section. 
    FieldSection = 65
    # Insert the total number of pages in the section. 
    FieldSectionPages = 66
    # Insert an automatic sequence number. 
    FieldSequence = 12
    # Assign new text to a bookmark.
    FieldSet = 6
    # Conditionally skip a record in a mail merge. 
    FieldSkipIf = 43
    # Insert the text from a like-style paragraph. 
    FieldStyleRef = 10
    #  The document's subject from Summary Info.
    FieldSubject = 16
    #  The document's Subscriber from Summary Info.
    FieldSubscriber = 82
    #  Insert a special character
    FieldSymbol = 57
    # The name of the template attached to the document.
    FieldTemplate = 30
    #  The current time.
    FieldTime = 32
    # The document's title from Summary Info.
    FieldTitle = 15
    # Create a table of authorities.
    FieldTOA = 73
    # Make a table of authorities entry. 
    FieldTOAEntry = 74
    # Create a table of contents.
    FieldTOC = 13
    #  Make a table of contents entry. 
    FieldTOCEntry = 9
    # Address from Tools Options User Info. 
    FieldUserAddress = 62
    # Initials form Tools Options User Info. 
    FieldUserInitials = 61
    #  Name from Tools Options User Info. 
    FieldUserName = 60
    # Specifies Type as Shape.
    FieldShape = 95
    # Specifies Type as BIDIOUTLINE.
    FieldBidiOutline = 92
    # Specifies AddressBlock
    FieldAddressBlock = 93
    #  Specifies Type as Unknown.
    FieldUnknown = 1000
    # Specifies that the field was unable to be parsed.
    FieldCannotParse = 1
    # Greeting Line field
    FieldGreetingLine = 94
    # Specifies that the field represents a REF field where the keyword has been omitted.
    FieldRefNoKeyword = 2
    # Macro Field.
    FieldMacro = 76
    # MergeBarcode Field.
    FieldMergeBarcode = 6302
    # DisplayBarcode Field.
    FieldDisplayBarcode = 6301
    # Represents a bibliography field.
    FieldBibliography = 100500

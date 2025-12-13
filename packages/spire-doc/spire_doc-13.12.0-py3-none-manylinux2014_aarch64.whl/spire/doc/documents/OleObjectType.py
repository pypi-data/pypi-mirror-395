from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class OleObjectType(Enum):
    """
    Enum class that defines the types of OLE object.
    """

    # Type is not defined
    Undefined = 0
    # Adobe Acrobat Document. File has ".pdf" extension.
    AdobeAcrobatDocument = 1
    # Bitmap Image. File has ".png" extension.
    BitmapImage = 2
    # Media Clip
    MediaClip = 3
    # Equation
    Equation = 4
    # Graph Chart
    GraphChart = 5
    # Excel 97-2003 Worksheet. File has ".xls" extension
    Excel_97_2003_Worksheet = 6
    # Excel Binary Worksheet. File has ".xlsb" extension
    ExcelBinaryWorksheet = 7
    # Excel chart. File has ".xls" extension
    ExcelChart = 8
    # Excel Macro-Enabled Worksheet. File has ".xlsm" extension.
    ExcelMacroWorksheet = 9
    # Excel Worksheet. File has ".xlsx" extension.
    ExcelWorksheet = 10
    # PowerPoint 97-2003 Presentation. File has ".ppt" extension.
    PowerPoint_97_2003_Presentation = 11
    # PowerPoint 97-2003 Slide. File has ".sld" extension.
    PowerPoint_97_2003_Slide = 12
    # PowerPoint Macro-Enabled Presentation. File has ".pptm" extension.
    PowerPointMacroPresentation = 13
    # PowerPoint Macro-Enabled Slide. File has ".sldm" extension.
    PowerPointMacroSlide = 14
    # PowerPoint Presentation. File has ".pptx" extension.
    PowerPointPresentation = 15
    # PowerPoint Slide. File has ".sldx" extension.
    PowerPointSlide = 16
    # Word 97-2003 Document. File has ".doc" extension.
    Word_97_2003_Document = 17
    # Word Document. File has ".docx" extension.
    WordDocument = 18
    # Word Macro-Enabled Document. File has ".docm" extension.
    WordMacroDocument = 19
    # Visio Deawing
    VisioDrawing = 20
    # MIDI Sequence
    MIDISequence = 21
    # OpenDocument Presentation
    OpenDocumentPresentation = 22
    # OpenDocument Spreadsheet
    OpenDocumentSpreadsheet = 23
    # OpenDocument Text
    OpenDocumentText = 24
    # OpenOffice.org 1.1 Spreadsheet
    OpenOfficeSpreadsheet1_1 = 25
    # OpenOffice.org 1.1 Text
    OpenOfficeText_1_1 = 26
    # Package
    Package = 27
    # Video Clip
    VideoClip = 28
    # Wave Sound
    WaveSound = 29
    # WordPad Document
    WordPadDocument = 30
    # OpenOffice spreadsheet
    OpenOfficeSpreadsheet = 31
    # OpenOffice Text
    OpenOfficeText = 32
    # Visio Deawing for visio 2013.
    VisioDrawing_2013 = 33
    # word picture
    WordPicture = 34
    # Equation DSMT4
    MathType = 35
    # Word.Template.12
    WordTemplate = 36
    # Microsoft Word Macro-Enabled Template
    WordMacroTemplate = 37

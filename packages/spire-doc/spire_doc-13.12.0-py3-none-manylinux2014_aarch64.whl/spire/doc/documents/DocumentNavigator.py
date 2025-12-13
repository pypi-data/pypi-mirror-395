from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentNavigator (SpireObject) :
    @dispatch
    def __init__(self):
        """
        Initializes a new instance of the DocumentNavigator class with no params.

        Returns:
            None
        """
        GetDllLibDoc().DocumentNavigator_CreateDocumentNavigator.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_CreateDocumentNavigator,)
        super(DocumentNavigator, self).__init__(intPtr)

    """

    """
    @dispatch
    def __init__(self, doc:Document):
        """

        """
        intPdoc:c_void_p = doc.Ptr

        GetDllLibDoc().DocumentNavigator_CreateDocumentNavigatorD.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_CreateDocumentNavigatorD.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_CreateDocumentNavigatorD,intPdoc)
        super(DocumentNavigator, self).__init__(intPtr)

    """

    """
    @property
    def IsAtStartOfParagraph(self)->bool:
        """
        Indicates whether the cursor is at the start of the current paragraph.
        """
        GetDllLibDoc().DocumentNavigator_get_IsAtStartOfParagraph.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_IsAtStartOfParagraph.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().DocumentNavigator_get_IsAtStartOfParagraph,self.Ptr)
        return ret

    @property
    def IsAtEndOfParagraph(self)->bool:
        """
        Indicates whether the cursor is at the end of the current paragraph.
        """
        GetDllLibDoc().DocumentNavigator_get_IsAtEndOfParagraph.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_IsAtEndOfParagraph.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().DocumentNavigator_get_IsAtEndOfParagraph,self.Ptr)
        return ret


    def InsertDocumentObject(self ,documentObject:'DocumentObject'):
        """
        Inserts a DocumentObject.
        """
        intPtrdocumentObject:c_void_p = documentObject.Ptr

        GetDllLibDoc().DocumentNavigator_InsertDocumentObject.argtypes=[c_void_p ,c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_InsertDocumentObject,self.Ptr, intPtrdocumentObject)

    @property

    def CurrentDocumentObject(self)->'DocumentObject':
        """
        Gets the currently selected node in the document (the position of the cursor). Content inserted using the Navigator is inserted at this location.
        """
        GetDllLibDoc().DocumentNavigator_get_CurrentDocumentObject.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CurrentDocumentObject.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CurrentDocumentObject,self.Ptr)
        ret = None if intPtr==None else DocumentObject(intPtr)
        return ret


    @property

    def CurrentParagraph(self)->'Paragraph':
        """
        Gets the current paragraph object (the paragraph where the cursor is located).
        """
        GetDllLibDoc().DocumentNavigator_get_CurrentParagraph.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CurrentParagraph.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CurrentParagraph,self.Ptr)
        ret = None if intPtr==None else Paragraph(intPtr)
        return ret


    @property

    def CurrentBody(self)->'Body':
        """
        Gets the main text body object (Body object) of the current paragraph.
        """
        GetDllLibDoc().DocumentNavigator_get_CurrentBody.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CurrentBody.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CurrentBody,self.Ptr)
        ret = None if intPtr==None else Body(intPtr)
        return ret


    @property

    def CurrentSection(self)->'Section':
        """
        Gets the current section object (the section where the cursor is located).
        """
        GetDllLibDoc().DocumentNavigator_get_CurrentSection.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CurrentSection.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CurrentSection,self.Ptr)
        ret = None if intPtr==None else Section(intPtr)
        return ret


    def MoveToDocumentStart(self):
        """
        Moves the cursor to the start of the document.
        """
        GetDllLibDoc().DocumentNavigator_MoveToDocumentStart.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToDocumentStart,self.Ptr)

    def MoveToDocumentEnd(self):
        """
        Moves the cursor to the end of the document.
        """
        GetDllLibDoc().DocumentNavigator_MoveToDocumentEnd.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToDocumentEnd,self.Ptr)


    def MoveToSection(self ,sectionIndex:int):
        """
        Moves the cursor to a section.
        """
        
        GetDllLibDoc().DocumentNavigator_MoveToSection.argtypes=[c_void_p ,c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToSection,self.Ptr, sectionIndex)


    def MoveToHeaderFooter(self ,headerFooterType:'HeaderFooterType'):
        """
        Moves the cursor to a Header or Footer.
        """
        enumheaderFooterType:c_int = headerFooterType.value

        GetDllLibDoc().DocumentNavigator_MoveToHeaderFooter.argtypes=[c_void_p ,c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToHeaderFooter,self.Ptr, enumheaderFooterType)


    def MoveToField(self ,field:'Field',isAfter:bool):
        """
        Moves the cursor to a field.

        Args:
            field:The field.
            isAfter:Whether Move to after the field.

        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibDoc().DocumentNavigator_MoveToField.argtypes=[c_void_p ,c_void_p,c_bool]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToField,self.Ptr, intPtrfield,isAfter)


    def MoveToParagraph(self ,paragraphIndex:int,characterIndex:int):
        """
        Moves the cursor to a Paragraph.

        Args:
            paragraphIndex:index of the paragraph in the document.
            characterIndex:Character position within the paragraph.
        """
        
        GetDllLibDoc().DocumentNavigator_MoveToParagraph.argtypes=[c_void_p ,c_int,c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToParagraph,self.Ptr, paragraphIndex,characterIndex)


    def MoveToCell(self ,tableIndex:int,rowIndex:int,columnIndex:int,characterIndex:int):
        """
        Moves the cursor to a specific cell.

        Args:
            tableIndex:index of the table in the document.
            rowIndex:index of the row in the table.
            columnIndex:index of the column in the row.
            characterIndex:Character position within the cell .
        """
        
        GetDllLibDoc().DocumentNavigator_MoveToCell.argtypes=[c_void_p ,c_int,c_int,c_int,c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveToCell,self.Ptr, tableIndex,rowIndex,columnIndex,characterIndex)


    def MoveTo(self ,documentObject:'DocumentObject'):
        """
        Moves the cursor to the specified documentObject.
        """
        intPtrdocumentObject:c_void_p = documentObject.Ptr

        GetDllLibDoc().DocumentNavigator_MoveTo.argtypes=[c_void_p ,c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_MoveTo,self.Ptr, intPtrdocumentObject)


    def DeleteRow(self ,tableIndex:int,rowIndex:int)->'TableRow':
        """
        Deletes a specific row in the specified table.

        Args:
            tableIndex:index of the table in the document.
            rowIndex:index of the row in the table.
        """
        
        GetDllLibDoc().DocumentNavigator_DeleteRow.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibDoc().DocumentNavigator_DeleteRow.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_DeleteRow,self.Ptr, tableIndex,rowIndex)
        ret = None if intPtr==None else TableRow(intPtr)
        return ret



    def Write(self ,text:str):
        """
        Writes text.
        """
        textPtr = StrToPtr(text)
        GetDllLibDoc().DocumentNavigator_Write.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_Write,self.Ptr, textPtr)

    @dispatch

    def Writeln(self ,text:str):
        """
        Writes a line of text.
        """
        textPtr = StrToPtr(text)
        GetDllLibDoc().DocumentNavigator_Writeln.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_Writeln,self.Ptr, textPtr)

    @dispatch
    def Writeln(self):
        """
        Writes a blank line.
        """
        GetDllLibDoc().DocumentNavigator_Writeln1.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_Writeln1,self.Ptr)


    def InsertParagraph(self)->'Paragraph':
        """
        Inserts a new paragraph.
        """
        GetDllLibDoc().DocumentNavigator_InsertParagraph.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_InsertParagraph.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertParagraph,self.Ptr)
        ret = None if intPtr==None else Paragraph(intPtr)
        return ret



    def InsertBreak(self ,breakType: BreakType):
        """
        Inserts a Break.
        """
        intPtrbreakType:c_int = breakType.value

        GetDllLibDoc().DocumentNavigator_InsertBreak.argtypes=[c_void_p ,c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_InsertBreak,self.Ptr, intPtrbreakType)

    @dispatch

    def InsertField(self ,fieldType:FieldType,updateField:bool)->Field:
        """
        Inserts a Field.
        
        Args:
            fieldType:Field type.
            updateField:Whether to update the field immediately.
        """
        enumfieldType:c_int = fieldType.value

        GetDllLibDoc().DocumentNavigator_InsertField.argtypes=[c_void_p ,c_int,c_bool]
        GetDllLibDoc().DocumentNavigator_InsertField.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertField,self.Ptr, enumfieldType,updateField)
        ret = None if intPtr==None else Field(intPtr)
        return ret


    @dispatch

    def InsertField(self ,fieldCode:str)->Field:
        """
        Inserts a Field.

        Args:
            fieldCode: Field code, e.g:"PAGE", "TOC \o '1-3'".
        """
        fieldCodePtr = StrToPtr(fieldCode)
        GetDllLibDoc().DocumentNavigator_InsertFieldF.argtypes=[c_void_p ,c_char_p]
        GetDllLibDoc().DocumentNavigator_InsertFieldF.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertFieldF,self.Ptr, fieldCodePtr)
        ret = None if intPtr==None else Field(intPtr)
        return ret


    @dispatch

    def InsertField(self ,fieldCode:str,fieldValue:str)->Field:
        """
        Inserts a Field.

        Args:
            fieldCode: Field code, e.g:"PAGE", "TOC \o '1-3'".
            fieldValue:Temporary text displayed if the field is not updated.
        """
        fieldCodePtr = StrToPtr(fieldCode)
        fieldValuePtr = StrToPtr(fieldValue)
        GetDllLibDoc().DocumentNavigator_InsertFieldFF.argtypes=[c_void_p ,c_char_p,c_char_p]
        GetDllLibDoc().DocumentNavigator_InsertFieldFF.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertFieldFF,self.Ptr, fieldCodePtr,fieldValuePtr)
        ret = None if intPtr==None else Field(intPtr)
        return ret



    def InsertTextFormField(self ,name:str,type:'TextFormFieldType',format:str,fieldValue:str,maxLength:int)->'FormField':
        """
        Inserts a text input form field component.

        Args:
            name: Name of the text form field.
            TextFormFieldType: Type of the text form field.
            format: Text format.
            fieldValue: Default text.
            maxLength: Maximum allowed input length.
        """
        namePtr = StrToPtr(name)
        enumtype:c_int = type.value
        formatPtr = StrToPtr(format)
        fieldValuePtr = StrToPtr(fieldValue)
        GetDllLibDoc().DocumentNavigator_InsertTextFormField.argtypes=[c_void_p ,c_char_p,c_int,c_char_p,c_char_p,c_int]
        GetDllLibDoc().DocumentNavigator_InsertTextFormField.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertTextFormField, self.Ptr, namePtr, enumtype, formatPtr, fieldValuePtr, maxLength)
        ret = None if intPtr==None else FormField(intPtr)
        return ret


    @dispatch

    def InsertCheckBox(self ,name:str,checkedValue:bool,size:int)->CheckBoxFormField:
        """
        Inserts a CheckBox

        Args:
            name: Checkbox name.
            checkedValue: Whether checked by default.
            size: Size of the checkbox.
        """
        namePtr = StrToPtr(name)
        GetDllLibDoc().DocumentNavigator_InsertCheckBox.argtypes=[c_void_p ,c_char_p,c_bool,c_int]
        GetDllLibDoc().DocumentNavigator_InsertCheckBox.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertCheckBox,self.Ptr, namePtr,checkedValue,size)
        ret = None if intPtr==None else CheckBoxFormField(intPtr)
        return ret


    @dispatch

    def InsertCheckBox(self ,name:str,defaultValue:bool,checkedValue:bool,size:int)->CheckBoxFormField:
        """
        Inserts a CheckBox

        Args:
            name: Checkbox name.
            defaultValue: Whether checked by default.
            checkedValue: Current check state.
            size: Size of the checkbox.
        """
        namePtr = StrToPtr(name)
        GetDllLibDoc().DocumentNavigator_InsertCheckBoxNDCS.argtypes=[c_void_p ,c_char_p,c_bool,c_bool,c_int]
        GetDllLibDoc().DocumentNavigator_InsertCheckBoxNDCS.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertCheckBoxNDCS,self.Ptr, namePtr,defaultValue,checkedValue,size)
        ret = None if intPtr==None else CheckBoxFormField(intPtr)
        return ret


    @dispatch

    def InsertImage(self ,fileName:str)->ShapeObject:
        """
        Inserts an Image

        Args:
            name: Path to the image file.
        """
        fileNamePtr = StrToPtr(fileName)
        GetDllLibDoc().DocumentNavigator_InsertImage.argtypes=[c_void_p ,c_char_p]
        GetDllLibDoc().DocumentNavigator_InsertImage.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImage,self.Ptr, fileNamePtr)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


    @dispatch

    def InsertImage(self ,stream:Stream)->ShapeObject:
        """
        Inserts an Image

        Args:
            stream: Stream containing image data.
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibDoc().DocumentNavigator_InsertImageS.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().DocumentNavigator_InsertImageS.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageS,self.Ptr, intPtrstream)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


#    @dispatch
#
#    def InsertImage(self ,imageBytes:'Byte[]')->ShapeObject:
#        """
#
#        """
#        #arrayimageBytes:ArrayTypeimageBytes = ""
#        countimageBytes = len(imageBytes)
#        ArrayTypeimageBytes = c_void_p * countimageBytes
#        arrayimageBytes = ArrayTypeimageBytes()
#        for i in range(0, countimageBytes):
#            arrayimageBytes[i] = imageBytes[i].Ptr
#
#
#        GetDllLibDoc().DocumentNavigator_InsertImageI.argtypes=[c_void_p ,ArrayTypeimageBytes]
#        GetDllLibDoc().DocumentNavigator_InsertImageI.restype=c_void_p
#        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageI,self.Ptr, arrayimageBytes)
#        ret = None if intPtr==None else ShapeObject(intPtr)
#        return ret
#


    @dispatch

    def InsertImage(self ,fileName:str,width:float,height:float)->ShapeObject:
        """
        Inserts an Image

        Args:
            fileName: Path to the image file.
            width: Image width.
            height: Image height.
        """
        fileNamePtr = StrToPtr(fileName)
        GetDllLibDoc().DocumentNavigator_InsertImageFWH.argtypes=[c_void_p ,c_char_p,c_double,c_double]
        GetDllLibDoc().DocumentNavigator_InsertImageFWH.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageFWH,self.Ptr, fileNamePtr,width,height)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


    @dispatch

    def InsertImage(self ,stream:Stream,width:float,height:float)->ShapeObject:
        """
        Inserts an Image

        Args:
            stream: Stream containing image data.
            width: Image width.
            height: Image height.
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibDoc().DocumentNavigator_InsertImageSWH.argtypes=[c_void_p ,c_void_p,c_double,c_double]
        GetDllLibDoc().DocumentNavigator_InsertImageSWH.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageSWH,self.Ptr, intPtrstream,width,height)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


#    @dispatch
#
#    def InsertImage(self ,imageBytes:'Byte[]',width:float,height:float)->ShapeObject:
#        """
#
#        """
#        #arrayimageBytes:ArrayTypeimageBytes = ""
#        countimageBytes = len(imageBytes)
#        ArrayTypeimageBytes = c_void_p * countimageBytes
#        arrayimageBytes = ArrayTypeimageBytes()
#        for i in range(0, countimageBytes):
#            arrayimageBytes[i] = imageBytes[i].Ptr
#
#
#        GetDllLibDoc().DocumentNavigator_InsertImageIWH.argtypes=[c_void_p ,ArrayTypeimageBytes,c_double,c_double]
#        GetDllLibDoc().DocumentNavigator_InsertImageIWH.restype=c_void_p
#        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageIWH,self.Ptr, arrayimageBytes,width,height)
#        ret = None if intPtr==None else ShapeObject(intPtr)
#        return ret
#


    @dispatch

    def InsertImage(self ,fileName:str,horzPos:HorizontalOrigin,left:float,vertPos:VerticalOrigin,top:float,width:float,height:float,wrapType:TextWrappingStyle)->ShapeObject:
        """
        Inserts an Image

        Args:
            fileName: Path to the image file.
            horzPos: Horizontal positioning origin.
            left: Horizontal offset from origin.
            vertPos: Vertical positioning origin.
            top: Vertical offset from origin.
            width: Image width.
            height: Image height.
            wrapType: Text wrapping style.
        """
        enumhorzPos:c_int = horzPos.value
        enumvertPos:c_int = vertPos.value
        enumwrapType:c_int = wrapType.value
        fileNamePtr = StrToPtr(fileName)
        GetDllLibDoc().DocumentNavigator_InsertImageFHLVTWHW.argtypes=[c_void_p ,c_char_p,c_int,c_double,c_int,c_double,c_double,c_double,c_int]
        GetDllLibDoc().DocumentNavigator_InsertImageFHLVTWHW.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageFHLVTWHW,self.Ptr, fileNamePtr,enumhorzPos,left,enumvertPos,top,width,height,enumwrapType)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


    @dispatch

    def InsertImage(self ,stream:Stream,horzPos:HorizontalOrigin,left:float,vertPos:VerticalOrigin,top:float,width:float,height:float,wrapType:TextWrappingStyle)->ShapeObject:
        """
        Inserts an Image

        Args:
            stream: Stream containing image data.
            horzPos: Horizontal positioning origin.
            left: Horizontal offset from origin.
            vertPos: Vertical positioning origin.
            top: Vertical offset from origin.
            width: Image width.
            height: Image height.
            wrapType: Text wrapping style.
        """
        intPtrstream:c_void_p = stream.Ptr
        enumhorzPos:c_int = horzPos.value
        enumvertPos:c_int = vertPos.value
        enumwrapType:c_int = wrapType.value

        GetDllLibDoc().DocumentNavigator_InsertImageSHLVTWHW.argtypes=[c_void_p ,c_void_p,c_int,c_double,c_int,c_double,c_double,c_double,c_int]
        GetDllLibDoc().DocumentNavigator_InsertImageSHLVTWHW.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageSHLVTWHW,self.Ptr, intPtrstream,enumhorzPos,left,enumvertPos,top,width,height,enumwrapType)
        ret = None if intPtr==None else ShapeObject(intPtr)
        return ret


#    @dispatch
#
#    def InsertImage(self ,imageBytes:'Byte[]',horzPos:HorizontalOrigin,left:float,vertPos:VerticalOrigin,top:float,width:float,height:float,wrapType:TextWrappingStyle)->ShapeObject:
#        """
#
#        """
#        #arrayimageBytes:ArrayTypeimageBytes = ""
#        countimageBytes = len(imageBytes)
#        ArrayTypeimageBytes = c_void_p * countimageBytes
#        arrayimageBytes = ArrayTypeimageBytes()
#        for i in range(0, countimageBytes):
#            arrayimageBytes[i] = imageBytes[i].Ptr
#
#        enumhorzPos:c_int = horzPos.value
#        enumvertPos:c_int = vertPos.value
#        enumwrapType:c_int = wrapType.value
#
#        GetDllLibDoc().DocumentNavigator_InsertImageIHLVTWHW.argtypes=[c_void_p ,ArrayTypeimageBytes,c_int,c_double,c_int,c_double,c_double,c_double,c_int]
#        GetDllLibDoc().DocumentNavigator_InsertImageIHLVTWHW.restype=c_void_p
#        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertImageIHLVTWHW,self.Ptr, arrayimageBytes,enumhorzPos,left,enumvertPos,top,width,height,enumwrapType)
#        ret = None if intPtr==None else ShapeObject(intPtr)
#        return ret
#


    @dispatch

    def InsertHtml(self ,html:str):
        """
        Inserts HTML

        Args:
            html: HTML string.
        """
        htmlPtr = StrToPtr(html)
        GetDllLibDoc().DocumentNavigator_InsertHtml.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_InsertHtml,self.Ptr, htmlPtr)

    @dispatch

    def InsertHtml(self ,html:str,useNavigatorFormatting:bool):
        """
        Inserts HTML

        Args:
            html: HTML string.
            useNavigatorFormatting: Whether to use the current builder's formatting.
        """
        htmlPtr = StrToPtr(html)
        GetDllLibDoc().DocumentNavigator_InsertHtmlHU.argtypes=[c_void_p ,c_char_p,c_bool]
        CallCFunction(GetDllLibDoc().DocumentNavigator_InsertHtmlHU,self.Ptr, htmlPtr,useNavigatorFormatting)


    def InsertCell(self)->'TableCell':
        """
        Inserts a table cell.
        """
        GetDllLibDoc().DocumentNavigator_InsertCell.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_InsertCell.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_InsertCell,self.Ptr)
        ret = None if intPtr==None else TableCell(intPtr)
        return ret



    def StartTable(self)->'Table':
        """
        Creates and inserts a new table.
        """
        GetDllLibDoc().DocumentNavigator_StartTable.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_StartTable.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_StartTable,self.Ptr)
        ret = None if intPtr==None else Table(intPtr)
        return ret



    def EndTable(self)->'Table':
        """
        After calling StartTable() to begin a table, EndTable() must be called to finalize the table structure.
        """
        GetDllLibDoc().DocumentNavigator_EndTable.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_EndTable.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_EndTable,self.Ptr)
        ret = None if intPtr==None else Table(intPtr)
        return ret



    def EndRow(self)->'TableRow':
        """
        Ends building the current table row. The cursor moves to the end of the row, ready to start a new row.
        """
        GetDllLibDoc().DocumentNavigator_EndRow.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_EndRow.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_EndRow,self.Ptr)
        ret = None if intPtr==None else TableRow(intPtr)
        return ret


    @property

    def Document(self)->'Document':
        """
        Gets or sets the Document object this navigator is attached to. A DocumentNavigator is always associated with a Document instance.
        """
        GetDllLibDoc().DocumentNavigator_get_Document.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_Document.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_Document,self.Ptr)
        ret = None if intPtr==None else Document(intPtr)
        return ret


    @Document.setter
    def Document(self, value:'Document'):
        GetDllLibDoc().DocumentNavigator_set_Document.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_set_Document,self.Ptr, value.Ptr)

    @property

    def Underline(self)->'UnderlineStyle':
        """
        Gets or sets the type of underline. Can be set to different underline styles, such as None, Single, Double, etc.
        """
        GetDllLibDoc().DocumentNavigator_get_Underline.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_Underline.restype=c_int
        ret = CallCFunction(GetDllLibDoc().DocumentNavigator_get_Underline,self.Ptr)
        objwraped = UnderlineStyle(ret)
        return objwraped

    @Underline.setter
    def Underline(self, value:'UnderlineStyle'):
        GetDllLibDoc().DocumentNavigator_set_Underline.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().DocumentNavigator_set_Underline,self.Ptr, value.value)

    @property

    def CharacterFormat(self)->'CharacterFormat':
        """
        Gets the CharacterFormat object representing the current font formatting. Used to set font name, size, color, etc.
        """
        GetDllLibDoc().DocumentNavigator_get_CharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CharacterFormat,self.Ptr)
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret


    @property

    def RowFormat(self)->'RowFormat':
        """
        Gets the formatting (RowFormat object) of the current table row.
        """
        GetDllLibDoc().DocumentNavigator_get_RowFormat.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_RowFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_RowFormat,self.Ptr)
        ret = None if intPtr==None else RowFormat(intPtr)
        return ret


    @property

    def CellFormat(self)->'CellFormat':
        """
        Gets the formatting (CellFormat object) of the current table cell.
        """
        GetDllLibDoc().DocumentNavigator_get_CellFormat.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_CellFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_CellFormat,self.Ptr)
        ret = None if intPtr==None else CellFormat(intPtr)
        return ret


    @property

    def ParagraphFormat(self)->'ParagraphFormat':
        """
        Gets the current paragraph formatting (ParagraphFormat object). Can set alignment, indentation, line spacing, and other paragraph properties.
        """
        GetDllLibDoc().DocumentNavigator_get_ParagraphFormat.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_ParagraphFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_ParagraphFormat,self.Ptr)
        ret = None if intPtr==None else ParagraphFormat(intPtr)
        return ret


    @property

    def ListFormat(self)->'ListFormat':
        """
        Gets the current list formatting (ListFormat object), used to handle bullets and numbering.
        """
        GetDllLibDoc().DocumentNavigator_get_ListFormat.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_ListFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_ListFormat,self.Ptr)
        ret = None if intPtr==None else ListFormat(intPtr)
        return ret


    @property

    def PageSetup(self)->'PageSetup':
        """
        Gets the page setup (PageSetup object) for the current section. Can set margins, paper orientation, size, etc.
        """
        GetDllLibDoc().DocumentNavigator_get_PageSetup.argtypes=[c_void_p]
        GetDllLibDoc().DocumentNavigator_get_PageSetup.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().DocumentNavigator_get_PageSetup,self.Ptr)
        ret = None if intPtr==None else PageSetup(intPtr)
        return ret


    def PushCharacterFormat(self):
        """
        Saves the current character formatting settings (font name, size, color, etc.) of the DocumentNavigator. Allows changing settings later without losing the current settings.
        """
        GetDllLibDoc().DocumentNavigator_PushCharacterFormat.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_PushCharacterFormat,self.Ptr)

    def PopCharacterFormat(self):
        """
        Applies previously saved character formatting settings to the current DocumentNavigator.
        """
        GetDllLibDoc().DocumentNavigator_PopCharacterFormat.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DocumentNavigator_PopCharacterFormat,self.Ptr)


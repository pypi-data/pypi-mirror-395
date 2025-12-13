from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkdownExportOptions (  SaveOptions) :
    """
    Class for customizing document conversion options to Markdown.
    """
    @property

    def TableTextAlignment(self)->'TableTextAlignment':
        """
        Controls how table text is aligned when saving to Markdown format.
        """
        GetDllLibDoc().MarkdownExportOptions_get_TableTextAlignment.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_TableTextAlignment.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_TableTextAlignment,self.Ptr)
        objwraped = TableTextAlignment(ret)
        return objwraped

    @TableTextAlignment.setter
    def TableTextAlignment(self, value:'TableTextAlignment'):
        GetDllLibDoc().MarkdownExportOptions_set_TableTextAlignment.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_TableTextAlignment,self.Ptr, value.value)

    @property

    def ImagesFolder(self)->str:
        """
        Defines the output directory for iamges during Markdown document conversion.
        """
        GetDllLibDoc().MarkdownExportOptions_get_ImagesFolder.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_ImagesFolder.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_ImagesFolder,self.Ptr))
        return ret


    @ImagesFolder.setter
    def ImagesFolder(self, value:str):
        valuePtr = StrToPtr(value)
        GetDllLibDoc().MarkdownExportOptions_set_ImagesFolder.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_ImagesFolder,self.Ptr, valuePtr)

    @property

    def ImagesFolderAlias(self)->str:
        """
        Defines the directory name for building images URIs in exported documents.
        """
        GetDllLibDoc().MarkdownExportOptions_get_ImagesFolderAlias.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_ImagesFolderAlias.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_ImagesFolderAlias,self.Ptr))
        return ret


    @ImagesFolderAlias.setter
    def ImagesFolderAlias(self, value:str):
        valuePtr = StrToPtr(value)
        GetDllLibDoc().MarkdownExportOptions_set_ImagesFolderAlias.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_ImagesFolderAlias,self.Ptr, valuePtr)

    @property
    def ImagesAsBase64(self)->bool:
        """
        Determines if images are embedded as Base64 in the output file.
        """
        GetDllLibDoc().MarkdownExportOptions_get_ImagesAsBase64.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_ImagesAsBase64.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_ImagesAsBase64,self.Ptr)
        return ret

    @ImagesAsBase64.setter
    def ImagesAsBase64(self, value:bool):
        GetDllLibDoc().MarkdownExportOptions_set_ImagesAsBase64.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_ImagesAsBase64,self.Ptr, value)

    @property

    def ListOutputMode(self)->'MarkdownListOutputMode':
        """
        Defines the method for writing list items to the output file.
        """
        GetDllLibDoc().MarkdownExportOptions_get_ListOutputMode.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_ListOutputMode.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_ListOutputMode,self.Ptr)
        objwraped = MarkdownListOutputMode(ret)
        return objwraped

    @ListOutputMode.setter
    def ListOutputMode(self, value:'MarkdownListOutputMode'):
        GetDllLibDoc().MarkdownExportOptions_set_ListOutputMode.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_ListOutputMode,self.Ptr, value.value)

    @property
    def SaveUnderlineFormatting(self)->bool:
        """
        Controls whether underlined text is converted to "++" syntax in Markdown format.
        """
        GetDllLibDoc().MarkdownExportOptions_get_SaveUnderlineFormatting.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_SaveUnderlineFormatting.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_SaveUnderlineFormatting,self.Ptr)
        return ret

    @SaveUnderlineFormatting.setter
    def SaveUnderlineFormatting(self, value:bool):
        GetDllLibDoc().MarkdownExportOptions_set_SaveUnderlineFormatting.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_SaveUnderlineFormatting,self.Ptr, value)

    @property

    def LinkOutputMode(self)->'MarkdownLinkOutputMode':
        """
        Defines the formatting method for hyperlinks in output documents.
        """
        GetDllLibDoc().MarkdownExportOptions_get_LinkOutputMode.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_LinkOutputMode.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_LinkOutputMode,self.Ptr)
        objwraped = MarkdownLinkOutputMode(ret)
        return objwraped

    @LinkOutputMode.setter
    def LinkOutputMode(self, value:'MarkdownLinkOutputMode'):
        GetDllLibDoc().MarkdownExportOptions_set_LinkOutputMode.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_LinkOutputMode,self.Ptr, value.value)

    @property

    def OfficeMathOutputMode(self)->'MarkdownOfficeMathOutputMode':
        """
        Defines the rendering method for OfficeMath equations in output documents.
        """
        GetDllLibDoc().MarkdownExportOptions_get_OfficeMathOutputMode.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_OfficeMathOutputMode.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_OfficeMathOutputMode,self.Ptr)
        objwraped = MarkdownOfficeMathOutputMode(ret)
        return objwraped

    @OfficeMathOutputMode.setter
    def OfficeMathOutputMode(self, value:'MarkdownOfficeMathOutputMode'):
        GetDllLibDoc().MarkdownExportOptions_set_OfficeMathOutputMode.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_OfficeMathOutputMode,self.Ptr, value.value)

    @property

    def SaveAsHtml(self)->'MarkdownSaveAsHtml':
        """
        Enables selection of elements to output as raw HTML in Markdown conversion.
        """
        GetDllLibDoc().MarkdownExportOptions_get_SaveAsHtml.argtypes=[c_void_p]
        GetDllLibDoc().MarkdownExportOptions_get_SaveAsHtml.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MarkdownExportOptions_get_SaveAsHtml,self.Ptr)
        objwraped = MarkdownSaveAsHtml(ret)
        return objwraped

    @SaveAsHtml.setter
    def SaveAsHtml(self, value:'MarkdownSaveAsHtml'):
        GetDllLibDoc().MarkdownExportOptions_set_SaveAsHtml.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().MarkdownExportOptions_set_SaveAsHtml,self.Ptr, value.value)


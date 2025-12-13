from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SaveOptions (SpireObject) :
    """
    This is an abstract base class for classes that allow the user to specify additional
    options when saving a document into a particular format.
    """
    @property
    def UseHighQualityRendering(self)->bool:
        """
        Gets or sets a value determining whether or not to use high quality (i.e. slow) rendering algorithms.
        """
        GetDllLibDoc().SaveOptions_get_UseHighQualityRendering.argtypes=[c_void_p]
        GetDllLibDoc().SaveOptions_get_UseHighQualityRendering.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().SaveOptions_get_UseHighQualityRendering,self.Ptr)
        return ret

    @UseHighQualityRendering.setter
    def UseHighQualityRendering(self, value:bool):
        GetDllLibDoc().SaveOptions_set_UseHighQualityRendering.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().SaveOptions_set_UseHighQualityRendering,self.Ptr, value)

    @property
    def NeedInitializeTheme(self)->bool:
        """

        """
        GetDllLibDoc().SaveOptions_get_NeedInitializeTheme.argtypes=[c_void_p]
        GetDllLibDoc().SaveOptions_get_NeedInitializeTheme.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().SaveOptions_get_NeedInitializeTheme,self.Ptr)
        return ret

    @NeedInitializeTheme.setter
    def NeedInitializeTheme(self, value:bool):
        GetDllLibDoc().SaveOptions_set_NeedInitializeTheme.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().SaveOptions_set_NeedInitializeTheme,self.Ptr, value)

    @property
    def AllowEmbeddingPostScriptFonts(self)->bool:
        """
        Gets or sets a boolean value indicating whether to embed PostScript outlined fonts along
        with TrueType fonts in a document upon saving.
        
        The default value is false.
        """
        GetDllLibDoc().SaveOptions_get_AllowEmbeddingPostScriptFonts.argtypes=[c_void_p]
        GetDllLibDoc().SaveOptions_get_AllowEmbeddingPostScriptFonts.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().SaveOptions_get_AllowEmbeddingPostScriptFonts,self.Ptr)
        return ret

    @AllowEmbeddingPostScriptFonts.setter
    def AllowEmbeddingPostScriptFonts(self, value:bool):
        GetDllLibDoc().SaveOptions_set_AllowEmbeddingPostScriptFonts.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().SaveOptions_set_AllowEmbeddingPostScriptFonts,self.Ptr, value)


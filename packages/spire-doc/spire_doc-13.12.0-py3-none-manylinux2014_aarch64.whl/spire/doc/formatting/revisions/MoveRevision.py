from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
from spire.doc.formatting.revisions.RevisionBase import RevisionBase
import abc

class MoveRevision (  RevisionBase) :
    """
    Represents info about an moveFrom or moveTo revision, occurs on runs of text.
    Two different move revision operations are possible on a run: moveFrom, and moveTo.
    """
    @property

    def Type(self)->'MoveRevisionType':
        """
        Indicates whether the run is 'moved from' or 'moved to' during the revision.
        """
        GetDllLibDoc().MoveRevision_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().MoveRevision_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().MoveRevision_get_Type,self.Ptr)
        objwraped = MoveRevisionType(ret)
        return objwraped

    @property
    def IsInheritedComplexAttr(self)->bool:
        """
        Reserved for system use. IComplexAttr.
        """
        GetDllLibDoc().MoveRevision_get_IsInheritedComplexAttr.argtypes=[c_void_p]
        GetDllLibDoc().MoveRevision_get_IsInheritedComplexAttr.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().MoveRevision_get_IsInheritedComplexAttr,self.Ptr)
        return ret


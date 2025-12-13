"""
image

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/image_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Embedded', 'File', 'Inline', 'Linked']
class Embedded(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Embedded**
    
    .. include:: /nodes/image/embedded.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> bytes:
        ...
    def setRaw(self, arg0: bytes) -> bool:
        ...
class File(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **File**
    
    .. include:: /nodes/image/file.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getPath(self) -> str:
        """
        Get the path parameter
        """
    def setPath(self, path: str) -> bool:
        """
        Set the path parameter
        """
class Inline(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Inline**
    
    .. include:: /nodes/image/inline.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getFormat(self) -> str:
        """
        Get the format parameter
        """
    def getFormatChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getHeight(self) -> int:
        """
        Get the height parameter
        """
    def getRaw(self) -> numpy.typing.NDArray[numpy.float32]:
        ...
    def getRawWavelengths(self) -> numpy.typing.NDArray[numpy.float32]:
        ...
    def getWidth(self) -> int:
        """
        Get the width parameter
        """
    def setFormat(self, format: str) -> bool:
        """
        Set the format parameter
        """
    def setHeight(self, height: typing.SupportsInt) -> bool:
        """
        Set the height parameter
        """
    def setRaw(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        ...
    def setRawWavelengths(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        ...
    def setWidth(self, width: typing.SupportsInt) -> bool:
        """
        Set the width parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/image/linked.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """

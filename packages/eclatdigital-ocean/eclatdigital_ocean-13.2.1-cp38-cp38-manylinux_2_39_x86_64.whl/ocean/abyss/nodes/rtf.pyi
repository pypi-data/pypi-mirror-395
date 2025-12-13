"""
rtf

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/rtf_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
__all__: list[str] = ['Linked', 'Rtf', 'Spectralrtfs']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Linked
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
class Rtf(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Rtf**
    
    .. include:: /nodes/rtf/rtf.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getRawIsBeams(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawIsOutputDirZUniformByPart(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawIsPlanar(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawOutputRadius(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def getRawPassPlaneDistance(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def getRawTermdx(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawTermdy(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawTermr(self) -> numpy.typing.NDArray[numpy.int32]:
        ...
    def getRawWavelength(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def getRawYMaxInput(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def getRawZInput(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def setRawIsBeams(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawIsOutputDirZUniformByPart(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawIsPlanar(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawOutputRadius(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
    def setRawPassPlaneDistance(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
    def setRawTermdx(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawTermdy(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawTermr(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.int32]) -> bool:
        ...
    def setRawWavelength(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
    def setRawYMaxInput(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
    def setRawZInput(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
class Spectralrtfs(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spectralrtfs**
    
    .. include:: /nodes/rtf/spectralrtf.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...

"""
avspectrum

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/avspectrum_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Linked', 'Table']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Linked
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setRaw(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """
class Table(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Table**
    
    .. include:: /nodes/avspectrum.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getInterp(self) -> str:
        """
        Get the interp parameter
        """
    def getInterpChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getNumwl(self) -> int:
        """
        Get the numwl parameter
        """
    def getRaw(self) -> numpy.typing.NDArray[numpy.float64]:
        ...
    def setInterp(self, interp: str) -> bool:
        """
        Set the interp parameter
        """
    def setNumwl(self, numwl: typing.SupportsInt) -> bool:
        """
        Set the numwl parameter
        """
    def setRaw(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> bool:
        ...

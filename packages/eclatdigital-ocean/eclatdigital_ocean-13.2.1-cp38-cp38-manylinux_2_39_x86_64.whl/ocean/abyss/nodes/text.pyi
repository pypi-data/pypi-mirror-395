"""
text

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/text_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
__all__: list[str] = ['Default', 'Linked']
class Default(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Default
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> str:
        ...
    def setRaw(self, arg0: str) -> bool:
        ...
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/text/linked.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> str:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setRaw(self, arg0: str) -> bool:
        ...
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """

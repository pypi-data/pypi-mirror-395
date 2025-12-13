"""
layer

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/layer_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
__all__: list[str] = ['Generic', 'Linked']
class Generic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Generic**
    
    .. include:: /nodes/layer/generic.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getVisible(self) -> bool:
        """
        Get the visible parameter
        """
    def setVisible(self, visible: bool) -> bool:
        """
        Set the visible parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/layer/linked.rst
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

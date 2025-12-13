"""
dielectricfunc

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/dielectricfunc_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
__all__: list[str] = ['Linked', 'Na', 'Nk']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/dielectricfunc/linked.rst
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
class Na(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Na**
    
    .. include:: /nodes/dielectricfunc/absorbance.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the a node 
        """
    def getN(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the n node 
        """
    def setA(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the a node 
        """
    def setN(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the n node 
        """
class Nk(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Nk**
    
    .. include:: /nodes/dielectricfunc/complex.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getK(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the k node 
        """
    def getN(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the n node 
        """
    def setK(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the k node 
        """
    def setN(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the n node 
        """

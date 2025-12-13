"""
medium

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/medium_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Linked', 'Mie', 'Simple']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/medium/linked.rst
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
class Mie(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Mie**
    
    .. include:: /nodes/medium/mie.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getHost(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the Host node 
        """
    def getPrecedence(self) -> int:
        """
        Get the precedence parameter
        """
    def setHost(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the Host node 
        """
    def setPrecedence(self, precedence: typing.SupportsInt) -> bool:
        """
        Set the precedence parameter
        """
class Simple(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Simple**
    
    .. include:: /nodes/medium/simple.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getPrecedence(self) -> int:
        """
        Get the precedence parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setPrecedence(self, precedence: typing.SupportsInt) -> bool:
        """
        Set the precedence parameter
        """

"""
colloid

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/colloid_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Default', 'Linked']
class Default(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Default**
    
    .. include:: /nodes/colloid.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> float:
        """
        Get the density parameter
        """
    def getParticle(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the Particle node 
        """
    def getSizedistribution(self) -> dict:
        """
        Get the sizedistribution parameter
        """
    def setDensity(self, density: typing.SupportsFloat) -> bool:
        """
        Set the density parameter
        """
    def setParticle(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the Particle node 
        """
    def setSizedistribution(self, sizedistribution: dict) -> bool:
        """
        Set the sizedistribution parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"size": np.array(...), "value": np.array(...)}
        """
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

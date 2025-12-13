"""
sensor

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/sensor_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Ciexyz', 'Custom', 'Energy', 'Linked', 'Spectralbox']
class Ciexyz(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Ciexyz**
    
    .. include:: /nodes/sensor/ciexyz.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getY_only(self) -> bool:
        """
        Get the y_only parameter
        """
    def setY_only(self, y_only: bool) -> bool:
        """
        Set the y_only parameter
        """
class Custom(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Custom**
    
    .. include:: /nodes/sensor/custom.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Energy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Energy**
    
    .. include:: /nodes/sensor/energy.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
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
class Spectralbox(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spectralbox**
    
    .. include:: /nodes/sensor/spectralbox.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getFirstwl(self) -> float:
        """
        Get the firstwl parameter
        """
    def getLastwl(self) -> float:
        """
        Get the lastwl parameter
        """
    def getNumpoints(self) -> int:
        """
        Get the numpoints parameter
        """
    def setFirstwl(self, firstwl: typing.SupportsFloat) -> bool:
        """
        Set the firstwl parameter
        """
    def setLastwl(self, lastwl: typing.SupportsFloat) -> bool:
        """
        Set the lastwl parameter
        """
    def setNumpoints(self, numpoints: typing.SupportsInt) -> bool:
        """
        Set the numpoints parameter
        """

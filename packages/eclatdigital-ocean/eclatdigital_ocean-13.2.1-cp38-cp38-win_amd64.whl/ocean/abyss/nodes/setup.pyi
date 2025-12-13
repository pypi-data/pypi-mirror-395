"""
setup

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/setup_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Default', 'Linked']
class Default(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Default**
    
    .. include:: /nodes/setup.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBackpathdepth(self) -> int:
        """
        Get the backpathdepth parameter
        """
    def getEnvironment(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the environment node 
        """
    def getHaltspp(self) -> int:
        """
        Get the haltspp parameter
        """
    def getHalttime(self) -> int:
        """
        Get the halttime parameter
        """
    def getInstrument(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the instrument node 
        """
    def getIntersector(self) -> str:
        """
        Get the intersector parameter
        """
    def getIntersectorChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getLayers(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the layers node 
        """
    def getLightpathdepth(self) -> int:
        """
        Get the lightpathdepth parameter
        """
    def getMetropolis(self) -> bool:
        """
        Get the metropolis parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setBackpathdepth(self, backpathdepth: typing.SupportsInt) -> bool:
        """
        Set the backpathdepth parameter
        """
    def setEnvironment(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the environment node 
        """
    def setHaltspp(self, haltspp: typing.SupportsInt) -> bool:
        """
        Set the haltspp parameter
        """
    def setHalttime(self, halttime: typing.SupportsInt) -> bool:
        """
        Set the halttime parameter
        """
    def setInstrument(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the instrument node 
        """
    def setIntersector(self, intersector: str) -> bool:
        """
        Set the intersector parameter
        """
    def setLayers(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the layers node 
        """
    def setLightpathdepth(self, lightpathdepth: typing.SupportsInt) -> bool:
        """
        Set the lightpathdepth parameter
        """
    def setMetropolis(self, metropolis: bool) -> bool:
        """
        Set the metropolis parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
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

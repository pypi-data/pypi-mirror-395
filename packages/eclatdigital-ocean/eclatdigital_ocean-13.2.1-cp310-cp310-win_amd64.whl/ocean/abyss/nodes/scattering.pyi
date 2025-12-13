"""
scattering

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/scattering_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Additive', 'Gegenbauerspectral', 'Henyeygreenstein', 'Henyeygreensteinspectral', 'Isotropic', 'Linked', 'Rayleigh', 'Tabulated']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Additive**
    
    .. include:: /nodes/scattering/additive.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Gegenbauerspectral(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Gegenbauerspectral**
    
    .. include:: /nodes/scattering/gegenbauerspectral.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlpha(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the alpha node 
        """
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getGGen(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the gGen node 
        """
    def setAlpha(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the alpha node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
        """
    def setGGen(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the gGen node 
        """
class Henyeygreenstein(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Henyeygreenstein**
    
    .. include:: /nodes/scattering/henyeygreenstein.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getG(self) -> float:
        """
        Get the g parameter
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
        """
    def setG(self, g: typing.SupportsFloat) -> bool:
        """
        Set the g parameter
        """
class Henyeygreensteinspectral(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Henyeygreensteinspectral**
    
    .. include:: /nodes/scattering/henyeygreensteinspectral.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getG(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the g node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
        """
    def setG(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the g node 
        """
class Isotropic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Isotropic**
    
    .. include:: /nodes/scattering/isotropic.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
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
class Rayleigh(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Rayleigh**
    
    .. include:: /nodes/scattering/rayleigh.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
        """
class Tabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Tabulated**
    
    .. include:: /nodes/scattering/tabulated.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getPhasefunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the phasefunc node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the density node 
        """
    def setPhasefunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the phasefunc node 
        """

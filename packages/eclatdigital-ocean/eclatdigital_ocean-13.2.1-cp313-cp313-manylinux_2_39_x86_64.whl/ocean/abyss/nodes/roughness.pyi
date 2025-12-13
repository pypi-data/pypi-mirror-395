"""
roughness

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/roughness_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
__all__: list[str] = ['Ashikhminshirley', 'Beckmann', 'Cosine', 'Flat', 'Isotable', 'Linked', 'Map', 'Mix', 'Phong', 'Trowbridge', 'Ward']
class Ashikhminshirley(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Ashikhminshirley**
    
    .. include:: /nodes/roughness/ashikhminshirley.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def getNv(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nv node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the nu node 
        """
    def setNv(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the nv node 
        """
class Beckmann(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Beckmann**
    
    .. include:: /nodes/roughness/beckmann.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the roughness node 
        """
class Cosine(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cosine**
    
    .. include:: /nodes/roughness/cosine.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Flat(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Flat**
    
    .. include:: /nodes/roughness/flat.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Isotable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Isotable**
    
    .. include:: /nodes/roughness/isotable.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDistribution(self) -> dict:
        """
        Get the distribution parameter
        """
    def setDistribution(self, distribution: dict) -> bool:
        """
        Set the distribution parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"angle": np.array(...), "pdf": np.array(...)}
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
class Map(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Map**
    
    .. include:: /nodes/roughness/map.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getMap(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the map node 
        """
    def getZscale(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the zscale node 
        """
    def setMap(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the map node 
        """
    def setZscale(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the zscale node 
        """
class Mix(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Mix**
    
    .. include:: /nodes/roughness/mix.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getWeights(self) -> dict:
        """
        Get the weights parameter
        """
    def setWeights(self, weights: dict) -> bool:
        """
        Set the weights parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"name": np.array(...), "weight": np.array(...)}
        """
class Phong(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Phong**
    
    .. include:: /nodes/roughness/phong.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getExponent(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the exponent node 
        """
    def setExponent(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the exponent node 
        """
class Trowbridge(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Trowbridge**
    
    .. include:: /nodes/roughness/trowbridge.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the nu node 
        """
class Ward(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Ward**
    
    .. include:: /nodes/roughness/ward.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the nu node 
        """

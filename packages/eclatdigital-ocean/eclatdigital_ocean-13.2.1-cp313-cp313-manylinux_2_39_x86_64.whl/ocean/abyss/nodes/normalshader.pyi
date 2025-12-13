"""
normalshader

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/normalshader_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Blend', 'Bumpmap', 'Heightmap', 'Linked', 'Normalmap', 'Switch', 'Uniform']
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Blend**
    
    .. include:: /nodes/normalshader/blendnormal.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBlend(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the blend node 
        """
    def setBlend(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the blend node 
        """
class Bumpmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Bumpmap**
    
    .. include:: /nodes/normalshader/bumpmap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Heightmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Heightmap**
    
    .. include:: /nodes/normalshader/heightmap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getUvscale(self) -> float:
        """
        Get the uvscale parameter
        """
    def getZscale(self) -> float:
        """
        Get the zscale parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setUvscale(self, uvscale: typing.SupportsFloat) -> bool:
        """
        Set the uvscale parameter
        """
    def setZscale(self, zscale: typing.SupportsFloat) -> bool:
        """
        Set the zscale parameter
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
class Normalmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Normalmap**
    
    .. include:: /nodes/normalshader/normalmap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Switch(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Switch**
    
    .. include:: /nodes/normalshader/switchnormal.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getSwitch(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the switch node 
        """
    def setSwitch(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the switch node 
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Uniform**
    
    .. include:: /nodes/normalshader/uniformnormal.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDirection(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the direction parameter
        """
    def setDirection(self, direction: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the direction parameter
        """

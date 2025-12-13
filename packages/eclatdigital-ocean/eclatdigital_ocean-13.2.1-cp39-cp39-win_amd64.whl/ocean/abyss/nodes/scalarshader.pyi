"""
scalarshader

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/scalarshader_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Angular', 'Linked', 'Random', 'Texture', 'Uniform']
class Angular(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Angular**
    
    .. include:: /nodes/scalarshader/angular.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAngularscale(self) -> str:
        """
        Get the angularscale parameter
        """
    def getAngularscaleChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getChannel(self) -> str:
        """
        Get the channel parameter
        """
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> float:
        """
        Get the offset parameter
        """
    def getScale(self) -> float:
        """
        Get the scale parameter
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setAngularscale(self, angularscale: str) -> bool:
        """
        Set the angularscale parameter
        """
    def setChannel(self, channel: str) -> bool:
        """
        Set the channel parameter
        """
    def setGreypt(self, greypt: typing.SupportsFloat) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setOffset(self, offset: typing.SupportsFloat) -> bool:
        """
        Set the offset parameter
        """
    def setScale(self, scale: typing.SupportsFloat) -> bool:
        """
        Set the scale parameter
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
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
class Random(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Random**
    
    .. include:: /nodes/scalarshader/random.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getSeed(self) -> int:
        """
        Get the seed parameter
        """
    def setSeed(self, seed: typing.SupportsInt) -> bool:
        """
        Set the seed parameter
        """
class Texture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Texture**
    
    .. include:: /nodes/scalarshader/texture.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getChannel(self) -> str:
        """
        Get the channel parameter
        """
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> float:
        """
        Get the offset parameter
        """
    def getScale(self) -> float:
        """
        Get the scale parameter
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setChannel(self, channel: str) -> bool:
        """
        Set the channel parameter
        """
    def setGreypt(self, greypt: typing.SupportsFloat) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setOffset(self, offset: typing.SupportsFloat) -> bool:
        """
        Set the offset parameter
        """
    def setScale(self, scale: typing.SupportsFloat) -> bool:
        """
        Set the scale parameter
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Uniform**
    
    .. include:: /nodes/scalarshader/uniform.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """

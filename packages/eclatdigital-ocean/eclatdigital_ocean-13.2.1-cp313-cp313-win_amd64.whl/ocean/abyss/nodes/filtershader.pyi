"""
filtershader

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/filtershader_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Angletable', 'Constant', 'Envmapground', 'Image', 'Linked', 'Texture', 'Uniform']
class Angletable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Angletable
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
class Constant(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Constant**
    
    .. include:: /nodes/filtershader/constant.rst
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
class Envmapground(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Envmapground**
    
    .. include:: /nodes/filtershader/envmapground.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedomax(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedomax node 
        """
    def setAlbedomax(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the albedomax node 
        """
class Image(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Image**
    
    .. include:: /nodes/filtershader/image.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getUvscale(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvscale parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setUvscale(self, uvscale: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvscale parameter
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
class Texture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Texture**
    
    .. include:: /nodes/filtershader/texture.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the offset parameter
        """
    def getSaturation(self) -> float:
        """
        Get the saturation parameter
        """
    def getScale(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the scale parameter
        """
    def getStepalpha(self) -> bool:
        """
        Get the stepalpha parameter
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setGreypt(self, greypt: typing.SupportsFloat) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setOffset(self, offset: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the offset parameter
        """
    def setSaturation(self, saturation: typing.SupportsFloat) -> bool:
        """
        Set the saturation parameter
        """
    def setScale(self, scale: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the scale parameter
        """
    def setStepalpha(self, stepalpha: bool) -> bool:
        """
        Set the stepalpha parameter
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Uniform**
    
    .. include:: /nodes/filtershader/uniform.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the spectrum node 
        """

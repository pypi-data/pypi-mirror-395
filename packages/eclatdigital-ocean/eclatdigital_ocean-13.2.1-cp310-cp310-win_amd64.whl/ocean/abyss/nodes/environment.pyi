"""
environment

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/environment_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Additive', 'Black', 'Ciesky', 'Directsun', 'Disc', 'Envmap', 'Hosek', 'Linked', 'Perezsky', 'Preetham', 'Uniform']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Additive**
    
    .. include:: /nodes/environment/additive.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Black(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Black
    """
    def __init__(self, name: str) -> None:
        ...
class Ciesky(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Ciesky**
    
    .. include:: /nodes/environment/ciesky.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> float:
        """
        Get the a parameter
        """
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def getD(self) -> float:
        """
        Get the d parameter
        """
    def getE(self) -> float:
        """
        Get the e parameter
        """
    def getLz(self) -> float:
        """
        Get the lz parameter
        """
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSkytype(self) -> str:
        """
        Get the skytype parameter
        """
    def getSkytypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSunpos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getZenith(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setA(self, a: typing.SupportsFloat) -> bool:
        """
        Set the a parameter
        """
    def setB(self, b: typing.SupportsFloat) -> bool:
        """
        Set the b parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the base node 
        """
    def setC(self, c: typing.SupportsFloat) -> bool:
        """
        Set the c parameter
        """
    def setD(self, d: typing.SupportsFloat) -> bool:
        """
        Set the d parameter
        """
    def setE(self, e: typing.SupportsFloat) -> bool:
        """
        Set the e parameter
        """
    def setLz(self, lz: typing.SupportsFloat) -> bool:
        """
        Set the lz parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setSkytype(self, skytype: str) -> bool:
        """
        Set the skytype parameter
        """
    def setSunpos(self, sunpos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setZenith(self, zenith: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Directsun(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Directsun**
    
    .. include:: /nodes/environment/directsun.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAirmass(self) -> float:
        """
        Get the airmass parameter
        """
    def getDni(self) -> float:
        """
        Get the dni parameter
        """
    def getSunpos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def setAirmass(self, airmass: typing.SupportsFloat) -> bool:
        """
        Set the airmass parameter
        """
    def setDni(self, dni: typing.SupportsFloat) -> bool:
        """
        Set the dni parameter
        """
    def setSunpos(self, sunpos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
class Disc(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Disc**
    
    .. include:: /nodes/environment/disc.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDirection(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the direction parameter
        """
    def getRadius(self) -> float:
        """
        Get the radius parameter
        """
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    def setDirection(self, direction: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the direction parameter
        """
    def setRadius(self, radius: typing.SupportsFloat) -> bool:
        """
        Set the radius parameter
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the spectrum node 
        """
class Envmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Envmap**
    
    .. include:: /nodes/environment/envmap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getFront(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the front parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getNormalize(self) -> str:
        """
        Get the normalize parameter
        """
    def getNormalizeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the base node 
        """
    def setFront(self, front: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the front parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the image node 
        """
    def setNormalize(self, normalize: str) -> bool:
        """
        Set the normalize parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
class Hosek(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Hosek**
    
    .. include:: /nodes/environment/hosek.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedo(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedo node 
        """
    def getSunpos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getSunscale(self) -> float:
        """
        Get the sunscale parameter
        """
    def getTurbidity(self) -> float:
        """
        Get the turbidity parameter
        """
    def getZenith(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setAlbedo(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the albedo node 
        """
    def setSunpos(self, sunpos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setSunscale(self, sunscale: typing.SupportsFloat) -> bool:
        """
        Set the sunscale parameter
        """
    def setTurbidity(self, turbidity: typing.SupportsFloat) -> bool:
        """
        Set the turbidity parameter
        """
    def setZenith(self, zenith: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/environment/linked.rst
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
class Perezsky(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Perezsky**
    
    .. include:: /nodes/environment/perezsky.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> float:
        """
        Get the a parameter
        """
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def getD(self) -> float:
        """
        Get the d parameter
        """
    def getDhi(self) -> float:
        """
        Get the dhi parameter
        """
    def getDhitype(self) -> str:
        """
        Get the dhitype parameter
        """
    def getDhitypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getE(self) -> float:
        """
        Get the e parameter
        """
    def getSunpos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getZenith(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setA(self, a: typing.SupportsFloat) -> bool:
        """
        Set the a parameter
        """
    def setB(self, b: typing.SupportsFloat) -> bool:
        """
        Set the b parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the base node 
        """
    def setC(self, c: typing.SupportsFloat) -> bool:
        """
        Set the c parameter
        """
    def setD(self, d: typing.SupportsFloat) -> bool:
        """
        Set the d parameter
        """
    def setDhi(self, dhi: typing.SupportsFloat) -> bool:
        """
        Set the dhi parameter
        """
    def setDhitype(self, dhitype: str) -> bool:
        """
        Set the dhitype parameter
        """
    def setE(self, e: typing.SupportsFloat) -> bool:
        """
        Set the e parameter
        """
    def setSunpos(self, sunpos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setZenith(self, zenith: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Preetham(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Preetham**
    
    .. include:: /nodes/environment/preetham.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedo(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedo node 
        """
    def getAtmosphere(self) -> bool:
        """
        Get the atmosphere parameter
        """
    def getSunpos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getTurbidity(self) -> float:
        """
        Get the turbidity parameter
        """
    def getZenith(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setAlbedo(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the albedo node 
        """
    def setAtmosphere(self, atmosphere: bool) -> bool:
        """
        Set the atmosphere parameter
        """
    def setSunpos(self, sunpos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setTurbidity(self, turbidity: typing.SupportsFloat) -> bool:
        """
        Set the turbidity parameter
        """
    def setZenith(self, zenith: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Uniform**
    
    .. include:: /nodes/environment/uniform.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNormalize(self) -> str:
        """
        Get the normalize parameter
        """
    def getNormalizeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setNormalize(self, normalize: str) -> bool:
        """
        Set the normalize parameter
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the spectrum node 
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: typing.SupportsFloat) -> bool:
        """
        Set the value parameter
        """

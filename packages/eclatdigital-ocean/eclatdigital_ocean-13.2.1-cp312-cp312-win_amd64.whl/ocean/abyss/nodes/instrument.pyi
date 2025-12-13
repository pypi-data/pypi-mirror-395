"""
instrument

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/instrument_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Bsdfcapture', 'Defaultrawinstrument', 'Fisheyecam', 'Fouriercam', 'Idealrectcam', 'Imported', 'Irradorthoview', 'Irradperspview', 'Irradsphereview', 'Lightmap', 'Linked', 'Materialirrad', 'Orthocam', 'Realrectcam', 'Spherecam', 'Stdcam']
class Bsdfcapture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Bsdfcapture**
    
    .. include:: /nodes/instrument/bsdfcapture.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAniso_sym(self) -> str:
        """
        Get the aniso_sym parameter
        """
    def getAniso_symChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getAnisotropy(self) -> str:
        """
        Get the anisotropy parameter
        """
    def getAnisotropyChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getIntent(self) -> str:
        """
        Get the intent parameter
        """
    def getIntentChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getNormal(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the normal parameter
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getReflection(self) -> str:
        """
        Get the reflection parameter
        """
    def getReflectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getResolution(self) -> str:
        """
        Get the resolution parameter
        """
    def getResolutionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSpotradius(self) -> float:
        """
        Get the spotradius parameter
        """
    def getTangent(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the tangent parameter
        """
    def getTransmission(self) -> str:
        """
        Get the transmission parameter
        """
    def getTransmissionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def setAniso_sym(self, aniso_sym: str) -> bool:
        """
        Set the aniso_sym parameter
        """
    def setAnisotropy(self, anisotropy: str) -> bool:
        """
        Set the anisotropy parameter
        """
    def setIntent(self, intent: str) -> bool:
        """
        Set the intent parameter
        """
    def setNormal(self, normal: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the normal parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setReflection(self, reflection: str) -> bool:
        """
        Set the reflection parameter
        """
    def setResolution(self, resolution: str) -> bool:
        """
        Set the resolution parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSpotradius(self, spotradius: typing.SupportsFloat) -> bool:
        """
        Set the spotradius parameter
        """
    def setTangent(self, tangent: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the tangent parameter
        """
    def setTransmission(self, transmission: str) -> bool:
        """
        Set the transmission parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
class Defaultrawinstrument(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Defaultrawinstrument
    """
    def __init__(self, name: str) -> None:
        ...
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Fisheyecam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Fisheyecam**
    
    .. include:: /nodes/instrument/fisheyecam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: typing.SupportsFloat) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocusdistance(self, focusdistance: typing.SupportsFloat) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Fouriercam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Fouriercam
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getLensradius(self) -> float:
        """
        Get the lensradius parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getSpotradius(self) -> float:
        """
        Get the spotradius parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setLensradius(self, lensradius: typing.SupportsFloat) -> bool:
        """
        Set the lensradius parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setSpotradius(self, spotradius: typing.SupportsFloat) -> bool:
        """
        Set the spotradius parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Idealrectcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Idealrectcam**
    
    .. include:: /nodes/instrument/idealrectcam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_shift_x(self) -> float:
        """
        Get the sensor_shift_x parameter
        """
    def getSensor_shift_y(self) -> float:
        """
        Get the sensor_shift_y parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: typing.SupportsFloat) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: typing.SupportsFloat) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: typing.SupportsFloat) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_shift_x(self, sensor_shift_x: typing.SupportsFloat) -> bool:
        """
        Set the sensor_shift_x parameter
        """
    def setSensor_shift_y(self, sensor_shift_y: typing.SupportsFloat) -> bool:
        """
        Set the sensor_shift_y parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Imported(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Imported**
    
    .. include:: /nodes/instrument/imported.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getRtfs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the rtfs node 
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_offset(self) -> float:
        """
        Get the sensor_offset parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setRtfs(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the rtfs node 
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_offset(self, sensor_offset: typing.SupportsFloat) -> bool:
        """
        Set the sensor_offset parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Irradorthoview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Irradorthoview**
    
    .. include:: /nodes/instrument/irradorthoview.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getHeight(self) -> float:
        """
        Get the height parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWidth(self) -> float:
        """
        Get the width parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setHeight(self, height: typing.SupportsFloat) -> bool:
        """
        Set the height parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWidth(self, width: typing.SupportsFloat) -> bool:
        """
        Set the width parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Irradperspview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Irradperspview**
    
    .. include:: /nodes/instrument/irradperspview.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setFocallength(self, focallength: typing.SupportsFloat) -> bool:
        """
        Set the focallength parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Irradsphereview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Irradsphereview**
    
    .. include:: /nodes/instrument/irradsphereview.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Lightmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Lightmap**
    
    .. include:: /nodes/instrument/lightmap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getMaterial(self) -> str:
        """
        Get the material parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUmax(self) -> float:
        """
        Get the umax parameter
        """
    def getUmin(self) -> float:
        """
        Get the umin parameter
        """
    def getUv_window(self) -> str:
        """
        Get the uv_window parameter
        """
    def getUv_windowChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getVmax(self) -> float:
        """
        Get the vmax parameter
        """
    def getVmin(self) -> float:
        """
        Get the vmin parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setMaterial(self, material: str) -> bool:
        """
        Set the material parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUmax(self, umax: typing.SupportsFloat) -> bool:
        """
        Set the umax parameter
        """
    def setUmin(self, umin: typing.SupportsFloat) -> bool:
        """
        Set the umin parameter
        """
    def setUv_window(self, uv_window: str) -> bool:
        """
        Set the uv_window parameter
        """
    def setVmax(self, vmax: typing.SupportsFloat) -> bool:
        """
        Set the vmax parameter
        """
    def setVmin(self, vmin: typing.SupportsFloat) -> bool:
        """
        Set the vmin parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
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
    **Linked**
    
    .. include:: /nodes/instrument/linked.rst
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
class Materialirrad(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Materialirrad**
    
    .. include:: /nodes/instrument/materialirrad.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getMatlist(self) -> dict:
        """
        Get the matlist parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def setMatlist(self, matlist: dict) -> bool:
        """
        Set the matlist parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"mat": np.array(...), "weight": np.array(...)}
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
class Orthocam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Orthocam**
    
    .. include:: /nodes/instrument/orthocam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getHeight(self) -> float:
        """
        Get the height parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWidth(self) -> float:
        """
        Get the width parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setHeight(self, height: typing.SupportsFloat) -> bool:
        """
        Set the height parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWidth(self, width: typing.SupportsFloat) -> bool:
        """
        Set the width parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Realrectcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Realrectcam**
    
    .. include:: /nodes/instrument/realrectcam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAcoma(self) -> float:
        """
        Get the acoma parameter
        """
    def getAcurvature(self) -> float:
        """
        Get the acurvature parameter
        """
    def getAradial(self) -> float:
        """
        Get the aradial parameter
        """
    def getAspherical(self) -> float:
        """
        Get the aspherical parameter
        """
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAcoma(self, acoma: typing.SupportsFloat) -> bool:
        """
        Set the acoma parameter
        """
    def setAcurvature(self, acurvature: typing.SupportsFloat) -> bool:
        """
        Set the acurvature parameter
        """
    def setAradial(self, aradial: typing.SupportsFloat) -> bool:
        """
        Set the aradial parameter
        """
    def setAspherical(self, aspherical: typing.SupportsFloat) -> bool:
        """
        Set the aspherical parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: typing.SupportsFloat) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: typing.SupportsFloat) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: typing.SupportsFloat) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Spherecam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spherecam**
    
    .. include:: /nodes/instrument/spherecam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getRadius(self) -> float:
        """
        Get the radius parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: typing.SupportsFloat) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocusdistance(self, focusdistance: typing.SupportsFloat) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setRadius(self, radius: typing.SupportsFloat) -> bool:
        """
        Set the radius parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """
class Stdcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Stdcam**
    
    .. include:: /nodes/instrument/stdcam.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_shift_x(self) -> float:
        """
        Get the sensor_shift_x parameter
        """
    def getSensor_shift_y(self) -> float:
        """
        Get the sensor_shift_y parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: typing.SupportsFloat) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: typing.SupportsFloat) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: typing.SupportsFloat) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: typing.SupportsFloat) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_shift_x(self, sensor_shift_x: typing.SupportsFloat) -> bool:
        """
        Set the sensor_shift_x parameter
        """
    def setSensor_shift_y(self, sensor_shift_y: typing.SupportsFloat) -> bool:
        """
        Set the sensor_shift_y parameter
        """
    def setSensor_width(self, sensor_width: typing.SupportsFloat) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: typing.SupportsFloat) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: typing.SupportsFloat) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: typing.SupportsFloat) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: typing.SupportsInt) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: typing.SupportsInt) -> bool:
        """
        Set the yresolution parameter
        """

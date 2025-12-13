"""
emitter

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/emitter_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Additive', 'Cone', 'Cosexp', 'Dirac', 'Gaussian', 'Hemispheremap', 'Lambertian', 'Linearblend', 'Linked', 'Map', 'Planar_ies', 'Singaussian', 'Softcone', 'Spherical_ies']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Additive**
    
    .. include:: /nodes/emitter/additive.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Cone(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cone**
    
    .. include:: /nodes/emitter/cone.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getTanangle(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the tanangle node 
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    def setTanangle(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the tanangle node 
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
class Cosexp(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cosexp**
    
    .. include:: /nodes/emitter/cosexp.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getExponent(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the exponent node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
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
    def setExponent(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the exponent node 
        """
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
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
class Dirac(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Dirac**
    
    .. include:: /nodes/emitter/dirac.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
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
class Gaussian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Gaussian**
    
    .. include:: /nodes/emitter/gaussian.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getStddev(self) -> float:
        """
        Get the stddev parameter
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    def setStddev(self, stddev: typing.SupportsFloat) -> bool:
        """
        Set the stddev parameter
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
class Hemispheremap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Hemispheremap**
    
    .. include:: /nodes/emitter/hemispheremap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMap(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the map node 
        """
    @typing.overload
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    @typing.overload
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPhotometry(self) -> str:
        """
        Get the photometry parameter
        """
    def getPhotometryChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getThetamax(self) -> float:
        """
        Get the thetamax parameter
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
    def setMap(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the map node 
        """
    @typing.overload
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    @typing.overload
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPhotometry(self, photometry: str) -> bool:
        """
        Set the photometry parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setThetamax(self, thetamax: typing.SupportsFloat) -> bool:
        """
        Set the thetamax parameter
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
class Lambertian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Lambertian**
    
    .. include:: /nodes/emitter/lambertian.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
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
class Linearblend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linearblend**
    
    .. include:: /nodes/emitter/linearblend.rst
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
    
    .. include:: /nodes/emitter/map.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMap(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the map node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
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
    def setMap(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the map node 
        """
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
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
class Planar_ies(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Planar_ies**
    
    .. include:: /nodes/emitter/planar_ies.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getFlux(self) -> str:
        """
        Get the flux parameter
        """
    def getFluxChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getForward(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forward parameter
        """
    def getIesdata(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the iesdata node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getRight(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the right parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the base node 
        """
    def setFlux(self, flux: str) -> bool:
        """
        Set the flux parameter
        """
    def setForward(self, forward: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forward parameter
        """
    def setIesdata(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the iesdata node 
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setRight(self, right: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the right parameter
        """
class Singaussian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Singaussian**
    
    .. include:: /nodes/emitter/singaussian.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getStddev(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the stddev node 
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    def setStddev(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the stddev node 
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
class Softcone(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Softcone**
    
    .. include:: /nodes/emitter/softcone.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getMetric(self) -> str:
        """
        Get the metric parameter
        """
    def getMetricChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getPosmod(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the posmod node 
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantity(self) -> str:
        """
        Get the quantity parameter
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getQuantityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getTanfalloff(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the tanfalloff node 
        """
    def getTanfull(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the tanfull node 
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
    def setMetric(self, metric: str) -> bool:
        """
        Set the metric parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setPosmod(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the posmod node 
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    @typing.overload
    def setQuantity(self, quantity: str) -> bool:
        """
        Set the quantity parameter
        """
    def setTanfalloff(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the tanfalloff node 
        """
    def setTanfull(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the tanfull node 
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
class Spherical_ies(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spherical_ies**
    
    .. include:: /nodes/emitter/spherical_ies.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getFlux(self) -> str:
        """
        Get the flux parameter
        """
    def getFluxChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getForward(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the forward parameter
        """
    def getIesdata(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the iesdata node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getRight(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the right parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the base node 
        """
    def setFlux(self, flux: str) -> bool:
        """
        Set the flux parameter
        """
    def setForward(self, forward: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the forward parameter
        """
    def setIesdata(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the iesdata node 
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    def setRight(self, right: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the right parameter
        """

"""
intlaw

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/intlaw_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Advfoil', 'Artistic', 'Cfresnel', 'Foil', 'Fresnel', 'Halffoil', 'Linked', 'Mixtabulated', 'Mm44', 'Null', 'Polarizer', 'Poltabulated', 'Simple', 'Thinfilm']
class Advfoil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Advfoil**
    
    .. include:: /nodes/intlaw/advfoil.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getExternal(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the external node 
        """
    def getInternal(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the internal node 
        """
    def getThickness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the thickness node 
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setExternal(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the external node 
        """
    def setInternal(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the internal node 
        """
    def setThickness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the thickness node 
        """
class Artistic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Artistic**
    
    .. include:: /nodes/intlaw/artistic.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getR0(self) -> float:
        """
        Get the r0 parameter
        """
    def getReflection(self) -> float:
        """
        Get the reflection parameter
        """
    def getReflectioncolor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the reflectioncolor node 
        """
    def getTransmission(self) -> float:
        """
        Get the transmission parameter
        """
    def getTransmissioncolor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the transmissioncolor node 
        """
    def setR0(self, r0: typing.SupportsFloat) -> bool:
        """
        Set the r0 parameter
        """
    def setReflection(self, reflection: typing.SupportsFloat) -> bool:
        """
        Set the reflection parameter
        """
    def setReflectioncolor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the reflectioncolor node 
        """
    def setTransmission(self, transmission: typing.SupportsFloat) -> bool:
        """
        Set the transmission parameter
        """
    def setTransmissioncolor(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the transmissioncolor node 
        """
class Cfresnel(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cfresnel**
    
    .. include:: /nodes/intlaw/cfresnel.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
class Foil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Foil**
    
    .. include:: /nodes/intlaw/foil.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: typing.SupportsFloat) -> bool:
        """
        Set the thickness parameter
        """
class Fresnel(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Fresnel**
    
    .. include:: /nodes/intlaw/fresnel.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Halffoil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Halffoil**
    
    .. include:: /nodes/intlaw/halffoil.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: typing.SupportsFloat) -> bool:
        """
        Set the thickness parameter
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
class Mixtabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Mixtabulated**
    
    .. include:: /nodes/intlaw/mixtabulated.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEr(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er node 
        """
    def getIr(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir node 
        """
    def getT(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t node 
        """
    def setEr(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er node 
        """
    def setIr(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir node 
        """
    def setT(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t node 
        """
class Mm44(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Mm44
    """
    def __init__(self, name: str) -> None:
        ...
    def getEr11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er11 node 
        """
    def getEr12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er12 node 
        """
    def getEr13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er13 node 
        """
    def getEr14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er14 node 
        """
    def getEr21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er21 node 
        """
    def getEr22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er22 node 
        """
    def getEr23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er23 node 
        """
    def getEr24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er24 node 
        """
    def getEr31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er31 node 
        """
    def getEr32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er32 node 
        """
    def getEr33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er33 node 
        """
    def getEr34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er34 node 
        """
    def getEr41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er41 node 
        """
    def getEr42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er42 node 
        """
    def getEr43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er43 node 
        """
    def getEr44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er44 node 
        """
    def getIr11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir11 node 
        """
    def getIr12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir12 node 
        """
    def getIr13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir13 node 
        """
    def getIr14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir14 node 
        """
    def getIr21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir21 node 
        """
    def getIr22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir22 node 
        """
    def getIr23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir23 node 
        """
    def getIr24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir24 node 
        """
    def getIr31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir31 node 
        """
    def getIr32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir32 node 
        """
    def getIr33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir33 node 
        """
    def getIr34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir34 node 
        """
    def getIr41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir41 node 
        """
    def getIr42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir42 node 
        """
    def getIr43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir43 node 
        """
    def getIr44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir44 node 
        """
    def getT11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t11 node 
        """
    def getT12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t12 node 
        """
    def getT13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t13 node 
        """
    def getT14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t14 node 
        """
    def getT21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t21 node 
        """
    def getT22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t22 node 
        """
    def getT23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t23 node 
        """
    def getT24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t24 node 
        """
    def getT31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t31 node 
        """
    def getT32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t32 node 
        """
    def getT33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t33 node 
        """
    def getT34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t34 node 
        """
    def getT41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t41 node 
        """
    def getT42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t42 node 
        """
    def getT43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t43 node 
        """
    def getT44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t44 node 
        """
    def setEr11(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er11 node 
        """
    def setEr12(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er12 node 
        """
    def setEr13(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er13 node 
        """
    def setEr14(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er14 node 
        """
    def setEr21(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er21 node 
        """
    def setEr22(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er22 node 
        """
    def setEr23(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er23 node 
        """
    def setEr24(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er24 node 
        """
    def setEr31(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er31 node 
        """
    def setEr32(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er32 node 
        """
    def setEr33(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er33 node 
        """
    def setEr34(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er34 node 
        """
    def setEr41(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er41 node 
        """
    def setEr42(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er42 node 
        """
    def setEr43(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er43 node 
        """
    def setEr44(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the er44 node 
        """
    def setIr11(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir11 node 
        """
    def setIr12(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir12 node 
        """
    def setIr13(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir13 node 
        """
    def setIr14(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir14 node 
        """
    def setIr21(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir21 node 
        """
    def setIr22(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir22 node 
        """
    def setIr23(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir23 node 
        """
    def setIr24(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir24 node 
        """
    def setIr31(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir31 node 
        """
    def setIr32(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir32 node 
        """
    def setIr33(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir33 node 
        """
    def setIr34(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir34 node 
        """
    def setIr41(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir41 node 
        """
    def setIr42(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir42 node 
        """
    def setIr43(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir43 node 
        """
    def setIr44(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ir44 node 
        """
    def setT11(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t11 node 
        """
    def setT12(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t12 node 
        """
    def setT13(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t13 node 
        """
    def setT14(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t14 node 
        """
    def setT21(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t21 node 
        """
    def setT22(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t22 node 
        """
    def setT23(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t23 node 
        """
    def setT24(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t24 node 
        """
    def setT31(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t31 node 
        """
    def setT32(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t32 node 
        """
    def setT33(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t33 node 
        """
    def setT34(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t34 node 
        """
    def setT41(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t41 node 
        """
    def setT42(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t42 node 
        """
    def setT43(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t43 node 
        """
    def setT44(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the t44 node 
        """
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Null**
    
    .. include:: /nodes/intlaw/null.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Polarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Polarizer**
    
    .. include:: /nodes/intlaw/polarizer.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getM11(self) -> float:
        """
        Get the m11 parameter
        """
    def getM12(self) -> float:
        """
        Get the m12 parameter
        """
    def getM13(self) -> float:
        """
        Get the m13 parameter
        """
    def getM14(self) -> float:
        """
        Get the m14 parameter
        """
    def getM21(self) -> float:
        """
        Get the m21 parameter
        """
    def getM22(self) -> float:
        """
        Get the m22 parameter
        """
    def getM23(self) -> float:
        """
        Get the m23 parameter
        """
    def getM24(self) -> float:
        """
        Get the m24 parameter
        """
    def getM31(self) -> float:
        """
        Get the m31 parameter
        """
    def getM32(self) -> float:
        """
        Get the m32 parameter
        """
    def getM33(self) -> float:
        """
        Get the m33 parameter
        """
    def getM34(self) -> float:
        """
        Get the m34 parameter
        """
    def getM41(self) -> float:
        """
        Get the m41 parameter
        """
    def getM42(self) -> float:
        """
        Get the m42 parameter
        """
    def getM43(self) -> float:
        """
        Get the m43 parameter
        """
    def getM44(self) -> float:
        """
        Get the m44 parameter
        """
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    @typing.overload
    def getPhi(self) -> float:
        """
        Get the phi parameter
        """
    @typing.overload
    def getPhi(self) -> float:
        """
        Get the phi parameter
        """
    @typing.overload
    def getPx(self) -> float:
        """
        Get the px parameter
        """
    @typing.overload
    def getPx(self) -> float:
        """
        Get the px parameter
        """
    @typing.overload
    def getPy(self) -> float:
        """
        Get the py parameter
        """
    @typing.overload
    def getPy(self) -> float:
        """
        Get the py parameter
        """
    def getSubtype(self) -> str:
        """
        Get the subtype parameter
        """
    def getSubtypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    def setM11(self, m11: typing.SupportsFloat) -> bool:
        """
        Set the m11 parameter
        """
    def setM12(self, m12: typing.SupportsFloat) -> bool:
        """
        Set the m12 parameter
        """
    def setM13(self, m13: typing.SupportsFloat) -> bool:
        """
        Set the m13 parameter
        """
    def setM14(self, m14: typing.SupportsFloat) -> bool:
        """
        Set the m14 parameter
        """
    def setM21(self, m21: typing.SupportsFloat) -> bool:
        """
        Set the m21 parameter
        """
    def setM22(self, m22: typing.SupportsFloat) -> bool:
        """
        Set the m22 parameter
        """
    def setM23(self, m23: typing.SupportsFloat) -> bool:
        """
        Set the m23 parameter
        """
    def setM24(self, m24: typing.SupportsFloat) -> bool:
        """
        Set the m24 parameter
        """
    def setM31(self, m31: typing.SupportsFloat) -> bool:
        """
        Set the m31 parameter
        """
    def setM32(self, m32: typing.SupportsFloat) -> bool:
        """
        Set the m32 parameter
        """
    def setM33(self, m33: typing.SupportsFloat) -> bool:
        """
        Set the m33 parameter
        """
    def setM34(self, m34: typing.SupportsFloat) -> bool:
        """
        Set the m34 parameter
        """
    def setM41(self, m41: typing.SupportsFloat) -> bool:
        """
        Set the m41 parameter
        """
    def setM42(self, m42: typing.SupportsFloat) -> bool:
        """
        Set the m42 parameter
        """
    def setM43(self, m43: typing.SupportsFloat) -> bool:
        """
        Set the m43 parameter
        """
    def setM44(self, m44: typing.SupportsFloat) -> bool:
        """
        Set the m44 parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setMultiplier(self, multiplier: typing.SupportsFloat) -> bool:
        """
        Set the multiplier parameter
        """
    @typing.overload
    def setPhi(self, phi: typing.SupportsFloat) -> bool:
        """
        Set the phi parameter
        """
    @typing.overload
    def setPhi(self, phi: typing.SupportsFloat) -> bool:
        """
        Set the phi parameter
        """
    @typing.overload
    def setPx(self, px: typing.SupportsFloat) -> bool:
        """
        Set the px parameter
        """
    @typing.overload
    def setPx(self, px: typing.SupportsFloat) -> bool:
        """
        Set the px parameter
        """
    @typing.overload
    def setPy(self, py: typing.SupportsFloat) -> bool:
        """
        Set the py parameter
        """
    @typing.overload
    def setPy(self, py: typing.SupportsFloat) -> bool:
        """
        Set the py parameter
        """
    def setSubtype(self, subtype: str) -> bool:
        """
        Set the subtype parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: typing.SupportsFloat) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
class Poltabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Poltabulated**
    
    .. include:: /nodes/intlaw/poltabulated.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getErp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the erp node 
        """
    def getErs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ers node 
        """
    def getIrp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the irp node 
        """
    def getIrs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the irs node 
        """
    def getTp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the tp node 
        """
    def getTs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ts node 
        """
    def setErp(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the erp node 
        """
    def setErs(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ers node 
        """
    def setIrp(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the irp node 
        """
    def setIrs(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the irs node 
        """
    def setTp(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the tp node 
        """
    def setTs(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the ts node 
        """
class Simple(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Simple**
    
    .. include:: /nodes/intlaw/simple.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getR0(self) -> float:
        """
        Get the r0 parameter
        """
    def setR0(self, r0: typing.SupportsFloat) -> bool:
        """
        Set the r0 parameter
        """
class Thinfilm(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Thinfilm**
    
    .. include:: /nodes/intlaw/thinfilm.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: typing.SupportsFloat) -> bool:
        """
        Set the thickness parameter
        """

"""
material

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/material_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Axf_svbrdf', 'Blend', 'Clone', 'Doublesided', 'Generic', 'Idealreflpolarizer', 'Idealtranspolarizer', 'Linked', 'Multi', 'Null']
class Axf_svbrdf(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Axf_svbrdf**
    
    .. include:: /nodes/material/axf-svbrdf.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getDiffuse_model(self) -> str:
        """
        Get the diffuse-model parameter
        """
    def getDiffuse_modelChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getFresnel(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the fresnel node 
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def getUvtran(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setDiffuse_model(self, diffuse_model: str) -> bool:
        """
        Set the diffuse-model parameter
        """
    def setFresnel(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the fresnel node 
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the roughness node 
        """
    def setUvtran(self, uvtran: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Blend**
    
    .. include:: /nodes/material/blend.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBlend(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the blend node 
        """
    def getForcestep(self) -> bool:
        """
        Get the forcestep parameter
        """
    def getMaterial_a(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_a node 
        """
    def getMaterial_b(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_b node 
        """
    def setBlend(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the blend node 
        """
    def setForcestep(self, forcestep: bool) -> bool:
        """
        Set the forcestep parameter
        """
    def setMaterial_a(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the material_a node 
        """
    def setMaterial_b(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the material_b node 
        """
class Clone(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Clone
    """
    def __init__(self, name: str) -> None:
        ...
    def getTarget(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the target node 
        """
    def setTarget(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the target node 
        """
class Doublesided(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Doublesided**
    
    .. include:: /nodes/material/doublesided.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getMaterial_b(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_b node 
        """
    def getMaterial_f(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_f node 
        """
    def setMaterial_b(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the material_b node 
        """
    def setMaterial_f(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the material_f node 
        """
class Generic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Generic**
    
    .. include:: /nodes/material/generic.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBsdf(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the bsdf node 
        """
    def setBsdf(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the bsdf node 
        """
class Idealreflpolarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Idealreflpolarizer**
    
    .. include:: /nodes/material/idealreflpolarizer.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getF(self) -> float:
        """
        Get the F parameter
        """
    def getM00(self) -> float:
        """
        Get the m00 parameter
        """
    def getM01(self) -> float:
        """
        Get the m01 parameter
        """
    def getM02(self) -> float:
        """
        Get the m02 parameter
        """
    def getM03(self) -> float:
        """
        Get the m03 parameter
        """
    def getM10(self) -> float:
        """
        Get the m10 parameter
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
    def getM20(self) -> float:
        """
        Get the m20 parameter
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
    def getM30(self) -> float:
        """
        Get the m30 parameter
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
    def getPhase(self) -> float:
        """
        Get the phase parameter
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
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setF(self, F: typing.SupportsFloat) -> bool:
        """
        Set the F parameter
        """
    def setM00(self, m00: typing.SupportsFloat) -> bool:
        """
        Set the m00 parameter
        """
    def setM01(self, m01: typing.SupportsFloat) -> bool:
        """
        Set the m01 parameter
        """
    def setM02(self, m02: typing.SupportsFloat) -> bool:
        """
        Set the m02 parameter
        """
    def setM03(self, m03: typing.SupportsFloat) -> bool:
        """
        Set the m03 parameter
        """
    def setM10(self, m10: typing.SupportsFloat) -> bool:
        """
        Set the m10 parameter
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
    def setM20(self, m20: typing.SupportsFloat) -> bool:
        """
        Set the m20 parameter
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
    def setM30(self, m30: typing.SupportsFloat) -> bool:
        """
        Set the m30 parameter
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
    def setPhase(self, phase: typing.SupportsFloat) -> bool:
        """
        Set the phase parameter
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
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Idealtranspolarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Idealtranspolarizer**
    
    .. include:: /nodes/material/idealtranspolarizer.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getF(self) -> float:
        """
        Get the F parameter
        """
    def getM00(self) -> float:
        """
        Get the m00 parameter
        """
    def getM01(self) -> float:
        """
        Get the m01 parameter
        """
    def getM02(self) -> float:
        """
        Get the m02 parameter
        """
    def getM03(self) -> float:
        """
        Get the m03 parameter
        """
    def getM10(self) -> float:
        """
        Get the m10 parameter
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
    def getM20(self) -> float:
        """
        Get the m20 parameter
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
    def getM30(self) -> float:
        """
        Get the m30 parameter
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
    def getPhase(self) -> float:
        """
        Get the phase parameter
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
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setF(self, F: typing.SupportsFloat) -> bool:
        """
        Set the F parameter
        """
    def setM00(self, m00: typing.SupportsFloat) -> bool:
        """
        Set the m00 parameter
        """
    def setM01(self, m01: typing.SupportsFloat) -> bool:
        """
        Set the m01 parameter
        """
    def setM02(self, m02: typing.SupportsFloat) -> bool:
        """
        Set the m02 parameter
        """
    def setM03(self, m03: typing.SupportsFloat) -> bool:
        """
        Set the m03 parameter
        """
    def setM10(self, m10: typing.SupportsFloat) -> bool:
        """
        Set the m10 parameter
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
    def setM20(self, m20: typing.SupportsFloat) -> bool:
        """
        Set the m20 parameter
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
    def setM30(self, m30: typing.SupportsFloat) -> bool:
        """
        Set the m30 parameter
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
    def setPhase(self, phase: typing.SupportsFloat) -> bool:
        """
        Set the phase parameter
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
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: typing.SupportsFloat) -> bool:
        """
        Set the valabs parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/material/linked.rst
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
class Multi(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Multi
    """
    def __init__(self, name: str) -> None:
        ...
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Null**
    
    .. include:: /nodes/material/null.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...

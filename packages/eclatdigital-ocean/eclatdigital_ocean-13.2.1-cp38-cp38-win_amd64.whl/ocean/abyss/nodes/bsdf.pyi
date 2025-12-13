"""
bsdf

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/bsdf_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Additive', 'Black', 'Blend', 'Carpaint', 'Coateddiffuse', 'Doublesided', 'Equisolidtable', 'Fluo_lambertian', 'Fluo_oren_nayar', 'Glossy', 'Igloomatrix', 'Isomap', 'Lambertian', 'Lambertian_transmitter', 'Linked', 'Lobe', 'Null', 'Oren_nayar', 'Phong', 'Reflective', 'Reflective_diffraction_map', 'Refractive', 'Rusinkiewicztable', 'Simpleisotable', 'Sparklify', 'Specular', 'Switch', 'Velvet']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Additive**
    
    .. include:: /nodes/bsdf/additive.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Black(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Black**
    
    .. include:: /nodes/bsdf/black.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Blend**
    
    .. include:: /nodes/bsdf/blend.rst
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
class Carpaint(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Carpaint**
    
    .. include:: /nodes/bsdf/carpaint.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffusionthickness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffusionthickness node 
        """
    def getDye(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dye node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getParticle(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the particle node 
        """
    def getParticledisalignment(self) -> float:
        """
        Get the particledisalignment parameter
        """
    def getParticleroughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the particleroughness node 
        """
    def getParticlesize(self) -> float:
        """
        Get the particlesize parameter
        """
    def getPigment(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the pigment node 
        """
    def getSurfaceroughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the surfaceroughness node 
        """
    def setDiffusionthickness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffusionthickness node 
        """
    def setDye(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dye node 
        """
    def setIor(self, ior: typing.SupportsFloat) -> bool:
        """
        Set the ior parameter
        """
    def setParticle(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the particle node 
        """
    def setParticledisalignment(self, particledisalignment: typing.SupportsFloat) -> bool:
        """
        Set the particledisalignment parameter
        """
    def setParticleroughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the particleroughness node 
        """
    def setParticlesize(self, particlesize: typing.SupportsFloat) -> bool:
        """
        Set the particlesize parameter
        """
    def setPigment(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the pigment node 
        """
    def setSurfaceroughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the surfaceroughness node 
        """
class Coateddiffuse(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Coateddiffuse**
    
    .. include:: /nodes/bsdf/coateddiffuse.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getCoatingthickness(self) -> float:
        """
        Get the coatingthickness parameter
        """
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def setCoatingthickness(self, coatingthickness: typing.SupportsFloat) -> bool:
        """
        Set the coatingthickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the dielectricfunc node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the intlaw node 
        """
class Doublesided(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Doublesided**
    
    .. include:: /nodes/bsdf/doublesided.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBack(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the back node 
        """
    def getFront(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the front node 
        """
    def setBack(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the back node 
        """
    def setFront(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the front node 
        """
class Equisolidtable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Equisolidtable**
    
    .. include:: /nodes/bsdf/equisolidtable.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAniso_sym(self) -> int:
        """
        Get the aniso_sym parameter
        """
    def getKh_corr(self) -> bool:
        """
        Get the kh_corr parameter
        """
    def getNumphii(self) -> int:
        """
        Get the numphii parameter
        """
    def getNumthetai(self) -> int:
        """
        Get the numthetai parameter
        """
    def setAniso_sym(self, aniso_sym: typing.SupportsInt) -> bool:
        """
        Set the aniso_sym parameter
        """
    def setKh_corr(self, kh_corr: bool) -> bool:
        """
        Set the kh_corr parameter
        """
    def setNumphii(self, numphii: typing.SupportsInt) -> bool:
        """
        Set the numphii parameter
        """
    def setNumthetai(self, numthetai: typing.SupportsInt) -> bool:
        """
        Set the numthetai parameter
        """
class Fluo_lambertian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Fluo_lambertian**
    
    .. include:: /nodes/bsdf/fluo_lambertian.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAbsorption(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the absorption node 
        """
    def getConcentrationParameter(self) -> float:
        """
        Get the concentrationParameter parameter
        """
    def getDiffusion(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffusion node 
        """
    def getEmission(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the emission node 
        """
    def getQuantumYield(self) -> float:
        """
        Get the quantumYield parameter
        """
    def setAbsorption(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the absorption node 
        """
    def setConcentrationParameter(self, concentrationParameter: typing.SupportsFloat) -> bool:
        """
        Set the concentrationParameter parameter
        """
    def setDiffusion(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffusion node 
        """
    def setEmission(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the emission node 
        """
    def setQuantumYield(self, quantumYield: typing.SupportsFloat) -> bool:
        """
        Set the quantumYield parameter
        """
class Fluo_oren_nayar(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Fluo_oren_nayar**
    
    .. include:: /nodes/bsdf/fluo_oren_nayar.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAbsorption(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the absorption node 
        """
    def getConcentrationParameter(self) -> float:
        """
        Get the concentrationParameter parameter
        """
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getEmission(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the emission node 
        """
    def getQuantumYield(self) -> float:
        """
        Get the quantumYield parameter
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def setAbsorption(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the absorption node 
        """
    def setConcentrationParameter(self, concentrationParameter: typing.SupportsFloat) -> bool:
        """
        Set the concentrationParameter parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setEmission(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the emission node 
        """
    def setQuantumYield(self, quantumYield: typing.SupportsFloat) -> bool:
        """
        Set the quantumYield parameter
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sigma node 
        """
class Glossy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Glossy**
    
    .. include:: /nodes/bsdf/glossy.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setIor(self, ior: typing.SupportsFloat) -> bool:
        """
        Set the ior parameter
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the roughness node 
        """
class Igloomatrix(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Igloomatrix**
    
    .. include:: /nodes/bsdf/igloomatrix.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBrdf_back(self) -> dict:
        """
        Get the brdf_back parameter
        """
    def getBrdf_front(self) -> dict:
        """
        Get the brdf_front parameter
        """
    def getBtdf(self) -> dict:
        """
        Get the btdf parameter
        """
    def getNumphi(self) -> dict:
        """
        Get the numphi parameter
        """
    def getTheta(self) -> dict:
        """
        Get the theta parameter
        """
    def setBrdf_back(self, brdf_back: dict) -> bool:
        """
        Set the brdf_back parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"brdf_back": np.array(...)}
        """
    def setBrdf_front(self, brdf_front: dict) -> bool:
        """
        Set the brdf_front parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"brdf_front": np.array(...)}
        """
    def setBtdf(self, btdf: dict) -> bool:
        """
        Set the btdf parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"btdf": np.array(...)}
        """
    def setNumphi(self, numphi: dict) -> bool:
        """
        Set the numphi parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"numphi": np.array(...)}
        """
    def setTheta(self, theta: dict) -> bool:
        """
        Set the theta parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"theta": np.array(...)}
        """
class Isomap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Isomap**
    
    .. include:: /nodes/bsdf/isomap.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getThetas(self) -> dict:
        """
        Get the thetas parameter
        """
    def setThetas(self, thetas: dict) -> bool:
        """
        Set the thetas parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"map": np.array(...), "theta": np.array(...)}
        """
class Lambertian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Lambertian**
    
    .. include:: /nodes/bsdf/lambertian.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
class Lambertian_transmitter(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Lambertian_transmitter**
    
    .. include:: /nodes/bsdf/lambertiantransmitter.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Linked**
    
    .. include:: /nodes/bsdf/linked.rst
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
class Lobe(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Lobe**
    
    .. include:: /nodes/bsdf/lobe.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getLobe(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the lobe node 
        """
    def setLobe(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the lobe node 
        """
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Null**
    
    .. include:: /nodes/bsdf/null.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
class Oren_nayar(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Oren_nayar**
    
    .. include:: /nodes/bsdf/oren_nayar.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sigma node 
        """
class Phong(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Phong**
    
    .. include:: /nodes/bsdf/phong.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getExponent(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the exponent node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getSpecular(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the specular node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setExponent(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the exponent node 
        """
    def setIor(self, ior: typing.SupportsFloat) -> bool:
        """
        Set the ior parameter
        """
    def setSpecular(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the specular node 
        """
class Reflective(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Reflective**
    
    .. include:: /nodes/bsdf/reflective.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getRereflections(self) -> bool:
        """
        Get the rereflections parameter
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the intlaw node 
        """
    def setRereflections(self, rereflections: bool) -> bool:
        """
        Set the rereflections parameter
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the roughness node 
        """
class Reflective_diffraction_map(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Reflective_diffraction_map**
    
    .. include:: /nodes/bsdf/reflective_diffraction_map.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDispersion_power(self) -> float:
        """
        Get the dispersion_power parameter
        """
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getLambda_map(self) -> float:
        """
        Get the lambda_map parameter
        """
    def getLambda_max(self) -> float:
        """
        Get the lambda_max parameter
        """
    def getLambda_min(self) -> float:
        """
        Get the lambda_min parameter
        """
    def getTheta_max(self) -> float:
        """
        Get the theta_max parameter
        """
    def setDispersion_power(self, dispersion_power: typing.SupportsFloat) -> bool:
        """
        Set the dispersion_power parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the intlaw node 
        """
    def setLambda_map(self, lambda_map: typing.SupportsFloat) -> bool:
        """
        Set the lambda_map parameter
        """
    def setLambda_max(self, lambda_max: typing.SupportsFloat) -> bool:
        """
        Set the lambda_max parameter
        """
    def setLambda_min(self, lambda_min: typing.SupportsFloat) -> bool:
        """
        Set the lambda_min parameter
        """
    def setTheta_max(self, theta_max: typing.SupportsFloat) -> bool:
        """
        Set the theta_max parameter
        """
class Refractive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Refractive**
    
    .. include:: /nodes/bsdf/refractive.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getRereflections(self) -> bool:
        """
        Get the rereflections parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the intlaw node 
        """
    def setRereflections(self, rereflections: bool) -> bool:
        """
        Set the rereflections parameter
        """
class Rusinkiewicztable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Rusinkiewicztable**
    
    .. include:: /nodes/bsdf/rusinkiewicztable.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNum_phi_d(self) -> dict:
        """
        Get the num_phi_d parameter
        """
    def getNum_phi_h(self) -> dict:
        """
        Get the num_phi_h parameter
        """
    def getPhi_h_sym(self) -> int:
        """
        Get the phi_h_sym parameter
        """
    def getTheta_h(self) -> dict:
        """
        Get the theta_h parameter
        """
    def getTransmission(self) -> bool:
        """
        Get the transmission parameter
        """
    def getValues(self) -> dict:
        """
        Get the values parameter
        """
    def setNum_phi_d(self, num_phi_d: dict) -> bool:
        """
        Set the num_phi_d parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"num_phi_d": np.array(...)}
        """
    def setNum_phi_h(self, num_phi_h: dict) -> bool:
        """
        Set the num_phi_h parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"num_phi_h": np.array(...)}
        """
    def setPhi_h_sym(self, phi_h_sym: typing.SupportsInt) -> bool:
        """
        Set the phi_h_sym parameter
        """
    def setTheta_h(self, theta_h: dict) -> bool:
        """
        Set the theta_h parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"theta_h": np.array(...)}
        """
    def setTransmission(self, transmission: bool) -> bool:
        """
        Set the transmission parameter
        """
    def setValues(self, values: dict) -> bool:
        """
        Set the values parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"values": np.array(...)}
        """
class Simpleisotable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Simpleisotable**
    
    .. include:: /nodes/bsdf/simpleisotable.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNum_phi_out(self) -> int:
        """
        Get the num_phi_out parameter
        """
    def getPhi_out_sym(self) -> int:
        """
        Get the phi_out_sym parameter
        """
    def getTheta_in(self) -> dict:
        """
        Get the theta_in parameter
        """
    def getTheta_out(self) -> dict:
        """
        Get the theta_out parameter
        """
    def getValues(self) -> dict:
        """
        Get the values parameter
        """
    def setNum_phi_out(self, num_phi_out: typing.SupportsInt) -> bool:
        """
        Set the num_phi_out parameter
        """
    def setPhi_out_sym(self, phi_out_sym: typing.SupportsInt) -> bool:
        """
        Set the phi_out_sym parameter
        """
    def setTheta_in(self, theta_in: dict) -> bool:
        """
        Set the theta_in parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"theta_in": np.array(...)}
        """
    def setTheta_out(self, theta_out: dict) -> bool:
        """
        Set the theta_out parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"theta_out": np.array(...)}
        """
    def setValues(self, values: dict) -> bool:
        """
        Set the values parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"values": np.array(...)}
        """
class Sparklify(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Sparklify**
    
    .. include:: /nodes/bsdf/sparklify.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAverage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the average node 
        """
    def getDensity(self) -> float:
        """
        Get the density parameter
        """
    def getRoughness(self) -> dict:
        """
        Get the roughness parameter
        """
    def setAverage(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the average node 
        """
    def setDensity(self, density: typing.SupportsFloat) -> bool:
        """
        Set the density parameter
        """
    def setRoughness(self, roughness: dict) -> bool:
        """
        Set the roughness parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"angle": np.array(...), "value": np.array(...)}
        """
class Specular(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Specular**
    
    .. include:: /nodes/bsdf/specular.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getIrtrmin_tweak(self) -> float:
        """
        Get the irtrmin_tweak parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the intlaw node 
        """
    def setIrtrmin_tweak(self, irtrmin_tweak: typing.SupportsFloat) -> bool:
        """
        Set the irtrmin_tweak parameter
        """
class Switch(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Switch**
    
    .. include:: /nodes/bsdf/switch.rst
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
class Velvet(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Velvet**
    
    .. include:: /nodes/bsdf/velvet.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getRebounce(self) -> float:
        """
        Get the rebounce parameter
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def getSpread(self) -> float:
        """
        Get the spread parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the diffuse node 
        """
    def setRebounce(self, rebounce: typing.SupportsFloat) -> bool:
        """
        Set the rebounce parameter
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> ocean.abyss.nodes.Node:
        """
                    Set the sigma node 
        """
    def setSpread(self, spread: typing.SupportsFloat) -> bool:
        """
        Set the spread parameter
        """

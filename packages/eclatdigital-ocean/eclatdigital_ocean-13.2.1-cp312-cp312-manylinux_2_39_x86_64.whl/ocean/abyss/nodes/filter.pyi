"""
filter

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/filter_desc.rst
 
"""
from __future__ import annotations
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Averageautogain', 'Drago', 'Gain', 'Gaussianblur', 'Glare', 'Histogramautogain', 'Illuminance', 'Isosensitivity', 'Linked', 'Merge', 'Noisekiller', 'Purkinje', 'Reinhardglobal', 'Reinhardlocal', 'Resize', 'Spectocustom', 'Spectoxyz', 'Spectraltohv', 'Sphereresolutionfix', 'Watermark']
class Averageautogain(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Averageautogain**
    
    .. include:: /nodes/filter/averageautogain.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getEvadjust(self) -> float:
        """
        Get the evadjust parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setEvadjust(self, evadjust: typing.SupportsFloat) -> bool:
        """
        Set the evadjust parameter
        """
class Drago(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Drago**
    
    .. include:: /nodes/filter/drago.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getLd(self) -> int:
        """
        Get the ld parameter
        """
    def setB(self, b: typing.SupportsFloat) -> bool:
        """
        Set the b parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setLd(self, ld: typing.SupportsInt) -> bool:
        """
        Set the ld parameter
        """
class Gain(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Gain**
    
    .. include:: /nodes/filter/gain.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getGainev(self) -> float:
        """
        Get the gainev parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setGainev(self, gainev: typing.SupportsFloat) -> bool:
        """
        Set the gainev parameter
        """
class Gaussianblur(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Gaussianblur**
    
    .. include:: /nodes/filter/gaussianblur.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getSigma(self) -> float:
        """
        Get the sigma parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setSigma(self, sigma: typing.SupportsFloat) -> bool:
        """
        Set the sigma parameter
        """
class Glare(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Glare**
    
    .. include:: /nodes/filter/glare.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAge(self) -> int:
        """
        Get the age parameter
        """
    @typing.overload
    def getDispersion(self) -> bool:
        """
        Get the dispersion parameter
        """
    @typing.overload
    def getDispersion(self) -> bool:
        """
        Get the dispersion parameter
        """
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getLuminance(self) -> str:
        """
        Get the luminance parameter
        """
    def getLuminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getThreshold(self) -> float:
        """
        Get the threshold parameter
        """
    def setAge(self, age: typing.SupportsInt) -> bool:
        """
        Set the age parameter
        """
    @typing.overload
    def setDispersion(self, dispersion: bool) -> bool:
        """
        Set the dispersion parameter
        """
    @typing.overload
    def setDispersion(self, dispersion: bool) -> bool:
        """
        Set the dispersion parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setLuminance(self, luminance: str) -> bool:
        """
        Set the luminance parameter
        """
    def setThreshold(self, threshold: typing.SupportsFloat) -> bool:
        """
        Set the threshold parameter
        """
class Histogramautogain(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Histogramautogain**
    
    .. include:: /nodes/filter/histogramautogain.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getEvadjust(self) -> float:
        """
        Get the evadjust parameter
        """
    def getHigh(self) -> float:
        """
        Get the high parameter
        """
    def getLow(self) -> float:
        """
        Get the low parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setEvadjust(self, evadjust: typing.SupportsFloat) -> bool:
        """
        Set the evadjust parameter
        """
    def setHigh(self, high: typing.SupportsFloat) -> bool:
        """
        Set the high parameter
        """
    def setLow(self, low: typing.SupportsFloat) -> bool:
        """
        Set the low parameter
        """
class Illuminance(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Illuminance**
    
    .. include:: /nodes/filter/illuminance.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getIlluminance(self) -> dict:
        """
        Get the illuminance parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setIlluminance(self, illuminance: dict) -> bool:
        """
        Set the illuminance parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"yInput": np.array(...), "iInput": np.array(...)}
        """
class Isosensitivity(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Isosensitivity**
    
    .. include:: /nodes/filter/isosensitivity.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getIso(self) -> float:
        """
        Get the iso parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setIso(self, iso: typing.SupportsFloat) -> bool:
        """
        Set the iso parameter
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
class Merge(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Merge**
    
    .. include:: /nodes/filter/merge.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getRaw_path(self) -> str:
        """
        Get the raw_path parameter
        """
    def getRegion_height(self) -> int:
        """
        Get the region_height parameter
        """
    def getRegion_width(self) -> int:
        """
        Get the region_width parameter
        """
    def getX_offset(self) -> int:
        """
        Get the x_offset parameter
        """
    def getY_offset(self) -> int:
        """
        Get the y_offset parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setRaw_path(self, raw_path: str) -> bool:
        """
        Set the raw_path parameter
        """
    def setRegion_height(self, region_height: typing.SupportsInt) -> bool:
        """
        Set the region_height parameter
        """
    def setRegion_width(self, region_width: typing.SupportsInt) -> bool:
        """
        Set the region_width parameter
        """
    def setX_offset(self, x_offset: typing.SupportsInt) -> bool:
        """
        Set the x_offset parameter
        """
    def setY_offset(self, y_offset: typing.SupportsInt) -> bool:
        """
        Set the y_offset parameter
        """
class Noisekiller(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Noisekiller**
    
    .. include:: /nodes/filter/noisekiller.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getMethod(self) -> str:
        """
        Get the method parameter
        """
    def getMethodChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getQuality(self) -> str:
        """
        Get the quality parameter
        """
    def getQualityChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getStrength(self) -> float:
        """
        Get the strength parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setMethod(self, method: str) -> bool:
        """
        Set the method parameter
        """
    def setQuality(self, quality: str) -> bool:
        """
        Set the quality parameter
        """
    def setStrength(self, strength: typing.SupportsFloat) -> bool:
        """
        Set the strength parameter
        """
class Purkinje(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Purkinje
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getVisionmode(self) -> float:
        """
        Get the visionmode parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setVisionmode(self, visionmode: typing.SupportsFloat) -> bool:
        """
        Set the visionmode parameter
        """
class Reinhardglobal(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Reinhardglobal**
    
    .. include:: /nodes/filter/reinhardglobal.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getStops(self) -> float:
        """
        Get the stops parameter
        """
    def getStrength(self) -> float:
        """
        Get the strength parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setStops(self, stops: typing.SupportsFloat) -> bool:
        """
        Set the stops parameter
        """
    def setStrength(self, strength: typing.SupportsFloat) -> bool:
        """
        Set the strength parameter
        """
class Reinhardlocal(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Reinhardlocal**
    
    .. include:: /nodes/filter/reinhardlocal.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getStops(self) -> float:
        """
        Get the stops parameter
        """
    def getStrength(self) -> float:
        """
        Get the strength parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setStops(self, stops: typing.SupportsFloat) -> bool:
        """
        Set the stops parameter
        """
    def setStrength(self, strength: typing.SupportsFloat) -> bool:
        """
        Set the strength parameter
        """
class Resize(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Resize**
    
    .. include:: /nodes/filter/resize.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getHeight(self) -> int:
        """
        Get the height parameter
        """
    def getSharpness(self) -> float:
        """
        Get the sharpness parameter
        """
    def getUnit(self) -> str:
        """
        Get the unit parameter
        """
    def getUnitChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getWidth(self) -> int:
        """
        Get the width parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setHeight(self, height: typing.SupportsInt) -> bool:
        """
        Set the height parameter
        """
    def setSharpness(self, sharpness: typing.SupportsFloat) -> bool:
        """
        Set the sharpness parameter
        """
    def setUnit(self, unit: str) -> bool:
        """
        Set the unit parameter
        """
    def setWidth(self, width: typing.SupportsInt) -> bool:
        """
        Set the width parameter
        """
class Spectocustom(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spectocustom**
    
    .. include:: /nodes/filter/spectocustom.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
class Spectoxyz(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spectoxyz**
    
    .. include:: /nodes/filter/spectoxyz.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
class Spectraltohv(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Spectraltohv**
    
    .. include:: /nodes/filter/spectraltohv.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getAge(self) -> int:
        """
        Get the age parameter
        """
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    @typing.overload
    def getIlluminance(self) -> str:
        """
        Get the illuminance parameter
        """
    @typing.overload
    def getIlluminance(self) -> str:
        """
        Get the illuminance parameter
        """
    @typing.overload
    def getIlluminance(self) -> str:
        """
        Get the illuminance parameter
        """
    @typing.overload
    def getIlluminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getIlluminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getIlluminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getLuminance(self) -> str:
        """
        Get the luminance parameter
        """
    @typing.overload
    def getLuminance(self) -> str:
        """
        Get the luminance parameter
        """
    @typing.overload
    def getLuminance(self) -> str:
        """
        Get the luminance parameter
        """
    @typing.overload
    def getLuminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getLuminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getLuminanceChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getTime(self) -> int:
        """
        Get the time parameter
        """
    @typing.overload
    def getTime(self) -> int:
        """
        Get the time parameter
        """
    def getTime_adaptation(self) -> str:
        """
        Get the time_adaptation parameter
        """
    def getTime_adaptationChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setAge(self, age: typing.SupportsInt) -> bool:
        """
        Set the age parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    @typing.overload
    def setIlluminance(self, illuminance: str) -> bool:
        """
        Set the illuminance parameter
        """
    @typing.overload
    def setIlluminance(self, illuminance: str) -> bool:
        """
        Set the illuminance parameter
        """
    @typing.overload
    def setIlluminance(self, illuminance: str) -> bool:
        """
        Set the illuminance parameter
        """
    @typing.overload
    def setLuminance(self, luminance: str) -> bool:
        """
        Set the luminance parameter
        """
    @typing.overload
    def setLuminance(self, luminance: str) -> bool:
        """
        Set the luminance parameter
        """
    @typing.overload
    def setLuminance(self, luminance: str) -> bool:
        """
        Set the luminance parameter
        """
    @typing.overload
    def setTime(self, time: typing.SupportsInt) -> bool:
        """
        Set the time parameter
        """
    @typing.overload
    def setTime(self, time: typing.SupportsInt) -> bool:
        """
        Set the time parameter
        """
    def setTime_adaptation(self, time_adaptation: str) -> bool:
        """
        Set the time_adaptation parameter
        """
class Sphereresolutionfix(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Sphereresolutionfix**
    
    .. include:: /nodes/filter/sphereresolutionfix.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
class Watermark(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Watermark**
    
    .. include:: /nodes/filter/watermark.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getEnabled(self) -> bool:
        """
        Get the enabled parameter
        """
    def getFilepath(self) -> str:
        """
        Get the filepath parameter
        """
    def getRepeat(self) -> bool:
        """
        Get the repeat parameter
        """
    def getScale(self) -> float:
        """
        Get the scale parameter
        """
    def getStrength(self) -> float:
        """
        Get the strength parameter
        """
    def getX(self) -> int:
        """
        Get the X parameter
        """
    def getY(self) -> int:
        """
        Get the Y parameter
        """
    def setEnabled(self, enabled: bool) -> bool:
        """
        Set the enabled parameter
        """
    def setFilepath(self, filepath: str) -> bool:
        """
        Set the filepath parameter
        """
    def setRepeat(self, repeat: bool) -> bool:
        """
        Set the repeat parameter
        """
    def setScale(self, scale: typing.SupportsFloat) -> bool:
        """
        Set the scale parameter
        """
    def setStrength(self, strength: typing.SupportsFloat) -> bool:
        """
        Set the strength parameter
        """
    def setX(self, X: typing.SupportsInt) -> bool:
        """
        Set the X parameter
        """
    def setY(self, Y: typing.SupportsInt) -> bool:
        """
        Set the Y parameter
        """

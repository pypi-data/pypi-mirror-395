"""
spectrum

.. only:: not api_only 

    .. include:: /nodes/classtypes_desc/spectrum_desc.rst
 
"""
from __future__ import annotations
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['Abbenumber', 'Blackbody', 'Cauchy', 'Cie_xyz', 'Linked', 'Preset', 'Rgb', 'Square', 'Tabulated', 'Triangle', 'Uniform']
class Abbenumber(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Abbenumber**
    
    .. include:: /nodes/spectrum/abbenumber.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getNd(self) -> float:
        """
        Get the nd parameter
        """
    def getVd(self) -> float:
        """
        Get the Vd parameter
        """
    def setNd(self, nd: typing.SupportsFloat) -> bool:
        """
        Set the nd parameter
        """
    def setVd(self, Vd: typing.SupportsFloat) -> bool:
        """
        Set the Vd parameter
        """
class Blackbody(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Blackbody**
    
    .. include:: /nodes/spectrum/blackbody.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getGain(self) -> float:
        """
        Get the gain parameter
        """
    def getTemp(self) -> float:
        """
        Get the temp parameter
        """
    def setGain(self, gain: typing.SupportsFloat) -> bool:
        """
        Set the gain parameter
        """
    def setTemp(self, temp: typing.SupportsFloat) -> bool:
        """
        Set the temp parameter
        """
class Cauchy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cauchy**
    
    .. include:: /nodes/spectrum/cauchy.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def setB(self, b: typing.SupportsFloat) -> bool:
        """
        Set the b parameter
        """
    def setC(self, c: typing.SupportsFloat) -> bool:
        """
        Set the c parameter
        """
class Cie_xyz(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Cie_xyz**
    
    .. include:: /nodes/spectrum/cie-xyz.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getXyz(self) -> dict:
        """
        Get the xyz parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setXyz(self, xyz: dict) -> bool:
        """
        Set the xyz parameter
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
class Preset(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Preset**
    
    .. include:: /nodes/spectrum/preset.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getGain(self) -> float:
        """
        Get the gain parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setGain(self, gain: typing.SupportsFloat) -> bool:
        """
        Set the gain parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Rgb(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Rgb**
    
    .. include:: /nodes/spectrum/rgb.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getGamma(self) -> float:
        """
        Get the gamma parameter
        """
    def getRgb(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Get the rgb parameter
        """
    def setGamma(self, gamma: typing.SupportsFloat) -> bool:
        """
        Set the gamma parameter
        """
    def setRgb(self, rgb: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        """
        Set the rgb parameter
        """
class Square(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Square**
    
    .. include:: /nodes/spectrum/square.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> float:
        """
        Get the base parameter
        """
    def getMax(self) -> float:
        """
        Get the max parameter
        """
    def getMin(self) -> float:
        """
        Get the min parameter
        """
    def getTop(self) -> float:
        """
        Get the top parameter
        """
    def setBase(self, base: typing.SupportsFloat) -> bool:
        """
        Set the base parameter
        """
    def setMax(self, max: typing.SupportsFloat) -> bool:
        """
        Set the max parameter
        """
    def setMin(self, min: typing.SupportsFloat) -> bool:
        """
        Set the min parameter
        """
    def setTop(self, top: typing.SupportsFloat) -> bool:
        """
        Set the top parameter
        """
class Tabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Tabulated**
    
    .. include:: /nodes/spectrum/tabulated.rst
       :start-after: api-include-start
       :end-before: api-include-end
    """
    def __init__(self, name: str) -> None:
        ...
    def getData(self) -> dict:
        """
        Get the data parameter
        """
    def getRaw(self) -> numpy.typing.NDArray[numpy.float32]:
        ...
    def setData(self, data: dict) -> bool:
        """
        Set the data parameter
                Table is passed as a dict with this format:
        
                .. code-block:: python
        
                    table = {"wl": np.array(...), "val": np.array(...)}
        """
    def setRaw(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> bool:
        ...
class Triangle(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Triangle
    """
    def __init__(self, name: str) -> None:
        ...
    def getCenter(self) -> float:
        """
        Get the center parameter
        """
    def getMax(self) -> float:
        """
        Get the max parameter
        """
    def getMin(self) -> float:
        """
        Get the min parameter
        """
    def getTop(self) -> float:
        """
        Get the top parameter
        """
    def setCenter(self, center: typing.SupportsFloat) -> bool:
        """
        Set the center parameter
        """
    def setMax(self, max: typing.SupportsFloat) -> bool:
        """
        Set the max parameter
        """
    def setMin(self, min: typing.SupportsFloat) -> bool:
        """
        Set the min parameter
        """
    def setTop(self, top: typing.SupportsFloat) -> bool:
        """
        Set the top parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    **Uniform**
    
    .. include:: /nodes/spectrum/uniform.rst
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

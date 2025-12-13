from __future__ import annotations
import collections.abc
import numpy
import typing
from . import nodes
__all__: list[str] = ['All', 'CRawHandler', 'CRendererHandler', 'CServerHandler', 'Critcal', 'Debug', 'Default', 'Error', 'Image8bitInfo', 'Info', 'Licensing', 'None', 'Raw', 'Renderer', 'Server', 'Warning', 'getWorkDir', 'init', 'listOpenCLDevices', 'messageType', 'nodes', 'onMessage', 'setWorkDir', 'version']
class CRawHandler:
    def getPtr(self) -> int:
        """
        Return memory address of the underlying c ptr
        """
    def isIdentical(self, arg0: CRawHandler) -> bool:
        """
        Does this handler use the same C pointer 
        """
    def isValid(self) -> bool:
        """
        Does this handler uses a valid C pointer
        """
class CRendererHandler:
    def getPtr(self) -> int:
        """
        Return memory address of the underlying c ptr
        """
    def isIdentical(self, arg0: CRendererHandler) -> bool:
        """
        Does this handler use the same C pointer 
        """
    def isValid(self) -> bool:
        """
        Does this handler uses a valid C pointer
        """
class CServerHandler:
    def getPtr(self) -> int:
        """
        Return memory address of the underlying c ptr
        """
    def isIdentical(self, arg0: CServerHandler) -> bool:
        """
        Does this handler use the same C pointer 
        """
    def isValid(self) -> bool:
        """
        Does this handler uses a valid C pointer
        """
class Image8bitInfo:
    def __repr__(self) -> str:
        ...
    @property
    def alignment(self) -> int:
        ...
    @property
    def height(self) -> int:
        ...
    @property
    def stride(self) -> int:
        ...
    @property
    def succeed(self) -> bool:
        ...
    @property
    def width(self) -> int:
        ...
class Licensing:
    """
    
            Singleton Class to handle license 
            
            Aims to handle your Ocean's licence and configure how to retrieve it.
    
            Example:
    
            Ask ocean to get its license from your local server and run the server if it is not running
    
            .. code-block:: python
    
                from ocean import abyss
    
                autoStartServer = True # ask license server to start if it is not reachable
                liOpt=abyss.Licensing.Options.Client # license option
                licence=abyss.Licensing() # get license singleton
                licence.setNetworkMode(liOpt, "127.0.0.1", autoStartServer)
                #check the license
                licence.check()
    
                # The network server might takes some time to initialize
                # so wait for it
                n=0
                while n < 10:
                    if licence.isDemoMode():
                        print("Can't connect to license server, retrying...")
                        time.sleep(1)
                        licence.setNetworkMode(liOpt, "127.0.0.1", False)
                        licence.check()
                    else:
                        break
                    n+=1
                print(licence.lastErrorMessage()) # print error message if any
    
        
    """
    class Options:
        """
        Enumerator for licence options
        
        Members:
        
          None : No options
        
          Client : Client mode
        
          Server : Server mode
        
          All : All Options
        """
        All: typing.ClassVar[Licensing.Options]  # value = <Options.All: 3>
        Client: typing.ClassVar[Licensing.Options]  # value = <Options.Client: 1>
        None: typing.ClassVar[Licensing.Options]  # value = <Options.None: 0>
        Server: typing.ClassVar[Licensing.Options]  # value = <Options.Server: 2>
        __members__: typing.ClassVar[dict[str, Licensing.Options]]  # value = {'None': <Options.None: 0>, 'Client': <Options.Client: 1>, 'Server': <Options.Server: 2>, 'All': <Options.All: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    All: typing.ClassVar[Licensing.Options]  # value = <Options.All: 3>
    Client: typing.ClassVar[Licensing.Options]  # value = <Options.Client: 1>
    None: typing.ClassVar[Licensing.Options]  # value = <Options.None: 0>
    Server: typing.ClassVar[Licensing.Options]  # value = <Options.Server: 2>
    def __init__(self) -> None:
        ...
    def check(self) -> bool:
        """
        Check the license
        
                It will set license to demo if no license server found.
        
                Example:
        
                .. code-block:: python
        
                    license = abyss.Licensing() # get license singleton
                    license.check()
        
                .. note:: 
        
                    It returs True if license is found.
                    It returns True if license is not found but demo mode is allowed.
                    It returns False if license is not found and demo mode is not allowed.
        """
    def dongleKey(self) -> str:
        """
        Gets license dongle key as base64
        """
    def expiration(self) -> str:
        """
        Gets license expiration date
        """
    def hasDatakitFormat(self, arg0: str) -> bool:
        """
        Checks if license includes the specified datakit format
        """
    def hasOptions(self, options: Licensing.Options) -> bool:
        """
        Check if the license includes this :meth:`ocean.abyss.Licensing.Options`
        
                Example:
        
                .. code-block:: python
        
                    license=abyss.Licensing()
                    license.hasOptions(abyss.Licensing.Options.Server)
        
                .. warning::
        
                    Licensing has to be checked before using this. 
        """
    def info(self) -> str:
        """
        Gets license text
        
                 company name, etc...
        """
    def isDemoMode(self) -> bool:
        """
        Check if abyss runs in demo mode
        
                demoMode can be set automatically or with :meth:`ocean.abyss.licensing.setDemoMode`
        
                Example:
        
                .. code-block:: python
        
                    license = abyss.Licensing() # get license singleton
                    isInDemoMode = license.isDemoMode()
        """
    def isDemoModeAllowed(self) -> bool:
        """
        Check if demo mode is allowed
        
                Example:
        
                .. code-block:: python
                        
                    isDemoModeAllowed = abyss.Licensing().isDemoModeAllowed()
        """
    def lastErrorMessage(self) -> str:
        """
        Retrieves last license error message
        """
    def maxThreads(self) -> int:
        """
        Retrieves maximum working threads allowed by the license
        """
    def requireOptions(self, options: Licensing.Options) -> bool:
        """
        Requires the corresponding :meth:`ocean.abyss.Licensing.Options` for all subsequent renders
        
                .. warning::
        
                    Render will fail if the options are not included in the license.
        """
    def setDemoMode(self) -> None:
        """
        Switches abyss to demo mode 
        
                Example:
        
                .. code-block:: python
                    
                    license = abyss.Licensing() # get license singleton
                    license.setDemoMode()
        
                It will not require a license, but will add limitations such as adding watermarks on rendered images. 
        """
    def setDemoModeAllowed(self, arg0: bool) -> None:
        """
        Sets if demo mode is allowed. 
            
                Demo mode may be forbidden if you want to avoid rendering watermarked images when licensing fails
        
                Example:
        
                .. code-block:: python
        
                    license = abyss.Licensing() # get license singleton
                    #Disable demoMode    
                    license.setDemoModeAllowed(False)
                    #Enable demoMode
                    license.setDemoModeAllowed(True)
        """
    def setNetworkMode(self, opts: Licensing.Options, host: str = '127.0.0.1', auto_start: bool = True) -> None:
        """
        Switches abyss licensing to network license
        
                "Specifies a license server host or tells to auto start a local license server.
        """
class Raw(CRawHandler):
    """
            
            Aims to handle Ocean's outputs
    
            There is no explicit constructor for this class. You can only copy an existing :class:`abyss.Raw`,
            load one from file or get one from an abyss callback.
    
            Example:
    
            .. code-block:: python
    
                from ocean import *
                #load an ocraw
                aRaw = abyss.Raw.readOcraw("C:\\path\\to\\an\\ocraw.ocraw")
                #load a .exr as an ocraw
                aRaw = abyss.Raw.readOpenExr("C:\\path\\to\\an\\exr.exr")
                #copy
                aRawCopy = aRaw.copy()
    
                #get Raw from update callback
                renderer = abyss.Renderer()
                def onUpdate(raw: abyss.Raw):
                    # do something with the raw
        
                renderer.onUpdate(onUpdate)
                
            
    """
    class quantity:
        """
        Enumerator for raw quantities
        
        Members:
        
          Raw
        
          SensorIrradiance
        
          SceneRadiance
        
          SceneIrradiance
        
          SensorPower
        
          SensorExposure
        
          ComputedBSDF
        """
        ComputedBSDF: typing.ClassVar[Raw.quantity]  # value = <quantity.ComputedBSDF: 6>
        Raw: typing.ClassVar[Raw.quantity]  # value = <quantity.Raw: 0>
        SceneIrradiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SceneIrradiance: 3>
        SceneRadiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SceneRadiance: 2>
        SensorExposure: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorExposure: 5>
        SensorIrradiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorIrradiance: 1>
        SensorPower: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorPower: 4>
        __members__: typing.ClassVar[dict[str, Raw.quantity]]  # value = {'Raw': <quantity.Raw: 0>, 'SensorIrradiance': <quantity.SensorIrradiance: 1>, 'SceneRadiance': <quantity.SceneRadiance: 2>, 'SceneIrradiance': <quantity.SceneIrradiance: 3>, 'SensorPower': <quantity.SensorPower: 4>, 'SensorExposure': <quantity.SensorExposure: 5>, 'ComputedBSDF': <quantity.ComputedBSDF: 6>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    ComputedBSDF: typing.ClassVar[Raw.quantity]  # value = <quantity.ComputedBSDF: 6>
    Raw: typing.ClassVar[Raw.quantity]  # value = <quantity.Raw: 0>
    SceneIrradiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SceneIrradiance: 3>
    SceneRadiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SceneRadiance: 2>
    SensorExposure: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorExposure: 5>
    SensorIrradiance: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorIrradiance: 1>
    SensorPower: typing.ClassVar[Raw.quantity]  # value = <quantity.SensorPower: 4>
    @staticmethod
    def fromImageNode(data: str, size: typing.SupportsInt) -> Raw:
        """
        Creates an abyss raw from an \\"image\\" abyss node
        """
    @staticmethod
    def readOcraw(filename: str) -> Raw:
        """
        Reads an OCRAW file and returns the created handle
        
                Example:
        
                .. code-block:: python
        
                    aRawObject = abyss.Raw.readOcraw("/somewhere/ocean_raw.ocraw")
        """
    @staticmethod
    def readOpenExr(filename: str) -> Raw:
        """
        Reads an EXR file to an abyss raw and returns the created handle
        
                Example:
        
                .. code-block:: python
        
                    aRawObject = abyss.Raw.readOpenExr("/somewhere/ocean_raw.exr")
        """
    def SPP(self) -> float:
        """
        Returns samples per pixel average
        """
    def SPS(self) -> float:
        """
        Returns sample per second rate
        """
    def __repr__(self) -> str:
        ...
    def add(self, other: Raw) -> bool:
        """
        Merge result from other to this :class:`abyss.Raw`
        """
    def channelCount(self) -> int:
        """
        Returns the number of channels
        """
    def channelIndex(self, name: str) -> int:
        """
        Returns channel index by name or -1 if it doesn't exist
        """
    def channelName(self, idx: typing.SupportsInt) -> str:
        """
        Returns channel name by index
        """
    def channelResponse(self, idx: typing.SupportsInt) -> str:
        """
        Return the channel response type ("unknown", "energy", "luminous", "spectral")
        """
    def channelWavelength(self, idx: typing.SupportsInt) -> float:
        """
        Return the channel wavelength [m] for a spectral channel, zero otherwise
        """
    def copy(self) -> Raw:
        """
        Return a CHandler owning a copy of this CHandler C pointer
        """
    def filter(self, fast: bool = False) -> bool:
        """
        Applies output filters to an abyss raw
        
                Example:
        
                .. code-block:: python
        
                    aRaw.filter()
        """
    def getAutoRangeValue(self) -> float:
        """
        Returns the channel automatic range value
        """
    def getDefaultFormat(self) -> str:
        """
        Gets the default file format 
                
                \\"jpg\\", \\"exr\\", etc..., of the current output
        """
    def getImage8bit(self) -> numpy.ndarray:
        """
        Get the BGRA image as a numpy array
                        
                It follows the OpenCV memory layout: interleaved BGRA channels stored in row-major order. 
                It means that the shape of the numpy array is (height, width, 4).
        
                You can then directly call OpenCV methods on this numpy array.
        
                Example:
        
                .. code-block:: python
                
                    from ocean import *
                    import cv2
        
                    results = abyss.Raw.readOcraw("path/to/ocraw.ocraw")
        
                    img = results.getImage8bit()
                    cv2.imwrite("myImage.png", img)
        
                    # To get filtered image:
                    results.filter() # Apply Output filters
                    img = results.getImage8bit()
                    cv2.imwrite("myImageFiltered.png", img)
        
                If you need to write the ICC profile to your image, you can use pillow:
        
                .. code-block:: python
        
                    from PIL import Image
        
                    img = results.getImage8bit()
                    img_rgba = img[:, :, [2, 1, 0, 3]]
                    Image.fromarray(img_rgba).save("output_icc.png", icc_profile=results.getImage8bitProfile())
        
                .. note::
        
                    You have to call :meth:`ocean.abyss.Raw.filter` 
                    before calling this if you want the output filters to be applied (e.g: denoising, tone mapping, etc..)
        """
    def getImage8bitInfo(self) -> Image8bitInfo:
        """
        Retrieve memory info about the 8-bit image buffer
               
               Example:
        
               .. code-block:: python
        
                    from ocean import abyss
        
                    rawInfo = aRaw.getImage8bitInfo()
                    
                    if rawInfo.succeed:
                        print("Info :"rawInfo.width,rawInfo.height,rawInfo.stride,rawInfo.alignment)
                    else:
                        print(" is invalid (freed) or stride is negative or null ")
        """
    def getImage8bitProfile(self) -> bytes:
        """
        Retrieves the ICC profile corresponding to the output
        
                Example:
        
                .. code-block:: python
        
                    rawICCProfile = aRaw.getImage8bitProfile()
        """
    def getInstrument(self) -> bytes:
        """
        Gets the instrument associated with the raw buffer
        
                Instrument node is returned serialized, so you can write it as an ocbin file 
                or convert it to an abyss.node:
        
                Example:
        
                .. code-block:: python
        
                    instru = aRaw.getInstrument()
        
                    with open("instru.ocbin", "wb") as binary_file:
                        binary_file.write(instru)
        
                    # convert it to a abyss.nodes
                    scene = abyss.nodes.Scene("loader")
                    scene.readBytes(instru)
        
                    instru_node = scene.getNodes()[0]
        """
    def getInstrumentName(self) -> str:
        """
        Returns the instrument name
        """
    def getInstrumentOutput(self, idx: typing.SupportsInt) -> str:
        """
        Returns the instrument output's name by index
        
                An instrument may have multiple outputs presets or nullptr if index out of bounds
        """
    def getLightQuantity(self, chan: typing.SupportsInt, x: typing.SupportsInt, y: typing.SupportsInt, quantity: Raw.quantity) -> float:
        """
        Gets a light quantity for given channel, x/y position, and quantity
        
                Quantity is on of a :meth:`ocean.abyss.Raw.quantity` enumerator 
        """
    def getOutput(self) -> bytes:
        """
        Gets the output associated with the raw buffer
        
                Output node is returned serialized, so you can write it as an ocbin file:
        
                Example:
        
                .. code-block:: python
        
                    output = aRaw.getOutput()
        
                    with open("output.ocbin", "wb") as binary_file:
                        binary_file.write(output)
        """
    def getOutputFormat(self) -> list[str]:
        """
        Gets the file formats
        
                \\"jpg\\", \\"exr\\", etc..., supported 
        """
    def getOutputName(self) -> str:
        """
        Returns the current output name
        """
    def getQuantity(self, idx: typing.SupportsInt) -> Raw.quantity:
        """
        Get the nth quantity type provided by a raw buffer
        """
    def getQuantityCount(self) -> int:
        """
        Get the number of quantities provided by a raw buffer
        """
    def getUGR(self, x1: typing.SupportsInt, y1: typing.SupportsInt, x2: typing.SupportsInt, y2: typing.SupportsInt) -> float:
        """
        Returns Unified Glare Rating
                
                The coordinates values are clamped to image resolution.
        
                Example: For the UGR on the entire image:
                
                .. code-block:: python
        
                    ugr=aRaw.getUGR(0, 0, 1e100, 1e100)
        """
    def getXHeaderName(self, x: typing.SupportsInt) -> str:
        """
        Gets the result x header name for table views
        """
    def getYHeaderName(self, y: typing.SupportsInt) -> str:
        """
        Gets the result y header name for table views
        """
    def hasChannel(self, name: str) -> bool:
        """
        Returns true if a channel exists with given name
        """
    def hasMetaChannel(self, name: str) -> bool:
        """
        Returns true if a meta channel exists with this name ("variance", "spp", "snr", "depth")
        """
    def height(self) -> int:
        """
        Returns buffer height
        """
    def importOutput(self, other: Raw, output_name: str) -> bool:
        """
        Sets the output node to the 'raw' raw, from another 'other' raw and an output name
        """
    def isChannelEnergy(self, idx: typing.SupportsInt) -> bool:
        """
        Returns true if the channel by index has energy information
        """
    def isChannelLuminous(self, idx: typing.SupportsInt) -> bool:
        """
        Returns true if the channel by index has luminous information (photometric)
        """
    def isChannelSpectral(self, idx: typing.SupportsInt) -> bool:
        """
        Returns true if the channel by index has spectral information
        """
    def isCompatible(self, other: Raw) -> bool:
        """
        Returns true if the two raws can be merged (same size and channels)
        """
    def isDraft(self) -> bool:
        """
        Returns if the posprocessing is in draft mode
        """
    def metaPixels(self, name: str) -> numpy.ndarray:
        """
        Retrieves a copy of meta pixels data as a numpy array
        
                Shape is (width, height)
        
                Possible meta channels are:
        
                    - "variance" : the variance
                    - "spp" : samples per pixel
                    - "snr" : signal to noise ratio
                    - "depth" : distance [m] between camera optical center and first encounter surfaces
        """
    def pixels(self, quantity: Raw.quantity = Raw.quantity.quantity.Raw) -> numpy.ndarray:
        """
        Retrieves a copy of pixels data as a numpy array
        
                Shape is (width, height, channel)
        
                Number of channels depends on your sensor :
        
                    - CIE-XYZ: 3 channels (X, Y, Z)
                    - Spectral boxes: N channels, depends on your discretization (default: 41)
                    - Energy: 1 channel, E
        
                .. note::
        
                    For spectral boxes sensor you can retrieve the wavelength of a channel, using
                    :meth:`ocean.abyss.Raw.channelWavelength`
        
                Example:
        
                    .. code-block:: python
        
                        from ocean import *
        
                        results = abyss.Raw.readOcraw("path/to/ocraw.ocraw")
                        pixels = results.pixels()
                        print(pixels.shape)
        
                        # Assuming a spectral sensor is used, you can retrieve wavelength of each chan:
                        wavelengths = [ r.channelWavelength(i) for i in range(0, r.channelCount()) ]
        """
    def removeChannels(self) -> None:
        """
        Removes all channels from an abyss raw object
        
                Basically only the metadata is kept
        """
    def renderTime(self) -> float:
        """
        Returns render time in seconds
        """
    def setInstrument(self, data: str, size: typing.SupportsInt) -> bool:
        """
        Sets the instrument associated with the raw buffer
        
                Instrument node is passed serialized in a bytes object
        """
    def setOutput(self, data: str, size: typing.SupportsInt) -> bool:
        """
        Sets the output associated with the raw buffer
                
                Output node is passed serialized in a buffer
        """
    def width(self) -> int:
        """
        Returns buffer width
        """
    def writeAuto(self, filename: str) -> bool:
        """
        Write result to file
                
                Format is guessed from extension.
        
                Example:
        
                .. code-block:: python
        
                    aRaw.writeAuto("/somewhere/output.jpg")
        """
    def writeRaw(self, filename: str, format: str) -> bool:
        """
        Writes the raw buffer to a file using given format
                
                Possible formats:
        
                * ocraw
                * csv
                * exr
                * hdr
                
                Example:
        
                .. code-block:: python
        
                    aRaw.writeRaw("/somewhere/output.ocraw", "ocraw")
        """
    def writeResult(self, filename: str, format: str) -> bool:
        """
        Writes output result to a file in given format
                
                Possible formats:
        
                * Images
                    * jpg
                    * png
                    * exr
                    * hdr
                * Table
                    * csv
                * Glare report UGR (Unified Glare Rating)
                    * csv
                    * txt
                    * html
        
                Example:
        
                .. code-block:: python
        
                   aRaw.writeResult("/somewhere/output.jpeg", "jpg")
        """
    def writeResultBytes(self, format: str) -> bytes:
        """
        Writes output result to a stream in given format
        
                Possible formats:
        
                * Images
                    * jpg
                    * png
                    * exr
                    * hdr
                * Table
                    * csv
                * Glare report UGR (Unified Glare Rating)
                    * csv
                    * txt
                    * html
        """
class Renderer(CRendererHandler):
    """
     
            Create a Renderer object
    
            Example:
    
            .. code-block:: python
    
                from ocean import abyss, examples
                import time
        
                # ...
                # We suppose that license check and abyss initialization has been already done
    
                # Create a renderer
                localRenderer = abyss.Renderer()
                
                # configure renderer
                localRenderer.setParameter("num_threads", 4) # this renderer will use 4 threads
                abyssServer.setParameter("library_paths", OCLIB_PATH) # set path to material libraries
                localRenderer.setHaltCondition( time=0, spp=25, action=abyss.Renderer.halt_cond.stops)
                
                # define as a local renderer
                localRenderer.addLocalNode()
    
                # task to perform when renderer has finished
                finished = False
                def onFinishl(raw:abyss.Raw):
                    raw.writeAuto("cornellbox.png") #save results as a png
                    global finished
                    finished = True
    
                #start renderer
                localRenderer.start(examples["cornellbox"])
        
                # wait for renderer to finish
                while not finished:
                    time.sleep(2)
    
    
            Please refer to :ref:`tuto-network-rendering` for a more detailed usage.
    
        
    """
    class halt_cond:
        """
        Enumerator of actions to performed when halt condition (time, spp) has been reached
                    
                    .. note::
        
                        Each action triggers the :meth:`ocean.abyss.Renderer.onFinish` call back
                        even if using nochange action.
        
                
        
        Members:
        
          pauses
        
          stops
        
          nochange
        """
        __members__: typing.ClassVar[dict[str, Renderer.halt_cond]]  # value = {'pauses': <halt_cond.pauses: 0>, 'stops': <halt_cond.stops: 1>, 'nochange': <halt_cond.nochange: 2>}
        nochange: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.nochange: 2>
        pauses: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.pauses: 0>
        stops: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.stops: 1>
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class stat_type:
        """
        Enumerator of statistic value types
        
        Members:
        
          time : Elapsed rendering time
        
          samples : Number of samples
        
          spp : Samples per pixel
        
          spsaverage : Average samples per second
        
          spscurrent : Current samples per second
        
          wrongrate : Number of wrong (nan, inf, ...) samples per second
        
          halttime : Halt time condition
        
          haltspp : Halt sample per pixel condition
        """
        __members__: typing.ClassVar[dict[str, Renderer.stat_type]]  # value = {'time': <stat_type.time: 0>, 'samples': <stat_type.samples: 1>, 'spp': <stat_type.spp: 2>, 'spsaverage': <stat_type.spsaverage: 3>, 'spscurrent': <stat_type.spscurrent: 4>, 'wrongrate': <stat_type.wrongrate: 5>, 'halttime': <stat_type.halttime: 6>, 'haltspp': <stat_type.haltspp: 7>}
        haltspp: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.haltspp: 7>
        halttime: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.halttime: 6>
        samples: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.samples: 1>
        spp: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spp: 2>
        spsaverage: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spsaverage: 3>
        spscurrent: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spscurrent: 4>
        time: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.time: 0>
        wrongrate: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.wrongrate: 5>
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class state:
        """
        state of the renderer
        
        Members:
        
          idle
        
          running
        
          paused
        
          stopping
        """
        __members__: typing.ClassVar[dict[str, Renderer.state]]  # value = {'idle': <state.idle: 0>, 'running': <state.running: 1>, 'paused': <state.paused: 2>, 'stopping': <state.stopping: 3>}
        idle: typing.ClassVar[Renderer.state]  # value = <state.idle: 0>
        paused: typing.ClassVar[Renderer.state]  # value = <state.paused: 2>
        running: typing.ClassVar[Renderer.state]  # value = <state.running: 1>
        stopping: typing.ClassVar[Renderer.state]  # value = <state.stopping: 3>
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    haltspp: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.haltspp: 7>
    halttime: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.halttime: 6>
    idle: typing.ClassVar[Renderer.state]  # value = <state.idle: 0>
    nochange: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.nochange: 2>
    paused: typing.ClassVar[Renderer.state]  # value = <state.paused: 2>
    pauses: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.pauses: 0>
    running: typing.ClassVar[Renderer.state]  # value = <state.running: 1>
    samples: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.samples: 1>
    spp: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spp: 2>
    spsaverage: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spsaverage: 3>
    spscurrent: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.spscurrent: 4>
    stopping: typing.ClassVar[Renderer.state]  # value = <state.stopping: 3>
    stops: typing.ClassVar[Renderer.halt_cond]  # value = <halt_cond.stops: 1>
    time: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.time: 0>
    wrongrate: typing.ClassVar[Renderer.stat_type]  # value = <stat_type.wrongrate: 5>
    def __init__(self) -> None:
        ...
    def addLocalNode(self) -> None:
        """
        Adds a local render node
        
                Does not impact ongoing render. Will take effect at :meth:`ocean.abyss.Renderer.start`.
                Multiple local renderers can be used together
        """
    def addRemoteNode(self) -> None:
        """
        Adds a remote renderer
        
                Does not impact ongoing render. Will take effect at :meth:`ocean.abyss.Renderer.start`.
                It is requiered to previously set \\"remote_host\\" parameter using :meth:`ocean.abyss.Renderer.setParameter`
        """
    def clearNodes(self) -> None:
        """
        Removes all render nodes
        
                Does not impact ongoing render. Will take effect at :meth:`ocean.abyss.Renderer.start`.
        """
    def getStatistic(self, type: Renderer.stat_type) -> float:
        """
        Gets statistic values (spp, sps...).
        
                To avoid polling these values, set a notifier callback with :meth:`ocean.abyss.Renderer.onStatisticsUpdate`
        """
    def onChange(self, call_back: collections.abc.Callable[[Renderer.state], None]) -> None:
        """
        Sets a state changed callback.
                
                Removing the previous one if any.  The callback notifies when the renderer state changes between : Idle, Running, Paused, Stopping.
                Look at :meth:`ocean.abyss.Renderer.state` for the states list.
        """
    def onFinish(self, call_back: collections.abc.Callable[[Raw], None]) -> None:
        """
        Sets a render finished callback
        
                Removing the previous one if any.
        
                The callback notifies that render is finished passing a raw image.
        """
    def onMessage(self, call_back: collections.abc.Callable[[str, str, messageType], None]) -> None:
        """
        Sets a render message callback
                
                Removing the previous one if any.
        
                The callback notifies with log messages.
            
                 * First callback string parameter is the node path who emitted the message
                 * Second callback stringdoc parameter is the message itself
                 * Third parameter is the message level (see :meth:`oceanabyss.main.messageType`
        """
    def onStatisticsUpdate(self, call_back: collections.abc.Callable[[], None]) -> None:
        """
        Sets a render statistics callback
                
                Removing the previous one if any.
        
                The callback notifies periodycally with render performance statistics change.
                It does not pass statistics values, only notifies that they have been updated
        
                Use :meth:`ocean.abyss.Renderer.getStatistic` to get values.
        """
    def onUpdate(self, call_back: collections.abc.Callable[[Raw], None]) -> None:
        """
        Sets an update callback
                
                Removing the previous one if any.
        
                The callback notifies intermediate render results, passing a raw image.
        """
    def setHaltCondition(self, time: typing.SupportsFloat, spp: typing.SupportsFloat, action: Renderer.halt_cond) -> None:
        """
        Sets the halt condition
        
                 * time : halt time in seconds. Zero or negative value disables time halt condition
                 * spp : sample per pixes. Zero or negative value disables spp halt condition
                 * action : changes if halt stops or pauses render (or doesn't change it)
        
                This can be called before or during a render.
        """
    @typing.overload
    def setParameter(self, name: str, value: str) -> None:
        """
        Sets a renderer parameter
        
                Supported parameters: (list may not be up to date)
        
                 * \\"library_paths\\" : semicolon separated list of path to get oclibs from (for local renderers only)
                 * \\"setup\\" : the name of the setup to render in scene file
                 * \\"output_file_name\\" : path to final render saved file. Extension may be omitted or \\".auto\\" to let abyss choose one
                 * \\"local_remote_server\\" : instead of connecting to a remote server, creates a local server and connects to it (see :meth:`ocean.abyss.Renderer.addRemoteNode`)
                 * \\"output_raw\\" : \\"true\\" or \\"false\\", save final render to raw instead of using output node
                 * \\"remote_host\\" : address of abyss server to connect to
        
                .. note::
                
                    setParameter must be used before :meth:`ocean.abyss.Renderer.addLocalNode` and :meth:`ocean.abyss.Renderer.addRemoteNode` to take effect
                
                Example:
        
                .. code-block:: python
        
                    from ocean import abyss, OCLIB_PATH
        
                    renderer = abyss.Renderer()
                    renderer.setParameter("library_paths", OCLIB_PATH)
        """
    @typing.overload
    def setParameter(self, name: str, value: typing.SupportsInt) -> None:
        """
        Sets a renderer parameter
        
                Supported parameters: (list may not be up to date)
        
                 * \\"num_threads\\" : number of simulation threads (for local renderers only)
        
                .. note::
                
                    setParameter must be used before :meth:`ocean.abyss.Renderer.addLocalNode` and :meth:`ocean.abyss.Renderer.addRemoteNode` to take effect
                
                Example:
        
                .. code-block:: python
        
                    from ocean import abyss
        
                    renderer = abyss.Renderer()
                    renderer.setParameter("num_threads", 4)
        """
    @typing.overload
    def start(self, file_name: str) -> bool:
        """
        Start render from file
        
                File name must be relative to working directory for network rendering.
        
                Returns false if starting is not possible
        """
    @typing.overload
    def start(self, scene: ...) -> bool:
        """
        Start render from Scene object
        
                Returns false if starting is not possible
        
                .. warning::
        
                    This method can't be used for network rendering.
        """
    @typing.overload
    def startData(self, data: str, size: typing.SupportsInt) -> bool:
        """
        Start render from an ocxml or ocbin buffer
        
                Returns false if starting is not possible
        
                .. warning::
        
                    This method can't be used for network rendering.
        """
    @typing.overload
    def startData(self, file_obj: typing.Any) -> bool:
        """
        Start render from an ocxml or ocbin buffer
        
        Accepts any Python file-like object (StringIO, BytesIO, or an open file).
        Rewinds to the beginning before reading.
        Returns false if starting is not possible.
        
                .. warning::
        
                    This method can't be used for network rendering.
        """
    def stop(self) -> None:
        """
        Stops this renderer
                
                Does nothing if no rendering is in progress.
        """
    def togglePause(self, paused: bool) -> bool:
        """
        Pauses/unpauses a render
        
                Returns false if resuming is not possible.
        """
    def updateRaw(self) -> None:
        """
        Forces an update of the intermediate result
        
                Will likely trigger an update callback set with :meth:`ocean.abyss.Renderer.onUpdate`
        """
class Server(CServerHandler):
    """
    
            Create a Server object
    
            Aims to handle server rendering.
    
            It allows to create a renderer worker which wait for jobs, listening to a TCP port. Look at client 
            server rendering tutorial for usage.
        
    """
    def __init__(self) -> None:
        ...
    def close(self) -> None:
        """
        Stops the server from listening on a port.Returns when the port is actually closed
        """
    def onBusyStateChange(self, call_back: collections.abc.Callable[[bool], None]) -> None:
        """
        Sets a callback function for getting notifications on the server state
                
                Removing the previous one if any.
                Callback function is called with the server becomes busy(true) or available(false)
        """
    def open(self, port: typing.SupportsInt) -> int:
        """
        Opens the given port on a server
        
                This function is blocking and will return when the the server ready to listen or an error occured
                It may choose another port if either 0 is passed, or if the port is not available
                The function returns the open port or 0 if the server is not listening on any port
                If the server was already listening on a port, function does nothing and returns the open port
        """
    def openAsync(self, port: typing.SupportsInt) -> None:
        """
        Opens the given port on a server
        
                This will do nothing is the server already has an open port
                This function is asynchronous and will return before the server is listerning
                It may choose another port if either 0 is passed, or if the port is not available
        """
    def sendMessage(self, msg: str, type: typing.SupportsInt, name: str = 'server') -> None:
        """
        Sends a message to the client connected to this server
        
                This allows seeing server render log on the master
        """
    def setParameter(self, name: str, value: str) -> None:
        """
         Sets a server parameter
        
                Current parameters: (list may not be up to date)
                 - "num_threads" : number of simulation threads
                 - "library_paths" : semicolon separated list of path to get oclibs from
        """
class messageType:
    """
    Enumerator for message log level
    
    Members:
    
      None : no type
    
      Debug : Debug only 
    
      Info : Info only
    
      Warning : Warning only
    
      Error : Error only
    
      Critcal : Critcal only
    
      All : All types
    
      Default : Info Warning and Error
    """
    All: typing.ClassVar[messageType]  # value = <messageType.All: 63>
    Critcal: typing.ClassVar[messageType]  # value = <messageType.Critcal: 32>
    Debug: typing.ClassVar[messageType]  # value = <messageType.Debug: 2>
    Default: typing.ClassVar[messageType]  # value = <messageType.Default: 60>
    Error: typing.ClassVar[messageType]  # value = <messageType.Error: 16>
    Info: typing.ClassVar[messageType]  # value = <messageType.Info: 4>
    None: typing.ClassVar[messageType]  # value = <messageType.None: 0>
    Warning: typing.ClassVar[messageType]  # value = <messageType.Warning: 8>
    __members__: typing.ClassVar[dict[str, messageType]]  # value = {'None': <messageType.None: 0>, 'Debug': <messageType.Debug: 2>, 'Info': <messageType.Info: 4>, 'Warning': <messageType.Warning: 8>, 'Error': <messageType.Error: 16>, 'Critcal': <messageType.Critcal: 32>, 'All': <messageType.All: 63>, 'Default': <messageType.Default: 60>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def getWorkDir() -> str:
    """
    Get the current working directory
    """
def init(ocl_support: bool = False, ocl_device: str = '') -> bool:
    """
    Initialize abyss
    
            Call this to initialize abyss, You can enable OpenCL here and choose the OpenCL device by its name
            
            To retrieve your opencl device(s) name(s) and use the first in the list proceed as follow:
    
            .. code-block:: python
    
                from ocean import abyss
                
                devices = abyss.listOpenCLDevices()
                if len(devicename) > 0:
                    print("Initialize Abyss with Opencl Device: ", devicename[0])
                    abyss.init(ocl_device=devicename[0], ocl_support=True)
                else:
                    abyss.init()
    
            .. note::
                    Opencl is only used when post processing outputs. (image denoiser, human vision filters, ...)
    """
def listOpenCLDevices() -> list[str]:
    """
    Get available OpenCL Devices in a list
    
                Example:
    
                .. code-block:: python
    
                    from ocean import abyss
    
                    devices = abyss.listOpenCLDevices()
    """
def onMessage(call_back: collections.abc.Callable[[str, messageType], None]) -> None:
    """
    Sets the global message callback
            
            All messages sent by abyss are handle via this user defined call_back function.
    
             * First callback string parameter is the message
             * Second parameter is the :meth:`ocean.abyss.messageType` log level type"
    
            Example:
    
            .. code-block:: python
    
                def onMessage(msg, msg_type):
                    if msg_type > abyss.messageType.Info:
                        #print Warning and Error only
                        print(msg)
    
                abyss.onMessage(onMessage)
    
            .. note::
    
                If a callback has already been defined, then calling :meth:`ocean.abyss.onMessage` again will
                replace the previous one by the new one provided.
    """
def setWorkDir(work_dir: str) -> None:
    """
    Sets the current working directory
            
            Example:
    
            .. code-block:: python
    
                abyss.setWorkDir("/path/to/a/folder")
    
            .. warning::
                For network rendering scene files must be on the same path relative to working directory on every node.
    """
def version() -> str:
    """
    Gets the full version of abyss
            
            .. code-block:: python
    
                from ocean import abyss
    
                abyss.version() # e.g: \\"Ocean 2022 R8 (10.2.8-39ec4694adeb)\\"
    """
All: messageType  # value = <messageType.All: 63>
Critcal: messageType  # value = <messageType.Critcal: 32>
Debug: messageType  # value = <messageType.Debug: 2>
Default: messageType  # value = <messageType.Default: 60>
Error: messageType  # value = <messageType.Error: 16>
Info: messageType  # value = <messageType.Info: 4>
None: messageType  # value = <messageType.None: 0>
Warning: messageType  # value = <messageType.Warning: 8>

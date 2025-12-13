from __future__ import annotations
import collections.abc
import numpy
import numpy.typing
import ocean.abyss.nodes
import typing
__all__: list[str] = ['CGeomHandler', 'Cone', 'Geometry', 'Mesh', 'Sphere']
class CGeomHandler:
    def getPtr(self) -> int:
        """
        Return memory address of the underlying c ptr
        """
    def isIdentical(self, arg0: CGeomHandler) -> bool:
        """
        Does this handler use the same C pointer 
        """
    def isValid(self) -> bool:
        """
        Does this handler uses a valid C pointer
        """
class Cone(Geometry, CGeomHandler):
    @typing.overload
    def __init__(self, arg0: str, arg1: typing.SupportsFloat, arg2: bool) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str, arg1: typing.SupportsFloat) -> None:
        ...
    def getReverse(self) -> bool:
        """
        Does the normals are inverted
        """
    def getRtop(self) -> float:
        ...
    def setReverse(self, arg0: bool) -> bool:
        """
        Reverse the normals (True|False)
        """
    def setRtop(self, arg0: typing.SupportsFloat) -> bool:
        ...
class Geometry(CGeomHandler):
    def __repr__(self) -> str:
        ...
    def addLayerRef(self, arg0: typing.SupportsInt, arg1: collections.abc.Sequence[str]) -> None:
        """
        Add this geometry to a layer
        """
    def copy(self) -> Geometry:
        """
        Create a copy of this geom
        """
    def getMaterial(self) -> ocean.abyss.nodes.Node:
        """
        Retrieve the associated material
        """
    def getMaterialName(self) -> str:
        """
        Retrieve the associated material name
        """
    def name(self) -> str:
        """
        Retrieve the geometry name
        """
    def numPrimitives(self) -> int:
        """
        Retrieve the number of primitives
        """
    def print(self) -> str:
        """
        Return the node as an ocxml string
        """
    @typing.overload
    def setMaterial(self, arg0: str) -> None:
        """
        Associate a material named 'name' to this mesh
        """
    @typing.overload
    def setMaterial(self, arg0: ocean.abyss.nodes.Node) -> None:
        """
        Associate a material to this mesh
        """
    def setName(self, arg0: str) -> None:
        """
        Set the geometry name
        """
    def typeName(self) -> str:
        """
        Get the geometry type 'mesh', 'sphere' or 'cone'
        """
    def write(self, file: typing.Any) -> None:
        """
        Write data to a python file object
        """
class Mesh(Geometry, CGeomHandler):
    def __init__(self, name: str, vertices: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], normals: typing.Annotated[numpy.typing.ArrayLike, numpy.float32], triangles: typing.Annotated[numpy.typing.ArrayLike, numpy.int32], uvs: typing.Annotated[numpy.typing.ArrayLike, numpy.float32] = ..., mat_indices: typing.Annotated[numpy.typing.ArrayLike, numpy.int32] = ...) -> None:
        ...
    def copy(self) -> Mesh:
        """
        Create a copy of this mesh
        """
    def getTriangleNormals(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Retrieve the triangle normals as a numpy array
        """
    def getTriangles(self) -> numpy.typing.NDArray[numpy.int32]:
        """
        Retrieve the triangles indices as a numpy array
        """
    def getUvs(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Retrieve the uvs as a numpy array
        """
    def getVertexNormals(self) -> numpy.typing.NDArray[numpy.float32]:
        """
        Retrieve the vertex normals as a numpy array
        """
    def getVertices(self) -> numpy.typing.NDArray[numpy.float64]:
        """
        Retrieve the vertices as a numpy array
        """
class Sphere(Geometry, CGeomHandler):
    def __init__(self, name: str, radius: typing.SupportsFloat, reverse: bool = False) -> None:
        """
        Build a Sphere with its name, its radius [m] and reverse which inverse normals if set to true
        """
    def getRadius(self) -> float:
        """
        Retrieve the sphere radius [m]
        """
    def getReverse(self) -> bool:
        """
        Does the normals are inverted
        """
    def setRadius(self, arg0: typing.SupportsFloat) -> bool:
        """
        Set the sphere radius [m]
        """
    def setReverse(self, arg0: bool) -> bool:
        """
        Reverse the normals (True|False)
        """

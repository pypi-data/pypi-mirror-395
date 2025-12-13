from __future__ import annotations
import math as math
import numpy as np
import numpy
from ocean import abyss
import ocean.abyss.nodes
from ocean.utils import matrix
from ocean.utils import misc
__all__: list[str] = ['abyss', 'fromOcean', 'loadModel', 'math', 'matrix', 'misc', 'np', 'toOcean', 'toPyRenderCams', 'toPyrenderMeshes', 'toTriMeshes']
def __printHelp():
    """
    _summary_
        
        :meta: private
        
    """
def fromOcean(oScene: ocean.abyss.nodes.Scene, map: numpy.array = None):
    """
    Convert an Ocean scene to a pyrender one.
    
        :param oScene: an Ocean scene
        :type oScene: abyss.nodes.Scene
        :param map: an image to apply as a map to each mesh, defaults to None
        :type map: np.array, optional
        :return: the converted scene
        :rtype: pyrender.Scene
        
    """
def loadModel(filename: str):
    """
    Loads triangular meshes from a file.
    
        :param filename: Path to the mesh file. (.stl, .obj, .glb, .gltf, ...)
        :type filename: str
        :return: The meshes loaded from the file.
        :rtype: [trimesh.base.Trimesh]
        
    """
def toOcean(tmesh):
    """
    Convert a triMesh Mesh to an Ocean one.
        
        :param tmesh: The triMesh to convert to Ocean
        :type tmesh: :class:`trimesh.Trimesh`
        :return: the equivalent Ocean Mesh 
        :rtype: :class:`abyss.nodes.geometries.Mesh`
        
    """
def toPyRenderCams(scene: ocean.abyss.nodes.Scene):
    """
    Convert all cameras in an Ocean scene to pyrender cameras.
    
        :param scene: Ocean's Scene
        :type scene: :class:`abyss.nodes.Scene`
        :return: Meshes loaded from the file.
        :rtype: dict with cam name as key and value : { obj: :class:`pyrender.camera.PerspectiveCamera`, trans: :class:`numpy.array`, res: :class:`numpy.array`} 
        
    """
def toPyrenderMeshes(oScene: ocean.abyss.nodes.Scene, triMeshes: dict):
    """
    Convert all Ocean meshes in a scene to pyrender meshes.
    
        :param oScene: an Ocean scene
        :type oScene: abyss.nodes.Scene
        :param triMeshes: dict of trimeshes converted using toTriMeshes function
        :type triMeshes: dict
        :return: the list of pyrender meshes
        :rtype:  list of pyrender.Mesh
        
    """
def toTriMeshes(oScene: ocean.abyss.nodes.Scene, map: numpy.array = None):
    """
    Convert meshes from an Ocean scene to trimeshes ones.
    
        :param oScene: an Ocean scene
        :type oScene: abyss.nodes.Scene
        :param map: an image to apply as a map to each mesh, defaults to None
        :type map: np.array, optional
        :return: dict with key being mesh name and value the trimesh
        :rtype: dict
        
    """

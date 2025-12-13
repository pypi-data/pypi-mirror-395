import math
import numpy as np
from . import matrix
from . import misc
from .. import abyss

def __printHelp():
    """_summary_
    
    :meta: private
    """
    msg="\t> pip install '\"eclatdigital_ocean\"[utils]'"
    print("This function requieres Ocean trimesh extra package. Install it with:")
    print(msg)

def loadModel(filename:str):
    """Loads triangular meshes from a file.

    :param filename: Path to the mesh file. (.stl, .obj, .glb, .gltf, ...)
    :type filename: str
    :return: The meshes loaded from the file.
    :rtype: [trimesh.base.Trimesh]
    """

    if not misc.module_exists("trimesh"):
        __printHelp()
        return
    import trimesh
    meshes = trimesh.load(filename)
    # If we got a scene, dump the meshes
    if isinstance(meshes, trimesh.Scene):
        print(meshes.camera)
        meshes = list(meshes.dump())
        meshes = [g for g in meshes if isinstance(g, trimesh.Trimesh)]
    if isinstance(meshes, (list, tuple, set)):
        meshes = list(meshes)
        if len(meshes) == 0:
            raise ValueError('At least one mesh must be present in file')
        for r in meshes:
            if not isinstance(r, trimesh.Trimesh):
                raise TypeError('Could not load meshes from file')
    elif isinstance(meshes, trimesh.Trimesh):
        meshes = [meshes]
    else:
        raise ValueError('Unable to load mesh from file')
    return meshes

def toOcean(tmesh):
    """Convert a triMesh Mesh to an Ocean one.
    
    :param tmesh: The triMesh to convert to Ocean
    :type tmesh: :class:`trimesh.Trimesh`
    :return: the equivalent Ocean Mesh 
    :rtype: :class:`abyss.nodes.geometries.Mesh`
    """
    
    uv = np.array([])
    if hasattr(tmesh, 'visual') and hasattr(tmesh.visual, 'uv') and tmesh.visual.uv is not None:
        uv = np.array(tmesh.visual.uv.tolist(), dtype=np.float32)

    meshName = "unnamed"
    if "node" in tmesh.metadata.keys():
        meshName = tmesh.metadata["node"]
    elif "file_name" in tmesh.metadata.keys():
        meshName = tmesh.metadata["file_name"]
    tmesh.metadata["node"] = meshName

    omesh = abyss.nodes.geometries.Mesh(
        meshName,
        vertices=np.array(tmesh.vertices.tolist(), dtype=np.double),
        normals=np.array(tmesh.vertex_normals.tolist(), dtype=np.float32),
        triangles=np.array(tmesh.faces.tolist(), dtype=np.int32),
        uvs=uv
    )
    return omesh

def toPyRenderCams(scene: abyss.nodes.Scene):
    """Convert all cameras in an Ocean scene to pyrender cameras.

    :param scene: Ocean's Scene
    :type scene: :class:`abyss.nodes.Scene`
    :return: Meshes loaded from the file.
    :rtype: dict with cam name as key and value : { obj: :class:`pyrender.camera.PerspectiveCamera`, trans: :class:`numpy.array`, res: :class:`numpy.array`} 
    """

    if not misc.module_exists("pyrender"):
        __printHelp()
        return
    import pyrender

    ocean_cams: list[abyss.nodes.instrument.Idealrectcam] = scene.findNodes(type_name="idealrectcam")
    cams = {}
    for ocean_cam in ocean_cams:
        pyr_cam = pyrender.camera.PerspectiveCamera(
            name=ocean_cam.name(),
            yfov= 2 * math.atan(0.5 * ocean_cam.getSensor_width() / (ocean_cam.getSensor_ar() * ocean_cam.getFocallength())),
            aspectRatio=ocean_cam.getSensor_ar())
        extrinsinc_mat = matrix.composeFwdUpPos(
            ocean_cam.getPos(),
            ocean_cam.getForwards(),
            ocean_cam.getUp()
        )
        cams[ocean_cam.name()] = {"obj": pyr_cam,
                                "trans": extrinsinc_mat,
                                "res": [ocean_cam.getXresolution(), ocean_cam.getYresolution()]}
    return cams

def toPyrenderMeshes(oScene: abyss.nodes.Scene, triMeshes: dict ):
    """Convert all Ocean meshes in a scene to pyrender meshes.

    :param oScene: an Ocean scene
    :type oScene: abyss.nodes.Scene
    :param triMeshes: dict of trimeshes converted using toTriMeshes function
    :type triMeshes: dict
    :return: the list of pyrender meshes
    :rtype:  list of pyrender.Mesh
    """

    if not misc.module_exists("progressbar"):
        __printHelp()
        return
    import progressbar
    if not misc.module_exists("pyrender"):
        __printHelp()
        return
    import pyrender

    widgets = ['Adding instances ' + oScene.name(), ' ', progressbar.Bar(
    ), ' ',  progressbar.Percentage(), ' ', progressbar.Timer()]
    pbar = progressbar.ProgressBar(widgets=widgets, term_width=100)
    instances = oScene.getInstances()
    pbar.maxval = len(instances)
    pbar.start()
    pbar_idx = 0
    stats = {"instances": 0}
    extracted_instances = {}
    for inst in instances:
        pbar_idx += 1
        ocean_mesh_name = inst.geometryName()
        instances = []
        if ocean_mesh_name in triMeshes:
            if ocean_mesh_name in extracted_instances:
                extracted_instances[ocean_mesh_name]["trans"] = np.concatenate(
                    (extracted_instances[ocean_mesh_name]["trans"], [inst.getTransform()]))
            else:
                extracted_instances[ocean_mesh_name] = {
                    "mesh": triMeshes[ocean_mesh_name],
                    "trans": np.array([inst.getTransform()])
                }
        else:
            print("Instance has non existing mesh: ", ocean_mesh_name)
        pbar.update(pbar_idx)
    pyr_meshes = []
    for mesh_name in triMeshes.keys():
        if mesh_name in extracted_instances:
            stats["instances"] += 1
            pyr_meshes.append(pyrender.Mesh.from_trimesh(
                extracted_instances[mesh_name]["mesh"], poses=extracted_instances[mesh_name]["trans"]))
        else:
            # add meshes that are not related to instances
            pyr_meshes.append(
                pyrender.Mesh.from_trimesh(triMeshes[mesh_name]))
    pbar.finish()
    print(stats)
    return pyr_meshes
        
def toTriMeshes(oScene: abyss.nodes.Scene, map: np.array = None):
    """Convert meshes from an Ocean scene to trimeshes ones.

    :param oScene: an Ocean scene
    :type oScene: abyss.nodes.Scene
    :param map: an image to apply as a map to each mesh, defaults to None
    :type map: np.array, optional
    :return: dict with key being mesh name and value the trimesh
    :rtype: dict
    """

    if not misc.module_exists("trimesh"):
        __printHelp()
        return
    import trimesh
    if not misc.module_exists("progressbar"):
        __printHelp()
        return
    import progressbar
    
    widgets = ['Extracting meshes ' + oScene.name(), ' ', progressbar.Bar(
    ), ' ',  progressbar.Percentage(), ' ', progressbar.Timer()]
    pbar = progressbar.ProgressBar(widgets=widgets, term_width=100)
    ocean_loaded_meshes = oScene.getGeometries()
    ocean_geom_names = [g.name() for g in ocean_loaded_meshes]
    ocean_geom_dict = dict(zip(ocean_geom_names, ocean_loaded_meshes))
    pbar.maxval = len(ocean_loaded_meshes)
    pbar_idx = 0
    pbar.start()
    tri_meshes = {}
    stats = {"vertices": 0, "triangles": 0, "meshes": len(ocean_loaded_meshes)}
    for name, o_mesh in ocean_geom_dict.items():
        pbar_idx += 1
        if isinstance(o_mesh, abyss.nodes.geometries.Mesh):
            stats["vertices"] += len(o_mesh.getVertices())
            stats["triangles"] += len(o_mesh.getTriangles())
            tri_mesh = trimesh.Trimesh(
                vertices=o_mesh.getVertices(),
                faces=o_mesh.getTriangles(),
                face_normals=o_mesh.getTriangleNormals(),
                vertex_normals=o_mesh.getVertexNormals(),
                metadata={"name": o_mesh.name(), "node": o_mesh.name(), "processed": False},
                process=False
            )
            if map is not None:
                uvs = o_mesh.getUvs()
                if len(uvs) != 0:
                    # with PIL.Image.open(os.path.join("..", "_static", "uvs_checker.jpg")) as pil_img:
                    # map = np.asarray(pil_img)
                    material = trimesh.visual.material.SimpleMaterial(
                        image=map)
                    tri_mesh.visual = trimesh.base.TextureVisuals(
                        uv=uvs, image=map, material=material)
            tri_meshes[name] = tri_mesh
        elif isinstance(o_mesh, abyss.nodes.geometries.Sphere):
            radius = o_mesh.getRadius()
            tri_meshes[name] = trimesh.primitives.Sphere(radius)
        else:
            print("WARNING; unhandled ocean's geom\nname: ",
                o_mesh.name(), "\ntype:", o_mesh.__class__)
            continue
        pbar.update(pbar_idx)
    pbar.finish()
    print(stats)
    return tri_meshes

def fromOcean(oScene: abyss.nodes.Scene, map: np.array = None):
    """Convert an Ocean scene to a pyrender one.

    :param oScene: an Ocean scene
    :type oScene: abyss.nodes.Scene
    :param map: an image to apply as a map to each mesh, defaults to None
    :type map: np.array, optional
    :return: the converted scene
    :rtype: pyrender.Scene
    """

    if not misc.module_exists("pyrender"):
        __printHelp()
        return
    import pyrender

    pyrScene = pyrender.Scene()
    triMeshes = toTriMeshes(oScene, map)
    if len(triMeshes) != 0:
        pyrInstances = toPyrenderMeshes(oScene, triMeshes)
    else:
        print("No Ocean's meshes found in this file")
        return pyrScene
    
    for inst in pyrInstances:
        pyrScene.add(inst)
    return pyrScene

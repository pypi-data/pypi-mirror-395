import math
import numpy

def decomposeFwdUpPos(mat4x4: numpy.array):
    """Decompose a 4x4 transform matrix to forward, up, pose vectors

    :type mat4x4: numpy.array
    :return: a dict  {"forward": numpy.array, "up": numpy.array, "pose": numpy.array}
    :rtype: dict
    """

    trans4x3 = numpy.delete(mat4x4, 3, 0)
    forward = -trans4x3[:, -2]
    forward = forward/numpy.linalg.norm(forward)
    up = trans4x3[:, -3]
    up = up/numpy.linalg.norm(up)
    return {
        "forward": forward,
        "up": up,
        "pose": trans4x3[:, -1],
    }
def composeFwdUpPos(pose: numpy.array, fwd: numpy.array, up: numpy.array):
    """Compose  pose, forward and up vectors to a 4x4 transform matrix

    :param pose:  the pose vector
    :type pose: numpy.array
    :param fwd: the forward vector
    :type fwd: numpy.array
    :param up: the up vector
    :type up: numpy.array
    :return: The corresponding 4x4 transform matrix
    :rtype: numpy.array
    """

    _up = up
    _fwd = -fwd
    _fwd /= numpy.linalg.norm(_fwd)
    _up /= numpy.linalg.norm(_up)
    right = numpy.cross(_up, _fwd)
    right = right / numpy.linalg.norm(right)
    return numpy.array([
        [right[0], _up[0], _fwd[0], pose[0]],
        [right[1], _up[1], _fwd[1], pose[1]],
        [right[2], _up[2], _fwd[2], pose[2]],
        [0,      0,       0,       1]
    ], dtype="float32")
def decompose(mat4x4: numpy.array):
    """ Decompose a 4x4 matrix to position, rotation and scale

        :param mat4x4:  the 4x4 matrix

        :return: a dict with "position" "rotation" and "scale"

    """

    err = {
        "position": numpy.array([0,0,0]),
        "rotation": numpy.eye(3),
        "scale": numpy.array([1,1,1])
        } 
    if len(mat4x4.shape)!=2:
        print("decompose: mat4x4 has to be a 4x4 matrix")
        return err
    if mat4x4.shape[0] != 4 or mat4x4.shape[1] != 4:
        print("decompose: mat4x4 has to be a 4x4 matrix")
        return err

    scale = numpy.array([1,1,1])
    scale[0] = math.sqrt( mat4x4[0][0]**2 + mat4x4[1][0]**2 + mat4x4[2][0]**2) #sx
    scale[1] = math.sqrt( mat4x4[0][1]**2 + mat4x4[1][1]**2 + mat4x4[2][1]**2) #sy
    scale[2] = math.sqrt( mat4x4[0][2]**2 + mat4x4[1][2]**2 + mat4x4[2][2]**2) #sz

    det = numpy.linalg.det(mat4x4)    

    if det < 0 :
        scale[0] = - scale[0]

    position = numpy.array([0,0,0])
    position[0] = mat4x4[0][3]
    position[1] = mat4x4[1][3]
    position[2] = mat4x4[2][3]

    invScale = 1/scale

    rotation = numpy.array([[mat4x4[0][0]*invScale[0], mat4x4[0][1]*invScale[1], mat4x4[0][2]*invScale[2]],
                            [mat4x4[1][0]*invScale[0], mat4x4[1][1]*invScale[1], mat4x4[1][2]*invScale[2]],
                            [mat4x4[2][0]*invScale[0], mat4x4[2][1]*invScale[1], mat4x4[2][2]*invScale[2]]])

    return {
        "position": position,
        "rotation": rotation,
        "scale": scale
    }
def compose(position: numpy.array = numpy.array([0,0,0]), rotation: numpy.array = numpy.eye(3), scale = numpy.array([1,1,1])):
    """ Create a 4x4 transformation matrix from position, rotation and scale

    :param position: The translation vector, defaults to numpy.array([0,0,0])
    :type position: numpy.array, optional
    :param rotation: The rotation matrix, defaults to numpy.eye(3)
    :type rotation: numpy.array, optional
    :param scale: The scale vector, defaults to numpy.array([1,1,1])
    :type scale: numpy.array, optional
    :return: The 4x4 matrix
    :rtype: numpy.array
    """
    
    err = numpy.eye(4)
    if position.shape[0] != 3 or len(position.shape) != 1:
        print("compose: position has to be a vector of len 3")
        return err
    if scale.shape[0] != 3 or len(scale.shape) != 1:
        print("compose: scale has to be a vector of len 3")
        return err
    shape = rotation.shape
    if len(shape)!=2:
        print("compose: rotation has to be a 3x3 matrix")
        return err  
    if shape[0] != 3 or shape[1] != 3:
        print("compose: rotation has to be a 3x3 matrix")
        return err
    
    return numpy.array([
        [rotation[0][0]*scale[0],rotation[0][1]*scale[1],rotation[0][2]*scale[2], position[0]],
        [rotation[1][0]*scale[0],rotation[1][1]*scale[1],rotation[1][2]*scale[2], position[1]],
        [rotation[2][0]*scale[0],rotation[2][1]*scale[1],rotation[2][2]*scale[2], position[2]],
        [0,0,0,1]
        ]
    )

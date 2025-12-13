from __future__ import annotations
import math as math
import numpy as numpy
__all__: list[str] = ['compose', 'composeFwdUpPos', 'decompose', 'decomposeFwdUpPos', 'math', 'numpy']
def compose(position: numpy.array = ..., rotation: numpy.array = ..., scale = ...):
    """
    Create a 4x4 transformation matrix from position, rotation and scale
    
    :param position: The translation vector, defaults to numpy.array([0,0,0])
    :type position: numpy.array, optional
    :param rotation: The rotation matrix, defaults to numpy.eye(3)
    :type rotation: numpy.array, optional
    :param scale: The scale vector, defaults to numpy.array([1,1,1])
    :type scale: numpy.array, optional
    :return: The 4x4 matrix
    :rtype: numpy.array
    """
def composeFwdUpPos(pose: numpy.array, fwd: numpy.array, up: numpy.array):
    """
    Compose  pose, forward and up vectors to a 4x4 transform matrix
    
    :param pose:  the pose vector
    :type pose: numpy.array
    :param fwd: the forward vector
    :type fwd: numpy.array
    :param up: the up vector
    :type up: numpy.array
    :return: The corresponding 4x4 transform matrix
    :rtype: numpy.array
    """
def decompose(mat4x4: numpy.array):
    """
    Decompose a 4x4 matrix to position, rotation and scale
    
    :param mat4x4:  the 4x4 matrix
    
    :return: a dict with "position" "rotation" and "scale"
    
    """
def decomposeFwdUpPos(mat4x4: numpy.array):
    """
    Decompose a 4x4 transform matrix to forward, up, pose vectors
    
    :type mat4x4: numpy.array
    :return: a dict  {"forward": numpy.array, "up": numpy.array, "pose": numpy.array}
    :rtype: dict
    """

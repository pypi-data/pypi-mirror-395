"""
Utility functions for depth and normal processing.
"""

import struct

import cv2
import numpy as np


def get_cam_params(calib_path):
    """
    Read camera parameters from a text file.

    Parameters
    ----------
    calib_path : str
        Path to the calibration file containing camera parameters.

    Returns
    -------
    tuple
        (cam_fx, cam_fy, u0, v0) - Camera focal lengths and principal point.
    """
    with open(calib_path, "r") as f:
        data = f.read()
        params = list(map(int, (data.split())))[:-1]
    return tuple(params)


def get_normal_gt(normal_path):
    """
    Read ground truth normal map from an image file.

    Parameters
    ----------
    normal_path : str
        Path to the normal map image file.

    Returns
    -------
    numpy.ndarray
        Normal map with values in range [-1, 1], shape (H, W, 3).
    """
    normal_gt = cv2.imread(normal_path, -1)
    normal_gt = normal_gt[:, :, ::-1]
    normal_gt = 1 - normal_gt / 65535 * 2
    return normal_gt


def get_depth(depth_path, height, width):
    """
    Read depth map from a binary file.

    Parameters
    ----------
    depth_path : str
        Path to the binary depth file.
    height : int
        Height of the depth map.
    width : int
        Width of the depth map.

    Returns
    -------
    tuple
        (depth, mask) - Depth map and foreground mask (1 for foreground, 0 for background).
    """
    with open(depth_path, "rb") as f:
        data_raw = struct.unpack("f" * width * height, f.read(4 * width * height))
        z = np.array(data_raw).reshape(height, width)

    # create mask, 1 for foreground, 0 for background
    mask = np.ones_like(z)
    mask[z == 1] = 0

    return z, mask


def vector_normalization(normal, eps=1e-8):
    """
    Normalize normal vectors to unit length.

    Parameters
    ----------
    normal : numpy.ndarray
        Normal map with shape (H, W, 3).
    eps : float, optional
        Small epsilon value to avoid division by zero (default: 1e-8).

    Returns
    -------
    numpy.ndarray
        Normalized normal map.
    """
    mag = np.linalg.norm(normal, axis=2)
    normal /= np.expand_dims(mag, axis=2) + eps
    return normal


def visualization_map_creation(normal, mask):
    """
    Create visualization map from normal map.

    Parameters
    ----------
    normal : numpy.ndarray
        Normal map with shape (H, W, 3), values in range [-1, 1].
    mask : numpy.ndarray
        Foreground mask with shape (H, W).

    Returns
    -------
    numpy.ndarray
        Visualization map with values in range [0, 1], shape (H, W, 3).
    """
    mask = np.expand_dims(mask, axis=2)
    vis = normal * mask + mask - 1
    vis = (1 - vis) / 2  # transform the interval from [-1, 1] to [0, 1]
    return vis


def angle_normalization(err_map):
    """
    Normalize error angles to [0, π/2] range.

    Parameters
    ----------
    err_map : numpy.ndarray
        Error map in radians.

    Returns
    -------
    numpy.ndarray
        Normalized error map.
    """
    err_map[err_map > np.pi / 2] = np.pi - err_map[err_map > np.pi / 2]
    return err_map


def evaluation(n_gt, n_est, mask):
    """
    Evaluate estimated normal map against ground truth.

    Parameters
    ----------
    n_gt : numpy.ndarray
        Ground truth normal map with shape (H, W, 3).
    n_est : numpy.ndarray
        Estimated normal map with shape (H, W, 3).
    mask : numpy.ndarray
        Foreground mask with shape (H, W).

    Returns
    -------
    tuple
        (error_map, ea) - Error map in degrees and mean angular error.
    """
    scale = np.pi / 180
    error_map = np.arccos(np.sum(n_gt * n_est, axis=2))
    error_map = angle_normalization(error_map) / scale
    error_map *= mask
    ea = error_map.sum() / mask.sum()
    return error_map, ea


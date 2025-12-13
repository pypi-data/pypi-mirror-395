"""
D2NT: A High-Performing Depth-to-Normal Translator

This package provides functionality to convert depth maps to surface normal maps.
"""

from .core import depth2normal
from .utils import (
    get_cam_params,
    get_depth,
    get_normal_gt,
    vector_normalization,
    visualization_map_creation,
    evaluation,
)

__version__ = "0.1.0"
__all__ = [
    "depth2normal",
    "get_cam_params",
    "get_depth",
    "get_normal_gt",
    "vector_normalization",
    "visualization_map_creation",
    "evaluation",
]


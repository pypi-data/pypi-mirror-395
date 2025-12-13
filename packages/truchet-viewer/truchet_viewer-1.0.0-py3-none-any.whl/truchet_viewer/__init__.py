"""
truchet-viewer - A Python library for generating multi-scale Truchet tile patterns and images using PyCairo.
"""

from .n6 import (
    n6_circles,
    n6_lattice,
    n6_tiles,
)
from .tiler import (
    TileBase,
    multiscale_truchet,
    show_tiles,
    tile_value,
    tile_value4,
)

__all__ = [
    'TileBase',
    'multiscale_truchet',
    'show_tiles',
    'tile_value',
    'tile_value4',
    'n6_tiles',
    'n6_circles',
    'n6_lattice',
]

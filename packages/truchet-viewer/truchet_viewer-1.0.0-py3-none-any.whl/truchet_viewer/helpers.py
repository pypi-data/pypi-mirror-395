"""Helpers for drawing in Jupyter notebooks with PyCairo."""

import colorsys
import itertools
import random


def range2d(nx, ny):
    return itertools.product(range(nx), range(ny))


def array_slices_2d(arr, x0, y0, nx, dx=None, ny=None, dy=None):
    """
    Produce slices of the array in a 2d grid.

    The slices start at x0,y0.  There are nx across, ny (defaulting to nx) down.
    The slices are dx across, dy (defaulting to dx) down.
    """
    ny = ny or nx
    dy = dy or dx
    if dx is None or dy is None:
        raise ValueError('dx and dy must be specified, either directly or via nx/ny')
    for ix, iy in range2d(nx, ny):
        x = x0 + ix * dx
        y = y0 + iy * dy
        yield arr[y : y + dy, x : x + dx]


def get_random_hex_color():
    """Generate a random hex color string."""
    return f'#{random.randint(0, 0xFFFFFF):06x}'


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert a hex color string to an RGB tuple with values in the range [0, 1]."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


def color(val):
    """Create an RGBA color tuple from a variety of inputs."""
    if isinstance(val, (int, float)):
        return (val, val, val, 1)
    elif isinstance(val, (list, tuple)):
        if len(val) == 3:
            return (*val, 1)
        else:
            return tuple(val)
    elif isinstance(val, str):
        if val[0] == '#':
            return (*hex_to_rgb(val), 1)


def make_bgfg(hs, ls, ss):
    hslsss = [[v, v] if isinstance(v, (int, float)) else v for v in [hs, ls, ss]]
    return dict(zip(['bg', 'fg'], [colorsys.hls_to_rgb(*hls) for hls in zip(*hslsss)]))


def ffffx(start, f):
    allfx = set()
    to_call = [start]
    while to_call:
        next_to_call = []
        for v in to_call:
            for vv in f(v):
                if vv not in allfx:
                    allfx.add(vv)
                    next_to_call.append(vv)
        to_call = next_to_call
    return allfx


def all_subclasses(cls):
    """Return a set of all subclasses of `cls`, including subclasses of subclasses."""
    return ffffx(cls, lambda c: c.__subclasses__())


def closest(x, values):
    return min(values, key=lambda v: abs(v - x))

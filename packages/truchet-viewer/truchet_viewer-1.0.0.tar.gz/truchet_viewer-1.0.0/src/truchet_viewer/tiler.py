"""Classes and functions for working with Truchet tiles and generating images from them.

Originally based on Ned Batchelder's truchet code: https://github.com/nedbat/truchet
"""

import random
from typing import Callable

import numpy as np
from PIL import Image

from truchet_viewer.drawing import DEG90, _CairoContext, cairo_context
from truchet_viewer.helpers import array_slices_2d, color, range2d

# Copyright Ned Batchelder 2022
# Copyright Joseph Barraud 2025


def rotations(cls, num_rots=4):
    return map(cls, range(num_rots))


def collect(tile_list: list, repeat: int = 1, rotations=None, flip=None):
    def _dec(cls):
        rots = rotations
        if rots is None:
            rots = cls.rotations
        will_flip = flip
        if will_flip is None:
            will_flip = cls.flip
        flips = [False, True] if will_flip else [False]
        for _ in range(repeat):
            for rot in range(rots):
                for flipped in flips:
                    tile_list.append(cls(rot=rot, flipped=flipped))
        return cls

    return _dec


def stroke(method):
    method.is_stroke = True
    return method


class TileBase:
    class G:
        def __init__(self, wh: int, bgfg: list | None = None):
            self.wh: int = wh
            if bgfg is None:
                self.bgfg = [color(1), color(0)]
            else:
                self.bgfg = bgfg

    rotations = 4
    flip = False

    def __init__(self, rot: int = 0, flipped: bool = False):
        self.rot = rot
        self.flipped = flipped

    def init_tile(self, ctx: _CairoContext, g: G, base_color=None): ...

    def draw_tile(self, ctx: _CairoContext, wh: int, bgfg=None, base_color=None, meth_name='draw'):
        g = self.G(wh, bgfg)
        self.init_tile(ctx, g, base_color=base_color)
        getattr(self, meth_name)(ctx, g)


class TileBasePlus(TileBase):
    """Add rotation and symmetry to base tiles."""

    eps = 0.0

    class G(TileBase.G):
        def __init__(self, wh: int, bgfg=None):
            super().__init__(wh, bgfg)
            self.wh2 = wh / 2

    def init_tile(self, ctx: _CairoContext, g: G, base_color=None):
        if base_color is None:
            base_color = [color(1), color(0)]

        ctx.rectangle(0 - self.eps, 0 - self.eps, g.wh + self.eps, g.wh + self.eps)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*g.bgfg[1])
        ctx.translate(g.wh2, g.wh2)
        ctx.rotate(DEG90 * self.rot)
        ctx.translate(-g.wh2, -g.wh2)

        if self.flipped:
            ctx.translate(g.wh, 0)
            ctx.scale(-1, 1)

    def draw(self, ctx, wh: int, bgfg=None): ...


def tile_value(tile):
    """The gray value of a tile from 0 (black) to 1 (white)."""
    pic = multiscale_truchet(tiles=[tile], width=100, height=100, tilew=100, nlayers=1, format='png')
    a = np.array(Image.open(pic.pngio).convert('L'))  # type: ignore
    value = np.sum(a) / a.size / 255
    return value


def tile_value4(tile):
    """The four-quadrant gray values (0->1) of a tile."""
    pw = 10
    pw2 = pw // 2
    pic = multiscale_truchet(tiles=[tile], width=pw, height=pw, tilew=pw, nlayers=1, format='png')
    a = np.array(Image.open(pic.pngio).convert('L'))  # type: ignore
    values = []
    for a4 in array_slices_2d(a, 0, 0, nx=2, dx=pw2):
        values.append(np.sum(a4) / a4.size / 255)
    return np.array(values)


def value_chart(tiles, inverted=False):
    marg = 50
    width = 800
    mid = 30

    def tick(x, h):
        v = (width - 2 * marg) * x + marg
        ctx.move_to(v, mid - h / 2)
        ctx.line_to(v, mid + h / 2)
        ctx.stroke()

    with cairo_context(width, mid * 2) as ctx:
        ctx.set_line_width(0.5)
        ctx.move_to(marg, mid)
        ctx.line_to(width - marg, mid)
        ctx.stroke()
        tick(0, 20)
        tick(1, 20)
        for t in tiles:
            value = tile_value(t)
            tick(value, 20)
            if inverted:
                tick(1 - value, 20)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(2)
        for i in range(11):
            tick(i / 10, 10)
    return ctx


def show_tiles(
    tiles,
    size=100,
    frac=0.6,
    width=950,
    with_value=False,
    with_name=False,
    only_one=False,
    sort=True,
):
    if only_one:
        # Keep only one of each class
        classes = {tile.__class__ for tile in tiles}
        tiles = [cls() for cls in classes]
    if with_value:
        values = {t: f'{tile_value(t):.3f}' for t in tiles}
    if sort:
        tiles = sorted(tiles, key=lambda t: t.__class__.__name__)
        if with_value:
            tiles = sorted(tiles, key=values.get)  # type: ignore
    wh = size * frac
    gap = size / 10
    per_row = (width + gap) // (size + gap)
    nrows = len(tiles) // per_row + (1 if len(tiles) % per_row else 0)
    ncols = per_row if nrows > 1 else len(tiles)
    totalW = int((size + gap) * ncols - gap)
    totalH = int((size + gap) * nrows - gap)
    with cairo_context(totalW, totalH) as ctx:
        ctx.select_font_face('Sans')
        ctx.set_font_size(10)
        for i, tile in enumerate(tiles):
            r, c = divmod(i, per_row)
            ctx.save()
            ctx.translate((size + gap) * c, (size + gap) * r)
            ctx.rectangle(0, 0, size, size)
            ctx.set_source_rgb(0.85, 0.85, 0.85)
            ctx.fill()

            ctx.save()
            ctx.translate((size - wh) / 2, (size - wh) / 2)

            tile.draw_tile(ctx, wh)

            ctx.rectangle(0, 0, wh, wh)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
            ctx.set_line_width(1)
            ctx.set_dash([5, 5], 7.5)
            ctx.stroke()
            ctx.restore()

            if with_value:
                ctx.move_to(2, 10)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(f'r={tile.rot} f={tile.flipped} {values[tile]}')

            if with_name:
                ctx.move_to(2, size - 2)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(tile.__class__.__name__)

            ctx.restore()

    return ctx


def show_overlap(tile):
    W = 200
    bgfg = [color(1), color(0)]
    with cairo_context(W, W) as ctx:
        ctx.rectangle(0, 0, W, W)
        ctx.set_source_rgb(0.75, 0.75, 0.75)
        ctx.fill()
        ctx.save()
        ctx.translate(W / 4, W / 4)
        tile.draw(ctx, W / 2, bgfg)
        ctx.restore()
        offset = 0
        bgfg = [color((0, 0, 0.7)), color((1, 0.5, 0.5))]
        for x, y in range2d(2, 2):
            ctx.save()
            ctx.translate(W / 4 + x * W / 4 + offset, W / 4 + y * W / 4 + offset)
            tile.draw(ctx, W / 4, bgfg)
            ctx.restore()
    return ctx


def multiscale_truchet(
    tiles=None,
    tile_chooser: Callable | None = None,  # type: ignore
    width=400,
    height=200,
    tilew=40,
    nlayers=2,
    chance: Callable | float = 0.5,  # type: ignore
    should_split: Callable | None = None,  # type: ignore
    bg: tuple[int, float] | tuple[float, float, float] | float | str = 1.0,
    fg: tuple[int, float] | tuple[float, float, float] | float | str = 0.0,
    seed=None,
    format='svg',
    output=None,
    grid=False,
):
    all_boxes = []

    rand = random.Random(seed)

    if isinstance(tiles, (list, tuple)) and tile_chooser is None:

        def tile_chooser(ux, uy, uw, ilevel):
            return rand.choice(tiles)

    if isinstance(chance, float):
        _chance = chance

        def chance(*a, **k):
            return _chance

    if should_split is None:

        def should_split(x, y, size, ilayer):
            return rand.random() <= chance(x, y, size, ilayer)

    def one_tile(x, y, size, ilayer, ctx: _CairoContext):
        if tile_chooser is not None:
            tile: TileBase = tile_chooser(x / width, y / width, size / width, ilayer)
        with ctx.save_restore():
            ctx.translate(x, y)
            tile.draw_tile(ctx, size, bgfg)
        boxes.append((x, y, size))
        if grid:
            all_boxes.append((x, y, size))

    with cairo_context(width, height, format=format, output=output) as ctx:
        boxes = []
        bgfg = [color(bg), color(fg)]
        wextra = 1 if (width % tilew) else 0
        hextra = 1 if (height % tilew) else 0
        for ox, oy in range2d(int(width / tilew) + wextra, int(height / tilew) + hextra):
            one_tile(ox * tilew, oy * tilew, tilew, 0, ctx)

        for ilayer in range(nlayers - 1):
            last_boxes = boxes
            bgfg = bgfg[::-1]
            boxes = []
            for bx, by, bsize in last_boxes:
                if should_split((bx + bsize / 2) / width, (by + bsize / 2) / height, bsize / width, ilayer):
                    nbsize = bsize / 2
                    for dx, dy in range2d(2, 2):
                        nbx, nby = bx + dx * nbsize, by + dy * nbsize
                        one_tile(nbx, nby, nbsize, ilayer + 1, ctx)

        if grid:
            ctx.set_line_width(0.5)
            ctx.set_source_rgb(1, 0, 0)
            for x, y, size in all_boxes:
                ctx.rectangle(x, y, size, size)
                ctx.stroke()

    return ctx

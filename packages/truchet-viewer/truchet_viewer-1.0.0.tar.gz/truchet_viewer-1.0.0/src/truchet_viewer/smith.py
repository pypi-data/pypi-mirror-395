"""Basic Smith tiles."""

import random

from truchet_viewer.drawing import DEG90, DEG180, cairo_context
from truchet_viewer.helpers import color, range2d
from truchet_viewer.tiler import TileBasePlus, _CairoContext, collect

smith_tiles = []


@collect(smith_tiles, repeat=1, rotations=1, flip=True)
class SmithTile(TileBasePlus):
    def draw(self, ctx: _CairoContext, g: TileBasePlus.G, bgfg=None):
        ctx.move_to(0 - self.eps, g.wh2)
        ctx.arc(0 - self.eps, g.wh + self.eps, g.wh2 + self.eps, -DEG90, 0)
        ctx.line_to(0 - self.eps, g.wh + self.eps)
        ctx.close_path()
        ctx.fill()

        ctx.move_to(g.wh + self.eps, g.wh2)
        ctx.arc(g.wh + self.eps, 0 - self.eps, g.wh2 + self.eps, DEG90, DEG180)
        ctx.line_to(g.wh + self.eps, 0 - self.eps)
        ctx.close_path()
        ctx.fill()


def smith(width: int = 400, height: int = 200, tilew: int = 40, grid: bool = False, gap: int = 0, seed=None):
    """Demonstrate Smith tiles."""
    rand = random.Random(seed)
    with cairo_context(width, height) as ctx:
        tiles: list[SmithTile] = smith_tiles
        bgfgs = [
            [color(1), color(0)],
            [color(0), color(1)],
        ]
        for ox, oy in range2d(width // tilew, height // tilew):
            ctx.save()
            ctx.translate(ox * (tilew + gap), oy * (tilew + gap))
            coin = rand.choice([0, 1])
            tiles[coin].draw_tile(ctx, tilew, bgfgs[(ox + oy + coin) % 2], bgfgs[(ox + oy + coin) % 2])
            if grid:
                ctx.set_line_width(0.1)
                ctx.rectangle(0, 0, tilew, tilew)
                ctx.set_source_rgb(0, 0, 0)
                ctx.stroke()
            ctx.restore()
    return ctx

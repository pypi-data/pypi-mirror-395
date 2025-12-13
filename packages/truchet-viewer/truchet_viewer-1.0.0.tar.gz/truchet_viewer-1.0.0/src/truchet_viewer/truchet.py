"""Classic Truchet tiles."""

from truchet_viewer.tiler import TileBasePlus, collect

truchet_tiles = []


@collect(truchet_tiles, repeat=1, rotations=4, flip=False)
class TruchetTile(TileBasePlus):
    def draw(self, ctx, g, bgfg=None):
        ctx.move_to(0 - self.eps, g.wh + self.eps)
        ctx.line_to(g.wh + self.eps, g.wh + self.eps)
        ctx.line_to(0 - self.eps, 0 - self.eps)
        ctx.close_path()
        ctx.fill()

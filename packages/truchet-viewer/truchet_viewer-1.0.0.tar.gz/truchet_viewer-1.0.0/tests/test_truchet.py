from truchet_viewer.tiler import multiscale_truchet, show_tiles
from truchet_viewer.truchet import truchet_tiles


def test_truchet_tiles():
    ctx = show_tiles(truchet_tiles, size=100, with_name=True, with_value=True, sort=False)
    with open('tests/output/test_truchet_tiles.svg', 'wb') as f:
        f.write(ctx.svgio.getvalue())



def test_show_truchet():
    ctx = multiscale_truchet(tiles=truchet_tiles, width=800, height=600, tilew=100, nlayers=3, chance=0.5, seed=11, grid=False)
    with open('tests/output/test_show_truchet.svg', 'wb') as f:
        f.write(ctx.svgio.getvalue())

from truchet_viewer.smith import smith, smith_tiles
from truchet_viewer.tiler import show_tiles


def test_smith_tiles():
    ctx = show_tiles(smith_tiles, size=200, width=900, sort=False, with_value=True, with_name=True)
    with open('tests/output/test_smith_tiles.svg', 'wb') as f:
        f.write(ctx.svgio.getvalue())


def test_show_smith():
    ctx = smith(tilew=40, seed=4, grid=False)
    with open('tests/output/test_show_smith.svg', 'wb') as f:
        f.write(ctx.svgio.getvalue())

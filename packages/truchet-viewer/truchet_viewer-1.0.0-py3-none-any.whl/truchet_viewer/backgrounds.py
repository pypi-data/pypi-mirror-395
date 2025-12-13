"""Generate multiscale truchet images using n6_circles tiles."""

from pathlib import Path

from truchet_viewer.helpers import make_bgfg
from truchet_viewer.n6 import n6_circles
from truchet_viewer.tiler import multiscale_truchet

# Copyright Joseph Barraud 2025
# Copyright Ned Batchelder 2022


DIR = Path('~/wallpaper/tru6/1680').expanduser()
DIR.mkdir(parents=True, exist_ok=True)
NIMG = 30
for i in range(NIMG):
    print(f'Generating image {i + 1} of {NIMG}')
    print(f'Output: {DIR}/bg_{i:02d}.png')
    multiscale_truchet(
        tiles=n6_circles,
        width=1680,
        height=1050,
        tilew=200,
        nlayers=3,
        chance=0.4,
        seed=i,
        **make_bgfg(i / NIMG, (0.55, 0.45), 0.45),
        format='png',
        output=f'{DIR}/bg_{i:02d}.png',
        tile_chooser=None,
        grid=False,
        should_split=None,
    )

DIR = Path('~/wallpaper/tru6/1920').expanduser()
DIR.mkdir(parents=True, exist_ok=True)
NIMG = 15
for i in range(NIMG):
    print(f'Generating image {i + 1} of {NIMG}')
    print(f'Output: {DIR}/bg_{i:02d}.png')
    multiscale_truchet(
        tiles=n6_circles,
        width=1920,
        height=1080,
        tilew=200,
        nlayers=3,
        chance=0.4,
        seed=i,
        **make_bgfg(i / NIMG, (0.55, 0.45), 0.45),
        format='png',
        output=f'{DIR}/bg_{i:02d}.png',
        tile_chooser=None,
        grid=False,
        should_split=None,
    )

DIR = Path('~/wallpaper/tru6/2872').expanduser()
DIR.mkdir(parents=True, exist_ok=True)
for i in range(NIMG):
    print(f'Generating image {i + 1} of {NIMG}')
    print(f'Output: {DIR}/bg_{i:02d}.png')
    multiscale_truchet(
        tiles=n6_circles,
        width=2872,
        height=5108,
        tilew=300,
        nlayers=3,
        chance=0.4,
        bg='#335495',
        fg='#243b6a',
        seed=i,
        format='png',
        output=f'{DIR}/bg_{i:02d}.png',
    )

DIR = Path('~/wallpaper/tru6/1536').expanduser()
DIR.mkdir(parents=True, exist_ok=True)
for i in range(NIMG):
    print(f'Generating image {i + 1} of {NIMG}')
    print(f'Output: {DIR}/bg_{i:02d}.png')
    multiscale_truchet(
        tiles=n6_circles,
        width=1536,
        height=960,
        tilew=200,
        nlayers=3,
        chance=0.4,
        bg='#335495',
        fg='#243b6a',
        seed=i * 3,
        format='png',
        output=f'{DIR}/bg_{i:02d}.png',
    )

DIR = Path('~/wallpaper/tru6/2560').expanduser()
DIR.mkdir(parents=True, exist_ok=True)
NIMG = 60
for i in range(NIMG):
    print(f'Generating image {i + 1} of {NIMG}')
    print(f'Output: {DIR}/bg_{i:02d}.png')
    multiscale_truchet(
        tiles=n6_circles,
        tile_chooser=None,
        width=2560,
        height=1440,
        tilew=150,
        nlayers=3,
        chance=0.4,
        seed=i * 10,
        should_split=None,
        **make_bgfg(i / NIMG, (0.55, 0.45), 0.45),
        format='png',
        output=f'{DIR}/bg_{i:03d}.png',
        grid=False,
    )

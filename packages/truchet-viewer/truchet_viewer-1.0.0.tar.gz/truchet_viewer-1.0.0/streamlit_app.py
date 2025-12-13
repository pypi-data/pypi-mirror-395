"""Streamlit app to generate multiscale Truchet patterns."""

import re

import streamlit as st

from truchet_viewer import multiscale_truchet
from truchet_viewer.carlson import carlson_basic, carlson_extra, carlson_tiles
from truchet_viewer.helpers import get_random_hex_color
from truchet_viewer.n6 import n6_circles, n6_connected, n6_filled, n6_lattice, n6_strokes, n6_tiles, n6_weird
from truchet_viewer.truchet import truchet_tiles

# Copyright Joseph Barraud 2025

# Set page config
st.set_page_config(page_title='Truchet Pattern Generator', layout='wide')

# Title
st.title('Multiscale Truchet Pattern Generator')

# Create dictionary mapping tile set names to actual tile lists
TILE_SETS = {
    'All N6 tiles': n6_tiles,
    'Circles': n6_circles,
    'Connected': n6_connected,
    'Filled': n6_filled,
    'Lattice': n6_lattice,
    'Strokes': n6_strokes,
    'Weird': n6_weird,
    'Carlson Basic': carlson_basic,
    'Carlson': carlson_tiles,
    'Carlson Extra': carlson_extra,
    'Truchet': truchet_tiles,
}

# Create sidebar for controls
with st.sidebar:
    st.header('Pattern Controls')

    # Tile set selection
    tile_set = st.selectbox(
        'Tile Set',
        options=list(TILE_SETS.keys()),
        index=1,  # n6_circles by default
    )

    # Canvas dimensions
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input('Width', min_value=200, max_value=2560, value=800, step=100)
    with col2:
        height = st.number_input('Height', min_value=200, max_value=2000, value=800, step=100)

    # Tile parameters
    nlayers = st.number_input('Layers', min_value=1, max_value=6, value=2)
    tilew = st.slider('Tile Size', min_value=20, max_value=300, value=100, step=10)
    chance = st.slider('Split Chance', min_value=0.0, max_value=1.0, value=0.45, step=0.05)

    # Colors
    st.markdown('---')  # Visual separator

    if st.button('Randomize Colors'):
        st.session_state.bg_color = get_random_hex_color()
        st.session_state.fg_color = get_random_hex_color()

    bg_color = st.color_picker('Background Color', value='#335495', key='bg_color')
    fg_color = st.color_picker('Foreground Color', value='#243b6a', key='fg_color')

    st.markdown('---')  # Visual separator

    # Additional controls
    seed = st.number_input('Random Seed', value=42)
    grid = st.checkbox('Show Grid', value=False)

    # Add a download button
    download = st.button('Generate for Download')


# Main content area
@st.cache_data
def render_truchet_bytes(
    tile_set_label: str,
    width: int,
    height: int,
    tilew: int,
    nlayers: int,
    chance: float,
    bg: str,
    fg: str,
    grid: bool,
    seed: int,
):
    """Render truchet pattern and return PNG bytes. Cached by Streamlit to avoid re-rendering."""
    tiles = TILE_SETS[tile_set_label]
    pic = multiscale_truchet(
        tiles=tiles,
        width=width,
        height=height,
        tilew=tilew,
        nlayers=nlayers,
        chance=chance,
        bg=bg,
        fg=fg,
        grid=grid,
        seed=seed,
        format='png',
        output=None,
    )
    return pic.pngio.getvalue() if getattr(pic, 'pngio', None) is not None else None


try:
    # Get PNG bytes from cache (or render if needed)
    pattern_bytes = render_truchet_bytes(
        tile_set, width, height, tilew, nlayers, chance, bg_color, fg_color, grid, seed
    )

    # Display the pattern
    if pattern_bytes is not None:
        st.image(pattern_bytes, width='content')

    # Handle download if requested
    if download:
        # sanitize tile_set label for a filename
        def _sanitize(name: str) -> str:
            # Replace any sequence of non-alphanumeric, dot, underscore, or dash with underscore
            s = name.replace(' ', '_')
            s = re.sub(r'[^A-Za-z0-9._-]+', '_', s)
            return s.strip(' _').lower() or 'tiles'

        safe_label = _sanitize(tile_set)
        filename = f'truchet_{safe_label}_{seed}_{width}x{height}.png'

        if pattern_bytes:
            st.sidebar.download_button(
                label='Download PNG',
                data=pattern_bytes,
                file_name=filename,
                mime='image/png',
                icon=':material/download:',
            )
        else:
            st.sidebar.error('Failed to create PNG for download.')

except Exception as e:
    st.error(f'Error generating pattern: {str(e)}')

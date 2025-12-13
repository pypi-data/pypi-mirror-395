# Truchet Viewer

A Python library for generating and exploring multi-scale Truchet tile patterns using [PyCairo](https://pycairo.readthedocs.io/en/latest/)
and [Streamlit](https://docs.streamlit.io/).
This library provides tools for creating complex, visually appealing patterns through both interactive Jupyter notebooks and a web-based app.

![Truchet Tile Example](examples/truchet_circles_42_800x600.png)

## Features

- Generate multi-scale Truchet tile patterns with customizable depth and complexity
- Rich set of predefined tiles including circles, lattices, and filled shapes
- Interactive exploration through Jupyter notebooks and Streamlit app
- Flexible Cairo-based rendering supporting SVG and PNG output

## Description

The history of [Truchet tiles](https://en.wikipedia.org/wiki/Truchet_tile) begins in the early 18th century with **Father Sebastien Truchet**, who first described them in his 1704 memoir, _Mémoire sur les combinaisons_. Truchet's original square tiles were divided diagonally into two contrasting triangles, forming the basis for exploring intricate combinatorial patterns. The idea was significantly popularized in 1987 by **Cyril Stanley Smith** in his paper, _The tiling patterns of Sebastian Truchet and the topology of structural hierarchy_. Smith introduced the highly popular variation featuring quarter-circle arcs that connect the midpoints of adjacent sides, forming continuous, meandering paths when tiled. Building on this, [Christopher Carlson][carlson] later introduced multi-scale Truchet patterns by using "winged" tiles scaled by factors of 1/2, allowing different scale tiles to overlap and merge seamlessly.

The original implementation was done by [Ned Batchelder][batchelder-truchet] using PIL and PyCairo.
This library reimplements and extends that work, providing a more flexible and user-friendly interface for generating and exploring Truchet patterns.

---

## Installation

### Prerequisites

The package requires Python 3.12 or later and depends on PyCairo. On some systems, you may need to install Cairo development headers:

```bash
# Ubuntu/Debian
sudo apt-get install libcairo2-dev pkg-config python3-dev

# macOS
brew install cmake pkgconf cairo

# Windows
# Install Cairo through MSYS2 or use the wheels available on PyPI
```

### Installing from PyPI

The package is available on PyPI and can be installed via pip:

```bash
pip install truchet-viewer
```

### Installing from Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/jobar8/truchet-viewer.git
cd truchet-viewer
pip install -e .
```

Instead of using `pip`, you can also use [uv](https://docs.astral.sh/uv) to install the development dependencies in a local virtual environment:

```bash
uv sync
source .venv/bin/activate
```

## Quick Start

### Using the Jupyter Notebooks

Launch Jupyter Notebook and open the example notebooks in the `examples/` directory:

```bash
jupyter lab
```

### Using the Streamlit App

Launch the Streamlit app to interactively explore Truchet patterns:

```bash
cd truchet-viewer
streamlit run streamlit_app.py

# or if uv is installed (also installs dependencies):
uv run streamlit run streamlit_app.py
```

### Generating a Multi-Scale Truchet Pattern

Here is a simple example of generating a multi-scale Truchet pattern using the N6 tile set:

```python
from truchet_viewer import multiscale_truchet, show_tiles
from truchet_viewer.n6 import n6_tiles

# Display available tiles
show_tiles(n6_tiles, with_value=True, with_name=True)

# Generate a multi-scale pattern
multiscale_truchet(
    tiles=n6_tiles,
    width=800,
    height=600,
    tilew=100,
    nlayers=3,
    chance=0.45
)
```

This will create a multi-scale Truchet pattern using the N6 tile set. The `nlayers` parameter controls the number of levels.

It should look something like this:

![Example Truchet Pattern](examples/truchet_example.png)

## Examples

Check out the example notebooks in the `examples/` directory:

- `Truchet.ipynb` - Basic usage and pattern generation
- `N6.ipynb` - Exploring different tile types

## Acknowledgments

This project implements [Christopher Carlson][carlson]'s work on multi-scale Truchet tiles.
The original inspiration came from a [blog post][batchelder] by Ned Batchelder, who implemented
[the first version][batchelder-truchet].

## License

This code is Apache licensed. See LICENSE for details.

[carlson]: https://christophercarlson.com/portfolio/multi-scale-truchet-patterns
[batchelder]: https://nedbatchelder.com/blog/202208/truchet_images.html
[batchelder-truchet]: https://github.com/nedbat/truchet

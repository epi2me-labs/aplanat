"""Simple bokeh plotting API."""

import warnings

from bokeh.colors import RGB
import bokeh.io as bkio
from bokeh.layouts import gridplot
from bokeh.plotting import Figure

__version__ = '0.2.4'

# we don't run a comprehensive test suite and mostly in notebooks,
# so show warnings all the time.
warnings.simplefilter('always', DeprecationWarning)


class Grid(list):
    """Create a list of lists of fixed length."""

    def __init__(self, width=4):
        """Initialize the Grid."""
        self.width = width
        self.append(list())

    def add(self, item):
        """Add an item to the grid.

        :param item: item to add

        """
        self[-1].append(item)
        if len(self[-1]) == self.width:
            self.append(list())

    def extend(self, items):
        """Add multiple items.

        :param items: items to add.

        """
        for item in items:
            self.add(item)


def all_children(plotlike):
    """Recursively find all Figures in a plotting layout.

    :param plotlike: a bokeh layout or plot.
    """
    my_children = []
    if hasattr(plotlike, 'children'):
        for child in plotlike.children:
            if isinstance(child, tuple):
                child = child[0]
            my_children.extend(all_children(child))
    if isinstance(plotlike, Figure):
        my_children.append(plotlike)
    return my_children


def show(plot, background=None):
    """Show a plot in a notebook.

    :param background: a fill colour for the plot background, hex string or RGB
        tuple.

    """
    children = all_children(plot)
    orig_colours = None
    if background is not None:
        if isinstance(background, tuple):
            background = RGB(*background)
        elif not (isinstance(background, str) and background.startswith('#')):
            raise TypeError(
                "`background` should be a RGB tuple or hex-colour string.")
        orig_colours = list()
        for child in children:
            orig_colours.append((
                child.background_fill_color,
                child.border_fill_color))
            child.background_fill_color = background
            child.border_fill_color = background
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)
    if background is not None:
        for colours, child in zip(orig_colours, children):
            child.background_fill_color = colours[0]
            child.border_fill_color = colours[1]


def grid(plots, ncol=4, display=True, **kwargs):
    """Show a grid of plots in a notebook.

    :param plots: a list of bokeh plots.
    :param ncol: number of columns.
    :param kwargs: kwargs for bokeh `gridplot`.

    """
    warnings.warn(
        "Please use `bokeh.layout.gridplot` directly with an optional "
        "call to `.show()`", DeprecationWarning)

    grid = Grid(width=ncol)
    grid.extend(plots)
    plot = gridplot(grid, **kwargs)
    if display:
        show(plot)
    else:
        return plot


def InfoGraphItems():
    """Cumulatively create items for an infographic."""
    from aplanat import graphics
    warnings.warn(
        "This class has been moved to `aplanat.graphics.InfoGraphItems()`",
        DeprecationWarning)
    return graphics.InfoGraphItems()


def infographic(items, **kwargs):
    """Create an infographic 'plot'."""
    from aplanat import graphics
    warnings.warn(
        "This function has been moved to `aplanat.graphics.infographic()`",
        DeprecationWarning)
    return graphics.infographic(items, **kwargs)

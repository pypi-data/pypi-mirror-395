from functools import wraps
import pyvista
from .plot import reset_plotter

__all__ = ["set_interactive", "start_xvfb"]


# Expose pyvista callers
@wraps(pyvista.start_xvfb)
def start_xvfb(*args, **kwargs):
    pyvista.start_xvfb(*args, **kwargs)


start_xvfb.__doc__ = start_xvfb.__doc__.split("Notes", 1)[
    0
]  # Remove pyvista specific examples


def set_interactive(flag: bool = True, use_xvfb: bool = True, xvfb_wait: float = 0.1):
    """
    Change settings to swith from interactive to non-interactive plots.

    If `set` is `False`, this runs:

    >>> pyvista.OFF_SCREEN = False
    >>> pyvista4dolfinx.reset_plotter()

    If `set` and `use_xvfb` are `True` (this requires libgl1 libglx-mesa0
    and xvfb to be installed on a unix system):

    >>> pyvista.OFF_SCREEN = True
    >>> pyvista.start_xvfb()
    >>> pyvista4dolfinx.reset_plotter()

    If `set` is `True` and `use_xvfb` is `False` (this requires a renderable
    screen to be configured. May be tricky to set up properly):

    >>> pyvista.OFF_SCREEN = True
    >>> pyvista4dolfinx.reset_plotter()

    Parameters
    ----------
    set : bool
        Whether to set interactive plots, default True.
    use_xvfb : bool
        Whether to call `start_xvfb` in non-interactive mode, default True
    xvfb_wait : float
        How long to wait while setting up the virtual frame buffer.
        pyvista's default is 3 seconds, which we reduced to 0.1 second.
    """
    if flag:
        pyvista.OFF_SCREEN = False
        reset_plotter()
    else:
        pyvista.OFF_SCREEN = True
        if use_xvfb:
            start_xvfb(wait=xvfb_wait)
        reset_plotter()

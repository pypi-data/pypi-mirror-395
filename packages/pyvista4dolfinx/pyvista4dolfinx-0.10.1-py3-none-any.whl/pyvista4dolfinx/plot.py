# Copyright (C) 2025 Stein K.F. Stoter
#
# This file is part of pyvista4dolfinx
#
# SPDX-License-Identifier:    MIT

from functools import singledispatch, wraps
from typing import Any
import atexit

import basix
import dolfinx
from mpi4py import MPI
import numpy as np
import pyvista
import ufl.measure

from .safeplotter import Plotter
from .gather import _gather_grid, _gather_meshtags

__all__ = [
    "show",
    "screenshot",
    "reset_plotter",
    "plot",
    "plot_function_scalar",
    "plot_function_vector",
    "plot_mesh",
    "plot_meshtags",
]

pyvista.global_theme.allow_empty_mesh = True


@wraps(Plotter.show)
def show(*args, auto_close: bool = None, **kwargs):
    global PLOTTER
    ret = PLOTTER.show(*args, auto_close=auto_close, **kwargs)
    if auto_close is not False:
        reset_plotter()
    return ret


_show = show
show.__name__ = "show"
show.__qualname__ = "show"
show.__doc__ = show.__doc__.split("Examples", 1)[0]  # Remove pyvista specific examples


@wraps(Plotter.screenshot)
def screenshot(filename: str, *args, **kwargs):
    global PLOTTER
    ret = PLOTTER.screenshot(filename, *args, **kwargs)
    reset_plotter()
    return ret


screenshot.__name__ = "screenshot"
screenshot.__qualname__ = "screenshot"
screenshot.__doc__ = screenshot.__doc__.split("Examples", 1)[
    0
]  # Remove pyvista specific examples


# Module global plotter object on rank 0. Empty plotter on all other ranks.
PLOTTER = Plotter()


def reset_plotter(*args, plotter: Plotter = None, **kwargs):
    """
    Rsets the default module global `PLOTTER`. If specified, it is set to
    `plotter`. Else, a new empty `Plotter` is created and arguments and key-word
    arguments passed, are forwarded to the initialization of the new `Plotter`.

    Parameters
    ----------
    plotter : Plotter, optional
        If specified, the module global PLOTTER is set to this plotter,
        by default None
    """
    global PLOTTER
    PLOTTER = plotter if plotter is not None else Plotter(*args, **kwargs)


atexit.register(
    reset_plotter
)  # Mitigate python exiting conflict due to wrong PLOTTER state.


@singledispatch
def plot(plottable: Any, *args, **kwargs) -> Plotter:
    """
    Plots the plottable and returns the pyvista `Plotter` object. Depending
    on the type of the plottable, the call is dispatched to:

    >>> pyvista4dolfinx.plot.plot_function_scalar(plottable, *args, **kwargs)  # for scalar dolfinx.fem.Function
    >>> pyvista4dolfinx.plot.plot_function_vector(plottable, *args, **kwargs)  # for vector dolfinx.fem.Function
    >>> pyvista4dolfinx.plot.plot_mesh(plottable, *args, **kwargs)  # for dolfinx.mesh.Mesh
    >>> pyvista4dolfinx.plot.plot_meshtags(plottable, *args, **kwargs)  # for dolfinx.mesh.MeshTags
    >>> pyvista4dolfinx.plot.plot_measure(plottable, *args, **kwargs)  # for ufl.measure.Measure

    Parameters
    ----------
    plottable : dolfinx.fem.Function | dolfinx.mesh.Mesh | dolfinx.mesh.MeshTags
        The plottable entity.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """
    raise NotImplementedError(
        f"Plotting objects of type {type(plottable)} not implemented"
    )


@plot.register
def plot_function_(plottable: dolfinx.fem.Function, *args, **kwargs) -> Plotter:
    if len(plottable.ufl_shape) > 0:
        return plot_function_vector(plottable, *args, **kwargs)
    return plot_function_scalar(plottable, *args, **kwargs)


@plot.register
def plot_mesh_(
    plottable: dolfinx.mesh.Mesh,
    *args,
    show_partitioning: bool = False,
    **kwargs,
) -> Plotter:
    if show_partitioning:
        meshtags = _get_partitioning_meshtags(plottable)
        return plot_meshtags(meshtags, *args, mesh=plottable, name="MPI rank", **kwargs)
    return plot_mesh(plottable, *args, **kwargs)


@plot.register
def plot_meshtags_(plottable: dolfinx.mesh.MeshTags, *args, **kwargs) -> Plotter:
    return plot_meshtags(plottable, *args, **kwargs)


@plot.register
def plot_measure_(plottable: ufl.measure.Measure, *args, **kwargs) -> Plotter:
    return plot_measure(plottable, *args, **kwargs)


def plot_function_scalar(
    u: dolfinx.fem.Function,
    warp: dolfinx.fem.Function | bool = False,
    show_mesh: bool = True,
    name: str = "",
    plotter: Plotter | None = None,
    clear_plotter: bool = False,
    subplot: tuple | None = None,
    show: bool = False,
    **kwargs,
) -> Plotter:
    """
    Produce a contourplot of scalar-valued function `u`.

    Parameters
    ----------
    u : dolfinx.fem.Function
        The plotted scalar-valued function.
    warp: dolfinx.fem.Function | bool, optional
        Vector-valued function by which to warp the mesh. If `True`, it is
        assumed this is a 2D plot and the mesh is warped by `u` in
        `z`-direction, by default False
    show_mesh: bool, optional
        Whether to overlay a plot of the mesh edges.
    name : str
        The name to give field `u` in the colorbar.
    plotter: Plotter | None, optional
        The Plotting object to which to add this data. If None, the default
        (module-level) instance is used, by default None
    clear_plotter : bool, optional
        Whether to clear/reset the default Plotter instance, by default
        False
    subplot : tuple | None, optional
        If the Plotter is initialized with multiple subplots, specify with
        a tuple which sublot to plot in, by default None
    show : bool, optional
        Whether to show upon completion. Alternatively, call `.show()` on
        the returned Plotter `instance`. By default False
    **kwargs
        The remaining keyword arguments are passed to the
        `plotter.add_mesh` call.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """

    global PLOTTER
    if clear_plotter:
        reset_plotter()
    if subplot is not None:
        PLOTTER.subplot(*subplot)

    u, warp = _compatible_scalar_u_warp(u, warp)

    # Gather data onto MPI process 0
    grid = _gather_grid(u.function_space.mesh, u, warp=warp, name=name)
    if MPI.COMM_WORLD.rank != 0:
        return PLOTTER

    # Set the global plotter
    PLOTTER = plotter if plotter is not None else PLOTTER

    # Default plotting options
    defaults = {"show_scalar_bar": True}

    # Visualize
    options = defaults | kwargs
    PLOTTER.add_mesh(grid, **options)
    if show_mesh:
        _plot_feature_edges(PLOTTER, grid)
    if warp is not True and u.function_space.mesh.geometry.dim in [1, 2]:
        PLOTTER.view_xy()

    if show:
        _show()

    return PLOTTER


def plot_function_vector(
    u: dolfinx.fem.Function,
    warp: dolfinx.fem.Function | bool = False,
    show_mesh: bool = True,
    name: str = "",
    plotter: pyvista.Plotter | None = None,
    clear_plotter: bool = False,
    subplot: tuple | None = None,
    show: bool = False,
    **kwargs,
) -> Plotter:
    """
    Produce a glyph plot of `u`.

    Parameters
    ----------
    u : dolfinx.fem.Function.
        The plotted vector-valued function.
    warp: dolfinx.fem.Function | bool, optional
        Vector-valued function by which to warp the mesh. If
        `True`, mesh is warped by `u`, by default False
    show_mesh: bool, optional
        Whether to overlay a plot of the mesh edges.
    name : str
        The name to give field `u` in the colorbar.
    show_mesh : bool, optional
        Whether to also show the mesh, by default True
    plotter: Plotter | None, optional
        The Plotting object to which to add this data. If None, the default
        (module-level) instance is used, by default None
    clear_plotter : bool, optional
        Whether to clear/reset the default Plotter instance, by default
        False
    subplot : tuple | None, optional
        If the Plotter is initialized with multiple subplots, specify with
        a tuple which sublot to plot in, by default None
    show : bool, optional
        Whether to show upon completion. Alternatively, call `.show()` on
        the returned Plotter `instance`. By default False
    **kwargs
        The remaining keyword arguments are passed to the
        `plotter.add_mesh` call.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """
    global PLOTTER
    if clear_plotter:
        reset_plotter()
    if subplot is not None:
        PLOTTER.subplot(*subplot)

    # Handle element types not supported by pyvista
    if u.ufl_element().family_name not in [
        "Discontinuous Lagrange",
        "Lagrange",
        "DQ",
        "Q",
        "DP",
        "P",
    ]:
        u = _interpolate_vector_DG(u)
    if type(warp) is not bool and warp.function_space != u.function_space:
        warp = _interpolate(warp, u.function_space)

    # Gather data onto MPI process 0
    grid = _gather_grid(u.function_space.mesh, u, warp=warp, name=name)

    # Plot outline
    gdim = u.function_space.mesh.geometry.dim
    if gdim == 2 and not show_mesh and warp is False:
        outline_meshtags = _get_outline_meshtags(u.function_space.mesh)
        plot_meshtags(
            outline_meshtags,
            mesh=u.function_space.mesh,
            tagvalue=1,
            warp=warp,
            plotter=plotter,
            color="black",
            line_width=1,
            show_scalar_bar=False,
        )

    if MPI.COMM_WORLD.rank != 0:
        return PLOTTER

    # Set the global plotter
    PLOTTER = plotter if plotter is not None else PLOTTER

    # Manipulate grid data
    factor = kwargs.pop("factor") if "factor" in kwargs.keys() else 1
    glyphs = grid.glyph(orient=name if name else u.name, factor=factor)
    glyphs.rename_array("GlyphScale", name if name else u.name)

    # Default plotting options
    defaults = {"show_scalar_bar": True}

    # Visualize
    options = defaults | kwargs
    PLOTTER.add_mesh(glyphs, **options)  # Main operation
    if show_mesh and gdim in [2, 3]:
        _plot_feature_edges(PLOTTER, grid)
    if gdim in [1, 2]:
        PLOTTER.view_xy()

    if show:
        _show()

    return PLOTTER


def plot_mesh(
    mesh: dolfinx.mesh.Mesh,
    warp: dolfinx.fem.Function | bool = False,
    plotter: pyvista.Plotter | None = None,
    clear_plotter: bool = False,
    subplot: tuple | None = None,
    show: bool = False,
    **kwargs,
) -> Plotter:
    """
    Produce a plot of the mesh.

    Parameters
    ----------
    mesh : dolfinx.mesh.Mesh
        Mesh to be plotted.
    warp: dolfinx.fem.Function | bool, optional
        Field by which to warp the mesh, by default False
    plotter: Plotter | None, optional
        The Plotting object to which to add this data. If None, the default
        (module-level) instance is used, by default None
    clear_plotter : bool, optional
        Whether to clear/reset the default Plotter instance, by default
        False
    subplot : tuple | None, optional
        If the Plotter is initialized with multiple subplots, specify with
        a tuple which sublot to plot in, by default None
    show : bool, optional
        Whether to show upon completion. Alternatively, call `.show()` on
        the returned Plotter `instance`. By default False
    **kwargs
        The remaining keyword arguments are passed to the
        `plotter.add_mesh` call.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """
    global PLOTTER
    if clear_plotter:
        reset_plotter()
    if subplot is not None:
        PLOTTER.subplot(*subplot)

    # Gather data onto MPI process 0
    grid = _gather_grid(mesh, warp=warp)
    if MPI.COMM_WORLD.rank != 0:
        return PLOTTER

    # Set the global plotter
    PLOTTER = plotter if plotter is not None else PLOTTER

    # Default plotting options
    defaults = {"style": "wireframe", "color": "black"}

    # Visualize
    options = defaults | kwargs
    _plot_feature_edges(PLOTTER, grid, options=options)
    if mesh.geometry.dim in [1, 2]:
        PLOTTER.view_xy()

    if show:
        _show()

    return PLOTTER


def plot_meshtags(
    meshtags: dolfinx.mesh.MeshTags,
    mesh: dolfinx.mesh.Mesh | None = None,
    tagvalue: int | None = None,
    warp: None = None,
    show_mesh: bool = True,
    name: str = "Tags",
    plotter: pyvista.Plotter | None = None,
    clear_plotter: bool = False,
    subplot: tuple | None = None,
    show: bool = False,
    **kwargs,
) -> Plotter:
    """
    Produce a plot of the meshtags.

    Parameters
    ----------
    meshtags:  dolfinx.mesh.MeshTags
        Meshtags to be plotted
    mesh : dolfinx.mesh.Mesh
        Mesh corresponding to the meshtags.
    tagvalue: int | None, optional
        Which tag to show. If None, will show all tags. By detault None
    warp: dolfinx.fem.Function | bool, optional
        Field by which to warp the mesh, by default False
    show_mesh: bool, optional
        Whether to overlay a plot of the mesh edges.
    name : str
        The name to give tags in the colorbar.
    plotter: Plotter | None, optional
        The Plotting object to which to add this data. If None, the default
        (module-level) instance is used, by default None
    clear_plotter : bool, optional
        Whether to clear/reset the default Plotter instance, by default
        False
    subplot : tuple | None, optional
        If the Plotter is initialized with multiple subplots, specify with
        a tuple which sublot to plot in, by default None
    show : bool, optional
        Whether to show upon completion. Alternatively, call `.show()` on
        the returned Plotter `instance`. By default False
    **kwargs
        The remaining keyword arguments are passed to the
        `plotter.add_mesh` call.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """
    global PLOTTER
    if clear_plotter:
        PLOTTER = Plotter()
    if subplot is not None:
        PLOTTER.subplot(*subplot)

    if mesh is None:
        raise ValueError(
            "A `mesh` must be supplied to plot meshtags. See help `plot_meshtags`."
        )
    if warp:
        raise NotImplementedError("Warping a meshtags object is not supported")

    meshtags_indices, meshtag_values = _gather_meshtags(meshtags, mesh, tag=tagvalue)
    grid = _gather_grid(mesh, dim=meshtags.dim, entities=meshtags_indices)

    # Plot outline
    gdim = mesh.geometry.dim
    if gdim == 2 and not show_mesh:
        outline_meshtags = _get_outline_meshtags(mesh)
        plot_meshtags(
            outline_meshtags,
            mesh=mesh,
            tagvalue=1,
            warp=warp,
            plotter=plotter,
            color="black",
            line_width=1,
            show_scalar_bar=False,
        )

    if MPI.COMM_WORLD.rank != 0:
        return PLOTTER

    # Set the global plotter
    PLOTTER = plotter if plotter is not None else PLOTTER

    # Manipulate grid data
    grid.cell_data[name] = meshtag_values.astype(str)

    # Set plotting options:
    defaults = {"scalars": name, "show_edges": False, "show_scalar_bar": True}
    if meshtags.dim == 1:
        defaults |= {"line_width": 4}

    # Visualize
    options = defaults | kwargs
    gdim = mesh.geometry.dim
    PLOTTER.add_mesh(grid, **options)
    if show_mesh and gdim in [2, 3]:
        _plot_feature_edges(PLOTTER, grid)
    if gdim in [1, 2]:
        PLOTTER.view_xy()

    if show:
        _show()

    return PLOTTER


def plot_measure(
    measure: ufl.measure.Measure,
    mesh: dolfinx.mesh.Mesh | None = None,
    show_mesh: bool = False,
    name: str = "Measure",
    plotter: pyvista.Plotter | None = None,
    clear_plotter: bool = False,
    subplot: tuple | None = None,
    show: bool = False,
    **kwargs,
) -> Plotter:
    """
    Produce a plot of the measure, bu plotting the underlying meshtags.

    Parameters
    ----------
    measure: ufl.measure.Measure
        Measure to be plotted
    mesh : dolfinx.mesh.Mesh
        Mesh corresponding to the measure.
    show_mesh: bool, optional
        Whether to overlay a plot of the mesh edges.
    name : str
        The name to give measure in the colorbar.
    plotter: Plotter | None, optional
        The Plotting object to which to add this data. If None, the default
        (module-level) instance is used, by default None
    clear_plotter : bool, optional
        Whether to clear/reset the default Plotter instance, by default
        False
    subplot : tuple | None, optional
        If the Plotter is initialized with multiple subplots, specify with
        a tuple which sublot to plot in, by default None
    show : bool, optional
        Whether to show upon completion. Alternatively, call `.show()` on
        the returned Plotter `instance`. By default False
    **kwargs
        The remaining keyword arguments are passed to the
        `plotter.add_mesh` call.

    Returns
    -------
    Plotter
        An mpi-safe child of pyvista.Plotter.
    """
    # Forwards to plot_meshtags

    if mesh is None:
        raise ValueError(
            "A `mesh` must be supplied to plot measures. See help `plot_measure`."
        )

    meshtags = _get_measure_meshtags(measure, mesh)
    tagvalue = (
        measure.subdomain_id() if not measure.subdomain_id() == "everywhere" else None
    )
    kwargs = {"show_edges": False} | kwargs
    return plot_meshtags(
        meshtags,
        mesh=mesh,
        tagvalue=tagvalue,
        show_mesh=show_mesh,
        name=name,
        plotter=plotter,
        show=show,
        clear_plotter=clear_plotter,
        subplot=subplot,
        **kwargs,
    )


def _plot_feature_edges(
    plotter: pyvista.Plotter,
    grid: pyvista.UnstructuredGrid,
    options: dict = {"show_scalar_bar": False, "color": "black"},
    subdivisions: int = 4,
):
    surface = grid.separate_cells().extract_surface(nonlinear_subdivision=subdivisions)
    edges = surface.extract_feature_edges()
    plotter.add_mesh(edges, **options)


def _get_outline_meshtags(
    mesh: dolfinx.mesh.Mesh,
):
    tdim = mesh.topology.dim
    mesh.topology.create_entities(tdim - 1)
    mesh.topology.create_connectivity(tdim - 1, tdim)
    boundary_facets = dolfinx.mesh.exterior_facet_indices(mesh.topology)
    num_cells = mesh.topology.index_map(tdim - 1).size_local
    indices = np.arange(num_cells)
    values = np.zeros(num_cells, dtype=int)
    values[boundary_facets] = 1
    meshtags = dolfinx.mesh.meshtags(
        mesh,
        mesh.topology.dim - 1,
        indices,
        values,
    )
    return meshtags


def _get_partitioning_meshtags(mesh: dolfinx.mesh.Mesh) -> dolfinx.mesh.MeshTags:
    """
    Creates an element meshtags filled with the MPI ranks associated to
    that element
    """
    num_cells = mesh.topology.index_map(mesh.topology.dim).size_local
    meshtags = dolfinx.mesh.meshtags(
        mesh,
        mesh.topology.dim,
        np.arange(num_cells),
        np.ones(num_cells, dtype=int) * MPI.COMM_WORLD.rank,
    )
    return meshtags


def _get_measure_meshtags(
    measure: ufl.Measure, mesh: dolfinx.mesh.Mesh
) -> dolfinx.mesh.MeshTags:
    """
    Obtains the meshtags associated to an integration measure. Its values
    refer to the different integrable sub-measures.
    """
    if type(measure.subdomain_data()) is dolfinx.mesh.MeshTags:
        return measure.subdomain_data()
    num_cells = mesh.topology.index_map(mesh.topology.dim).size_local
    meshtags = dolfinx.mesh.meshtags(
        mesh, mesh.topology.dim, np.arange(num_cells), np.ones(num_cells)
    )
    return meshtags


def _interpolate_vector_DG(u: dolfinx.fem.Function):
    """
    Interpolate a vector-values field onto a DG superspace. For
    visualization of advanced FE spaces.
    """
    V = u.function_space
    domain = V.mesh
    gdim = domain.geometry.dim
    poldeg = V.element.basix_element.degree
    VDG = dolfinx.fem.functionspace(domain, ("Discontinuous Lagrange", poldeg, (gdim,)))
    return _interpolate(u, VDG)


def _interpolate(u: dolfinx.fem.Function, V: dolfinx.fem.FunctionSpace):
    """
    Basic interpolation helper.
    """
    u_new = dolfinx.fem.Function(V, name=u.name)
    u_new.interpolate(u)
    return u_new


def _compatible_scalar_u_warp(
    u: dolfinx.fem.Function, warp: dolfinx.fem.Function | bool
):
    """
    Ensures that the scalar u field and the warp field can be plotted on
    the same mesh. Essentially, the warp field is projected onto the
    functionspace of a vectorized u
    """
    V = u.function_space
    domain = V.mesh
    if V.element.basix_element.degree == 0:
        # DG0 functionspace can't be passed to plot.vtk_mesh
        V = dolfinx.fem.functionspace(domain, ("Discontinuous Lagrange", 1))
        u = _interpolate(u, V)

    if type(warp) == bool:
        return u, warp

    family_name = u.ufl_element().family_name
    discontinuous = u.ufl_element().discontinuous
    poldeg = V.element.basix_element.degree
    gdim = domain.geometry.dim

    if (
        warp.ufl_element().family_name != family_name
        or warp.function_space.element.basix_element.degree != poldeg
        or warp.ufl_element().discontinuous != discontinuous
    ):
        el = basix.ufl.element(
            family_name,
            domain.ufl_cell().cellname(),
            poldeg,
            shape=(gdim,),
            discontinuous=discontinuous,
        )
        Vwarp = dolfinx.fem.functionspace(domain, el)
        warp = _interpolate(warp, Vwarp)

    return u, warp

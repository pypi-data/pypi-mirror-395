# Copyright (C) 2025 Stein K.F. Stoter
#
# This file is part of pyvista4dolfinx
#
# SPDX-License-Identifier:    MIT

from mpi4py import MPI
import pyvista

__all__ = ["Plotter"]


class Plotter(pyvista.Plotter):
    _pv_doc = pyvista.Plotter.__doc__.split("\n", 1)[1].split("Examples", 1)[0]
    __doc__ = "An MPI-safe child of the `pyvista.Plotter` class. \n\n" + _pv_doc

    def __new__(cls, *args, **kwargs):
        if MPI.COMM_WORLD.rank == 0:
            return super().__new__(cls, *args, **kwargs)
        return PlotterEmpty()


class PlotterEmpty:
    """
    An empty mirror of the `pyvista.Plotter` class, automatically instanced
    on MPI ranks not equal 0 when `pyvista4dolfinx.Plotter` is instantiated.
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        for methodname in dir(pyvista.Plotter):
            if not methodname.startswith("_"):
                setattr(
                    instance,
                    methodname,
                    lambda *args, **kwargs: None,
                )
        return instance

    def __getattr__(self, name):
        """Handle any attribute access, including private methods."""
        return lambda *args, **kwargs: None

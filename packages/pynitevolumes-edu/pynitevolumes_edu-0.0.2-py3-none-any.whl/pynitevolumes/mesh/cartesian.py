#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for Cartesian meshes.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from pynitevolumes.mesh.base_struct import Mesh
from pynitevolumes.mesh.base_struct import Diamond
if TYPE_CHECKING:
    from typing import Literal
    from collections.abc import Sequence
    from numpy.typing import NDArray


class Cartesian:
    """Structured cartesian meshes.

    A cartesian meshe of a rectangle [a, b]x[c, d] can be meshed in a
    simple way by subdividing [a, b] into an increasing set of points
    x[i] and [c, d] into an increasing set of points y[j]. Then one can
    mesh by taking the vertices to be (x[i], y[j]) and for the mesh
    cells the quadrangular `Q_ij` ::

        [(x[i], y[j]), (x[i+1], y[j]), (x[i+1], y[j+1]), (x[i], y[j+1])]

    Parameters
    ----------
    subx, suby : int or array-like
        Subdivision of the x axis (resp. the y axis). If int then the
        horizontal (resp. the vertical) interval is subdivided in subx
        (resp. suby) equal parts. If array-like it must contain a finite
        increasing sequence of floats.
    AB, CD : tuple of float, optional
        Characterizes the intervals to be subdivided. If `subx` (resp.
        `suby`) is int, then AB=(a, b) (resp. CD=(c, d)). If `subx`
        (resp. `suby`) is array_like, then AB (resp. CD) has no purpose.
        The defaults are AB=(0.0, 1.0) and CD=(0.0, 1.0).
    k_c : (nx, ny) array_like of int, optional
        Numerotation for the centers of the grid. `k_c[i, j]` is the
        index attributed to the center of `Q_ij`. `nx` (resp. `ny`) is
        the number of subintervals in which the horizontal (resp.
        vertical) has been subdivided (see `subx`, `suby`). All integer
        between 0 and `nx*ny-1` must appear (uniquely) inside `k_c`.
        If not provided, the default numerotation is used: the centers
        are numbered from bottom-left to top-right in the
        lexicographical order: vertical-first, horizontal-second.
    k_v : (nx+1, ny+1) array_like of int, optional
        Numerotation for the vertices of the grid. `k_v[i, j]` is the
        index attributed to (x[i], y[j]). `nx` (resp. `ny`) is
        the number of subintervals in which the horizontal (resp.
        vertical) has been subdivided (see `subx`, `suby`). All integers
        between 0 and `(nx+1)*(ny+1)-1` must appear (uniquely) inside
        `k_v`. If not provided, the default numerotation is used: the
        vertices are numbered from bottom-left to top-right in the
        lexicographical order: vertical-first, horizontal-second.

    Attributes
    ----------
    box : tuple of float (a, b, c, d)
        Domain rectangle [a, b]x[c, d].
    nx : int
        Number of subintervals of [a, b].
    ny : int
        Number of subintervals of [c, d].
    xi : (nx+1,) numpy.ndarray of float
        Subdivision of [a, b].
    yj : (ny+1,) numpy.ndarray of float
        Subdivision of [c, d].
    k_c : (nx, ny) numpy.ndarray of float
        From `k_c`
    k_v : (nx+1, ny+1) numpy.ndarray of float
        From `k_v`
    """

    def __init__(self,
                 subx: int | NDArray[np.float64],
                 suby: int | NDArray[np.float64],
                 AB: Sequence[float] = (0.0, 1.0),
                 CD: Sequence[float] = (0.0, 1.0),
                 k_c: NDArray[np.int_] | None = None,
                 k_v: NDArray[np.int_] | None = None):
        """Create the Cartesian object."""
        if isinstance(subx, int):
            a, b = AB
            c, d = CD
            self.nx = subx
            self.xi = a+(b-a)/self.nx*np.arange(self.nx+1)
        else:
            subx = np.array(subx)
            self.nx = len(subx)-1
            a = np.min(subx)
            b = np.max(subx)
            self.xi = subx
        if isinstance(suby, int):
            self.ny = suby
            self.yj = c+(d-c)/self.ny*np.arange(self.ny+1)
        else:
            suby = np.array(suby)
            self.ny = len(suby)-1
            c = np.min(suby)
            d = np.max(suby)
            self.yj = suby
        self.box = a, b, c, d
        if k_c is not None:
            self.k_c = np.array(k_c, dtype='int')
        else:
            self.k_c = np.arange(self.nx*self.ny).reshape(self.nx, self.ny)
        if k_v is not None:
            self.k_v = np.array(k_v, dtype='int')
        else:
            self.k_v = np.arange((self.nx+1)*(self.ny+1)).reshape(self.nx+1,
                                                                  self.ny+1)

    def toMesh(self, period: Literal['None', 'bt', 'lr', 'both'] = 'None'
               ) -> Mesh:
        """Create a Mesh object from a Cartesian grid.

        Parameters
        ----------
        period : 'None', 'bt', 'lr', 'both', optional
            'bt' create a periodic relation between the bottom and top
            edges of the rectangle, 'lr' does the same between the left
            and right edges of the rectangle and 'both' does both
            simultaneously. The default is 'None'.

        Returns
        -------
        M : base_struct.Mesh
            The `Mesh` representation of the uniform mesh based on the
            grid.
        """
        conc = np.concatenate
        nx = self.nx
        ny = self.ny
        xi = self.xi
        yj = self.yj
        k_c = self.k_c
        k_v = self.k_v
        # Building centers
        ind_c = np.indices((nx, ny))
        centers = np.zeros((nx*ny, 2), dtype='float')
        centers[k_c] = np.stack(((xi[ind_c[0]]+xi[ind_c[0]+1])/2,
                                 (yj[ind_c[1]]+yj[ind_c[1]+1])/2),
                                axis=-1)

        # Building vertices
        ind_v = np.indices((nx+1, ny+1))
        vertices = np.zeros(((nx+1)*(ny+1), 2), dtype='float')
        vertices[k_v] = np.stack((xi[ind_v[0]], yj[ind_v[1]]), axis=-1)

        # Building edges
        ei_h = np.stack((k_v[:nx, 1:ny].ravel(), k_v[1:, 1:ny].ravel()))
        ei_v = np.stack((k_v[1:nx, :ny].ravel(), k_v[1:nx, 1:].ravel()))
        Ki_h = k_c[:, :-1].ravel()
        Li_h = k_c[:, 1:].ravel()
        Ki_v = k_c[:-1, :].ravel()
        Li_v = k_c[1:, :].ravel()

        eb_bot = np.stack((k_v[:nx, 0], k_v[1:, 0]))
        eb_top = np.stack((k_v[:nx, ny], k_v[1:, ny]))
        eb_lft = np.stack((k_v[0, :ny], k_v[0, 1:]))
        eb_rgt = np.stack((k_v[nx, :ny], k_v[nx, 1:]))
        Kb_bot = k_c[:, 0]
        Kb_top = k_c[:, -1]
        Kb_lft = k_c[0, :]
        Kb_rgt = k_c[-1, :]
        if period == 'None':
            ei = conc((ei_v, ei_h), axis=1)
            Ki = conc((Ki_v, Ki_h))
            Li = conc((Li_v, Li_h))
            eb = conc((eb_bot, eb_top, eb_lft, eb_rgt), axis=1)
            Kb = conc((Kb_bot, Kb_top, Kb_lft, Kb_rgt))
        elif period in {'tb', 'bt', 'vertical'}:
            ei = conc((ei_v, ei_h, eb_bot), axis=1)
            Ki = conc((Ki_v, Ki_h, k_c[:, 0]))
            Li = conc((Li_v, Li_h, k_c[:, -1]))
            eb = conc((eb_lft, eb_rgt), axis=1)
            Kb = conc((Kb_lft, Kb_rgt))
        elif period in {'lr', 'rl', 'horizontal'}:
            ei = conc((ei_v, ei_h, eb_lft), axis=1)
            Ki = conc((Ki_v, Ki_h, k_c[0, :]))
            Li = conc((Li_v, Li_h, k_c[-1, :]))
            eb = conc((eb_top, eb_bot), axis=1)
            Kb = conc((Kb_top, Kb_bot))
        elif period == 'both':
            ei = conc((ei_v, ei_h, eb_bot, eb_lft), axis=1)
            Ki = conc((Ki_v, Ki_h, k_c[:, 0], k_c[0, :]))
            Li = conc((Li_v, Li_h, k_c[:, -1], k_c[-1, :]))
            Kb = np.empty((0,), dtype='int')
            eb = np.empty((2, 0), dtype='int')
        M = Mesh(centers, vertices,
                 (Diamond({'c': np.stack((Ki, Li)), 'v': ei}),
                  Diamond({'c': Kb, 'v': eb})))
        return M

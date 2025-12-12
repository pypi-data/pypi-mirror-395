#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plot related functions for Mesh objects or discrete functions."""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
from warnings import warn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
if TYPE_CHECKING:
    from typing import Any
    from numpy.typing import NDArray, ArrayLike
    from matplotlib.quiver import Quiver
    from matplotlib.axes import Axes
    from matplotlib.collections import PolyCollection
    from ._array_types import IndexArray
    from .base_struct import Mesh
    from .md import PointType, MeshDescription
    from .disc import Discretizable


def _triangulate(M: Mesh, md: MeshDescription) -> tri.Triangulation:
    """Create a triangulation of a submesh.

    Creates a matplotlib.tri.Triangulation object for plotting purposes.

    Parameters
    ----------
    M : pynitevolumes.mesh.base_struct.Mesh
        The mesh to be triangulated.
    md : pynitevolumes.mesh.md.MeshDescription
        The submesh description.

    Returns
    -------
    matplotlib.tri.Triangulation
        The resulting triangulation.

    See Also
    --------
    pynitevolumes.mesh.md.MeshDescription, matplotlib.tri.Triangulation
    """
    offsets = {}
    current_offset = 0
    pos_in_order = []
    for pt in M.pointvars:
        if pt in md.used_points:
            offsets[pt] = current_offset
            current_offset += M.npoints_by_type[pt]
            pos_in_order.append(getattr(M, pt))
    triangles_list = []
    for c_tri in md.tri_seq:
        tri_indices = []
        for point in c_tri:
            Ind = point.index_from(M)
            tri_indices.append(Ind+offsets[point.attribute_name])
        triangles_list.append(np.stack(tri_indices, axis=-1))
    triangles = np.concatenate(triangles_list)
    P = np.concatenate(pos_in_order)
    return tri.Triangulation(P[:, 0], P[:, 1], triangles)


def _prepare_plotting(M: Mesh, md: MeshDescription, f: Discretizable
                      ) -> NDArray[np.float64]:
    """Prepare the display of a function."""
    feval = M.discretize(f, md)
    f_Part = []
    for c_tri in md.tri_seq:
        first = True
        for pt in c_tri.vp:
            ind = pt.index_from(M)
            if first:
                first = False
                fp = feval[pt.attribute_name][ind]
            else:
                fp += feval[pt.attribute_name][ind]
        f_Part.append(1/len(c_tri.vp)*fp)
    return np.concatenate(f_Part)


def pcolor_discrete(M: Mesh, md: MeshDescription, f: Discretizable,
                    **kwargs: Any) -> PolyCollection:
    """Create a pseudocolor plot for values on a submesh of Mesh.

    Parameters
    ----------
    M : base_struct.Mesh
        Underlying Mesh structure.
    md : md.MeshDescription
        Particular submesh on which `f` must be evaluated.
    f : disc.Discretizable
        The object to be evaluated by `M.evaluate`

    Keyword Arguments
    -----------------
    ax : matplotlib.axes.Axes
        Axes in which to plot. If not present, uses current axes.
    other_parameters
        Remaining keyword arguments are passed to
        `matplotlib.pyplot.tripcolor`.

    Returns
    -------
    matplotlib.collections.PolyCollection
        See `matplotlib.pyplot.tripcolor` for details.

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    matplotlib.pyplot.tripcolor

    Notes
    -----
    The function creates `T` a `matplotlib.tri.Triangulation` object
    and computes values c from `f` on `T` and then calls

    .. code-block:: python

        matplotlib.pyplot.tripcolor(T, c, **other_parameters)

    so pass all other arguments and keyword arguments in accordance with
    `matplotlib.pyplot.tripcolor` signature.
    """
    ax = kwargs.pop('ax', None)
    if 'shading' in kwargs and kwargs['shading'] != 'flat':
        warn("The 'shading' keyword argument cannot be different from 'flat'.")
        del kwargs['shading']
    if ax is not None:
        plt.sca(ax)
    T = _triangulate(M, md)
    fd = _prepare_plotting(M, md, f)
    result: PolyCollection = plt.tripcolor(T, fd, shading='flat', **kwargs)
    return result


def contour_discrete(M: Mesh, md: MeshDescription,
                     f: Discretizable,
                     levels: int | ArrayLike | None = None,
                     **kwargs: Any) -> tri.TriContourSet:
    """Draw contour lines on a Mesh.

    Parameters
    ----------
    M : base_struct.Mesh
        Underlying Mesh structure.
    md : md.MeshDescription
        Particular submesh on which `f` must be evaluated.
    f : disc.Discretizable
        Object to be evaluated by `M.evaluate`
    levels : int or array_like or None, default is None.
        Determines the number and positions of the contour lines /
        regions. See `matplotlib.pyplot.tricontour` for details.

    Keyword Arguments
    -----------------
    ax : matplotlib.axes.Axes
        Axes in which to plot. If not present, uses current axes.
    other_parameters
        Remaining keyword arguments are passed to
        `matplotlib.pyplot.tricontour`.

    Returns
    -------
    matplotlib.tri.TriContourSet

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    matplotlib.pyplot.tricontour

    Notes
    -----
    The function collects `X`, `Y` from the value points of `md` and
    from `M`, `Z` from the discretization of `f` on `md` and then calls

    .. code-block:: python

        matplotlib.pyplot.tricontour(X, Y, Z, levels,
                                     **other_parameters)

    so pass all keyword arguments in accordance with
    `matplotlib.pyplot.tricontour` signature.
    """
    ax = kwargs.pop('ax', None)
    if ax is not None:
        plt.sca(ax)
    X = []
    Y = []
    Z = []
    fd = M.discretize(f, md)
    for pt in md.used_centers:
        X.append(getattr(M, pt)[:, 0])
        Y.append(getattr(M, pt)[:, 1])
        Z.append(fd[pt])
    result: tri.TriContourSet = plt.tricontour(np.concatenate(X),
                                               np.concatenate(Y),
                                               np.concatenate(Z),
                                               levels=levels, **kwargs)
    return result


def quiver_discrete(M: Mesh, md: MeshDescription,
                    f: Discretizable,
                    g: Discretizable,
                    C: ArrayLike | None = None,
                    **kwargs: Any) -> Quiver:
    """Plot a 2D field of arrows on a Mesh.

    Parameters
    ----------
    M : base_struct.Mesh
        Underlying Mesh structure.
    md : md.MeshDescription
        Particular submesh on which `f` must be evaluated.
    f : disc.Discretizable
        Object to be evaluated by `M.evaluate` to obtain the horizontal
        value of the arrow.
    g : disc.Discretizable
        Object to be evaluated by `M.evaluate` to obtain the vertical
        value of the arrow.
    C : 1D array_like or None, default is None.
        Numeric data that defines the arrow colors. If `C` is not
        `None`, it must must be a 1D array-like whose length must be
        equal to `len(md.used_centers)`.

    Keyword Arguments
    -----------------
    ax : matplotlib.axes.Axes
        Axes in which to plot. If not present, uses current axes.
    other_parameters
        Remaining keyword arguments are passed to
        `matplotlib.pyplot.tricontour`.

    Returns
    -------
    matplotlib.quiver.Quiver

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    matplotlib.pyplot.quiver

    Notes
    -----
    The function collects `X`, `Y` from the value points of `md` and
    from `M`, `U` and `V` from the discretization of  `f` and `g` on
    `md` and then calls

    .. code-block:: python

        matplotlib.pyplot.quiver(X, Y, U, V, C, **other_parameters)

    so pass all keyword arguments in accordance with
    `matplotlib.pyplot.quiver` signature.
    """
    ax = kwargs.pop('ax', None)
    if ax is not None:
        plt.sca(ax)
    X = []
    Y = []
    U = []
    V = []
    fd = M.discretize(f, md)
    gd = M.discretize(g, md)
    for pt in md.used_centers:
        X.append(getattr(M, pt)[:, 0])
        Y.append(getattr(M, pt)[:, 1])
        U.append(fd[pt])
        V.append(gd[pt])
    if C is None:
        return plt.quiver(np.concatenate(X), np.concatenate(Y),
                          np.concatenate(U), np.concatenate(V),
                          **kwargs)
    else:
        return plt.quiver(np.concatenate(X), np.concatenate(Y),
                          np.concatenate(U), np.concatenate(V),
                          C, **kwargs)


class _PlottingProperties(TypedDict, total=False):
    offset: float | tuple[float, float]
    ecol_inner: str
    ecol_bnd: str
    cent: bool | str
    cent_txt: bool
    vert: bool | str
    vert_txt: bool
    centers_name: str
    vertices_name: str
    edges_num: bool


_defaultpm: _PlottingProperties = {
    'offset': 0.025,
    'ecol_inner': 'b',
    'ecol_bnd': 'm',
    'cent': 'ko',
    'cent_txt': False,
    'vert': 'sm',
    'vert_txt': False,
    'centers_name': 'K',
    'vertices_name': 'V',
    'edges_num': False}


def _sanitize_plotmesh_kwargs(d: dict[str, Any]) -> _PlottingProperties:
    res: _PlottingProperties = _defaultpm
    if 'offset' in d:
        offset = d['offset']
        if isinstance(offset, float):
            res['offset'] = offset
        elif isinstance(offset, tuple):
            try:
                hx, hy = offset
            except ValueError:
                raise TypeError("If given as tuple, 'offset' kwarg should be" +
                                "exactly two float")
            if not (isinstance(hx, float) and isinstance(hy, float)):
                raise TypeError("If given as tuple, 'offset' kwarg should be" +
                                "exactly two float")
            else:
                res['offset'] = offset
        else:
            TypeError("'offset' kwarg should be a float or a tuple of " +
                      "exactly two float")
    if 'ecol_inner' in d:
        ecol_inner = d['ecol_inner']
        if isinstance(ecol_inner, str):
            res['ecol_inner'] = ecol_inner
        else:
            raise TypeError("'ecol_inner' kwarg should be a formatting string")
    if 'ecol_bnd' in d:
        ecol_bnd = d['ecol_bnd']
        if isinstance(ecol_bnd, str):
            res['ecol_bnd'] = ecol_bnd
        else:
            raise TypeError("'ecol_bnd' kwarg should be a formatting string")
    if 'cent' in d:
        cent = d['cent']
        if isinstance(cent, (bool, str)):
            res['cent'] = cent
        else:
            raise TypeError("'cent' kwarg should be a boolean or a "
                            + "formatting string")
    if 'cent_txt' in d:
        cent_txt = d['cent_txt']
        if isinstance(cent_txt, bool):
            res['cent_txt'] = cent_txt
        else:
            raise TypeError("'cent_txt' kwarg should be boolean")
    if 'vert' in d:
        vert = d['vert']
        if isinstance(vert, (bool, str)):
            res['vert'] = vert
        else:
            raise TypeError("'vert' kwarg should be a boolean or a "
                            + "formatting string")
    if 'vert_txt' in d:
        vert_txt = d['vert_txt']
        if isinstance(vert_txt, bool):
            res['vert_txt'] = vert_txt
        else:
            raise TypeError("'vert_txt' kwarg should be boolean")
    if 'centers_name' in d:
        centers_name = d['centers_name']
        if isinstance(centers_name, str):
            res['centers_name'] = centers_name
        else:
            raise TypeError("'centers_name' kwarg should be a string")
    if 'vertices_name' in d:
        vertices_name = d['vertices_name']
        if isinstance(vertices_name, str):
            res['vertices_name'] = vertices_name
        else:
            raise TypeError("'vertices_name' kwarg should be a string")
    if 'edges_num' in d:
        edges_num = d['edges_num']
        if isinstance(edges_num, bool):
            res['edges_num'] = edges_num
        else:
            raise TypeError("'edges_num' kwarg should be a boolean")
    return res


def plotmesh(M: Mesh, md: MeshDescription, **kwargs: Any) -> Axes:
    """Plot a submesh of a mesh.

    Parameters
    ----------
    M : base_struct.Mesh
        The instance containing the mesh.
    md : md.MeshDescription
        Submesh description.

    Keyword Arguments
    -----------------
    ax : matplotlib.axes.Axes
        Axes in which to plot.
    offset : float or (float, float)
        Offset to use to write the name of a point type besides
        the point type marker. If a single float `offset` is the
        percentage of width or height to use. If tuple of float they
        are the absolute horizontal and vertical offset.
        The default is the single float 0.025.
    ecol_inner : str, default 'b'
        String formatter for the plotting of inner edges.
    ecol_bnd : str, default 'm'
        String formatter for the plotting of boundary edges.
    cent : bool or str, default 'ko'
        If `False`, nothing is displayed at the position of the
        centers of the submesh. If `True` the default value is used.
        Otherwise the string formatter of the marker.
    cent_txt : bool, default is False
        Set to `True` to trigger the plotting of the names of the
        centers besides the marker. No effect if `cent` is `False`.
    vert : bool or str, default 'sm'
        If `False`, nothing is displayed at the position of the
        vertices of the submesh. If `True` the default value is used.
        Otherwise the string formatter of the marker.
    vert_txt : bool, default is False
        Set to `True` to trigger the plotting of the names of the
        vertices besides the marker. No effect if `vert`is `False`.
    centers_name : str, default 'K'
        Text to use as name for the **primal** centers.
    vertices_name : str, default 'V'
        Text to use as name for the **primal** vertices.
    edges_num : bool, default is False
        Set to `True` to trigger the plotting of the edge number at the
        middle of the edge.
    details : dict[str, Any] or 'none' or 'all'
        Configuration parameters can be passed as a batch as a
        dictionary, `'none'` sets all possible parameters to `False` and
        `'all'` sets all possible parameters to `True`. Note that values
        set by `details` override individual keyword arguments.
    line_kwargs, text_kwargs : dict[str, Any]
        Dictionaries passed as keyword arguments to respectively
        `matplotlib.axes.Axes.plot` and `matplotlib.axes.Axes.text` so
        see the documentation there for more information.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes where the plot occured

    See Also
    --------
    matplotlib.axes.Axes.plot, matplotlib.axes.Axes.text

    Warnings
    --------
    In this function `cent` and `vert` refer to the points chosen as
    "centers" and "vertices" in the
    `pynitevolume.mesh.md.MeshDescription` while `centers` and
    `vertices` refer to the attributes of the same name in `M`.
    """
    mx, Mx, my, My = M.getbox()
    ax: Axes = kwargs.pop('ax', plt.gca())
    viewed: dict[str, dict[str, set[IndexArray]]] = {'cent': {}, 'vert': {}}
    names: dict[str, str] = {}
    draw_i: set[tuple[PointType, PointType]] = set()
    draw_b: set[tuple[PointType, PointType]] = set()

    def update[T](a: T, b: T, draw: set[tuple[T, T]]) -> None:
        if (a, b) not in draw and (b, a) not in draw:
            draw.add((a, b))

    for c_tri in md.tri_seq:
        for pt in c_tri.vp:
            if pt.attribute_name not in viewed['cent']:
                viewed['cent'][pt.attribute_name] = set()
                names[pt.attribute_name] = repr(pt)
            viewed['cent'][pt.attribute_name].update(pt.index_from(M))
        for pt in c_tri.comp:
            if pt.attribute_name not in viewed['vert']:
                viewed['vert'][pt.attribute_name] = set()
                names[pt.attribute_name] = repr(pt)
            viewed['vert'][pt.attribute_name].update(pt.index_from(M))
        if len(c_tri.vp) == 3:
            v0, v1, v2 = c_tri.vp
            for (pt0, pt1) in {(v0, v1), (v0, v2), (v1, v2)}:
                if pt0.on_b and pt1.on_b:
                    update(pt0, pt1, draw_b)
                else:
                    update(pt0, pt1, draw_i)
        if len(c_tri.vp) == 2:
            c0, c1 = c_tri.vp
            v = c_tri.comp[0]
            for pt in {c0, c1}:
                if pt.on_b and v.on_b:
                    update(pt, v, draw_b)
                else:
                    update(pt, v, draw_i)
            if c0.on_b and c1.on_b:
                update(c0, c1, draw_b)
        if len(c_tri.vp) == 1:
            c = c_tri.vp[0]
            v0, v1 = c_tri.comp
            if v0.on_b and v1.on_b:
                update(v0, v1, draw_b)
            else:
                update(v0, v1, draw_i)
            for v in {v0, v1}:
                if v.on_b and c.on_b:
                    update(v, c, draw_b)
    to_draw: list[tuple[NDArray[np.float64], NDArray[np.float64], str]] = []
    to_write: list[tuple[float, float, str]] = []
    details = kwargs.get('details', {})
    pm = _sanitize_plotmesh_kwargs(kwargs)
    if details == 'none':
        pm['cent'] = False
        pm['vert'] = False
        pm['cent_txt'] = False
        pm['vert_txt'] = False
        pm['edges_num'] = False
    elif details == 'all':
        pm['cent'] = True
        pm['vert'] = True
        pm['cent_txt'] = True
        pm['vert_txt'] = True
        pm['edges_num'] = True
    else:
        pm.update(details)
    for part in {'inner', 'bnd'}:
        if part == 'inner':
            draw = draw_i
            ec = pm['ecol_inner']
        else:
            draw = draw_b
            ec = pm['ecol_bnd']

        for (pt0, pt1) in draw:
            P0 = getattr(M, pt0.attribute_name)[pt0.index_from(M)]
            X0, Y0 = P0[:, 0], P0[:, 1]
            P1 = getattr(M, pt1.attribute_name)[pt1.index_from(M)]
            X1, Y1 = P1[:, 0], P1[:, 1]
            X = np.stack((X0, X1))
            Y = np.stack((Y0, Y1))
            to_draw.append((X, Y, ec))
    h = pm['offset']
    if isinstance(h, tuple):
        hx, hy = h
    else:
        hx, hy = h*(Mx-mx), h*(My-my)
    for basic in {'cent', 'vert'}:
        cc_raw: bool | str = pm[basic]  # type: ignore[literal-required]
        cc: str
        if isinstance(cc_raw, bool):
            if cc_raw:
                cc = _defaultpm[basic]  # type: ignore[literal-required]
            else:
                cc = ''
        else:
            cc = cc_raw
        if cc:
            for k, edges in viewed[basic].items():
                Pk: NDArray[np.float64] = getattr(M, k)[list(edges)]
                to_draw.append((Pk[:, 0], Pk[:, 1], cc))
        if pm[f'{basic}_txt']:  # type: ignore[literal-required]
            for k, edges in viewed[basic].items():
                Pk = getattr(M, k)[list(edges)]
                if k in {'centers', 'vertices'}:
                    name = pm[f'{k}_name']  # type: ignore[literal-required]
                else:
                    name = names[k]
                n = Pk.shape[0]
                for i in range(n):
                    if name[-1] == '$':
                        name_i = f'{name[:-1]}_{{{i}}}$'
                    else:
                        name_i = f'{name}$_{{{i}}}$'
                    to_write.append((Pk[i, 0]+hx, Pk[i, 1]-hy, name_i))
    if pm['edges_num']:
        Cin = (M.vertices[M.diam_i.v[0]]+M.vertices[M.diam_i.v[1]])/2
        Cbnd = (M.vertices[M.diam_b.v[0]]+M.vertices[M.diam_b.v[1]])/2
        for s in range(M.nin):
            to_write.append((Cin[s, 0], Cin[s, 1], str(s)))
        for s in range(M.nbnd):
            to_write.append((Cbnd[s, 0], Cbnd[s, 1], str(s)))
    try:
        plt_kw = kwargs.get('line_kwargs', {})
        txt_kw = kwargs.get('text_kwargs', {})
        for X, Y, fmt in to_draw:
            ax.plot(X, Y, fmt, **plt_kw)
        for txt in to_write:
            ax.text(*txt, **txt_kw)
    except AttributeError as plt_err:
        warn('Something went wrong with the keywords arguments because '
             + f'matplotlib returned the error\n{plt_err}\n We are '
             + 'dropping the control of the plot')
        for X, Y, fmt in to_draw:
            ax.plot(X, Y, fmt)
        for txt in to_write:
            ax.text(*txt)
    return ax

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module with predefined TPFA schemes for Delaunay admissible mesh.

This module provides functions to build various approximations using the
Finite Volumes framework for basic linear operators in 2D. They all
use the `tpfa_struct.TPFAStruct` geometry of a mesh.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from itertools import chain
import numpy as np
from pynitevolumes.mesh.md import PRIMAL, DIAM
from pynitevolumes.tools.geometry import multscalar as ms
from .bc_data import DirichletBC, NeumannBC, RobinBC, BCStructure, split_inflow
if TYPE_CHECKING:
    from typing import Literal, Any
    from collections.abc import Callable
    from ...mesh._array_types import IndexArray, ValueArray
    from ...mesh.disc import Discretizable
    from .bc_data import BoundaryCondition
    from .tpfa_struct import TPFAStruct


# %% Volumic terms
#    =============


def volumic(E: TPFAStruct, q: Discretizable) -> tuple[list[IndexArray],
                                                      list[IndexArray],
                                                      list[ValueArray]]:
    """Approximation of a zeroth order term using Finite Volumes.

    Parameters
    ----------
    E : tpfa_struct.TPFAStruct
        Mesh on which the approximation is done.
    q : pynitevolumes.mesh.disc.Discretizable
        Object containing coefficient of the volumic term. It is passed
        to `E.evaluate`.

    Returns
    -------
    row_mat : list of numpy.ndarray of int
        The list contain only one element which is the array of numbers
        from 0 to `E.nvol`.
    col_mat : list of numpy.ndarray of int
        The list contain only one element which is the array of numbers
        from 0 to `E.nvol`.
    dat_mat : list of numpy.ndarray of float
        The list contain only one element which is the array of values
        of `q` evaluated on `E.centers` multiplied by `E.vol`.

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    scipy.sparse.csr_array

    Notes
    -----
    The return value as a tuple of lists `row_mat`, `col_mat`, `dat_mat`
    is set up to work in conjunction with the `scipy.sparse` module.
    Precisely, the expected follow up to this function is something like

    .. code-block:: python

       scipy.sparse.csr_array((np.concatenate(dat_mat),
                               (np.concatenate(row_mat),
                                np.concatenate(col_mat))))

    to build the (E.nvol, E.nvol) matrix M such that MU is the Finite
    Volumes approximation of qu, where u is the unknown function.

    """
    row_mat = np.arange(E.nvol)
    col_mat = np.arange(E.nvol)
    val = E.discretize(q, PRIMAL)
    return [row_mat], [col_mat], [E.vol*val['centers']]

# %% Source term
#    ===========


def source(E: TPFAStruct, f: Discretizable) -> tuple[list[IndexArray],
                                                     list[ValueArray]]:
    """Approximation of source using standard Finite Volumes scheme.

    Parameters
    ----------
    E : tpfa_struct.TPFAStruct
        Mesh on which the approximation is done.
    f : pynitevolumes.mesh.disc.Discretizable
        Object containing the source term. It is passed to `E.evaluate`.

    Returns
    -------
    row_rhs : list of numpy.ndarray of int
        The list contain only one element which is the array of numbers
        from 0 to `E.nvol`.
    dat_rhs : list of numpy.ndarray of float
        The list contain only one element which is the array of values
        of `f` evaluated on `E.centers` multiplied by `E.vol`.

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    scipy.sparse.csc_array

    Notes
    -----
    The return value as a tuple of lists `row_rhs`, `dat_rhs` is set up
    to work in conjunction with the scipy.sparse module. Precisely, the
    expected follow up to this function is something like

    .. code-block:: python

       scipy.sparse.csc_array((np.concatenate(dat_rhs),
                               (np.concatenate(row_rhs),
                                np.concatenate(np.ones(len(row_rhs))))))

    to build the (E.nvol, 1) matrix b which is the Finite Volume
    approximation of f.
    """
    row_rhs = np.arange(E.nvol)
    val = E.discretize(f, PRIMAL)
    return [row_rhs], [E.vol*val['centers']]

# %% Diffusion
#    =========


def diff_i(E: TPFAStruct, Ai: ValueArray) -> tuple[list[IndexArray],
                                                   list[IndexArray],
                                                   list[ValueArray]]:
    """Inner edge contributions of the TPFA diffusion scheme."""
    K, L = E.diam_i.c[0], E.diam_i.c[1]
    row_mat = [K, L, K, L]
    col_mat = [K, K, L, L]
    val_i = E.len_i*Ai/E.dKL_i
    dat_mat = [val_i, -val_i, -val_i, val_i]
    return row_mat, col_mat, dat_mat


def diff_b_mat(E: TPFAStruct, Ab: ValueArray,
               bnd: BCStructure
               ) -> tuple[list[IndexArray],
                          list[IndexArray],
                          list[ValueArray]]:
    """Boundary edge contributions to the TPFA diffusion matrix."""
    Kb = E.diam_b.c
    row_mat = []
    col_mat = []
    dat_mat = []
    for bcpiece in chain(bnd.uncond_others, bnd.inflow_others):
        if isinstance(bcpiece, DirichletBC):
            we = bcpiece.w
            row_mat.append(Kb[we])
            col_mat.append(Kb[we])
            val_b = E.len_b[we]/E.dKs_b[we]*Ab[we]
            dat_mat.append(val_b)
        if isinstance(bcpiece, RobinBC):
            we = bcpiece.w
            a = bcpiece.a
            b = bcpiece.b
            row_mat.append(Kb[we])
            col_mat.append(Kb[we])
            val_b = E.len_b[we]/(a*E.dKs_b[we]+b)*Ab[we]
            dat_mat.append(a*val_b)
    return row_mat, col_mat, dat_mat


def diff_b_rhs(E: TPFAStruct, Ab: ValueArray,
               bnd: BCStructure
               ) -> tuple[list[IndexArray],
                          list[ValueArray]]:
    """Boundary edge contributions to the TPFA diffusion rhs."""
    Kb = E.diam_b.c
    row_rhs = []
    dat_rhs = []
    for bcpiece in chain(bnd.uncond_others, bnd.inflow_others):
        if isinstance(bcpiece, DirichletBC):
            we = bcpiece.w
            us = bcpiece.data
            val_b = E.len_b[we]/E.dKs_b[we]*Ab[we]
            row_rhs.append(Kb[we])
            dat_rhs.append(val_b*us)
        if isinstance(bcpiece, NeumannBC):
            we = bcpiece.w
            gs = bcpiece.data
            row_rhs.append(Kb[we])
            dat_rhs.append(E.len_b[we]*Ab[we]*gs)
        if isinstance(bcpiece, RobinBC):
            we = bcpiece.w
            gs = bcpiece.data
            a = bcpiece.a
            b = bcpiece.b
            val_b = E.len_b[we]/(a*E.dKs_b[we]+b)*Ab[we]
            row_rhs.append(Kb[we])
            dat_rhs.append(val_b*gs)
    return row_rhs, dat_rhs


def diffusion_matrix(E: TPFAStruct, A: Discretizable,
                     bnd: BCStructure
                     ) -> tuple[list[IndexArray],
                                list[IndexArray],
                                list[ValueArray]]:
    r"""Diffusion matrix using the TPFA standard scheme.

    Approximation of :math:`-\mathrm{div}(A\nabla u)=0` (where :math:`u`
    is the unknown function) by the TPFA standard scheme.

    Parameters
    ----------
    E : tpfa_struct.TPFAStruct
        Mesh on which the approximation is done.
    A : pynitevolumes.mesh.disc.Discretizable
        Object containing diffusion coefficient. It is passed
        to `E.evaluate`. Must be scalar-valued.
    bnd: bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    row_mat, col_mat, dat_mat
        `row_mat`, `col_mat` contain the  coordinates of non-zero
        coefficients and `dat_mat` the values of the TPFA Finite Volumes
        approximation matrix for the diffusion..

    Warning
    -------
    This function is based on the TPFA approximation of the diffusion
    flux which uses at its core the hypothesis that the underlying mesh
    satisfies the Delaunay condition. If this is not true the resulting
    scheme is not consistent. One can check the Delaunay condition with
    the functions pynitevolumes.scheme.tpfa.check_orthogonality and
    pynitevolumes.scheme.tpfa.check_centers_order.
    It also only works for isotropic diffusion.

    See Also
    --------
    diffusion_rhs
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    tpfa_struct.check_orthogonality
    tpfa_struct.check_centers_order

    Notes
    -----
    The return value as tuples of lists `row_mat`, `col_mat`, `dat_mat`
    (and `row_rhs`, `dat_rhs` for the parallel function `diffusion_rhs`)
    is set up to work in conjunction with the `scipy.sparse` module.
    Precisely the expected follow up to this function is something like

    .. code-block:: python

       scipy.sparse.csr_array((np.concatenate(dat_mat),
                               (np.concatenate(row_mat),
                                np.concatenate(col_mat))))

    to build the `(E.nvol, E.nvol)` matrix :math:`M` such that
    :math:`MU` is the TPFA Finite Volumes approximation of
    :math:`-\mathrm{div}(A\nabla u)` where :math:`u` is the unknown
    function.
    """
    Ad = E.discretize(A, DIAM)
    row_i, col_i, dat_i = diff_i(E, Ad['xs_i'])
    row_b, col_b, dat_b = diff_b_mat(E, Ad['xs_b'], bnd)
    return row_i+row_b, col_i+col_b, dat_i+dat_b


def diffusion_rhs(E: TPFAStruct, A: Discretizable,
                  bnd: BCStructure
                  ) -> tuple[list[IndexArray],
                             list[ValueArray]]:
    r"""Diffusion rhs using the TPFA standard scheme.

    Approximation of :math:`-\mathrm{div}(A\nabla u)=0` (where :math:`u`
    is the unknown function) by the TPFA standard scheme.

    Parameters
    ----------
    E : TPFAStruct
        Mesh on which the approximation is done.
    A : scalar or callable or array_like or dict
        Object containing diffusion coefficient. It is passed
        to `E.evaluate`. Must evaluate to a scalar.
    bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    (row_rhs, dat_rhs)
        `row_rhs`, `dat_rhs` contain the coordinate of non-zero
        coefficients of the contribution to the right-hand side due to
        inhomogneous boundary conditions.

    Warning
    -------
    This function is based on the TPFA approximation of the diffusion
    flux which uses at its core the hypothesis that the underlying mesh
    satisfies the Delaunay condition. If this is not true the resulting
    scheme is not consistent. One can check the Delaunay condition with
    the functions pynitevolumes.scheme.tpfa.check_orthogonality and
    pynitevolumes.scheme.tpfa.check_centers_order.
    It also only works for isotropic diffusion.

    See Also
    --------
    diffusion_matrix
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    tpfa_struct.check_orthogonality
    tpfa_struct.check_centers_order

    Notes
    -----
    The return value as tuples of lists `row_rhs`, `dat_rhs` (and
    `row_mat`, `col_mat`, `dat_mat` for the parallel function
    `diffusion_matrix`) is set up to work in conjunction with the
    `scipy.sparse` module. Precisely the expected follow up to this
    function is something like

    .. code-block:: python

       scipy.sparse.csc_array((np.concatenate(dat_rhs),
                               (np.concatenate(row_rhs),
                                np.concatenate(np.ones(len(row_rhs))))))

    to build the `(E.nvol, 1)` matrix b which contains the boundary
    contributions to the TPFA Finite  Volumes approximation of
    :math:`-\mathrm{div}(A\nabla u)=0` where :math:`u` is the unknown
    function.
    """
    Ad = E.discretize(A, DIAM)
    rrhs, drhs = diff_b_rhs(E, Ad['xs_b'], bnd)
    return rrhs, drhs

# %% Convection
#    ==========


def conv_center_i(E: TPFAStruct, flux_i: ValueArray
                  ) -> tuple[list[IndexArray],
                             list[IndexArray],
                             list[ValueArray]]:
    """Inner edge contributions of the centered advection scheme."""
    K, L = E.diam_i.c[0], E.diam_i.c[1]
    row_mat = [K, L, K, L]
    col_mat = [K, K, L, L]
    val_i = flux_i/2
    dat_mat = [val_i, -val_i, val_i, -val_i]
    return row_mat, col_mat, dat_mat


class _ConvectionBC[T: BoundaryCondition]:
    """Structure of boundary condition for convection."""

    def __init__(self,
                 conv_mat: Callable[[TPFAStruct, ValueArray, T], ValueArray],
                 conv_rhs: Callable[[TPFAStruct, ValueArray, T], ValueArray]):
        self._conv_mat = conv_mat
        self._conv_rhs = conv_rhs

    def get_mat(self, E: TPFAStruct, flux: ValueArray, bcpiece: T
                ) -> ValueArray:
        """Matrix data for convection boundary condition."""
        return self._conv_mat(E, flux, bcpiece)

    def get_rhs(self, E: TPFAStruct, flux: ValueArray, bcpiece: T
                ) -> ValueArray:
        """Right-hand side data for convection boundary condition."""
        return self._conv_rhs(E, flux, bcpiece)


def _conv_mat_dirichlet(E: TPFAStruct,
                        flux: ValueArray,
                        bcpiece: DirichletBC
                        ) -> ValueArray:
    return 0.5*flux


def _conv_rhs_dirichlet(E: TPFAStruct,
                        flux: ValueArray,
                        bcpiece: DirichletBC
                        ) -> ValueArray:
    us = bcpiece.data
    return -0.5*flux*us


conv_dir: _ConvectionBC[DirichletBC] = _ConvectionBC(_conv_mat_dirichlet,
                                                     _conv_rhs_dirichlet)


def _conv_mat_neumann(E: TPFAStruct,
                      flux: ValueArray,
                      bcpiece: NeumannBC
                      ) -> ValueArray:
    return flux


def _conv_rhs_neumann(E: TPFAStruct,
                      flux: ValueArray,
                      bcpiece: NeumannBC
                      ) -> ValueArray:
    we = bcpiece.w
    gs = bcpiece.data
    return -0.5*flux*E.dKs_b[we]*gs


conv_neu: _ConvectionBC[NeumannBC] = _ConvectionBC(_conv_mat_neumann,
                                                   _conv_rhs_neumann)


def _conv_mat_robin(E: TPFAStruct,
                    flux: ValueArray,
                    bcpiece: RobinBC
                    ) -> ValueArray:
    we = bcpiece.w
    a = bcpiece.a
    b = bcpiece.b
    val_b = flux/(a*E.dKs_b[we]+b)
    return (b+0.5*a*E.dKs_b[we])*val_b


def _conv_rhs_robin(E: TPFAStruct,
                    flux: ValueArray,
                    bcpiece: RobinBC
                    ) -> ValueArray:
    we = bcpiece.w
    gs = bcpiece.data
    a = bcpiece.a
    b = bcpiece.b
    val_b = flux/(a*E.dKs_b[we]+b)
    return -0.5*val_b*E.dKs_b[we]*gs


conv_rob: _ConvectionBC[RobinBC] = _ConvectionBC(_conv_mat_robin,
                                                 _conv_rhs_robin)

KNOWN_CONV_BC: dict[type[BoundaryCondition], _ConvectionBC[Any]] = {
    DirichletBC: conv_dir, NeumannBC: conv_neu, RobinBC: conv_rob}


def conv_center_b_mat(E: TPFAStruct, flux_b: ValueArray,
                      bnd: BCStructure
                      ) -> tuple[list[IndexArray],
                                 list[IndexArray],
                                 list[ValueArray]]:
    """Boundary edge contributions to the advection scheme."""
    Kbnd = E.diam_b.c
    row_mat = []
    col_mat = []
    dat_mat = []
    bc_i: list[BoundaryCondition] = []
    for bcpiece in bnd.inflow_others:
        wo, bcpiece_in = split_inflow(bcpiece, flux_b)
        row_mat.append(Kbnd[wo])
        col_mat.append(Kbnd[wo])
        dat_mat.append(flux_b[wo])
        bc_i.append(bcpiece_in)
    for bcpiece in chain(bnd.uncond_others, bc_i):
        if (bnd_type := type(bcpiece)) in KNOWN_CONV_BC:
            conv_bc = KNOWN_CONV_BC[bnd_type]
            row_mat.append(Kbnd[bcpiece.w])
            col_mat.append(Kbnd[bcpiece.w])
            dat_mat.append(conv_bc.get_mat(E, flux_b[bcpiece.w], bcpiece))
    return row_mat, col_mat, dat_mat


def conv_center_b_rhs(E: TPFAStruct, flux_b: ValueArray,
                      bnd: BCStructure
                      ) -> tuple[list[IndexArray],
                                 list[ValueArray]]:
    """Boundary edge contributions to the advection scheme."""
    Kbnd = E.diam_b.c
    row_rhs = []
    dat_rhs = []
    bc_i: list[BoundaryCondition] = []
    for bcpiece in bnd.inflow_others:
        _, bcpiece_in = split_inflow(bcpiece, flux_b)
        bc_i.append(bcpiece_in)
    for bcpiece in chain(bnd.uncond_others, bc_i):
        if (bnd_type := type(bcpiece)) in KNOWN_CONV_BC:
            conv_bc = KNOWN_CONV_BC[bnd_type]
            row_rhs.append(Kbnd[bcpiece.w])
            dat_rhs.append(conv_bc.get_rhs(E, flux_b[bcpiece.w], bcpiece))
    return row_rhs, dat_rhs


def centered_diff(s: ValueArray) -> ValueArray:
    """Numerical diffusion added by the centered scheme."""
    return np.zeros(np.atleast_1d(s).shape)


def upwind_diff(s: ValueArray) -> ValueArray:
    """Numerical diffusion added by the upwind scheme."""
    return np.abs(s)/2


PREDEF_CONV_DIFF = {'upwind': upwind_diff,
                    'centered': centered_diff}


def convection_matrix(E: TPFAStruct, v: Discretizable,
                      bnd: BCStructure,
                      scheme: Literal['upwind', 'centered'] = 'upwind'
                      ) -> tuple[list[IndexArray],
                                 list[IndexArray],
                                 list[ValueArray]]:
    r"""Convection matrix using a TPFA scheme.

    Approximation of :math:`\mathrm{div}(uv)=0` using `scheme` (where
    :math:`u` is the unknown function).

    Parameters
    ----------
    E : TPFAStruct
        Mesh on which the approximation is done.
    v : scalar or callable or array_like or dict
        Object containing velocity of the volumic term. It is passed
        to `E.evaluate`. Must evaluate to a vector field.
    bnd: BCStructure
        Description of the boundary conditions.
    scheme : {'upwind', 'centered'}, default 'upwind'
        The name of the scheme to be used for the approximation.

    Returns
    -------
    row_mat, col_mat, dat_mat
    `row_mat`, `col_mat` contain the  coordinates of non-zero
    coefficients and `dat_mat` the values of the TPFA Finite Volumes
    approximation matrix of the selected `scheme` for the advection.

    See Also
    --------
    convection_rhs
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    scipy.sparse.csr_array, scipy.sparse.csc_array

    Notes
    -----
    The return value as tuples of lists `row_mat`, `col_mat`, `dat_mat`
    (and `row_rhs`, `dat_rhs` for the parallel function
    `convection_rhs`) is set up to work in conjunction with the
    `scipy.sparse` module. recisely the expected follow up to this
    function is something like

    .. code-block:: python

       scipy.sparse.csr_array((np.concatenate(dat_mat),
                               (np.concatenate(row_mat),
                                np.concatenate(col_mat))))

    to build the (`E.nvol`, `E.nvol`) matrix :math:`M` such that
    :math:`MU` is the Finite Volumes approximation of
    :math:`\mathrm{div}(uv)` using `scheme` where :math:`u` is the
    unknown function.
    """
    V = E.discretize(v, DIAM)
    flux_i = ms(V['xs_i'], E.NKL_i)
    flux_b = ms(V['xs_b'], E.NKs_b)
    row_i, col_i, dat_i = conv_center_i(E, flux_i)
    row_b, col_b, dat_b = conv_center_b_mat(E, flux_b, bnd)
    num_diff_i = PREDEF_CONV_DIFF[scheme](flux_i/E.len_i*E.dKL_i)
    num_diff_b = PREDEF_CONV_DIFF[scheme](flux_b/E.len_b*E.dKs_b)
    row_di, col_di, dat_di = diff_i(E, num_diff_i)
    row_db, col_db, dat_db = diff_b_mat(E, num_diff_b, bnd)
    return (row_i+row_b+row_di+row_db,
            col_i+col_b+col_di+col_db,
            dat_i+dat_b+dat_di+dat_db)


def convection_rhs(E: TPFAStruct, v: Discretizable,
                   bnd: BCStructure,
                   scheme: Literal['upwind', 'centered'] = 'upwind',
                   ) -> tuple[list[IndexArray],
                              list[ValueArray],
                              ValueArray]:
    r"""Convection rhs using a TPFA scheme.

    Approximation of :math:`\mathrm{div}(uv)=0` using `scheme` (where
    :math:`u` is the unknown function).

    Parameters
    ----------
    E : tpfa_struct.TPFAStruct
        Mesh on which the approximation is done.
    v : pynitevolumes.mesh.disc.Discretizable
        Object containing velocity of the volumic term. It is passed
        to `E.evaluate`. Must be 2d vector-valued.
    scheme : {'upwind', 'centered'}, default 'upwind'
        The name of the scheme to be used for the approximation.
    bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    row_rhs, dat_rhs : tuple
        `row_rhs`, `dat_rhs` contain the coordinate of non-zero
        coefficients of the contribution to the right-hand side of the
        advection due to inhomogneous boundary conditions.
    flux_b: ValueArray
        Convective flux on the boundary. Avoids recomputing it in case
        of flux boundary conditions.

    See Also
    --------
    convection_matrix
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    scipy.sparse.csr_array, scipy.sparse.csc_array

    Notes
    -----
    The return value as tuples of lists `row_rhs`, `dat_rhs` (and
    `row_mat`, `col_mat`, `dat_mat` for the parallel function
    `convection_matrix`) is set up to work in conjunction with the
    `scipy.sparse` module. Precisely the expected follow up to this
    function is something like

    .. code-block:: python

       scipy.sparse.csc_array((np.concatenate(dat_rhs),
                               (np.concatenate(row_rhs),
                                np.concatenate(np.ones(len(row_rhs))))))

    to build the (`E.nvol`, 1) matrix :math:`b` such that :math:`b` is
    the contribution to the right-hand side of the Finite Volumes
    approximation of :math:`\mathrm{div}(uv)=0` using `scheme` where
    :math:`u` is the unknown function.
    """
    V = E.discretize(v, DIAM)
    flux_b = ms(V['xs_b'], E.NKs_b)
    rrhs_b, drhs_b = conv_center_b_rhs(E, flux_b, bnd)
    num_diff_b = PREDEF_CONV_DIFF[scheme](flux_b*E.dKs_b/E.len_b)
    row_db, dat_db = diff_b_rhs(E, num_diff_b, bnd)
    return rrhs_b+row_db, drhs_b+dat_db, flux_b

# %% Diffusion-convection
#    ====================


def sharfetter_gummel(E: TPFAStruct, A: Discretizable, v: Discretizable,
                      bnd: BCStructure
                      ) -> tuple[tuple[list[IndexArray],
                                       list[IndexArray],
                                       list[ValueArray]],
                                 tuple[list[IndexArray],
                                       list[ValueArray]]]:
    r"""Approximation of diffusion-convection by Sharfetter-Gummel.

    Approximation of :math:`-\mathrm{div}(A\nabla u)+\mathrm{div}(uv)=0`
    (where :math:`u` is the unknown function) by the Sharfetter-Gummel
    scheme.

    Parameters
    ----------
    E : tpfa_struct.TPFAStruct
        Mesh on which the approximation is done.
    A : pynitevolumes.mesh.disc.Discretizable
        Object containing diffusion coefficient. It is passed
        to `E.evaluate`. Must be scalar-valued.
    v : pynitevolumes.mesh.disc.Discretizable
        Object containing velocity of the advection term. It is passed
        to `E.evaluate`. Must be 2d vector-valued.
    bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    ((row_mat, col_mat, dat_mat), (row_rhs, dat_rhs)) : tuple
        `row_mat`, `col_mat` contain the  coordinates of non-zero
        coefficients and `dat_mat` the values of the Sharfetter-Gummel
        approximation matrix for the diffusion-advection.
        `row_rhs`, `dat_rhs` contain the coordinate of non-zero
        coefficients of the contribution to the right-hand side due to
        inhomogneous boundary conditions.

    Warning
    -------
    This function is based on the TPFA approximation of the diffusion
    flux which uses at its core the hypothesis that the underlying mesh
    satisfies the Delaunay condition. If this is not true the resulting
    scheme is not consistent. One can check the Delaunay condition with
    the functions pynitevolumes.scheme.tpfa.check_orthogonality and
    pynitevolumes.scheme.tpfa.check_centers_order.
    It also only works for isotropic diffusion.

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh.evaluate
    tpfa_struct.check_orthogonality
    tpfa_struct.check_centers_order

    Notes
    -----
    The return value as tuples of lists `row_mat`, `col_mat`, `dat_mat`
    and `row_rhs`, `dat_rhs` is set up to work in conjunction with the
    `scipy.sparse` module. Precisely the expected follow up to this
    function is something like

    .. code-block:: python

       scipy.sparse.csr_array((np.concatenate(dat_mat),
                               (np.concatenate(row_mat),
                                np.concatenate(col_mat))))

    and

    .. code-block:: python

       scipy.sparse.csc_array((np.concatenate(dat_rhs),
                               (np.concatenate(row_rhs),
                                np.concatenate(np.ones(len(row_rhs))))))

    to build the `(E.nvol, E.nvol)` matrix :math:`M` and the
    `(E.nvol, 1)` matrix b such that :math:`MU=b` is the Sharfetter-
    Gummel approximation of
    :math:`-\mathrm{div}(A\nabla u)+\mathrm{div}(uv)=0` where
    :math:`u` is the unknown function.
    """
    def B(s: ValueArray) -> ValueArray:
        def b(t: ValueArray) -> ValueArray:
            t_arr: np.ndarray = np.asarray(t, dtype=np.float64)
            res: ValueArray = t_arr / 2 * (np.exp(t_arr) + 1) / (np.exp(t_arr) - 1)
            return res
        res = np.zeros(s.shape, dtype=np.float64)
        s_plus_infinity = np.nonzero(s > 700.0)  # cutoff: np.exp(710)=np.inf
        s_finite_nonzero = np.nonzero(np.logical_and(
            np.abs(s) >= 1e-14, s <= 700.0))
        res[s_plus_infinity] = -1+s[s_plus_infinity]/2
        res[s_finite_nonzero] = -1+b(s[s_finite_nonzero])
        return res
    A_d = E.discretize(A, DIAM)
    V_d = E.discretize(v, DIAM)
    flux_i = ms(V_d['xs_i'], E.NKL_i)
    flux_b = ms(V_d['xs_b'], E.NKs_b)
    S_i = flux_i*E.dKL_i/(A_d['xs_i']*E.len_i)
    S_b = flux_b*E.dKs_b/(A_d['xs_b']*E.len_b)
    mat_c_i = conv_center_i(E, flux_i)
    mat_c_b = conv_center_b_mat(E, flux_b, bnd)
    rhs_c_b = conv_center_b_rhs(E, flux_b, bnd)
    mat_d_i = diff_i(E, A_d['xs_i']*(1+B(S_i)))
    A_db = A_d['xs_b']*(1+B(S_b))
    mat_d_b = diff_b_mat(E, A_db, bnd)
    rhs_d_b = diff_b_rhs(E, A_db, bnd)
    return ((mat_c_i[0]+mat_c_b[0]+mat_d_i[0]+mat_d_b[0],
             mat_c_i[1]+mat_c_b[1]+mat_d_i[1]+mat_d_b[1],
             mat_c_i[2]+mat_c_b[2]+mat_d_i[2]+mat_d_b[2]),
            (rhs_c_b[0]+rhs_d_b[0], rhs_c_b[1]+rhs_d_b[1]))


def build_whole_dirichlet(E: TPFAStruct, *,
                          value: Discretizable | None = None,
                          inflow: bool = False
                          ) -> BCStructure:
    """Build the data structure to impose Dirichlet on the whole domain.

    Parameters
    ----------
    E : TPFAStruct
        Mesh of the domain.
    value : Discretizable, optional
        Value to impose on the boundary. If omitted, is the same as
        passing `value=0.0`.
    inflow: bool, default=False
        Makes the boundary condition used only on the inflow part of the
        boundary.

    Returns
    -------
    bc_data.BCStructure
        Description of the boundary condition.
    """
    val: Discretizable
    if value is None:
        val = 0.0  # type: ignore
    else:
        val = value
    data = E.evaluate(val, 'xs_b')
    if inflow:
        return BCStructure(inflow_others=[DirichletBC(np.arange(E.nbnd),
                                                      data)])
    else:
        return BCStructure(uncond_others=[DirichletBC(np.arange(E.nbnd),
                                                      data)])


def build_whole_neumann(E: TPFAStruct, *,
                        value: Discretizable | None = None,
                        inflow: bool = False
                        ) -> BCStructure:
    """Build the sata structure to impose Neumann on the whole domain.

    Parameters
    ----------
    E : TPFAStruct
        Mesh of the domain.
    value : Discretizable | None
        Value to impose on the boundary. If omitted, is the same as
        passing `value=0.0`.
    inflow: bool, default is False
        Makes the boundary condition used only on the inflow part of the
        boundary.

    Returns
    -------
    bc_data.BCStructure
        Description of the boundary condition.
    """
    val: Discretizable
    if value is None:
        val = 0.0  # type: ignore
    else:
        val = value
    data = E.evaluate(val, 'xs_b')
    if inflow:
        return BCStructure(inflow_others=[NeumannBC(np.arange(E.nbnd), data)])
    else:
        return BCStructure(uncond_others=[NeumannBC(np.arange(E.nbnd), data)])

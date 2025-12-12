#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base module for managing meshes to use TPFA schemes."""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from scipy.spatial import Voronoi
from pynitevolumes.mesh.base_struct import Mesh, Diamond
from ...tools.geometry import (turn, wedge, triarea, multscalar, vnorm,
                               intersect, orthoproject, geometric_property)
if TYPE_CHECKING:
    from typing import ClassVar, Literal
    from ...mesh._array_types import PointArray, ValueArray, IndexArray
    from ...mesh.disc import Discretizable

_FLOAT_TEST = 1e-14


class TPFAStruct(Mesh):
    """Class of meshes used to write TPFA schemes.

    Instances of this class provide the geometric information needed to
    write TPFA numerical schemes on the primal mesh.

    An instance of the class is usually obtained by using the class
    method `fromMesh` on a pynitevolumes.Mesh instance.

    See Also
    --------
    pynitevolumes.mesh.base_struct.Mesh
    check_orthogonality, check_centers_order

    Notes
    -----
    This simpler structure is usually used when the centers and the edge
    of the mesh satisfy an admissibility condition that the inner edges
    are orthogonal to the line joining the two centers on each side.
    However, be aware that instantiating this class does not enforce
    this condition in any way.
    """

    #: Points defined in TPFAStruct
    pointvars: ClassVar[list[str]] = ['centers', 'vertices', 'xs_i', 'xs_b']
    #: Vectors defined in TPFAStruct
    vectorvars: ClassVar[list[str]] = ['NKL_i', 'NKs_b']
    #: Geometry defined in TPFAStruct
    geometry: ClassVar[list[str]] = ['sgn_i', 'sgn_b',
                                     'len_i', 'len_b',
                                     'dKL_i', 'dKs_i', 'dKs_b',
                                     'dqareas', 'areaK_i', 'areaK_b',
                                     'areaD_i', 'areaD_b',
                                     'vol', 'size']

    @geometric_property
    def xs_i(self) -> PointArray:
        """Centers of the inner edges."""
        k_i = self.centers[self.diam_i.c]
        s_i = self.vertices[self.diam_i.v]
        return intersect(k_i[0], k_i[1], s_i[0], s_i[1])

    @geometric_property
    def xs_b(self) -> PointArray:
        """Centers of the boundary edges."""
        k_b = self.centers[self.diam_b.c]
        s_b = self.vertices[self.diam_b.v]
        return orthoproject(k_b, s_b[0], s_b[1])

    @geometric_property
    def sgn_i(self) -> ValueArray:
        """Orientation of the inner diamonds."""
        k_i = self.centers[self.diam_i.c]
        s_i = self.vertices[self.diam_i.v]
        sgn_i = np.sign(wedge(k_i[1]-k_i[0], s_i[1]-s_i[0]))
        pbs = np.where(np.abs(sgn_i) <= _FLOAT_TEST)[0]
        if pbs.any():
            raise ValueError(f'Degenerate diamond(s) found at edges {pbs}')
        return sgn_i

    @geometric_property
    def sgn_b(self) -> ValueArray:
        """Orientation of the boundary diamonds."""
        k_b = self.centers[self.diam_b.c]
        s_b = self.vertices[self.diam_b.v]
        sgn_b = np.sign(wedge(self.xs_b-k_b, s_b[1]-s_b[0]))
        pbs = np.where(np.abs(sgn_b) <= _FLOAT_TEST)[0]
        if pbs.any():
            raise ValueError('Boundary center was found on a boundary edge at'
                             + f' {pbs}')
        return sgn_b

    @geometric_property
    def len_i(self) -> ValueArray:
        """Length of the inner edges."""
        s_i = self.vertices[self.diam_i.v]
        return vnorm(s_i[1]-s_i[0])

    @geometric_property
    def len_b(self) -> ValueArray:
        """Length of the boundary edges."""
        s_b = self.vertices[self.diam_b.v]
        return vnorm(s_b[1]-s_b[0])

    @geometric_property
    def dKL_i(self) -> ValueArray:
        """Distance between opposing centers of inner edges."""
        k_i = self.centers[self.diam_i.c]
        return vnorm(k_i[1]-k_i[0])

    @geometric_property
    def dKs_i(self) -> ValueArray:
        """Distance between inner centers and inner edge center."""
        k_i = self.centers[self.diam_i.c]
        return vnorm(self.xs_i-k_i)

    @geometric_property
    def dKs_b(self) -> ValueArray:
        """Distance between boundary center and boundary edge center."""
        k_b = self.centers[self.diam_b.c]
        return vnorm(self.xs_b-k_b)

    @geometric_property
    def NKL_i(self) -> PointArray:
        """Weighted normal to inner edge."""
        s_i = self.vertices[self.diam_i.v]
        return np.tile(self.sgn_i, (2, 1)).T*turn(s_i[0]-s_i[1])

    @geometric_property
    def NKs_b(self) -> PointArray:
        """Weighted normal to boundary edge."""
        s_b = self.vertices[self.diam_b.v]
        return -np.tile(self.sgn_b, (2, 1)).T*turn(s_b[1]-s_b[0])

    def dqarea_i(self, choice: str) -> ValueArray:
        """Access areas of quarters of inner diamonds.

        Convenience function to access the areas of the inner quarter-of
        -diamonds.

        Parameters
        ----------
        choice : str
            The string must consist of two characters each of them  is
            either '0' or '1'. For historical reasons, for the second
            character, '0' can be replace by 'K' and '1' by 'L'. It
            selects which of the quarter of diamonds is obtained.

        Returns
        -------
        numpy.ndarray
            The array of requested quarter-of-diamonds area.

        Notes
        -----
        The diamond associated to an inner edge is the quadrilateral
        formed of the two vertices V0 and V1 of the edge and the two
        centers of cells that are on each side of the edge. These
        centers have numbers attached to them that we traditionnaly note
        K and L. The diamond can then be split into four triangle pieces
        given by selecting one center, one vertex and the center of the
        edge. The function `dqarea_i` gives the corresponding values
        with respect to the description of diamonds in `self.diam_i`.
        """
        i = int(choice[0])
        j = choice[1]
        if j == 'K':
            j = 0
        elif j == 'L':
            j = 1
        else:
            j = int(j)
        res: ValueArray = self.dqareas['i'][i, j]
        return res

    def dqarea_b(self, choice: Literal['0', '1']) -> ValueArray:
        """Access areas of quarters of boundary diamonds.

        Convenience function to access the areas of the boundary quarter
        of diamonds.

        Parameters
        ----------
        choice : {'0', '1'}
            It selects which of the quarter-of-diamonds is obtained.

        Returns
        -------
        numpy.ndarray
            The array of requested quarter-of-diamonds area.

        Notes
        -----
        The diamond associated to a boundary edge is the triangle formed
        of the two vertices V0 and V1 of the edge and the center of the
        cell that the edge is part of the boundary to. The diamond can
        then be split into two triangle pieces given by selecting one
        vertex, the center of the cell and the center of the edge. The
        function `dqarea_b` gives the corresponding values
        with respect to the description of diamonds in `self.diam_b`.
        Note that quarter of diamond here is technically a misuse of the
        term (since there are only two half diamonds) but is classical
        to unify the vocabulary between inner and boundary diamonds.
        """
        i = int(choice)
        res: ValueArray = self.dqareas['b'][i]
        return res

    @geometric_property
    def dqareas(self) -> dict[Literal['i', 'b'], ValueArray]:
        """Areas of the quarter of diamonds."""
        m_i = np.empty((2, 2, self.nin), dtype='float')
        m_b = np.empty((2, self.nbnd), dtype='float')

        for i in range(2):
            m_b[i] = triarea(self.centers[self.diam_b.c],
                             self.vertices[self.diam_b.v[i]],
                             self.xs_b)
            for j in range(2):
                m_i[i, j] = triarea(self.centers[self.diam_i.c[j]],
                                    self.vertices[self.diam_i.v[i]],
                                    self.xs_i)
        return {'i': m_i, 'b': m_b}

    @geometric_property
    def areaK_i(self) -> ValueArray:
        """Area of inner half diamonds."""
        return np.stack((self.dqarea_i('0K')+self.dqarea_i('1K'),
                         self.dqarea_i('0L')+self.dqarea_i('1L')))

    @geometric_property
    def areaK_b(self) -> ValueArray:
        """Area of boundary diamonds."""
        return self.dqarea_b('0')+self.dqarea_b('1')

    @geometric_property
    def areaD_i(self) -> ValueArray:
        """Area of inner diamonds."""
        res: ValueArray = self.areaK_i[0]+self.areaK_i[1]
        return res

    @geometric_property
    def areaD_b(self) -> ValueArray:
        """Area of boundary diamonds."""
        return self.areaK_b

    @geometric_property
    def vol(self) -> ValueArray:
        """Volume of the cells."""
        vol = np.empty(self.nvol, dtype='float')
        for i in range(self.nvol):
            Iin, Jin, Ibnd = self._center_struct(i)
            vol[i] = (np.sum(self.areaK_i[0, Iin])
                      + np.sum(self.areaK_i[1, Jin])
                      + np.sum(self.areaK_b[Ibnd]))
        return vol

    @geometric_property
    def size(self) -> float:
        """Characteristic length of the primal mesh."""
        res: float = np.max(np.sqrt(self.vol))
        return res


def norm(M: TPFAStruct, f: Discretizable,
         r: int | Literal['inf'] = 2
         ) -> np.float64:
    """Discrete L^r norm of a function.

    Parameters
    ----------
    M : TPFAStruct
        The mesh on which the function is discretized.
    f : scalar or callable or array or dict
        Discretizable object.
    r : int or 'inf' or np.inf, optional
        The index of the norm. The default is 2.

    Returns
    -------
    float
        The discrete :math:`L^r` norm of `f` on mesh `M`.

    """
    fd = M.evaluate(f, 'centers')
    res: np.float64
    if r == 'inf':
        res = np.max(fd[..., :])
    else:
        res = np.sum(M.vol*fd[..., :]**r, axis=-1)**(1/r)
    return res


def h1norm(M: TPFAStruct, f: Discretizable, semi: bool = True
           ) -> np.float64:
    """Discrete H^1 norm of a function.

    Parameters
    ----------
    M : TPFAStruct
        The Mesh on which the function is discretized.
    f : scalar or callable or array or dict
        Discretizable object.
    semi : bool, optional
        If True, computes only the H^1 semi-norm and if False, computes
        the whole H^1 norm. The default is True.

    Returns
    -------
    float
        The discrete :math:`H^1` semi-norm or full norm.

    Notes
    -----
    For discrete functions `f` defined on a mesh with orthogonality
    condition, the :math:`H^1` semi-norm squared is the sum over all
    inner diamonds of the area of the diamond multiplied by
    :math:`(|f(K)-f(L)|/|K-L|)^2` where K and L would be the centers on
    each side of the edge.
    """
    p = M.evaluate(f, 'centers')
    K = M.diam_i.c[0]
    L = M.diam_i.c[1]
    Kb = M.diam_b.c
    semin_sq = (np.sum(M.areaD_i*((p[..., K]-p[..., L])/M.dKL_i)**2, axis=-1)
                + np.sum(M.areaD_b*(p[..., Kb]/M.dKs_b)**2, axis=-1))
    res: np.float64
    if semi:
        res = np.sqrt(semin_sq)
    else:
        res = np.sqrt(norm(M, p)**2+semin_sq)  # type: ignore
    return res


def check_orthogonality(M: Mesh |
                        tuple[PointArray, PointArray, Diamond, Diamond],
                        eps: float = _FLOAT_TEST, verbose: bool = True
                        ) -> bool:
    """Check if a mesh-like satisfies the orthogonality condition.

    For each inner edge, check if the segment of extremities the centers
    of the bounding cells is orthogonal to the edge.

    Parameters
    ----------
    M : pynitevolumes.mesh.base_struct.Mesh or tuple
        The Mesh to be tested. Can be a tuple of arguments that can be
        passed to the constuctor of
        `pynitevolumes.mesh.base_struct.Mesh`.
    eps : float, optional
        Parameter to control the proximity of floats.
    verbose : bool, default is True.
        In case of a failed test, prints the edges that made the test
        fail.

    Returns
    -------
    bool
        `True` if all inner edges are orthogonal to the segment joining
        the two centers. `False` otherwise.
    """
    if isinstance(M, Mesh):
        c = M.centers
        v = M.vertices
        ((k_i, l_i), s_i), (k_b, s_b) = M.diamonds()
    else:
        c, v, diam_i, diam_b = M
        s_i = v[diam_i.v]
        k_i = c[diam_i.c[0]]
        l_i = c[diam_i.c[1]]
    t_i = multscalar(s_i[1]-s_i[0], k_i-l_i)
    Pbs = np.abs(t_i) > eps
    failed_test = Pbs.any()
    if failed_test and verbose:
        print('Orthogonality test failed because of edges '
              + f'{Pbs.nonzero()}.')
    return not failed_test


def check_centers_order(M: TPFAStruct, eps: float = _FLOAT_TEST,
                        verbose: bool = True) -> bool:
    """Check if a TPFAStruct satisfies the centers-in order condition.

    For each inner edge K|L, check if M.centers[L]-M.centers[K] has the
    same direction as the normal vector outward of K.

    Parameters
    ----------
    M : TPFAStruct
        The Mesh with geometric structure to be tested.
    eps : float, optional
        Parameter to control the proximity of floats.
    verbose : bool, default is True.
        In case of a failed test, prints the edges that made the test
        fail.

    Returns
    -------
    bool
        `True` if for all inner edges, separating the volumes with
        centers indices `K` and `L`, the vector from center `K` to
        center `L` is in the same direction as the normal vector
        pointing outward of the cell `K`.
    """
    ((k_i, l_i), s_i), (k_b, s_b) = M.diamonds()
    t_i = multscalar(l_i-k_i, M.NKL_i)
    Pbs = t_i < 0
    failed_test = Pbs.any()
    if failed_test and verbose:
        print('Centers order test failed beacause of edges '
              + f'{Pbs.nonzero()}')
    return not failed_test


def build_voronoi_centers(M: Mesh |
                          tuple[PointArray, IndexArray, IndexArray]
                          ) -> tuple[PointArray,
                                     PointArray,
                                     tuple[Diamond, Diamond]]:
    """Construct an admissible family of center points.

    Given information about a mesh as a graph of vertices, compute a
    family of points with orthogonality property.

    Parameters
    ----------
    M : pynitevolumes.mesh.base_struct.Mesh or tuple
        An already constructed `pynitevolumes.mesh.base_struct.Mesh`
        object or a tuple of three arrays, `(v, Dvi, Dvb)`:

        * (nv, 2) array `v` contains the positions of the vertices
          in the plane.
        * (2, ni) array `Dvi` contains the inner edges, each column
          containing two indices refering to the corresponding line of
          `v`.
        * (2, nb) array `Dvb` contain the boundary edges, each
          column containing two indices refering to the corresponding
          line of `v`.

    Returns
    -------
    tuple
        Returns `(centers, vertices, (diam_i, diam_b))` where :
        `centers` is an (n, 2) array of constructed points,
        `vertices` is the original `v`, `diam_i` and `diam_b` are
        `pynitevolumes.mesh.base_struct.Diamond` instances which
        describe the relation between centers and edges if `centers` is
        chosen as a family of centers for the initial mesh.

    See Also
    --------
    scipy.spatial.Voronoi

    Notes
    -----
    We use the Voronoi algorithm on the family of vertices to produce a
    family of centers which satisfy the admissibility condition
    automatically. The function returns a tuple that can be unpacked
    into the arguments of the `TPFAStruct` constructor.
    """
    if isinstance(M, Mesh):
        Dvi = M.diam_i.v
        Dvb = M.diam_b.v
    else:
        v, Dvi, Dvb = M
    ni = Dvi.shape[-1]
    nb = Dvb.shape[-1]
    s_i0 = Dvi[0]
    s_i1 = Dvi[1]
    s_b0 = Dvb[0]
    s_b1 = Dvb[1]
    lookup_i = {}
    lookup_b = {}
    for i in range(ni):
        lookup_i[(s_i0[i], s_i1[i])] = i
        lookup_i[(s_i1[i], s_i0[i])] = i
    for i in range(nb):
        lookup_b[(s_b0[i], s_b1[i])] = i
        lookup_b[(s_b1[i], s_b0[i])] = i
    V = Voronoi(v)
    centers = V.vertices
    ndiam_ic = np.empty((2, ni), dtype=int)
    ndiam_bc = np.empty(nb, dtype=int)
    vrv = V.ridge_vertices
    vrp = V.ridge_points
    nridges = vrp.shape[0]
    for j in range(nridges):
        ridge = vrv[j]
        if -1 in {ridge[0], ridge[1]}:
            num_c = ({ridge[0], ridge[1]}-{-1}).pop()
            ib = lookup_b[(vrp[j, 0], vrp[j, 1])]
            ndiam_bc[ib] = num_c
        else:
            num_ck, num_cl = ridge[0], ridge[1]
            ii = lookup_i[(vrp[j, 0], vrp[j, 1])]
            ndiam_ic[:, ii] = np.array([num_ck, num_cl])
    return (centers, v,
            (Diamond({'c': ndiam_ic, 'v': Dvi}),
             Diamond({'c': ndiam_bc, 'v': Dvb})))

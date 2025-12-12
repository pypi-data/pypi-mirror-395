#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module containing tools to manipulate meshes."""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from warnings import warn
from .base_struct import Mesh, Diamond
from ..tools.geometry import multscalar
if TYPE_CHECKING:
    from typing import Literal
    from collections.abc import Iterable
    from numpy.typing import NDArray
    from ._array_types import IndexArray
    from .disc import Discretizable
_FLOAT_TEST = 1e-14


def adjacency(G: NDArray[np.int_], subg: NDArray[np.int_] | None = None
              ) -> dict[int, set[tuple[int, int]]]:
    """Build the adjacency map of a subgraph of G.

    Parameters
    ----------
    G : (2, n) numpy.ndarray of int
        G represents a symmetrical graph in that G[:, i] = [V, W] is the
        i-th edge in the graph and connects the vertice of number V with
        the one with number W.
    subg : array_like of int or None
        Indices of the edges to take into account. If None then all
        edges are take into account.

    Returns
    -------
    A : dict
        Adjacency map of the subgraph. Each key `S` is the number of a
        vertex in `G` and the value associated is a set of pairs
        `(T, e)` such that `G[:, e]` is the edge `[S, T]`.
    """
    if subg is None:
        subg = np.arange(G.shape[1])
    n = len(subg)
    S = G[:, subg]
    A = {S[0, 0]: {(S[1, 0], subg[0])}, S[1, 0]: {(S[0, 0], subg[0])}}
    for i in range(1, n):
        if S[0, i] in A.keys():
            A[S[0, i]].add((S[1, i], subg[i]))
        else:
            A[S[0, i]] = {(S[1, i], subg[i])}
        if S[1, i] in A.keys():
            A[S[1, i]].add((S[0, i], subg[i]))
        else:
            A[S[1, i]] = {(S[0, i], subg[i])}
    return A


def connex_comp(M: Mesh, Ind: NDArray[np.int_],
                where: Literal['boundary', 'inside'] = 'boundary'
                ) -> dict[str,
                          list[tuple[IndexArray, IndexArray]]]:
    """Compute the connex components of set of edges inside a Mesh.

    Parameters
    ----------
    M : `base_struct.Mesh`
        Mesh to obtain the edges from.
    Ind : array_like of int
        Edge indices which defines the set of edges.
    where : {'boundary', 'inside'}, optional
        What type of edges are concerned. The default is 'boundary'.

    Returns
    -------
    dict
        The dictionary is of the form {'lines': L, 'cycles': C}
        Both `L` and `C` are lists of pairs `(vertices, edges)` where
        `vertices` is an ordered list of vertex indices and `edges` is
        the corresponding ordered list of edge indices. Each pair
        corresponds to a connex component. If the pair is in `L` then it
        has two extremities while if it is in `C` it represents a closed
        curve. In this case, starting and closing vertex indices are
        arbitrary.
    """
    if where in {'boundary', 'bnd'}:
        G = M.diam_b.v
    elif where in {'inside', 'inner'}:
        G = M.diam_i.v
    A = adjacency(G, Ind)
    # First check for extremities and multiple points
    ex = []
    for s in A.keys():
        if len(A[s]) != 2:
            ex.extend(len(A[s])*[s])
    L = []  # for "line" connex components
    C = []  # for cycles

    # If there are extremities or multiple points, start from them until you
    # reach another extremity or a multiple point then stop
    while ex:
        # print(ex)
        s0 = ex.pop()
        s1, i1 = A[s0].pop()
        orders = [s0, s1]
        ordere = [i1]
        A[s1].remove((s0, i1))
        while s1 not in ex:
            sold = s1
            s1, i1 = A[s1].pop()
            orders.append(s1)
            ordere.append(i1)
            A[s1].remove((sold, i1))
            del A[sold]
        ex.remove(s1)
        if s1 not in ex:
            del A[s1]
        if (s0 not in ex) and (s1 != s0):
            del A[s0]
        if s1 == s0:
            C.append((np.array(orders), np.array(ordere)))
        else:
            L.append((np.array(orders), np.array(ordere)))

    # At this stage there are only cycles that can be left.
    while A:
        s0, S0 = A.popitem()
        (s1, i1) = S0.pop()
        orders = [s0, s1]
        ordere = [i1]
        while s1 != s0:
            sold = s1
            s1, i1 = (A[s1] - {(orders[-2], ordere[-1])}).pop()
            orders.append(s1)
            ordere.append(i1)
            del A[sold]
        C.append((np.array(orders), np.array(ordere)))
    data = {'lines': L, 'cycles': C}
    return data


def locate(M: Mesh, f: Discretizable,
           where: Literal['boundary', 'inside'] = 'boundary',
           eps: float | None = None) -> IndexArray:
    """Locate edges of M where both vertices satisfy f=0.

    Parameters
    ----------
    M : `base_struct.Mesh`
        The mesh in which you want to locate edges
    f : `disc.Discretizable`
        Criterion to be satisfied.
    where : {'boundary', 'inside'}, optional
        restricts the type of edges 'boundary' for only boundary edges,
        'inside' for inner edges. The default is 'boundary'.
    eps : float, optional
        configures how well the criterion must be satisfied.
        The default is None to use the default value.

    Returns
    -------
    (ne,) numpy.ndarray of int
        Array of edge indices satisfying the criterion. Edge
        indices are relative to the area where the edges have been
        looked for (inner edges or boundary edges).

    """
    if eps is None:
        eps = _FLOAT_TEST
    F = np.abs(M.evaluate(f, 'vertices')) <= eps
    if where in {'boundary', 'bnd'}:
        G = M.diam_b.v
    elif where in {'inside', 'inner'}:
        G = M.diam_i.v
    S0 = F[G[0]]
    S1 = F[G[1]]
    B = np.logical_and(S0, S1)
    return np.where(B)[0]


def order_param(M: Mesh, e: NDArray[np.int_],
                A: NDArray[np.float64],
                B: NDArray[np.float64] | None = None,
                bnd: bool = True
                ) -> tuple[NDArray[np.int_],
                           NDArray[np.int_],
                           NDArray[np.float64]]:
    """Order set of edges and vertices.

    Assuming a set of edges could be parametrized as the graph of a
    function in an orthogonal coordinate system (X, Y), they are ordered
    in increasing values of X.

    Parameters
    ----------
    M : base_struct.Mesh
        The mesh where the edges are extracted from.
    e : array_like of int
        The set of edge to be ordered.
    A, B : array_like of float
        The straight line over which the set of edge is assumed to have
        a functional dependence is given by an origin and a direction.
        If `B` is None, the origin is (0, 0) and `A` contains the
        direction. Else `A` contains the origin and the vector `B-A`
        gives the direction. The default is for `B` to be None.
    bnd : bool, optional default True
        If True, the edges are assumed to be coming from the boundary of
        the mesh. Otherwise they are inner edges of the mesh.
        The default is True.

    Raises
    ------
    ValueError
        Raised if the set of edges seem to not be parametrizable trough
        the given straight line.

    Returns
    -------
    I_sort : (2, n) numpy.ndarray of {0, 1}
        Indexes the position of the vertices in order. n is the length of
        `e`.
    e_sort : (n,) numpy.ndarray of int
        The array of sorted edges.
    Vx : (n,) numpy.ndarray of float
        The array of parameters for the vertices

    Notes
    -----
    First the mean point of each edge is orthogonally projected onto
    line (AB) and are ordered. If two projections are the same then the
    set of edges is dimmed not to be parametrizable. Then all of the
    vertices are projected orthogonally onto (AB) to find which one
    should come first. All of the  projections must now be in order or
    the parametrization fails.

    At the end, if `bnd` is True, `M.diam_b.v[(I_sort, e_sort)]` is a
    (2, n) shape array where the vertices number can be read in
    lexicographical order, 0th-axis first and 1st-axis second.

    Note also that the function does not require the set of edge to
    describe a connex set.
    """
    A = np.array(A, dtype='float')
    if B is None:
        B = A.copy()
        A = np.zeros(2, dtype='float')
    A, B = np.array(A, dtype='float'), np.array(B, dtype='float')
    e = np.array(e, dtype='int')
    if bnd:
        V = M.vertices[M.diam_b.v[:, e]]
    else:
        V = M.vertices[M.diam_i.v[:, e]]
    Vx = multscalar(V-A, B-A)
    X = (Vx[0]+Vx[1])/2
    if len(X) != len(np.unique(X)):
        raise ValueError(f'Edges {e} cannot be parametrized through'
                         + f' [{A}, {B}].')
    loc_sort = np.array([s for (s, x) in sorted(enumerate(X),
                                                key=lambda t: t[1])],
                        dtype=int)
    I_sort = np.argsort(Vx, axis=0)
    V_p = np.take_along_axis(Vx[:, loc_sort], I_sort[:, loc_sort],
                             axis=0).ravel('F')
    if (np.diff(V_p) < 0).any():
        raise ValueError(f'Edges {e} cannot be parametrized through'
                         + f' [{A}, {B}].')
    return I_sort, loc_sort, Vx


def create_interface(M0: Mesh, e0: IndexArray, M1: Mesh, e1: IndexArray,
                     A: NDArray[np.float64],
                     B: NDArray[np.float64] | None = None,
                     eps: float | None = None
                     ) -> tuple[NDArray[np.int_],
                                NDArray[np.int_],
                                NDArray[np.float64],
                                NDArray[np.int_]]:
    """Set up interface creation between two meshes.

    Take two meshes and a list of edges of their respective boundaries
    and creates the data necessary to merge the two into an inner
    interface.

    Parameters
    ----------
    M0, M1 : base_struct.Mesh
        The two meshes.
    e0, e1 : array-like of int
        The two arrays of boundary numbers in `M0` and `M1`
        respectively.
    A, B : array-like of float
        The straight line over which the set of edge is assumed to have
        a functional dependence is given by an origin and a direction.
        If `B` is None, the origin is (0, 0) and `A` containes the
        direction. Else `A` contains the origin and the vector `B-A`
        gives the direction. The default is for `B` to be None.
    eps : float, optional
        Parameter to control the proximity of floats.
        The default is None.

    Returns
    -------
    (2, n) numpy.ndarray of int
        Vertices of the edges in the interface. The value v at index
        [i, j] indicate that the edge j of the inteface has one of its
        vertex as v: v>=0 refer to the vertex number v in `M0` and v<0
        refer to the vertex -v in `M1`.
    (2, n) numpy.ndarray of int
        Centers that would be separated by the interface. The value v at
        index [0, j] means that the edge j of the interface has center
        number v of `M0` on its side and the the value v at index [1, j]
        means that the edge j of the interface has center number v of
        `M1` on its other side.
    (2,) numpy.ndarray of float
        Vector of translation of the two vertices at the extremity of
        edge `e0` onto the two vertices at the extremity of edge `e1`.
    (nv, 2) numpy.ndarray of int
        Vertices that are in common in both edges. Value v at [i, 0] and
        and value w at [i, 1] mean that vertex number v in `M0` and
        vertex number w in `M1` represent the same point in space.

    See Also
    --------
    order_param

    Warnings
    --------
    The algorithm assumes that the vertices at the extremity of each
    edge correspond exactly modulo a translation but does not enforce
    it.

    Notes
    -----
    The algorithm projects the two edges onto the common paramterization
    direction and then loops over the parameter values to build the
    interface.
    """
    if eps is None:
        eps = _FLOAT_TEST
    e0, e1 = np.array(e0, dtype='int'), np.array(e1, dtype='int')
    I1, p1, Vx1 = order_param(M0, e0, A, B)
    I2, p2, Vx2 = order_param(M1, e1, A, B)
    V1 = M0.diam_b.v[I1, e0[p1]]
    V2 = M1.diam_b.v[I2, e1[p2]]
    trans = (M1.vertices[V2[0, 0]]-M0.vertices[V1[0, 0]])
    # Building the new interface
    K_inter = []
    L_inter = []
    param_1 = Vx1[I1[:, p1], p1]  # Vertice number of e0 in order.
    param_2 = Vx2[I2[:, p2], p2]  # Vertice number of e1 in order.

    def advance(i: int, j: int) -> tuple[int, int]:
        # Parametrization of vertices allow to order them. When they are
        # 'put in an array in order', one can enumerate them by
        # following a 'snake' like pattern (0, j)->(1, j)->(0, j+1)...
        return (1-i, j+i)
    i1, j1 = 1, 0
    i2, j2 = 1, 0
    curr_v = V1[0, 0]
    v_inter0 = [curr_v]
    v_inter1 = []
    put_in1 = True
    v_inter = [curr_v]
    curr_K = M0.diam_b.c[e0[p1[0]]]
    curr_L = M1.diam_b.c[e1[p2[0]]]
    common_vertices = {(V1[0, 0], V2[0, 0])}
    while (j1 < len(e0)) and (j2 < len(e1)):
        if np.abs(param_1[i1, j1] - param_2[i2, j2]) <= eps:
            # The current vertex is common to both edges.
            # We advance both parametrization and keep the data from
            # M0.
            common_vertices.add((V1[i1, j1], V2[i2, j2]))
            curr_v = V1[i1, j1]
            curr_K = M0.diam_b.c[e0[p1[j1]]]
            v_inter.append(curr_v)
            i1, j1 = advance(i1, j1)
            curr_L = M1.diam_b.c[e1[p2[j2]]]
            i2, j2 = advance(i2, j2)
        elif param_1[i1, j1] < param_2[i2, j2]:
            # The current vertex comes from M0 so we update the data
            # for the next edge with the information from M0.
            curr_v = V1[i1, j1]
            curr_K = M0.diam_b.c[e0[p1[j1]]]
            v_inter.append(curr_v)
            i1, j1 = advance(i1, j1)
        else:
            # The current vertex comes from M1 so we update the data
            # for the next edge with the information from M1.
            curr_v = -V2[i2, j2]
            curr_L = M1.diam_b.c[e1[p2[j2]]]
            v_inter.append(curr_v)
            i2, j2 = advance(i2, j2)
        if put_in1:
            # Finish an edge.
            v_inter1.append(curr_v)
            K_inter.append(curr_K)
            L_inter.append(curr_L)
        else:
            # Begin an edge.
            v_inter0.append(curr_v)
        put_in1 = not put_in1
    return (np.array([v_inter0, v_inter1]),
            np.array([K_inter, L_inter]),
            trans, np.array(list(common_vertices)))


def glue(M0: Mesh, e0: NDArray[np.int_],
         M1: Mesh, e1: NDArray[np.int_],
         A: NDArray[np.float64],
         B: NDArray[np.float64] | None = None,
         eps: float | None = None) -> Mesh:
    """Create a mesh by merging two boundary pieces.

    This function creates a new mesh from two existing ones by gluing
    boundary parts from each one and creating an inner interface from
    it.

    Parameters
    ----------
    M0, M1 : base_struct.Mesh
        The two meshes.
    e0, e1 : array_like of int
        The two arrays of boundary numbers in `M0` and `M1`
        respectively.
    A, B : array_like of float
        The straight line over which the set of edge is assumed to have
        a functional dependence is given by an origin and a direction.
        If `B` is None, the origin is (0, 0) and `A` containes the
        direction. Else `A` contains the origin and the vector `B-A`
        gives the direction. The default is for `B` to be None.
    eps : float, optional
        Parameter to control the proximity of floats.
        The default is None.

    Returns
    -------
    base_struct.Mesh
        The resulting mesh.

    See Also
    --------
    create_interface

    """
    v_inter, K_inter, t, cv = create_interface(M0, e0, M1, e1, A, B, eps)
    # Vertices number that come from M1
    from_2 = np.where(v_inter < 0)
    # number of interface edges
    ninter = v_inter.shape[1]
    # Array to convert vertices from M1 into their corresponding vertice
    # number from M0 or into their final value in the mesh.
    filter_v2 = np.empty(M1.nvert, dtype='int')
    # kept is the indices from M1 vertices that must appear in the final
    # mesh.
    kept = np.where(np.logical_not(np.isin(np.arange(M1.nvert), cv[:, 1])))
    # First, correspondance  with M0 vertices number
    filter_v2[cv[:, 1]] = cv[:, 0]
    # Then restart the numbering for the remaing vertices
    filter_v2[kept] = np.arange(M1.nvert-len(cv))+M0.nvert

    # Build the centers. Centers from M0 come first then M1
    n_centers = np.empty((M0.nvol+M1.nvol, 2), dtype='float')
    n_centers[:M0.nvol] = M0.centers
    n_centers[M0.nvol:] = M1.centers-t  # t sends M0 to M1

    # Build the vertices. Vertices from M0 come first. Then vertices
    # from M1 which are not already vertices from M0
    n_vertices = np.empty((M0.nvert+M1.nvert-len(cv), 2), dtype='float')
    n_vertices[:M0.nvert] = M0.vertices
    v_inter[from_2] = filter_v2[-v_inter[from_2]]
    n_vertices[M0.nvert:] = M1.vertices[kept]-t

    # Build the inner diamonds. First the inner diamonds of M0 then the
    # inner diamonds of M1 and finally, the inner diamonds of the
    # interface.
    n_dic = np.empty((2, M0.nin+M1.nin+ninter), dtype='int')
    n_div = np.empty((2, M0.nin+M1.nin+ninter), dtype='int')
    n_dic[:, :M0.nin] = M0.diam_i.c
    n_div[:, :M0.nin] = M0.diam_i.v
    n_dic[:, M0.nin:M0.nin+M1.nin] = M1.diam_i.c+M0.nvol
    n_div[:, M0.nin:M0.nin+M1.nin] = filter_v2[M1.diam_i.v]
    n_dic[0, M0.nin+M1.nin:] = K_inter[0]
    n_dic[1, M0.nin+M1.nin:] = K_inter[1]+M0.nvol
    n_div[:, M0.nin+M1.nin:] = v_inter

    # Build the boundary diamonds. First the boundary diamonds of M0
    # then the boundary diamonds of M1
    n_dbc = np.empty(M0.nbnd+M1.nbnd-len(e0)-len(e1), dtype='int')
    n_dbv = np.empty((2, M0.nbnd+M1.nbnd-len(e0)-len(e1)), dtype='int')
    n_dbc[:M0.nbnd-len(e0)] = np.delete(M0.diam_b.c, e0)
    n_dbc[M0.nbnd-len(e0):] = np.delete(M1.diam_b.c, e1)+M0.nvol
    n_dbv[:, :M0.nbnd-len(e0)] = np.delete(M0.diam_b.v, e0, axis=1)
    n_dbv[:, M0.nbnd-len(e0):] = filter_v2[np.delete(M1.diam_b.v, e1, axis=1)]
    n_diam_i = Diamond.pack(n_dic, n_div)
    n_diam_b = Diamond.pack(n_dbc, n_dbv)
    return Mesh(n_centers, n_vertices, (n_diam_i, n_diam_b))


def periodize(M: Mesh, e0: IndexArray, e1: IndexArray,
              A: NDArray[np.float64],
              B: NDArray[np.float64] | None = None,
              eps: float | None = None) -> Mesh:
    """Create a mesh with periodicity in one direction.

    Parameters
    ----------
    M : base_struct.Mesh
        The base mesh.
    e0, e1 : array_like of int
        Two arrays of boundary numbers of `M`.
    A, B : array_like of float
        The straight line over which the set of edge is assumed to have
        a functional dependence is given by an origin and a direction.
        If `B` is None, the origin is (0, 0) and `A` containes the
        direction. Else `A` contains the origin and the vector `B-A`
        gives the direction. The default is for `B` to be None.
    eps : float, optional
        Parameter to control the proximity of floats.
        The default is None.

    Returns
    -------
    base_struct.Mesh
        A mesh where the boundary pieces have been connected to form an
        inner interface.

    Notes
    -----
    The function creates a new mesh where the two boundary pieces have
    been transformed into inner edges.
    """
    e = np.concatenate((e0, e1))
    v_inter, K_inter, t, cv = create_interface(M, e0, M, e1, A, B, eps)
    v_inter = np.abs(v_inter)
    n_dbc = np.delete(M.diam_b.c, e)
    n_dbv = np.delete(M.diam_b.v, e, axis=1)
    n_dic = np.concatenate((M.diam_i.c, K_inter), axis=1)
    n_div = np.concatenate((M.diam_i.v, v_inter), axis=1)
    n_diam_i = Diamond.pack(n_dic, n_div)
    n_diam_b = Diamond.pack(n_dbc, n_dbv)
    return Mesh(M.centers, M.vertices, (n_diam_i, n_diam_b))


def refine(M: Mesh,
           method: Literal['homotopic', 'split_center'] = 'homotopic',
           namax: int = 5) -> Mesh:
    """Refine a mesh.

    Parameters
    ----------
    M : base_struct.Mesh
        The mesh to be refined.
    method : {'homotopic', 'split_center'}, optional
        The refining method. The default is 'homotopic'.
    namax : int , optional
        The maximal number of edges a cell can have after refinement.
        The default is 5.

    Raises
    ------
    TypeError
        The homotopic method can only be applied if the cells consist
        only of triangles and quadrangles. A TypeError is raised if this
        is not the case.

    Returns
    -------
    base_struct.Mesh
        The refined Mesh.
    """
    # choisir orthocenter/barycenter pour les triangles un jour
    Kin, Lin, inner, Kbnd, bnd = M._oldway()

    temp_vol = np.zeros((M.nvol, namax+1), int)
    for i in range(M.nin):
        #  print(i,M.Kin[i],M.Lin[i],temp_vol[M.Kin[i],0],temp_vol[M.Lin[i],0])
        temp_vol[Kin[i], 0] += 1
        temp_vol[Kin[i], temp_vol[Kin[i], 0]] = i
        temp_vol[Lin[i], 0] += 1
        temp_vol[Lin[i], temp_vol[Lin[i], 0]] = i
        #  print(i,M.Kin[i],M.Lin[i],temp_vol[M.Kin[i],0],temp_vol[M.Lin[i],0])
    for i in range(M.nbnd):
        temp_vol[Kbnd[i], 0] += 1
        temp_vol[Kbnd[i], temp_vol[Kbnd[i], 0]] = -i-1
    # print(temp_vol)
    ind_tri: Iterable[int]
    ind_quad: Iterable[int]
    if method == 'homotopic':
        ind_tri = np.where(temp_vol[:, 0] == 3)[0]
        ntri = np.size(ind_tri)
        ind_quad = np.where(temp_vol[:, 0] == 4)[0]
        nquad = np.size(ind_quad)
        if ntri+nquad < M.nvol:
            raise TypeError('Impossible to refine this mesh by this method')
    elif method == 'split_center':
        ind_tri = []
        ntri = 0
        ind_quad = [i for i in range(M.nvol)]
        nquad = M.nvol
        warn('WARNING : this method is not adapted to locally refined meshes')
    # Volumes reconstruction in terms of vertices
    temp_volb = np.zeros((M.nvol, namax+1), int)
    for i in range(M.nvol):
        t = np.zeros((2, temp_vol[i, 0]), int)
        for j in range(temp_vol[i, 0]):
            na = temp_vol[i, j+1]
            if na < 0:
                t[0, j] = bnd[0, -na-1]
                t[1, j] = bnd[1, -na-1]
            else:
                t[0, j] = inner[0, na]
                t[1, j] = inner[1, na]
        tt = np.zeros(temp_vol[i, 0])
        tt[0] = t[0, 0]
        tt[1] = t[1, 0]
        k = 1
        lst = list(range(1, temp_vol[i, 0]))
        ll = [temp_vol[i, 1]]
        while k < (temp_vol[i, 0]-1):
            for j in lst:
                if t[0, j] == tt[k]:
                    k += 1
                    tt[k] = t[1, j]
                    lst.remove(j)
                    ll.append(temp_vol[i, j+1])
                elif t[1, j] == tt[k]:
                    k += 1
                    tt[k] = t[0, j]
                    lst.remove(j)
                    ll.append(temp_vol[i, j+1])
        ll.append(temp_vol[i, 1+lst[0]])
        temp_volb[i, 0] = temp_vol[i, 0]
        temp_volb[i, 1:temp_volb[i, 0]+1] = tt
        temp_vol[i, 1:temp_vol[i, 0]+1] = ll
        # print(temp_vol)
        # print(temp_volb)
    # new mesh construction
    # vertices
    vert = np.zeros((M.nvert+M.nin+M.nbnd+nquad, 2))
    vert[: M.nvert, :] = M.vertices
    vert[M.nvert:M.nvert+M.nin, :] = 0.5*(M.vertices[inner[0]]
                                          + M.vertices[inner[1]])
    vert[M.nvert+M.nin:M.nvert+M.nin+M.nbnd, :] = 0.5*(M.vertices[bnd[0]]
                                                       + M.vertices[bnd[1]])
    vert[M.nvert+M.nin+M.nbnd:, :] = M.centers[ind_quad, :]
    nvert_ai = M.nvert
    nvert_ab = M.nvert+M.nin
    nvert_cen = M.nvert+M.nin+M.nbnd
    # new volumes defined by their vertices
    if method == 'homotopic':
        vol = np.zeros((4*ntri+4*nquad, namax+1), int)
        cent = np.zeros((4*ntri+4*nquad, 2))
    if method == 'split_center':
        nn = np.sum(temp_vol[:, 0])
        vol = np.zeros((nn, namax+1), int)
        cent = np.zeros((nn, 2))
    k = 0
    for i in ind_tri:
        nar = []
        for j in range(1, 4):
            na = temp_vol[i, j]
            if na < 0:
                nar.append(nvert_ab-(na+1))
            else:
                nar.append(nvert_ai+na)
        vol[k, 0] = 3
        for j in range(3):
            vol[k, 1+j] = nar[j]
        cent[k, 0] = np.sum(vert[vol[k, 1:4], 0])/3
        cent[k, 1] = np.sum(vert[vol[k, 1:4], 1])/3
        k += 1
        for j in range(3):
            vol[k, 0] = 3
            vol[k, 1] = nar[j]
            vol[k, 2] = nar[j-1]
            vol[k, 3] = temp_volb[i, j+1]
            cent[k, 0] = np.sum(vert[vol[k, 1:4], 0])/3
            cent[k, 1] = np.sum(vert[vol[k, 1:4], 1])/3
            k += 1
    for ii in range(len(ind_quad)):
        i = ind_quad[ii]
        nar = []
        for j in range(1, temp_vol[i, 0]+1):
            na = temp_vol[i, j]
            if na < 0:
                nar.append(nvert_ab-(na+1))
            else:
                nar.append(nvert_ai+na)
        for j in range(temp_vol[i, 0]):
            vol[k, 0] = 4
            vol[k, 1] = nar[j]
            vol[k, 3] = nar[j-1]
            vol[k, 2] = temp_volb[i, j+1]
            vol[k, 4] = nvert_cen+ii
            cent[k, 0] = np.sum(vert[vol[k, 1:5], 0])/4
            cent[k, 1] = np.sum(vert[vol[k, 1:5], 1])/4
            k += 1
        # print(M.nvol,k,vol)
    for i in range(k):
        v = vol[i, 1:vol[i, 0]+1].tolist()
        v.append(vol[i, 1])
        # print(v)
        # plt.plot(vert[v,0],vert[v,1])
    nvol_new = k
    # creation of the edges
    na = np.sum(vol[:, 0])
    temp_edge = np.zeros((na, 3), int)
    s = 0
    j1 = 0
    for i in range(nvol_new):
        for j in range(vol[i, 0]):
            if j1 < vol[i, 0]:
                j1 = j+1
            else:
                j1 = 1
            if j > 0:
                j2 = j
            else:
                j2 = vol[i, 0]
            temp_edge[s, 2] = i
            temp_edge[s, 0] = min(vol[i, j1], vol[i, j2])
            temp_edge[s, 1] = max(vol[i, j1], vol[i, j2])
            s += 1
    # print('old=', temp_edge)
    temp_edge = temp_edge[np.lexsort((temp_edge[:, 1], temp_edge[:, 0]))]
    # print('new=', temp_edge)
    s = 0
    nin = 0
    nbnd = 0
    Div = np.zeros((2, na), int)
    Dic = np.zeros((2, na), int)
    Dbc = np.zeros(na, int)
    Dbv = np.zeros((2, na), int)
    while s < na:
        if (temp_edge[s, 0] == temp_edge[s+1, 0]
                and temp_edge[s, 1] == temp_edge[s+1, 1]):
            Div[:, nin] = temp_edge[s, :2]
            Dic[0, nin] = temp_edge[s, 2]
            Dic[1, nin] = temp_edge[s+1, 2]
            nin += 1
            s += 2
        else:
            Dbv[:, nbnd] = temp_edge[s, :2]
            Dbc[nbnd] = temp_edge[s, 2]
            nbnd += 1
            s += 1
    return Mesh(cent, vert, (Diamond({'c': Dic, 'v': Div}),
                             Diamond({'c': Dbc, 'v': Dbv})))

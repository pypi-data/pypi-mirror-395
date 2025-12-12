#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base module for mesh management.

This module provides the core tools to manage meshes given by their
edge structure.
"""
from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING, overload
from ..tools.geometry import findbox
from .disc import Discretizable
if TYPE_CHECKING:
    from typing import ClassVar, Self, Iterable, Any
    from numpy.typing import ArrayLike, NDArray
    from ._array_types import PointArray, IndexArray, ValueArray
    from .md import MeshDescription

_FLOAT_TEST = 1e-14


class Diamond:
    """Container class for diamonds.

    Parameters
    ----------
    diam : dict[tuple['c', 'v'], IndexArray]
        The value associated with 'v' is expected to be a (2, n)
        array-like of int. The value associated with 'c' is expected to
        be a (2, n) or (n,) array-like of int. For 0<=j<=n-1,
        diam['c'][:, j] or diam['c'][j] contain the indices (resp. the
        index) of the two (resp. one) centers of the diamond number j
        while diam['v'][:, j] contains the indices of the two vertices
        of the diamond number j.

    Attributes
    ----------
    c : IndexArray
        Data about the centers
    v : IndexArray
        Data about the vertices

    Notes
    -----
    A Diamond class object is expected to work with an outside
    array of centers and an outside array of vertices. Thus centers and
    vertices are referenced to their indexed position in the relevant
    array. An instance of the class can regroup diamonds sharing a
    feature into array of points.

    Instances of this class wrap up data about diamonds. In a 2d mesh,
    a diamond is a set of four points forming a quadrilateral or three
    points forming a triangle. In the case of a quadrilateral, two of
    those points are vertices and the other two are centers. In the case
    of a triangle, one of these points is a center and the other two are
    vertices.
    """

    @classmethod
    def pack(cls, Dc: IndexArray, Dv: IndexArray) -> Self:
        """
        Form a Diamond object from a arrays.

        Parameters
        ----------
        Dc : (2, n) or (n,) array_like of int
            The centers of the diamonds.
        Dv : (2, n) array_like of int
            The vertices of the diamonds

        Returns
        -------
        Diamond

        """
        return cls({'c': np.array(Dc, dtype='int'),
                    'v': np.array(Dv, dtype='int')})

    def __init__(self, diam: dict[str, IndexArray]):
        self.c: IndexArray = np.array(diam['c'], dtype='int')
        self.v: IndexArray = np.array(diam['v'], dtype='int')

    def unpack(self) -> tuple[IndexArray, IndexArray]:
        """Return the diamond as a tuple.

        Centers first and vertices second.
        """
        return (self.c, self.v)


class _MetaMesh(type):
    """A Meta class to construct mesh handling classes."""

    def __new__(mcs, name: str,
                base: tuple[type],
                namespace: dict[str, Any]) -> type:
        """Create a MetaMesh type class."""
        if '_pointvars' in namespace:
            del namespace['_pointvars']
        elif 'pointvars' not in namespace:
            raise AttributeError('Classes derived from BaseMesh must define '
                                 + 'pointvars as a class attribute.')
        if '_geometry' in namespace:
            del namespace['_geometry']
        elif 'geometry' not in namespace:
            raise AttributeError('Classes derived from BaseMesh must define '
                                 + 'geometry as a class attribute.')
        return super().__new__(mcs, name, base, namespace)


class BaseMesh(metaclass=_MetaMesh):
    """Root class of the MetaMesh type."""

    _pointvars = True
    _geometry = True


class Mesh(BaseMesh):
    """Base class for mesh management through the edge structure.

    The `Mesh` class is designed to handle standard operations on 2d
    meshes of a bounded polygonal domain of the plane through what is
    called its edge structure. Subclasses need only to describe the
    geometric information and the `Mesh` class will use this information
    to handle various operations such as plotting or managing discrete
    functions.

    Parameters
    ----------
    c : PointArray
        Array containing the positions of the centers.
    v : PointArray
        Array containing the positions of the vertices.
    diams : tuple
        If diams has two elements, they must be `Diamond` objects. In
        this case the first element contains the data of the inner edges
        while the second element contains the data of the boundary
        edges. Otherwise diams should have four elements which are
        arrays. The first two elements are packed into an inner edges
        `Diamond` object and the last two are packed into a boundary
        edges `Diamond` object.
    **geom
        Geometric information can be passed under the form `_attr=value`
        where `attr` (no leading underscore) is a
        `tools.geometry.geometric_property`.

    Attributes
    ----------
    centers : (nvol, 2) numpy.ndarray
        Array containing the positions of the centers in the plane.
    vertices : (nvert, 2) numpy.ndarray
        Array containing the positions of the vertices in the plane.
    diam_i : Diamond
        Diamond object containing the data of the inner edges.
        `diam_i.c[0, s]` and `diam_i.c[1, s]` are the cell volume
        numbers that the edge separate while `diam_i.v[0, s]` and
        `diam_i.v[1, s]` are the two vertice numbers that bound the
        edge.
    diam_b : Diamond
        Diamond object containing the data of the boundary edges.
        `diam_b.c[s]` is the cell volume number that the edge
        separate from the exterior while `diam_b.v[0, s]` and
        `diam_b.v[1, s]` are the two vertice numbers that bound the
        edge.
    nvol : int
        Number of control volumes in the mesh.
    nvert : int
        Number of vertices in the mesh.
    npoints_by_type : dict[str, int]
        Number of points of each type present in the `pointvars`
        attribute.
    npoints : int
        Total number of points. This is the sum of all the number of
        points in attributes defined by `pointvars`.
    nin : int
        Number of inner edges.
    nbnd : int
        Number of boundary edges.
    box : (float, float, float, float)
        A rectangle box containing all the points defined by
        `pointvars`. The box is `(mx, Mx, my, My)` so that
        [mx, Mx]x[my, My] contains all the points.

    Warnings
    --------
    No control is done on the data given to instantiate a `Mesh` object.
    The purpose of this class is to store mesh data in a way that
    facilitates the writing of schemes. Actual meshes should be obtained
    from other tools and then their data transfered to the `Mesh` object
    in a suitable way.

    See Also
    --------
    Diamond
    pynitevolumes.tools.geometry.geometric_property

    Notes
    -----
    A mesh is conceptualized here as a set of edges which are segments
    in the plane which are bound by vertices. These edges enclose
    polygonals called cells or control volumes. In a `Mesh` object
    almost all data is stored in reference to an attached edge (hence
    the name edge structure).

    To facilitate the writing of Finite Volume Schemes, a `Mesh` object
    maintains two type of edges: inner edges which are characterized by
    the fact that they separate two cells, and boundary edges which
    separate one cell to the exterior of the domain. Each cell also has
    a point called its center attached to it. A mesh is then subdivided
    into its diamonds :

    * for an inner edge, a diamond consist of the two vertices bounding
      the edge and the two centers of the two cells that the edge
      separates,
    * for a boundary edge, a diamond consist of the two vertices
      bounding the edge and the center of the cell which the edge
      separates from the exterior of the domain.

    """

    #: Geometric properties that are points in the plane.
    #: Must be defined for every subclass of `Mesh`.
    #: Note that attributes refered to in this list must be array_like of shape
    #: (n, 2).
    pointvars: ClassVar[list[str]] = ['centers', 'vertices']
    #: Geometric properties that are vector fields in nature.
    #: Optional for subclasses but recommended.
    vectorvars: ClassVar[list[str]] = []
    #: Geometric properties not recorded in `pointvars`or `vectorvars`.
    #: Must be defined for every subclass of `Mesh`.
    #: This list must contain the name of the attributes of `Mesh`
    #: instances that are `pynitevolumes.tools.geometry.geometric_property`.
    #: The order in which the properties appear in this list is the
    #: order in which they will be constructed when instantiating an
    #: object so if a geometric object is needed for the computation of
    #: another geometric object, it must appear before in the
    #: `geometry` list.
    geometry: ClassVar[list[str]] = []

    @classmethod
    def fromMesh(cls, M: 'Mesh', *args: Any, **kwargs: Any) -> Self:
        """Class method to enrich a base object to a richer structure.

        Subclasses of `Mesh` can form a hierarchy of increasingly richer
        geometric structure. In order to not recompute geometric
        information already contained in a parent class one can use the
        method `fromMesh` of the child class to compute only geometric
        properties not known to the parent class.

        Parameters
        ----------
        M : Mesh
            Object in a parent `Mesh` subclass to be enriched with the
            geometry of the child subclass.
        *args, **kwargs
            Additional arguments to be passed to the child subclass
            constructor.

        Returns
        -------
        type[Mesh]
            The instance of the child subclass.
        """
        known_geometry = {k: getattr(M, k) for k in M.geometry}
        return cls(M.centers, M.vertices, (M.diam_i, M.diam_b),
                   *args, **known_geometry, **kwargs)

    def __init__(self, c: PointArray, v: PointArray,
                 diams: tuple[IndexArray,
                              IndexArray,
                              IndexArray,
                              IndexArray] | tuple[Diamond, Diamond],
                 **geom: Any):
        self.centers = np.array(c)
        self.vertices = np.array(v)
        if len(diams) > 2:
            self.diam_i = Diamond.pack(np.array(diams[0]), np.array(diams[1]))
            self.diam_b = Diamond.pack(np.array(diams[2]), np.array(diams[3]))
        else:
            self.diam_i, self.diam_b = diams
        self.getinfo()
        geo_to_compute = [set(self.pointvars)-{'centers', 'vertices'},
                          self.geometry,
                          self.vectorvars]
        for geo in geo_to_compute:
            for attr in geo:
                if f'_{attr}' in geom:
                    setattr(self, attr, geom.pop(f'_{attr}'))
                else:
                    setattr(self, attr,
                            getattr(type(self), attr).initialize(self))
        if geom:
            for k, v in geom.items():
                setattr(self, k, v)
        self.npoints_by_type = {k: len(getattr(self, k))
                                for k in self.pointvars}
        self.npoints = sum(self.npoints_by_type.values())
        self.box = self.getbox()

    def getbox(self, margin: float = 0.0) -> tuple[float, float, float, float]:
        """Compute the mesh box extremities."""
        p = []
        for t in self.pointvars:
            p.append(getattr(self, t))
        return findbox(*p, margin=margin)

    def getinfo(self) -> None:
        """Compute basic information.

        Compute the number of volumes, vertices, inner and boundary
        edges.
        """
        self.nvol = self.centers.shape[0]
        self.nvert = self.vertices.shape[0]
        self.nin = self.diam_i.v.shape[1]
        self.nbnd = self.diam_b.v.shape[1]

    def move_rigid(self, v: ArrayLike = (0.0, 0.0),
                   theta: float |
                   None |
                   tuple[float, NDArray[np.float64]] = None
                   ) -> None:
        """Move the mesh through a rigid motion of the plane.

        Parameters
        ----------
        v : (2,) array_like, optional
            The translation part of the motion. The default is
            (0.0, 0.0).
        theta : scalar or tuple or None, optional
            The rotation part of the motion.

            * If None, there is no rotation.
            * If scalar, represents the angle of rotation, the center of
              the rotations is assumed to be the origin of the
              coordinates.
            * If tuple, the first element is the scalar angle of the
              rotation and the second is an array-like of length 2
              containing the coordinates of the origin of the rotation.

            The default is None.

        Returns
        -------
        None.

        Notes
        -----
        For the `Mesh` class, `move_rigid` only acts on the coordinates
        of the centers and the coordinates of the vertices.

        For child classes of `Mesh`, `move_rigid` will silently
        change the coordinates of any array whose name is in `pointvars`
        and will rotate (no translation) the coordinates of any array
        whose name is in `vectorvars`. Keeping these two attributes
        up-to-date with the relevant geometrical information is thus
        desirable.

        """
        if theta is not None:
            if isinstance(theta, float):
                angle = theta
                origin = np.zeros(2, dtype=np.float64)
            else:
                angle, origin = theta
            Q = np.array([[np.cos(angle), np.sin(angle)],
                         [-np.sin(angle), np.cos(angle)]])
            for t in self.pointvars:
                nt = origin+(getattr(self, t)-origin).dot(Q)
                setattr(self, t, nt)
            for t in self.vectorvars:
                nt = getattr(self, t).dot(Q)
                setattr(self, t, nt)
        for t in self.pointvars:
            nt = getattr(self, t)+v
            setattr(self, t, nt)

    def diamonds(self) -> tuple[tuple[tuple[PointArray, PointArray],
                                      tuple[PointArray, PointArray]],
                                tuple[PointArray,
                                      tuple[PointArray, PointArray]]]:
        """Compute the geometrical diamonds.

        This method gives the actual positions in the plane of the
        points refered to by the diamonds.

        Returns
        -------
        (diamint, diamext) : tuple
            `diamint` is a tuple of tuple  `((K, L), (V0, V1))
            where `K, L, V0, V1` are all arrays of the same shape
            (`self.nin`, 2).

            * For all `s`, `K[s]` and `L[s]` contain the coordinates of
              the two **centers** that are on each side of the inner
              edge of index `s`.
            * For all `s`, `V0[s]` and `V1[s]` contain the coordinates
              of the two **vertices** that bound the inner edge of index
              `s`.

            `diamext` is a tuple `(Kb, (Vb0, Vb1))`where `Kb, Vb0, Vb1``
            are all arrays are of the same shape (`self.nbnd`, 2).

            * For all `s`, `Kb[s]` contains the coordinates of the
              **center** that the boundary edge of index `s` separates
              from the exterior.
            * For all `s`, `Vb0[s]` and `Vb1[s]` contain the coordinates
              of the two **vertices** that bound the boundary edge of
              index `s`.

        Notes
        -----
        This method returns
        `((Kin, Lin), (Vin0, Vin1)), (Kb, (Vb0, Vb1))`
        where the quadrilateral of the plane `Kin[s]`, `Vin0[s]`,
        `Lin[s]`, `Vin1[s]` is the diamond associated to the inner edge
        of index `s` and the triangle of the plane `Kb[s]`, `Vb0[s]`,
        `Vb1[s]` is the (half) diamond associated to the boundary edge
        of index `s`.
        """
        Dic, Div = self.diam_i.unpack()
        Dbc, Dbv = self.diam_b.unpack()
        diamint = ((self.centers[Dic[0]], self.centers[Dic[1]]),
                   (self.vertices[Div[0]], self.vertices[Div[1]]))
        diamext = (self.centers[Dbc],
                   (self.vertices[Dbv[0]], self.vertices[Dbv[1]]))
        return (diamint, diamext)

    @overload
    def evaluate(self, f: Discretizable,
                 point_types: str,
                 *args: Any, **kwargs: Any
                 ) -> ValueArray: ...

    @overload
    def evaluate(self, f: Discretizable,
                 point_types: Iterable[str],
                 *args: Any, **kwargs: Any
                 ) -> dict[str, ValueArray]: ...

    def evaluate(self, f: Discretizable,
                 point_types: str | Iterable[str],
                 *args: Any, **kwargs: Any
                 ) -> ValueArray | dict[str, ValueArray]:
        """Evaluate an object on a set of points.

        This function splits the data contained in `f` and returns a
        dictionary allowing easy access to its values on the points
        contained in `point_types`.

        Parameters
        ----------
        f : disc.Discretizable
            Object to be evaluated.
        point_types : str or iterable of str
            The attribute(s) of `self` where one wants to evaluate `f`.
        *args, **kwargs
            Supplementary arguments needed by `f` for evaluation.

        Returns
        -------
        f_Part : dict[str, numpy.ndarray] or numpy.ndarray
            A dictionary whose keys are the elements of `point_types`
            and the associated values are (np, ...) `numpy.ndarray`
            where `np` is the number of the corresponding `point_types`
            inside `self` representing somehow the evaluation of `f` on
            the different `point_types`. To find out how this evaluation
            is obtained for a particular type, use
            `help(disc.Discretizable)`. If `point_types` is a str or has
            only one element, return the evaluation itself.

        Raises
        ------
        TypeError
            Only subclasses of the `disc.Discretizable` type can be
            evaluated. If you want an object that is not a subclass to
            `disc.Discretizable` to be supported, use
            `disc.Discretizable.add_type` to register it first.

        Warning
        -------
        If there are several protocols available for evaluation of `f`
        because of multiple inheritance but not one that matches the
        type of `f` exactly, there is no guarantee that a specific
        protocol will be used.
        """
        point_types_seq: Iterable[str]
        if isinstance(point_types, str):
            point_types_seq = [point_types]
        else:
            point_types_seq = point_types
        # If there is a protocol for exactly the type of f.
        if type(f) in Discretizable._ev_map:
            fd = Discretizable._ev_map[type(f)](self, f, point_types_seq,
                                                *args, **kwargs)
            if isinstance(point_types, str):
                return fd[point_types]
            else:
                return fd
        # There is no protocol for the exact type of f so loop to find
        # if there is at least one for a super type of f.
        for known_subcls, ev_protocol in Discretizable._ev_map.items():
            if isinstance(f, known_subcls):
                fd = ev_protocol(self, f, point_types_seq, *args, **kwargs)
                if isinstance(point_types, str):
                    return fd[point_types]
                else:
                    return fd
        raise TypeError("Could not find a way to  evaluate object " +
                        f"of type {type(f)}")

    def discretize(self, f: Discretizable, md: MeshDescription,
                   *args: Any, **kwargs: Any
                   ) -> dict[str, ValueArray]:
        """Return the evaluation of a function on a submesh.

        This function evaluates a discrete function to work with a
        submesh described by a `md.MeshDescription`.

        Parameters
        ----------
        f : disc.Discretizable
            Representation of a discrete function.
            See Mesh.evaluate for details.
        md : md.MeshDescription
            The submesh object.

        Returns
        -------
        dict
            Discretized function over all relevant points in `md`.

        See Also
        --------
        Mesh.evaluate, md.MeshDescription

        Notes
        -----
        While `Mesh.evaluate` is useful when evaluating objects on a
        specific element of `Mesh.pointvars`, `discretize` will take
        care of the evaluation on whole standard submeshes.

        """
        return self.evaluate(f, md.used_centers, *args, **kwargs)

    def _oldway(self) -> tuple[IndexArray, IndexArray, IndexArray,
                               IndexArray, IndexArray]:
        return (self.diam_i.c[0], self.diam_i.c[1], self.diam_i.v,
                self.diam_b.c, self.diam_b.v)

    def _center_struct(self, i: int) -> tuple[IndexArray,
                                              IndexArray,
                                              IndexArray]:
        Iin = np.where(self.diam_i.c[0] == i)[0]
        Jin = np.where(self.diam_i.c[1] == i)[0]
        Ibnd = np.where(self.diam_b.c == i)[0]
        return Iin, Jin, Ibnd

    def _find_bound_vert(self) -> IndexArray:
        return np.unique(self.diam_b.v)

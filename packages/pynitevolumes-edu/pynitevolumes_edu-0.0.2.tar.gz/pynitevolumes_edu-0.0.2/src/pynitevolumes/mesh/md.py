#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mesh descriptions.

This module provide tools to access in a systematic and hopefully
readable way into information contained inside `base_struct.Mesh`
objects.

For the moment, what this module provides are tools that work with
`pynitevolumes.schemes.tpfa` and `pynitevolumes.schemes.ddfv`.

What is most probably needed from this module are only the predefined
`MeshDescription` objects and among them the most useful is `PRIMAL`.
Using these we have only one function for plotting a submesh and one
protocol to evaluate discrete functions independently of the submesh
on which they are defined. If these objects are not sufficient one may
try to create more appropriate `MeshDescription` objects than the ones
that already exist.

Attributes
----------
K, L, A, B, Kb, Ab, Bb, Xsi, Xsb : PointType
PRIMAL, DUAL, DIAM, TAU, TAU_FULL : MeshDescription

Notes
-----
The preconstructed `PointType` are standard names in the literature of
Finite Volume Schemes: inner diamonds are defined by the two vertices
which are designated by `PointType` `A` and `B` and two centers which
are designated by `PointType` `K` and `L`; boundary diamonds are defined
by the two vertices which are designated by `PointType` `Ab` and `Bb`
and the center which is designated by `PointType` `Kb`. `PointType`
`Xsi` and `Xsb` designate the so-called center of the inner and boundary
edges respectively.

The `MeshDescription` `PRIMAL` is obtained by aggregating all the
triangles of the form `K` `A` `B`, `L` `A` `B` and `Kb` `Ab` `Bb`.
This is the only `MeshDescription` that can be used with `Mesh`
instances as they only involve the centers and the vertices. The
`TriangleType` are set up so that the `value_points` are at centers.

The `MeshDescription` `DUAL` is obtained by aggregating the triangles of
the form `A` `K` `L`, `B` `K` `L`, `Ab` `Kb` `Xsb`, `Bb` `Kb` `Xsb`.
This `MeshDescription` can be used as soon as edge centers `xs_i` and
`xs_b` are defined for the `Mesh` subclass. The `TriangleType` are set
up so that the `value_points` are at the vertices.

The `MeshDescription` `DIAM` is obtained by aggregating the triangles of
the form `Xsi` `K` `A`, `Xsi` `K` `B`, `Xsi` `L` `A`, `Xsi` `L` `B`,
`Xsb` `Ab` `Kb` and `Xsb` `Bb` `Kb`. The `TriangleType` are set up so
that the `value_points` are at the edge centers.

The `MeshDescription` `TAU` and `TAU_FULL` aggregate the same triangles
as `DIAM` except that they use as `value_points` the centers and the
vertices.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal
import numpy as np
if TYPE_CHECKING:
    from collections.abc import Sequence, Iterable, Generator
    from pynitevolumes.mesh._array_types import IndexArray
    from pynitevolumes.mesh.base_struct import Mesh


@dataclass(slots=True, frozen=True)
class PointType:
    """Description of a category of point inside a Mesh.

    Parameters
    ----------
    attribute_name : str
        Name of the attribute inside a
        `pynitevolumes.mesh.base_struct.Mesh` subclass the instance
        refers to.
    numbering : {'i', 'b'}
        Whether the category of point is indexed through the inner edges
        numerotation or the boundary edges numerotation.
    on_b : bool
        Set to True to signify that the points rest geometrically on the
        boundary of the mesh.
    display_name : str
        Character chain representing the point type.

    Notes
    -----
    `t` should refer to the corresponding name of attribute inside the
    `pynitevolumes.mesh.base_struct.Mesh` subclass but without the '_i'
    or '_b' as this is handled separately via `numbering`.
    """

    type: str
    numbering: Literal['i', 'b']
    on_b: bool
    display_name: str | None
    attribute_name: str = field(init=False)

    def __post_init__(self) -> None:
        """Add the `attribute_name`."""
        object.__setattr__(self, 'attribute_name',
                           self.type+ '_' + self.numbering)

    def __repr__(self) -> str:
        """Return repr(self)."""
        if self.display_name is None:
            rep = (f"PointType({self.attribute_name}, "
                   + f"{self.numbering}, "
                   + f"{repr(self.on_b)}, "
                   + "None)")
        else:
            rep = self.display_name
        return rep

    def index_from(self, M: Mesh) -> IndexArray:
        """Index category of points.

        Parameters
        ----------
        M : `base_struct.Mesh`
            The mesh to get the indices from.

        Returns
        -------
        IndexArray
            The indices relevant for the category of point for the mesh
            `M`.

        """
        if self.numbering == 'i':
            return np.arange(M.nin)
        elif self.numbering == 'b':
            return np.arange(M.nbnd)


@dataclass(slots=True, frozen=True)
class CVPointType(PointType):
    """Point types associated to centers or vertices.

    Parameters
    ----------
    select: {0, 1} or None. Default is None
        When two point of the same type can be attached to a diamond
        (two centers for an inner diamond and the two vertices for every
        diamond) select one of the two.
    """

    select: int | None = None

    def __post_init__(self) -> None:
        """Add the `attribute_name`."""
        object.__setattr__(self, 'attribute_name', self.type)

    def index_from(self, M: Mesh) -> IndexArray:
        """Index the category of points.

        Since centers and vertices get special treatment in a mesh,
        this method gets the indices for the points of such a category.
        """
        c_or_v = self.type[0].lower()
        if c_or_v == 'c' and self.numbering == 'b':
            return M.diam_b.c
        else:
            attr = f"diam_{self.numbering}"
            return getattr(getattr(M, attr), c_or_v)[self.select]  # type: ignore

    def __repr__(self) -> str:
        """Return repr(self)."""
        c_or_v = self.type[0].lower()
        rep = f"diam_{self.numbering}.{c_or_v}"
        if self.select is not None:
            rep += f"[{self.select}]"

        return rep


class TriangleType:
    """Description of a category of triangle inside a Mesh.

    Instances of this class are abstract designation of triangles
    inside `Mesh` objects by designating the `PointType` that make their
    vertices.

    Parameters
    ----------
    value_points, complement : PointType or sequence of PointType
        The number of PointType in between these two arguments must sum
        up to 3. `value_points` must contain at least one `PointType`.
        `complement` may be omitted if `value_points` has length 3.

    Attributes
    ----------
    vp : list of PointType
        From `value_points`.
    comp : list of PointType
        From `complement`.

    Notes
    -----
    `TriangleType` instances are iterable and will enumerate the `PointType`
    instances starting with those from `vp` in order and ending with the
    ones from `comp`.
    `value_points` and `complement` differ because evaluation of a
    function on a triangle of the TriangleType will be done by averaging
    the values of the function at `value_points` and `PointType` from
    `complement` are ignored in the process.
    """

    def __init__(self, value_points: Iterable[PointType],
                 complement: Iterable[PointType] | None = None):
        self.vp = list(value_points)
        if complement is None:
            self.comp = []
        else:
            self.comp = list(complement)
        if len(self.vp)+len(self.comp) != 3:
            raise ValueError('Triangles should get exactly 3 references '
                             + 'splitted between value_points and complement')

    def __iter__(self) -> Generator[PointType]:
        """Yield the value points and then the complement."""
        def iterTriangle() -> Generator[PointType]:
            for p in self.vp:
                yield p
            for p in self.comp:
                yield p
        return iterTriangle()

    # def get_verts(self):
    #     return self.vp+self.comp

    # def has_same_verts(self, other):
    #     if not isinstance(other, TriangleType):
    #         return NotImplemented
    #     c0, e0, f0 = self.get_verts()
    #     c1, e1, f1 = other.get_verts()
    #     return {c0, e0, f0} == {c1, e1, f1}

    def __repr__(self) -> str:
        """Represent the TriangleType by its vertices."""
        value_points = ','.join((repr(p) for p in self.vp))
        complements = ','.join((repr(p) for p in self.comp))
        return f'{type(self).__name__}(({value_points}), ({complements}))'


class MeshDescription:
    """Description of a submesh inside a Mesh object.

    Abstract description of submeshes obtained from a single primal
    mesh.

    Parameters
    ----------
    tri_seq : sequence of TriangleType
        Sequence of all the `TriangleType` that make up the submesh.

    Attributes
    ----------
    used_points : set[str]
        Set of `PointType.type` needed for the submesh description.
    used_centers : set[str]
        Subset of `used_points` of the `PointType.type` appearing as
        `value_points` for the `TriangleType`
    tri_seq
        from `tri_seq`

    """

    def __init__(self, tri_seq: Sequence[TriangleType]):
        self.tri_seq = tri_seq
        used_points: set[str] = set()
        used_centers: set[str] = set()
        for c_tri in tri_seq:
            used_centers.update([p.attribute_name for p in c_tri.vp])
            for point in c_tri:
                used_points.add(point.attribute_name)
        self.used_points = used_points
        self.used_centers = used_centers


K = CVPointType('centers', 'i', False, None, select=0)
L = CVPointType('centers', 'i', False, None, select=1)
A = CVPointType('vertices', 'i', False, None, select=0)
B = CVPointType('vertices', 'i', False, None, select=1)
Kb = CVPointType('centers', 'b', False, None)
Ab = CVPointType('vertices', 'b', True, None, select=0)
Bb = CVPointType('vertices', 'b', True, None, select=1)

_base_PRIMAL = [TriangleType([K], (A, B)),
                TriangleType([L], (A, B)),
                TriangleType([Kb], (Ab, Bb))]

PRIMAL = MeshDescription(_base_PRIMAL)

Xsi = PointType('xs', 'i', False, r'$x^\sigma$')
Xsb = PointType('xs', 'b', True, r'$x^\sigma$')

_base_DUAL = [TriangleType([A], (K, L)),
              TriangleType([B], (K, L)),
              TriangleType([Ab], (Kb, Xsb)),
              TriangleType([Bb], (Kb, Xsb))]

DUAL = MeshDescription(_base_DUAL)

_base_diam = [TriangleType([Xsi], (K, A)),
              TriangleType([Xsi], (K, B)),
              TriangleType([Xsi], (L, A)),
              TriangleType([Xsi], (L, B)),
              TriangleType([Xsb], (Ab, Kb)),
              TriangleType([Xsb], (Bb, Kb))]

DIAM = MeshDescription(_base_diam)

_base_tau = [TriangleType((K, A), [Xsi]),
             TriangleType((L, A), [Xsi]),
             TriangleType((K, B), [Xsi]),
             TriangleType((L, B), [Xsi]),
             TriangleType((Kb, Ab), [Xsb]),
             TriangleType((Kb, Bb), [Xsb])]

TAU = MeshDescription(_base_tau)

_base_tau_full = [TriangleType((K, A), [Xsi]),
                  TriangleType((L, A), [Xsi]),
                  TriangleType((K, B), [Xsi]),
                  TriangleType((L, B), [Xsi]),
                  TriangleType((Kb, Ab, Xsb)),
                  TriangleType((Kb, Bb, Xsb))]

TAU_FULL = MeshDescription(_base_tau_full)

PREDEFINED_MD = {'PRIMAL': PRIMAL,
                 'primal': PRIMAL,
                 'DUAL': DUAL,
                 'dual': DUAL,
                 'DIAM': DIAM,
                 'diam': DIAM,
                 'TAU': TAU,
                 'tau': TAU,
                 'TAU_FULL': TAU_FULL,
                 'tau_full': TAU_FULL}

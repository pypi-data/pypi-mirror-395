#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools to handle geometric operations on points and vectors.

This module takes advantage of the NumPy library to efficiently perform
certain 2d geometric computations on large collections of points
(or vectors) contained in arrays. In these functions it is always
assumed that the x,y coordinates are in the last axis (of dimension at
least 2). Any prior dimensions will be essentially looped upon.
"""
from __future__ import annotations
import numpy as np
from numpy.linalg import norm
from typing import TYPE_CHECKING, overload
if TYPE_CHECKING:
    from typing import Self, Any
    from collections.abc import Callable
    from numpy.typing import NDArray
    from pynitevolumes.mesh._array_types import PointArray, ValueArray


class geometric_property[T, S]:
    """Descriptor class of a geometric property.

    A `geometric_property` instance is a descriptor with an
    initialization mechanism. Following the same idiom as `property`, it
    is best used as a decorator.

    Parameters
    ----------
    build : function
        The initialization function for the property. The name of the
        function serves as a name for the property.

    Attributes
    ----------
    build
        from `build`
    """

    def __set_name__(self, owner: T, name: str) -> None:
        """Set name for the property."""
        self.public_name: str = name
        self.private_name: str = '_' + name

    def __init__(self, build: Callable[[T], S]) -> None:
        self.build = build
        self.__doc__ = build.__doc__

    @overload
    def __get__(self, obj: None, objtype: type | None) -> Self: ...

    @overload
    def __get__(self, obj: T, objtype: type | None) -> S: ...

    def __get__(self, obj: T | None, objtype: type | None) -> Self | S:
        """Return the value of the property."""
        if obj is None:
            return self
        value: S = getattr(obj, self.private_name)
        return value

    def __set__(self, obj: T, value: Any) -> None:
        """Set the value of the property."""
        setattr(obj, self.private_name, value)

    def __delete__(self, obj: T) -> None:
        """Delete the value of the property."""
        if hasattr(obj, self.private_name):
            delattr(obj, self.private_name)
        else:
            raise AttributeError(f"{type(obj).__name__} has no attribute "
                                 + "'{self.public_name}'",
                                 name=self.public_name,
                                 obj=obj)

    def initialize(self, obj: T, *args: Any, **kwargs: Any) -> S:
        """Initialize the value of the property."""
        return self.build(obj, *args, **kwargs)


def findbox(*args: PointArray,
            margin: float = 0.0) -> tuple[float, float, float, float]:
    """Find a square box containing points.

    Parameters
    ----------
    *args : array-like
        (n, 2) array-like objects containing points.
    margin : float, optional
        If margin is non-zero, increase the dimensions of the box of a
        factor margin. The points then do not fall on the border of the
        box. The default is 0.0.

    Returns
    -------
    mx, Mx, my, My : tuple[float]
        The box [mx, Mx]x[my, My] contain all of the points.
    """
    args_list = list(args)
    points, *args_list = args_list
    mx = np.min(points[:, 0])
    Mx = np.max(points[:, 0])
    my = np.min(points[:, 1])
    My = np.max(points[:, 1])

    while args_list:
        points, *args_list = args_list
        if points.size > 0:
            mx = np.min([mx, np.amin(points[:, 0])])
            Mx = np.max([Mx, np.amax(points[:, 0])])
            my = np.min([my, np.amin(points[:, 1])])
            My = np.max([My, np.amax(points[:, 1])])
    mx = mx-margin*(Mx-mx)
    Mx = Mx+margin*(Mx-mx)
    my = my-margin*(My-my)
    My = My+margin*(My-my)
    return mx, Mx, my, My


def turn(u: PointArray) -> PointArray:
    r"""Rotate a 2D vector of pi/2 in the direct sense.

    Parameters
    ----------
    u : (\* shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\* shape, 2) numpy.ndarray
        Array containing the scalar product of the two vectors.
    """
    u = np.array(u)
    return np.stack((-u[..., 1], u[..., 0]), axis=-1)


def wedge(u: PointArray, v: PointArray) -> ValueArray:
    r"""Compute the wedge product of two 2D vectors.

    Parameters
    ----------
    u, v : (\*shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, ) numpy.ndarray
        Array containing the wedge product (or determinant) of the two
        vectors.
    """
    u, v = np.array(u), np.array(v)
    return u[..., 0]*v[..., 1]-u[..., 1]*v[..., 0]


def multscalar(u: PointArray, v: PointArray) -> ValueArray:
    r"""Compute the scalar product of two 2D vectors line-by-line.

    Parameters
    ----------
    u, v : (\*shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, ) numpy.ndarray
        Array containing the scalar product of the two vectors.
    """
    u, v = np.array(u), np.array(v)
    return u[..., 0]*v[..., 0]+u[..., 1]*v[..., 1]


def vnorm(u: PointArray) -> ValueArray:
    """Compute norm of an array line-by-line.

    Parameters
    ----------
    u : array-like
        Array containing the data.

    Returns
    -------
    numpy.ndarray
        Array containing the euclidean vector norm of `u` with respect
        to the last axis. Its shape is thus `u.shape[:-1]`.

    Warning
    -------
    If `u` only has one axis of length n it is considered as a singular
    vector in an n dimensional space, not n vectors in a 1 dimensional
    space. Use `numpy.abs` for the latter case.
    """
    u = np.array(u)
    result: ValueArray = norm(u, 2, -1)
    return result


def multmatvect(A: NDArray[np.float64], v: PointArray) -> PointArray:
    r"""Compute the matrix product of a matrix A and a vector v.

    Parameters
    ----------
    A : (2, 2, \*shape) array_like
        Array of matrices. The coordinates acting on 2d space must be
        contained on the first two axes.
    v : (\*shape, 2) array_like
        Array of vectors. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, 2) numpy.ndarray
        Array containing the result of the matrix vector product.
    """
    A, v = np.array(A), np.array(v)
    result: PointArray = np.einsum('ij...,...j->...i', A, v)
    return result


def triarea(A: PointArray, B: PointArray, C: PointArray) -> ValueArray:
    r"""Compute the area of a triangle given by three vertices.

    Parameters
    ----------
    A, B, C : (\*shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape,) numpy.ndarray
        Array containing the area of the triangle with vertices `A`, `B`
        and `C`.
    """
    A, B, C = np.array(A), np.array(B), np.array(C)
    return 0.5*np.abs(wedge(B-A, C-A))


def orthocenter(A: PointArray, B: PointArray, C: PointArray) -> PointArray:
    r"""Compute the orthocenter of a triangle given by three vertices.

    Parameters
    ----------
    A, B, C : (\*shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, 2) numpy.ndarray
        Array containing the coordinates of the orthocenter of the
        triangle with vertices `A`, `B` and `C`.
    """
    A, B, C = np.array(A), np.array(B), np.array(C)
    Orth: PointArray = (A+0.5*(B-A)
                        - 0.5*np.inner(C-B, C-A)/wedge(C-B, B-A)*turn(B-A))
    return Orth


def barycenter(point: PointArray, *points: PointArray) -> PointArray:
    """Compute the barycenter of points."""
    n = len(points)
    points_arr = (np.array(point) for point in points)
    return 1/(n+1)*sum(points_arr, start=point)


def intersect(A: PointArray, B: PointArray, C: PointArray, D: PointArray
              ) -> PointArray:
    r"""Compute the intersection of points.

    Parameters
    ----------
    A, B, C, D : (\*shape, 2) array_like
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, 2) numpy.ndarray
        The array containing the coordinates of the intersection of
        `[A, B]` with `[C, D]`.
    """
    A, B, C, D = np.array(A), np.array(B), np.array(C), np.array(D)
    return A+(np.tile(wedge(D-C, D-A)/wedge(D-C, B-A), (2, 1)).T)*(B-A)


def orthoproject(A: PointArray, B: PointArray, C: PointArray) -> PointArray:
    r"""Compute the orthogonal projection of points.

    Parameters
    ----------
    A, B, C : (\*shape, 2) numpy.ndarray.
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, 2) numpy.ndarray
        Array containing the coordinates of the orthogonal
        projection of `A` onto `[B, C]`.
    """
    A, B, C = np.array(A), np.array(B), np.array(C)
    u = B-C
    v = C-A
    return C-(np.tile(multscalar(u, v)/multscalar(u, u), (2, 1)).T)*u


def circum_center(A: PointArray, B: PointArray, C: PointArray) -> PointArray:
    r"""Compute the center of the circumscribed triangle.

    Parameters
    ----------
    A, B, C : (\*shape, 2) array_like.
        Arrays of points. The 2d coordinates must be contained in the
        last axis.

    Returns
    -------
    (\*shape, 2) numpy.ndarray
        Array containing the center of the circumscribed triangle of
        vertices `A`, `B` and `C`.
    """
    A, B, C = np.array(A), np.array(B), np.array(C)
    u = B-A
    v = C-A
    w = wedge(u, v)
    nu = multscalar(u, u)
    nv = multscalar(v, v)
    s = multscalar(u, v)
    x = A+nu*(nv-s)/(2*w**2)*u+nv*(nu-s)/(2*w**2)*v
    return x

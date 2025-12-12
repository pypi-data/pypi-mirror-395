#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for discretization on `base_struct.Mesh` objects."""
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from warnings import warn
from abc import ABC
from collections.abc import Callable
import numpy as np
if TYPE_CHECKING:
    from pynitevolumes.mesh._array_types import ValueArray, PointArray
    from typing import Any
    from collections.abc import Iterable
    from .base_struct import Mesh


def _format(description: str) -> str:
    return '\t' + '\t'.join(description.strip().splitlines(True))+'\n'


type EvaluationMethod = Callable[[Mesh, Any, Iterable[str]],
                                 dict[str, ValueArray]]


class Discretizable(ABC):
    """Type of objects that can be discretized on a `Mesh` object.

    This class serves as a type description of all the types that can be
    discretized on a `Mesh` instance `M`. Use `add_type` to add a new
    type.

    The following is a list of all the types currently implemented.

    """

    _ev_map: dict[type, EvaluationMethod]

    @classmethod
    def add_type(cls, subclass: type, description: str,
                 ev_method: EvaluationMethod) -> None:
        """Add a new type to the type of `Discretizable` objects.

        `Discretizable` objects are objects that can somehow be
        understood as giving a value to category of points belonging to
        a `base_struct.Mesh`.

        Parameters
        ----------
        subclass : type
            Type of object that can be discretized.
        description : str
            Description of how the object is meant to be interpreted.
        ev_method : EvaluationMethod
            How to give a value to any type of points. The expected
            signature is

            .. code-block:: python

               ev_method(M: base_struct.Mesh,
                         f: subclass,
                         pt: list[str],
                         *args, **kwargs)->dict[str, ValueArray]

            and the expected behavior is that the return dictionary keys
            are the elements of `pt` and the values associated are
            arrays of length `len(getattr(M, pt[key]))` corresponding to
            the 'values' taken by `f` on each point of the type `pt[key]`.

        Returns
        -------
        None.

        """
        cls.register(subclass)
        assert isinstance(cls.__doc__, str)
        cls.__doc__ += f"{subclass.__name__}\n"
        cls.__doc__ += _format(description)
        cls.__doc__ += "\n\tSketch idea of evaluation on M.pt "
        cls.__doc__ += "of length np:\n\n"
        cls.__doc__ += _format(str(ev_method.__doc__)) + "\n"
        if not hasattr(cls, '_ev_map'):
            cls._ev_map = {subclass: ev_method}
        else:
            cls._ev_map[subclass] = ev_method


_CallableDescription = """
represent regular mathematical functions of two variables with
values in finite dimensional spaces. A callable `f(x, *args, *kwargs)`
is actually discretizable only:

* if `x` can be a `numpy.ndarray` of shape `(n, 2)` where `n` is an
  integer and
* if when `y=f(x, *args, **kwargs)`, `y` is a `numpy.ndarray` of shape
  `(n,)`(in which case we say that `f` is a scalar(-valued) function) or
  `(n, m)` where `m>=2` is an integer (in which case we say that `f`
  is a `m` D vector(-valued) function) and
* if `f` is vectorized in the sense that for all  `0<=k<n`  we  have
  `f(x[k], *args, **kwargs) == y[k]`.
"""


def _evaluate_fun(M: Mesh,
                  f: Callable[[PointArray], ValueArray],
                  point_types: Iterable[str],
                  *args: Any, **kwargs: Any
                  ) -> dict[str, ValueArray]:
    """`f(getattr(M, pt), *args, **kwargs)`."""
    f_part: dict[str, ValueArray] = {}
    for pt in point_types:
        f_part[pt] = f(getattr(M, pt), *args, **kwargs)
    return f_part


Discretizable.add_type(Callable,  # type: ignore
                       _CallableDescription, _evaluate_fun)

_constantDescription = """
represent constant mathematical functions.
"""


def _evaluate_scalar(M: Mesh,
                     f: int | float,
                     point_types: Iterable[str],
                     *args: Any, **kwargs: Any
                     ) -> dict[str, ValueArray]:
    """`f*numpy.ones(np)`."""
    f_part: dict[str, ValueArray] = {}
    for pt in point_types:
        f_part[pt] = float(f)*np.ones(len(getattr(M, pt)),
                                      dtype=float)
    return f_part


Discretizable.add_type(int, _constantDescription, _evaluate_scalar)
Discretizable.add_type(float, _constantDescription, _evaluate_scalar)


_arrayDescription = """
represent already discretized functions.
Often these are the objects that would come out of the resolution
of a numerical scheme. The values inside the array must be
organized to correspond to certain point categories in the mesh
but exactly what is this correspondence depends on the scheme
used.
"""


def _evaluate_arr(M: Mesh,
                  f: ValueArray,
                  point_types: Iterable[str], verbose: bool = False,
                  *args: Any, **kwargs: Any
                  ) -> dict[str, ValueArray]:
    """`f[i:i+np]` where i depends on f and the index of pt in M.pointvars."""
    f = np.array(f)
    f_part: dict[str, ValueArray] = {}
    data_length = len(f)
    full_array = data_length >= M.npoints
    needed_data_length = sum((v for k, v in M.npoints_by_type.items()
                              if k in point_types))
    tight_array = not full_array and (len(f) >= needed_data_length)
    if verbose and data_length > M.npoints:
        warn('f is larger than necessary. Will use only the '
             + f'{M.npoints} first lines')
    if verbose and tight_array and (data_length > needed_data_length):
        warn('f is larger than necessary. Will use only the '
             + f'{needed_data_length} first lines')
    i = 0
    for pt in M.pointvars:
        pt_len = M.npoints_by_type[pt]
        if pt in point_types:
            f_part[pt] = f[..., i:i+pt_len]
            i += pt_len
        if full_array and pt not in point_types:
            i += pt_len
    return f_part
    msg = f'len(f) must be at least {needed_data_length} but is {data_length}'
    raise ValueError(msg)


Discretizable.add_type(np.ndarray, _arrayDescription, _evaluate_arr)

_dictDescription = """
represent objects obtained from the
`Mesh.evaluate` or `Mesh.discretize` functions. Contrary to the
pure `numpy.ndarray` form the values inside the array have been
splitted to their corresponding point category which serve as a
key to the category."""


def _evaluate_dict(M: Mesh,
                   f: dict[str, ValueArray],
                   point_types: Iterable[str],
                   *args: Any, **kwargs: Any
                   ) -> dict[str, ValueArray]:
    """`f[pt]`."""
    if not set(point_types).issubset(f.keys()):
        raise ValueError('Dictionary f does not contain the '
                         + 'information required for evaluation')
    return f


Discretizable.add_type(dict, _dictDescription, _evaluate_dict)


class DiscreteFunction(Protocol):
    """Callable objects that can be evaluated on array of points."""

    def __call__(self, x: PointArray, **params: Any) -> ValueArray:
        """Evaluate the object."""
        ...

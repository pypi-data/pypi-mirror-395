#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boundary condition data types."""
from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
import numpy as np
from pynitevolumes.mesh._array_types import IndexArray, ValueArray
if TYPE_CHECKING:
    from typing import Self
    from collections.abc import Iterable


@dataclass(slots=True)
class BoundaryCondition:
    """Base class for boundary conditions."""

    w: IndexArray
    """Edges where to apply the condition."""


@dataclass(slots=True)
class DirichletBC(BoundaryCondition):
    """Dirichlet boundary condition."""

    data: ValueArray
    """Value of the solution at the corresponding edges."""


@dataclass(slots=True)
class NeumannBC(BoundaryCondition):
    """Neumann boundary condition."""

    data: ValueArray
    """Value of the normal derivative at the corresponding edges."""


@dataclass(slots=True)
class RobinBC(BoundaryCondition):
    """Robin boundary condition."""

    data: ValueArray
    r"""Value of :math:`au+b\partial_n u` on the corresponding edges."""
    a: ValueArray
    """Value of the coefficient of order 0."""
    b: ValueArray
    """Value of the coefficient of order 1."""


@dataclass(slots=True)
class FluxBC(BoundaryCondition):
    """Flux boundary condition."""

    data: ValueArray
    """Value of the total flux on the corresponding edges."""


@dataclass(slots=True)
class BCStructure:
    """Description of the boundary conditions in a TPFA scheme."""

    uncond_others: list[BoundaryCondition] = field(default_factory=list)
    """Non flux, unconditionally applied boundary conditions."""
    uncond_fluxes: list[FluxBC] = field(default_factory=list)
    """Flux boundary conditions, applied unconditionally."""
    inflow_others: list[BoundaryCondition] = field(default_factory=list)
    """Non flux boundary conditions, applied only on inflow edges."""
    inflow_fluxes: list[FluxBC] = field(default_factory=list)
    """Flux boundary conditions, applied ony on inflow edges."""

    @classmethod
    def from_iter(cls,
                  unconditional: Iterable[BoundaryCondition] | None = None,
                  inflow: Iterable[BoundaryCondition] | None = None
                  ) -> Self:
        """Split boundary conditions between fluxes/others."""
        uncond_others: list[BoundaryCondition] = []
        uncond_fluxes: list[FluxBC] = []
        inflow_others: list[BoundaryCondition] = []
        inflow_fluxes: list[FluxBC] = []
        if unconditional is not None:
            for bc in unconditional:
                if isinstance(bc, FluxBC):
                    uncond_fluxes.append(bc)
                else:
                    uncond_others.append(bc)
        if inflow is not None:
            for bc in inflow:
                if isinstance(bc, FluxBC):
                    inflow_fluxes.append(bc)
                else:
                    inflow_others.append(bc)
        return cls(uncond_others, uncond_fluxes, inflow_others, inflow_fluxes)


def split_inflow[T: BoundaryCondition](bc: T, flux_b: ValueArray
                                       ) -> tuple[IndexArray, T]:
    """Split relevant boundary condition in out/inflow part."""
    we = bc.w
    wo = np.where(flux_b[we] >= 0)
    wi = np.where(flux_b[we] < 0)
    init = {s: getattr(bc, s)[wi] for s in bc.__slots__ if s != 'w'}
    init['w'] = wi
    return (wo, type(bc).__call__(**init))  # type: ignore
    # Cannot make mypy recognize that type(bc).__call__ produces a type(bc)
    # object.

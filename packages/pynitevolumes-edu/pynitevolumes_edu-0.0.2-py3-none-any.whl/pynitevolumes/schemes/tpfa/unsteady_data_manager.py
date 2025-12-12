#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read XML files as data input for unsteady simulations."""
from __future__ import annotations
from ast import literal_eval
from typing import TYPE_CHECKING
from dataclasses import dataclass, InitVar
from defusedxml.ElementTree import parse as parse_xml
import numpy as np
from pynitevolumes.tools.expr import Numeric, gradient, diff
from pynitevolumes.tools.expr import divergence as div
from .data_manager import (_ExprCoeffs, Coeffs, Reference, Problem,
                           _filter_none, _const_to_fun, _expr_from, _fun_from,
                           _to_scal_fun, _to_vect_fun, _construct_BCbuilder,
                           BC_DISC, BC_REF,
                           _load_space,
                           MissingError)
from .data_manager import _load_bndcnd as _load_steady_bndcnd
from .data_manager import _load_problem_coeffs as _load_steady_problem_coeffs
if TYPE_CHECKING:
    from typing import Any
    from os import PathLike
    from xml.etree.ElementTree import Element
    from ...mesh._array_types import PointArray, ValueArray
    from ...mesh.disc import DiscreteFunction
    from ...tools.expr import Expr
    from .data_manager import SpaceDiscretization, BCRecipe


@dataclass
class _UnsteadyExprCoeffs(_ExprCoeffs):
    d_t_init: InitVar[Expr | None] = None

    def __post_init__(self, d_t_init: Expr | None) -> None:
        d_t_e: Expr
        if d_t_init is None:
            d_t_e = Numeric(1.0)
        else:
            d_t_e = d_t_init
        self.d_t_e = d_t_e


@dataclass
class UnsteadyCoeffs(Coeffs):
    """Coefficients describing an unsteady operator."""

    d_t: DiscreteFunction = _const_to_fun(1.0)
    """Coefficient inside the time derivative."""


@dataclass
class UnsteadyProblem(Problem):
    """Description of an unsteady problem."""

    coeffs: UnsteadyCoeffs
    """Coefficients of the unsteady differential operator."""
    u0: DiscreteFunction
    """Initial solution value."""
    rebuild: set[str]
    """Instruction of what to rebuild at each time-step.

    The keys are "mat", for rebuilding the matrix, "f" for rebuilding
    from the right-hand side element, "rhs" for rebuilding the
    right-hand side contribution of the boundary conditions
    """


@dataclass
class TimeDiscretization:
    """Description of the time discretizations to be used."""

    t0: float
    """Initial value."""
    tf: float
    """Final value (possibly not included)."""
    first_step: list[float]
    """Initial time steps to use. One item is one simulation."""
    max_step: list[float]
    """Smallest time steps to use in case of adaptative scheme.
    One item is one simulation, with the corresponding item in
    `first_step`."""
    metadata: dict[str, Any]
    """Other data about the time discretization."""


@dataclass
class UnsteadySimulation:
    """Description of the parameters used in a steady simulation."""

    space: SpaceDiscretization
    """Space simulation parameters."""
    time: TimeDiscretization
    """Time simulation parameters."""


def _load_time(time: Element) -> TimeDiscretization:
    """Load the time element."""
    t0 = float(time.get('t0', '0.0'))
    tf = float(_filter_none(time, 'tf'))
    dt = time.find('dt')
    if dt is None:
        raise MissingError("Time must have a subelement with tag 'dt'")
    else:
        dt_type = dt.get('type', 'single')
        if dt_type == 'single':
            value = _filter_none(dt, 'value')
            first_step = [float(value)]
        elif dt_type == 'linear':
            coarsest = _filter_none(dt, 'coarsest')
            finest = _filter_none(dt, 'finest')
            value = _filter_none(dt, 'value')
            step = _filter_none(dt, 'step')
            first_step = [float(value)-i*float(step)
                          for i in range(int(coarsest), int(finest)+1)]
        elif dt_type == 'exponential':
            coarsest = _filter_none(dt, 'coarsest')
            finest = _filter_none(dt, 'finest')
            value = _filter_none(dt, 'value')
            step = _filter_none(dt, 'step')
            first_step = [float(value)*float(step)**(-i)
                          for i in range(int(coarsest), int(finest)+1)]
        elif dt_type == 'list':
            dt_list = _filter_none(dt, 'value')
            first_step = literal_eval(dt_list)
        max_step = first_step
    time_res = {k: literal_eval(v) for k, v in time.items()
                if k not in {'t0', 'tf'}}
    return TimeDiscretization(t0, tf, first_step, max_step, time_res)


def _load_simulation(sim: Element) -> UnsteadySimulation:
    """Load space and time parameters."""
    if sim is None:
        raise MissingError("No 'simulation' element found")
    space = sim.find('space')
    time = sim.find('time')
    if space is None:
        raise MissingError("No 'space' element found")
    space_d = _load_space(space)
    if time is None:
        raise MissingError("No 'time' element found")
    else:
        time_d = _load_time(time)
    return UnsteadySimulation(space_d, time_d)


def _load_problem_coeffs(operator: Element) -> tuple[_UnsteadyExprCoeffs,
                                                     bool]:
    """Load coefficients of the differential operator."""
    space_coeffs = _load_steady_problem_coeffs(operator)
    schemes = space_coeffs.schemes

    d_t = operator.find('time-derivative')

    if d_t is not None:
        schemes['d_t'] = d_t.get('scheme', 'ExplicitEuler')
        d_t_e = _expr_from(d_t)
    else:
        schemes['d_t'] = 'ExplicitEuler'
        d_t_e = Numeric(1.0)

    non_autonomous = literal_eval(operator.get('non-autonomous', 'False'))
    return (_UnsteadyExprCoeffs(space_coeffs.A_e,
                                space_coeffs.v_e,
                                space_coeffs.q_e,
                                d_t_e, schemes=schemes), non_autonomous)


def _load_rhs(rhs: Element | None) -> tuple[DiscreteFunction | None,
                                            bool]:
    rhs_fun = _fun_from(rhs)
    if rhs is None:
        return rhs_fun, False  # 0 constant function is not time dependent
    else:
        return rhs_fun, bool(literal_eval(rhs.get('time-dependent', 'True')))


def _load_bndcnd(bnd: Element) -> tuple[dict[str, list[BCRecipe]],
                                        dict[str, list[BCRecipe]],
                                        bool]:
    """Load the boundary conditions."""
    bndcnd_no_ref, bndcnd_ref = _load_steady_bndcnd(bnd)
    bndloc_time_dep = False
    bndval_time_dep = False
    for condition in bnd:
        where = condition.find('where')
        data = condition.find('data')
        if where is None:
            where_mthd = 'whole'
            condloc_time_dep = False
        else:
            where_mthd = where.get('type', 'whole')
            condloc_time_dep = literal_eval(where.get('time-dependent',
                                                      'True'))
        if where_mthd == 'whole':
            bndloc_time_dep = False
        elif where_mthd == 'expr':
            bndloc_time_dep = bndloc_time_dep or condloc_time_dep
        else:
            raise ValueError("Unknown 'type' for 'where' element")

        if data is None:
            data_method = 'const'
            condval_time_dep = False
        else:
            data_method = data.get('type', 'const')
            condval_time_dep = literal_eval(data.get('time-dependent', 'True'))
        if data_method == 'const':
            condval_time_dep = False
        elif data_method == 'expr':
            bndval_time_dep = bndval_time_dep or condval_time_dep
        elif data_method == 'reference':
            pass
        else:
            raise ValueError("Unknown 'type' for element 'data'")
    return bndcnd_no_ref, bndcnd_ref, bndloc_time_dep or bndval_time_dep


def _load_reference(reference: Element) -> tuple[Expr, bool]:
    """Load the reference element."""
    if reference.get('type', 'expr') == 'expr':
        u_e = _expr_from(reference)
        return u_e, literal_eval(reference.get('time-dependent', 'True'))
    else:
        raise NotImplementedError("'reference' element must be "
                                  + "of type 'expr'")


def _build_init_from_ref(ref: Reference, t0: float) -> DiscreteFunction:
    """Build init function by taking reference at t=t0."""
    def u0(x: PointArray, **kwargs: Any) -> ValueArray:
        x = np.array(x)
        if 'T' in kwargs:
            del kwargs['T']
        return ref.u(x, T=t0, **kwargs)
    return u0


def _build_source_from_ref(
        coeffs_e: _UnsteadyExprCoeffs,
        u_e: Expr
        ) -> Expr:
    """Build rhs function by applying the operator to the reference."""
    operator: Expr = diff(coeffs_e.d_t_e*u_e, 'T')
    grad_u_e = np.array(gradient(u_e, 'X', 'Y'), dtype=np.object_)
    if (A := coeffs_e.A_e) is not None:
        operator = operator - div(A*grad_u_e, ('X', 'Y'))  # type:  ignore
        # Ignore typing in the previous line because it is too complicated to
        # make numpy recognize Expr as a numeric type on which arithmetic is
        # valid.
    if (v_e := coeffs_e.v_e) is not None:
        v = np.array(v_e, dtype=np.object_)
        operator = operator + div(u_e*v, ('X', 'Y'))  # type: ignore
        # Ignore typing in the previous line because it is too complicated to
        # make numpy recognize Expr as a numeric type on which arithmetic is
        # valid.
    if (q := coeffs_e.q_e) is not None:
        operator = operator + q*u_e
    return operator.simplify()


def load_data(filename: str | PathLike[Any]
              ) -> tuple[dict[str, Any],
                         UnsteadySimulation,
                         UnsteadyProblem,
                         Reference | None]:
    """Load data from an XML file for `run_pvexamples`.

    Parameters
    ----------
    filename : str or file object
        XML file describing the simulation of an unsteady PDE.

    Returns
    -------
    description: dict[str, Any]
        Metadata of the dsimulation.
    simulation: UnsteadySimulation
        Parameters for the numerical schemes to be used.
    Pb: UnsteadyProblem
        Parameters to construct the numerical parts of the scheme.
    ref: Reference or None
        The reference solution and its gradient to compute errors.
        If not available, then is left to None.
    """
    comp = parse_xml(filename).getroot()
    if comp is None:
        raise ValueError("Could not parse " + str(filename))
    description = {k: literal_eval(v) for k, v in comp.items()
                   if k not in {'name', 'text'}}
    description['name'] = comp.get('name', None)
    description['text'] = comp.text

    def _is_present(e: Element, element_name: str) -> Element:
        element = e.find(element_name)
        if element is None:
            raise MissingError("Missing required element " +
                               f"'{element_name}' " +
                               f"in {e.tag}.")
        else:
            return element

    sim = _is_present(comp, 'simulation')
    simulation = _load_simulation(sim)
    problem = _is_present(comp, 'problem')
    operator = _is_present(problem, 'operator')
    # Building the coefficient functions
    coeffs_e, non_auto = _load_problem_coeffs(operator)
    if (A_e := coeffs_e.A_e) is not None:
        A_fun = _to_scal_fun(A_e)
    else:
        A_fun = None
    if (v_e := coeffs_e.v_e) is not None:
        v_fun = _to_vect_fun(v_e)
    else:
        v_fun = None
    if (q_e := coeffs_e.q_e) is not None:
        q_fun = _to_scal_fun(q_e)
    else:
        q_fun = None
    d_t_fun = _to_scal_fun(coeffs_e.d_t_e)
    coeffs = UnsteadyCoeffs(A_fun, v_fun, q_fun, d_t_fun,
                            schemes=coeffs_e.schemes)
    init = problem.find('init')
    u0_fun_temp = _fun_from(init)
    init_needs_ref = u0_fun_temp is None
    # Building the rhs function if it does not need ref
    rhs_fun_temp, rhs_time_indep = _load_rhs(problem.find('right-hand-side'))
    rhs_needs_ref = rhs_fun_temp is None
    rhs_time_dep = not rhs_time_indep
    # Building boundary condition
    bnd = _is_present(problem, 'boundary')
    bndcnd, bnd_needs_ref, bnd_time_dep = _load_bndcnd(bnd)
    # # Building BC which do not need ref
    bndcnd_disc_u, bndcnd_disc_i = _construct_BCbuilder(bndcnd, BC_DISC,
                                                        coeffs)
    # Building everything that needs ref if needed
    ref = None
    if rhs_needs_ref or bnd_needs_ref or init_needs_ref:
        # building the ref
        reference = _is_present(comp, 'reference')
        u_e, ref_time_dep = _load_reference(reference)
        ref = Reference(_to_scal_fun(u_e),
                        _to_vect_fun(gradient(u_e, 'X', 'Y')))
        u0_ref = _build_init_from_ref(ref, simulation.time.t0)
    if rhs_fun_temp is None:
        # building the rhs if it needs ref
        rhs_fun = _to_scal_fun(_build_source_from_ref(coeffs_e, u_e))
        rhs_time_dep = ref_time_dep or non_auto
    else:
        rhs_fun = rhs_fun_temp
    if bnd_needs_ref:
        # building the BC if it needs ref
        bndcnd_ref_u, bndcnd_ref_i = _construct_BCbuilder(bnd_needs_ref,
                                                          BC_REF,
                                                          coeffs,
                                                          ref)
        bnd_time_dep = bnd_time_dep or ref_time_dep
    else:
        bndcnd_ref_u, bndcnd_ref_i = [], []
    if u0_fun_temp is None:
        u0_fun = u0_ref
    else:
        u0_fun = u0_fun_temp
    bnd_final = (bndcnd_disc_u + bndcnd_ref_u, bndcnd_disc_i+bndcnd_ref_i)
    rebuild: set[str] = set()
    if non_auto or ('robin' in bndcnd and bnd_time_dep):
        rebuild.add('mat')
    if bnd_time_dep:
        rebuild.add('rhs')
    if rhs_time_dep:
        rebuild.add('f')
    Pb = UnsteadyProblem(coeffs, bnd_final, rhs_fun, u0_fun, rebuild)
    return description, simulation, Pb, ref

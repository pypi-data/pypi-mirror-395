#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read XML files as data input for steady simulations."""
from __future__ import annotations
from ast import literal_eval
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol
from functools import partial
from defusedxml.ElementTree import parse as parse_xml
import numpy as np
from ...tools.expr import (Expr, Empty, Numeric, parse, ev_array, array_expr,
                           subs, ZERO, gradient)
from pynitevolumes.tools.expr import divergence as div
from pynitevolumes.mesh.meshtools import locate as locate_boundary
from pynitevolumes.tools.geometry import multscalar as ms
from .bc_data import BoundaryCondition, DirichletBC, NeumannBC, RobinBC, FluxBC
if TYPE_CHECKING:
    from typing import Callable, Any
    from os import PathLike
    from xml.etree.ElementTree import Element
    from ...mesh._array_types import PointArray, IndexArray, ValueArray
    from ...mesh.base_struct import Mesh
    from ...mesh.disc import Discretizable, DiscreteFunction
    from .tpfa_struct import TPFAStruct


# %% Function/Expr constructors
#    ==========================


def _to_scal_fun(expr: Expr) -> DiscreteFunction:
    """Return a scalar function based on expression."""
    def expr_fun(x: PointArray, **params: Any) -> ValueArray:
        x = np.array(x)
        return eval(ev_array(subs(expr, **params)))  # type: ignore
    # The eval does return a ValueArray
    return expr_fun


def _to_vect_fun(array_of_expr: list[Expr]
                 ) -> DiscreteFunction:
    """Return a vector function based on array of expression."""
    def expr_fun(x: PointArray, **params: Any) -> ValueArray:
        x = np.array(x)
        y = eval(ev_array(subs(array_expr(array_of_expr), **params)))
        return y.T  # type: ignore
        # The eval does return a ValueArray
    return expr_fun


def _const_to_fun(value: int | float) -> DiscreteFunction:
    """Return a function based on val."""
    if value == 0.0:
        def const_fun(x: PointArray, **params: Any) -> ValueArray:
            x = np.array(x)
            return np.zeros(x.shape[:-1], dtype='float')
        return const_fun
    else:
        def const_fun(x: PointArray, **params: Any) -> ValueArray:
            x = np.array(x)
            return value*np.ones(x.shape[:-1], dtype='float')
        return const_fun


def _expr_from(element: Element | None) -> Expr:
    """Return an expression based on element type."""
    if element is None:
        return ZERO
    el_type = element.get('type')
    if el_type == 'expr':
        if (el_text := element.text) is None:
            raise MissingError('expr value missing '
                               + f'from text in {element.tag}')
        else:
            return parse(el_text)
    elif el_type == 'const':
        if (val := element.text) is None:
            raise MissingError('const value missing '
                               + f'from text in {element.tag}')
        else:
            return Numeric(float(val))
    elif el_type == 'reference':
        return Empty()
    else:
        raise UnknownTypeError(element)


def _fun_from(element: Element | None) -> DiscreteFunction | None:
    """Return a function based on element type.

    Returns `None` only if type is 'reference' to do specific things.
    """
    if element is None:
        return _const_to_fun(0.0)
    el_type = element.get('type')
    if el_type == 'expr':
        if (el_text := element.text) is None:
            raise MissingError('expr value missing '
                               + f'from text in {element.tag}')
        else:
            return _to_scal_fun(parse(el_text))
    elif el_type == 'const':
        val = element.text
        if val is None:
            raise MissingError('const value missing '
                               + f'from text in {element.tag}')
        else:
            return _const_to_fun(float(val))
    elif el_type == 'reference':
        return None
    else:
        raise UnknownTypeError(element)

# %% Data structures
#    ===============


@dataclass
class _ExprCoeffs:
    A_e: Expr | None = None
    v_e: list[Expr] | None = None
    q_e: Expr | None = None
    schemes: dict[str, str] = field(default_factory=dict, kw_only=True)


@dataclass
class Coeffs:
    """Coefficients describing a steady operator.

    If the coefficient is None, it means that the corresponding term is
    not present in the operator.
    """

    A: DiscreteFunction | None = None
    """Diffusion coefficient."""
    v: DiscreteFunction | None = None
    """Convection vector field."""
    q: DiscreteFunction | None = None
    """Volumic coefficient."""
    schemes: dict[str, str] = field(default_factory=dict, kw_only=True)
    """Which scheme to use for each part of the operator."""


@dataclass
class Problem:
    """Description of a steady problem."""

    coeffs: Coeffs
    """Coefficients of the steady differential operator."""
    bndcnd: tuple[list[BCConstructor[BoundaryCondition]],
                  list[BCConstructor[BoundaryCondition]]]
    """Boundary conditions constructors.

    The first element are the boundary conditions which apply
    unconditionally while the second element are the boundary condition
    that apply only if the flow is entering in the domain. Beware that
    the flow is only the convective flow."""
    rhs: DiscreteFunction
    """The right-hand side of the PDE."""


@dataclass
class Reference:
    """Description of a reference solution to a PDE."""

    u: DiscreteFunction
    """Reference solution to the PDE."""
    grad_u: DiscreteFunction
    """Spatial gradient of the reference solution to the PDE."""


@dataclass
class SpaceDiscretization:
    """Description of the mesh(es) to be used."""

    mesh_list: list[str]
    """List of mesh file paths."""
    metadata: dict[str, Any]
    """Metadata associated with the space discretization."""


# %% Exceptions
#    ==========

class UnknownTypeError(ValueError):
    """Error to raise when an element as an unknown 'type'."""

    def __init__(self, element: Element):
        msg = (f"Unknown 'type={element.get('type')}' for element "
               + f"{element.tag}")
        super().__init__(msg)


class MissingError(Exception):
    """Error when a required piece of data is missing."""

    pass


def _filter_none(e: Element, att: str) -> str:
    s = e.get(att)
    if s is None:
        msg = f"Attrib {att} needed for element {e.tag}"
        raise MissingError(msg)
    else:
        return s

# %% Specific element loaders
#    ========================


def _load_space(space: Element) -> SpaceDiscretization:
    """Load the space element."""
    def _add_pvm_ext(s: str) -> str:
        if not s.endswith('.pvm'):
            return s + '.pvm'
        else:
            return s
    mesh_list = []
    mesh_fam = space.get('mesh_family', None)
    if mesh_fam is not None:
        coarsest = _filter_none(space, 'coarsest')
        start_range = int(coarsest)
        finest = _filter_none(space, 'finest')
        stop_range = int(finest) + 1
        mesh_list.extend([f'{mesh_fam}/{mesh_fam}_{i}.pvm'
                          for i in range(start_range, stop_range)])
    mesh_name = space.get('mesh_name', None)
    if mesh_name is not None:
        mesh_list.append(_add_pvm_ext(mesh_name))
    mesh_explicit = space.get('mesh_list', None)
    if mesh_explicit is not None:
        mesh_list.extend([_add_pvm_ext(s)
                          for s in literal_eval(mesh_explicit)])
    space_res = {k: literal_eval(v) for k, v in space.items()
                 if k not in {'mesh_family', 'mesh_name', 'mesh_list',
                              'finest', 'coarsest'}}  # get unknown properties
    return SpaceDiscretization(mesh_list, space_res)


def _load_simulation(sim: Element) -> SpaceDiscretization:
    """Load space and time parameters."""
    if sim is None:
        raise MissingError("No 'simulation' element found")
    space = sim.find('space')
    if space is None:
        raise MissingError("No 'space' element found")
    return _load_space(space)


def _load_problem_coeffs(operator: Element) -> _ExprCoeffs:
    """Load coefficients of the differential operator."""
    schemes: dict[str, str] = {}
    if operator is None:
        raise MissingError("Missing 'operator' element from 'problem'")
    diff = operator.find('diffusion')
    conv = operator.find('convection')
    volumic = operator.find('volumic')

    if diff is not None:
        schemes['diffusion'] = 'default'
        A_e = _expr_from(diff)
    else:
        A_e = None

    if volumic is not None:
        schemes['volumic'] = 'default'
        q_e = _expr_from(volumic)
    else:
        q_e = None

    if conv is not None:
        schemes['convection'] = conv.get('scheme', 'upwind')
        v_e = [_expr_from(conv.find('vx')), _expr_from(conv.find('vy'))]
    else:
        v_e = None

    return _ExprCoeffs(A_e, v_e, q_e, schemes=schemes)


def _load_reference(reference: Element) -> Expr:
    """Load the reference element."""
    if reference.get('type', 'expr') == 'expr':
        u_e = _expr_from(reference)
        return u_e
    else:
        raise NotImplementedError("'reference' element must be "
                                  + "of type 'expr'")


# %% Data building from reference outside of boundary conditions
#    ===========================================================


def _build_source_from_ref(
        coeffs_e: _ExprCoeffs,
        u_e: Expr
        ) -> Expr:
    """Build rhs function by applying the operator to the reference."""
    operator: Expr = Empty()
    grad_u_e = np.array(gradient(u_e, 'X', 'Y'), dtype=np.object_)
    if (A := coeffs_e.A_e) is not None:
        operator = operator - div(A*grad_u_e, ('X', 'Y'))  # type: ignore
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

# %% Boundary condition building
#    ===========================


class Locator(Protocol):
    """Function locating specific edges inside a mesh."""

    def __call__(self, E: Mesh, **kwargs: Any) -> IndexArray:
        """Call signature."""
        ...


def locate_whole(E: Mesh, **params: Any) -> IndexArray:
    """Whole boundary index range."""
    return np.arange(E.nbnd)


def locate_fun(loc_fun: DiscreteFunction) -> Locator:
    """Array of boundary edges indices where `loc_fun=0`."""

    def locate(E: Mesh, **params: Any) -> IndexArray:
        return locate_boundary(E,
                               lambda x: loc_fun(x, **params))  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # DiscreteFunction as a subtype of Discretizable when
        # it is.
    return locate


type BCRecipe = tuple[Locator, list[Discretizable]]
"""Boundary recipe.

All the information needed to build the data for the boundary
condition."""

type BCConstructor[T: BoundaryCondition] = Callable[[TPFAStruct], T]
"""Construct the boundary condition relevant data on the given mesh."""


class _BCCMaker(Protocol):

    def __call__(self, locate: Locator, *f: Discretizable, **kwargs: Any
                 ) -> BCConstructor[BoundaryCondition]:
        ...


def build_BCdata_from_disc[T: BoundaryCondition](bctype: type[T],
                                                 locate: Locator,
                                                 *f: Discretizable,
                                                 **kwargs: Any
                                                 ) -> BCConstructor[T]:
    """Make data constructor from generic Discretizable."""

    def builder(E: TPFAStruct, **params: Any) -> T:
        we = locate(E, **params)
        res = []
        for h in f:
            res.append(E.evaluate(h, 'xs_b', **params)[we])
        return bctype(we, *res)
    return builder


def build_flux_BCdata_from_disc(locate: Locator,
                                *g: Discretizable,
                                **kwargs: Any
                                ) -> BCConstructor[FluxBC]:
    """Make flux data constructor from generic Discretizable."""

    def builder(E: TPFAStruct, **params: Any) -> FluxBC:
        we = locate(E, **params)
        g_d = E.evaluate(g[0], 'xs_b', **params)[we]
        return FluxBC(we, g_d)
    return builder


def build_dir_BCdata_from_ref(locate: Locator, *args: Discretizable,
                              **kwargs: Any) -> BCConstructor[DirichletBC]:
    """Make Dirichlet data constructor from reference."""
    ref = kwargs.pop('ref')
    return build_BCdata_from_disc(DirichletBC, locate, ref.u)


def build_neu_BCdata_from_ref(locate: Locator, *args: Discretizable,
                              **kwargs: Any) -> BCConstructor[NeumannBC]:
    """Make Neumann data constructor from reference."""
    ref = kwargs.pop('ref')

    def builder(E: TPFAStruct, **params: Any) -> NeumannBC:
        we = locate(E, **params)
        gradu_d = E.evaluate(ref.grad_u, 'xs_b', **params)
        return NeumannBC(we, ms(E.NKs_b[we], gradu_d[we])/E.len_b[we])
    return builder


def build_rob_BCdata_from_ref(locate: Locator, *args: Discretizable,
                              **kwargs: Any) -> BCConstructor[RobinBC]:
    """Make Robin data constructor from reference."""
    ref = kwargs.pop('ref')

    def builder(E: TPFAStruct, **params: Any) -> RobinBC:
        we = locate(E, **params)
        a_d = E.evaluate(args[0], 'xs_b', **params)[we]
        b_d = E.evaluate(args[1], 'xs_b', **params)[we]
        u_d = E.evaluate(ref.u, 'xs_b', **params)[we]
        gradu_d = E.evaluate(ref.grad_u, 'xs_b', **params)[we]
        dnu_d = ms(E.NKs_b[we], gradu_d)/E.len_b[we]
        g_d = a_d*u_d+b_d*dnu_d
        return RobinBC(we, g_d, a_d, b_d)
    return builder


def build_flux_BCdata_from_ref(locate: Locator, *args: Discretizable,
                               **kwargs: Any) -> BCConstructor[FluxBC]:
    """Make flux data constructor from reference."""
    coeffs: Coeffs = kwargs.pop('coeffs')
    ref = kwargs.pop('ref')

    def builder(E: TPFAStruct, **params: Any) -> FluxBC:
        we = locate(E, **params)
        if (v := coeffs.v) is not None:
            v_d = E.evaluate(v, 'xs_b', **params)[we]  # type: ignore
            a_d = -ms(v_d, E.NKs_b[we])
        else:
            a_d = np.zeros(len(we))
        if (A := coeffs.A) is not None:
            b_d = E.evaluate(A, 'xs_b', **params)[we]*E.len_b[we]  # type: ignore
        else:
            b_d = np.zeros(len(we))
        u_d = E.evaluate(ref.u, 'xs_b', **params)[we]
        gradu_d = E.evaluate(ref.grad_u, 'xs_b', **params)[we]
        dnu_d = ms(E.NKs_b[we], gradu_d)/E.len_b[we]
        g_d = a_d*u_d+b_d*dnu_d
        return FluxBC(we, g_d)
    return builder


BC_DISC: dict[str, _BCCMaker] = {
    'dirichlet': partial(build_BCdata_from_disc, DirichletBC),
    'neumann': partial(build_BCdata_from_disc, NeumannBC),
    'robin': partial(build_BCdata_from_disc, RobinBC),
    'flux': build_flux_BCdata_from_disc
    }

BC_REF: dict[str, _BCCMaker] = {
    'dirichlet': build_dir_BCdata_from_ref,
    'neumann': build_neu_BCdata_from_ref,
    'robin': build_rob_BCdata_from_ref,
    'flux': build_flux_BCdata_from_ref
    }


def _load_bndcnd(bnd: Element) -> tuple[dict[str, list[BCRecipe]],
                                        dict[str, list[BCRecipe]]]:
    """Load the boundary conditions."""
    bndcnd_no_ref: dict[str, list[BCRecipe]] = {}
    bndcnd_ref: dict[str, list[BCRecipe]] = {}
    for condition in bnd:
        cond_name = condition.tag
        where = condition.find('where')
        data = condition.find('data')
        if where is None:
            where_mthd = 'whole'
            inflow = False
        else:
            where_mthd = where.get('type', 'whole')
            inflow = literal_eval(where.get('inflow', 'False'))
            if where.text is None:
                where_txt = ''
            else:
                where_txt = where.text
        if inflow:
            cond_name += '_inflow'
        if where_mthd == 'whole':
            locator = locate_whole
        elif where_mthd == 'expr':
            locator = locate_fun(_to_scal_fun(parse(where_txt)))
        else:
            raise ValueError("Unknown 'type=' for 'where' element")

        to_build: list[Discretizable] = []
        if data is None:
            data_method = 'const'
            data_content = '0.0'
        else:
            data_method = data.get('type', 'const')
            if data.text is None:
                data_content = '0.0'
            else:
                data_content = data.text
        if data_method == 'const':
            to_build.append(float(data_content))  # type: ignore
            # Because of mypy Issue #2922 mypy does not recognize
            # float as a subtype of Discretizable when it is.
            dest = bndcnd_no_ref
        elif data_method == 'expr':
            to_build.append(_to_scal_fun(parse(data_content)))  # type: ignore
            # Because of mypy Issue #2922 mypy does not recognize
            # DiscreteFunction as a subtype of Discretizable
            # when it is.
            dest = bndcnd_no_ref
        elif data_method == 'reference':
            dest = bndcnd_ref
        else:
            raise ValueError("Unknown 'type' for element 'data'")
        params = condition.find('parameters')
        if params is not None:
            for param in params:
                to_build.append(_fun_from(param))  # type: ignore
                # Because of mypy Issue #2922 mypy does not recognize
                # DiscreteFunction as a subtype of
                # Discretizable when it is.
        if cond_name in dest:
            dest[cond_name].append((locator, to_build))
        else:
            dest[cond_name] = [(locator, to_build)]
    return bndcnd_no_ref, bndcnd_ref


def _construct_BCbuilder(bnd: dict[str, list[BCRecipe]],
                         bnd_mapping: dict[str, _BCCMaker],
                         coeffs: Coeffs,
                         ref: Reference | None = None
                         ) -> tuple[list[BCConstructor[BoundaryCondition]],
                                    list[BCConstructor[BoundaryCondition]]]:
    unconditional: list[BCConstructor[BoundaryCondition]] = []
    inflow: list[BCConstructor[BoundaryCondition]] = []
    for condition, seq_bnd in bnd.items():
        true_cond = condition.removesuffix('_inflow')
        is_inflow = condition.endswith('_inflow')
        if is_inflow:
            dest = inflow
        else:
            dest = unconditional
        for (loc, to_build) in seq_bnd:
            bnd_data = bnd_mapping[true_cond](loc, *to_build, coeffs=coeffs,
                                              ref=ref)
            dest.append(bnd_data)
    return unconditional, inflow

# %% Public loader
#    =============


def load_data(filename: str | PathLike[Any]
              ) -> tuple[dict[str, Any],
                         SpaceDiscretization,
                         Problem,
                         Reference | None]:
    """Load data from an XML file for `run_pvexamples`..

    Parameters
    ----------
    filename : str or file object
        XML file describing the simulation of a steady PDE.

    Returns
    -------
    description: dict[str, Any]
        Metadata of the dsimulation.
    simulation: SpaceDiscretization
        Parameters for the numerical schemes to be used.
    Pb: Problem
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
    space = _load_simulation(sim)
    problem = _is_present(comp, 'problem')
    operator = _is_present(problem, 'operator')
    # Building the coefficient functions
    coeffs_e = _load_problem_coeffs(operator)
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
    coeffs = Coeffs(A_fun, v_fun, q_fun, schemes=coeffs_e.schemes)

    # Building the rhs function if it does not need ref
    rhs_fun_temp = _fun_from(problem.find('right-hand-side'))
    rhs_needs_ref = rhs_fun_temp is None
    # Building boundary condition
    bnd = _is_present(problem, 'boundary')
    bndcnd, bnd_needs_ref = _load_bndcnd(bnd)
    # # Building BC which do not need ref
    bndcnd_disc_u, bndcnd_disc_i = _construct_BCbuilder(bndcnd, BC_DISC,
                                                        coeffs)
    # Building everything that needs ref if needed
    ref = None
    if rhs_needs_ref or bnd_needs_ref:
        # building the ref
        reference = _is_present(comp, 'reference')
        u_e = _load_reference(reference)
        ref = Reference(_to_scal_fun(u_e),
                        _to_vect_fun(gradient(u_e, 'X', 'Y')))
    if rhs_fun_temp is None:
        # building the rhs if it needs ref
        rhs_fun = _to_scal_fun(_build_source_from_ref(coeffs_e, u_e))
    else:
        rhs_fun = rhs_fun_temp
    if bnd_needs_ref:
        # building the BC if it needs ref
        bndcnd_ref_u, bndcnd_ref_i = _construct_BCbuilder(bnd_needs_ref,
                                                          BC_REF,
                                                          coeffs,
                                                          ref)
    else:
        bndcnd_ref_u, bndcnd_ref_i = [], []
    bnd_final = (bndcnd_disc_u + bndcnd_ref_u, bndcnd_disc_i+bndcnd_ref_i)
    Pb = Problem(coeffs, bnd_final, rhs_fun)
    return description, space, Pb, ref

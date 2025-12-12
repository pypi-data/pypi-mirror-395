#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Run examples of PDE solving using pynitevolumes.schemes.tpfa."""
from __future__ import annotations
from typing import TYPE_CHECKING
from argparse import ArgumentParser
from pathlib import Path
from importlib.resources import files, as_file
from importlib.resources.abc import Traversable
from functools import partial
from scipy.sparse import csr_array, eye_array
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pynitevolumes.mesh.base_struct import Mesh
import pynitevolumes.schemes.tpfa.data_manager as dm
import pynitevolumes.schemes.tpfa.unsteady_data_manager as udm
import pynitevolumes.schemes.tpfa.output_manager as om
from pynitevolumes.mesh.mesh_io import loadmesh
import pynitevolumes.schemes.tpfa as tpfa
from .bc_data import BCStructure, split_inflow
from pynitevolumes.mesh.md import PRIMAL
if TYPE_CHECKING:
    from os import PathLike
    from typing import Callable, Any
    from collections.abc import Iterable
    from ...mesh._array_types import IndexArray, ValueArray
    from ...mesh.disc import DiscreteFunction
    from .tpfa_struct import TPFAStruct
    from .bc_data import BoundaryCondition
    from .data_manager import BCConstructor, Problem, Coeffs, Reference
    from .unsteady_data_manager import UnsteadyCoeffs, UnsteadyProblem
    from .output_manager import GenericFigure, ResultFigure


# %% Steady tools
#    ============

def discretize_BC(M: TPFAStruct,
                  bndcnd: tuple[list[BCConstructor[BoundaryCondition]],
                                list[BCConstructor[BoundaryCondition]]],
                  **params: Any
                  ) -> BCStructure:
    """Construct the discretized BC data from recipes."""
    uncond_constr, inflow_constr = bndcnd
    unconditional = [constr(M, **params) for constr in uncond_constr]
    inflow = [constr(M, **params) for constr in inflow_constr]
    return BCStructure.from_iter(unconditional, inflow)


def assemble_steady_mat(M: TPFAStruct,
                        coeffs: Coeffs,
                        M_bnd: BCStructure) -> csr_array:
    r"""
    Assemble matrix of 2nd order linear steady PDEs.

    Parameters
    ----------
    M : pynitevolumes.schemes.tpfa.TPFAStruct
        The mesh on which the problem is solved.
    coeffs : data_manager.Coeffs
        The coefficients of the (spatial part) of the PDE being
        simulated.
    M_bnd : bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    A : scipy.sparse.csr_array
        The matrix of the system.

    See Also
    --------
    scipy.sparse.csr_array
    pynitevolumes.schemes.tpfa.diffusion
    pynitevolumes.schemes.tpfa.convection
    pynitevolumes.schemes.tpfa.volumic
    """
    Nunk = M.nvol

    # Matrix assembly
    row_mat = []
    col_mat = []
    dat_mat = []

    # Diffusion terms
    if coeffs.A is not None:
        row_mat_d, col_mat_d, dat_mat_d = tpfa.diffusion_matrix(
            M, coeffs.A, M_bnd)  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # DiscreteFunction as a subtype of Discretizable when
        # it is.
        row_mat.extend(row_mat_d)
        col_mat.extend(col_mat_d)
        dat_mat.extend(dat_mat_d)

    # Convection
    if coeffs.v is not None:
        if (c_scheme := coeffs.schemes['convection']) == 'default':
            c_scheme = 'upwind'

        row_mat_c, col_mat_c, dat_mat_c = tpfa.convection_matrix(
            M, coeffs.v, M_bnd, c_scheme)  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.
        row_mat.extend(row_mat_c)
        col_mat.extend(col_mat_c)
        dat_mat.extend(dat_mat_c)

    # Volumic terms
    if coeffs.q is not None:
        row_mat_v, col_mat_v, dat_mat_v = tpfa.volumic(
            M, coeffs.q)  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.
        row_mat.extend(row_mat_v)
        col_mat.extend(col_mat_v)
        dat_mat.extend(dat_mat_v)

    # Linear system construction
    row_mat = np.concatenate(row_mat)
    col_mat = np.concatenate(col_mat)
    dat_mat = np.concatenate(dat_mat)

    A = csr_array((dat_mat, (row_mat, col_mat)), shape=(Nunk, Nunk))
    return A


def _build_vector(row_rhs: list[IndexArray],
                  dat_rhs: list[ValueArray],
                  Nunk: int) -> ValueArray:
    """Build a vector from row/data lists of arrays."""
    b = np.zeros(Nunk, dtype='float')
    row = np.concatenate(row_rhs)
    dat = np.concatenate(dat_rhs)
    for r, d in zip(row, dat):
        b[r] += d
    return b


def assemble_steady_rhs(M: TPFAStruct,
                        coeffs: Coeffs,
                        M_bnd: BCStructure
                        ) -> ValueArray:
    r"""
    Assemble right-hand side of 2nd order linear steady PDEs.

    Parameters
    ----------
    M : pynitevolumes.schemes.tpfa.TPFAStruct
        The mesh on which the problem is solved.
    coeffs : data_manager.Coeffs
        The coefficients of the (spatial part) of the PDE being
        simulated.
    M_bnd : bc_data.BCStructure
        Description of the boundary conditions.

    Returns
    -------
    b : numpy.ndarray
        The right-hand side of the system.

    See Also
    --------
    pynitevolumes.schemes.tpfa.diffusion
    pynitevolumes.schemes.tpfa.convection
    pynitevolumes.schemes.tpfa.volumic
    """
    Nunk = M.nvol

    # Matrix assembly
    row_rhs = []
    dat_rhs = []

    # Diffusion terms
    if coeffs.A is not None:
        row_rhs_d, dat_rhs_d = tpfa.diffusion_rhs(
            M, coeffs.A, M_bnd)  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.
        row_rhs.extend(row_rhs_d)
        dat_rhs.extend(dat_rhs_d)

    # Convection
    if coeffs.v is not None:
        if (c_scheme := coeffs.schemes['convection']) == 'default':
            c_scheme = 'upwind'
        row_rhs_c, dat_rhs_c, c_flux_b = tpfa.convection_rhs(
            M, coeffs.v, M_bnd, c_scheme)  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.
        row_rhs.extend(row_rhs_c)
        dat_rhs.extend(dat_rhs_c)

    Kbnd = M.diam_b.c
    for flux_bc in M_bnd.uncond_fluxes:
        row_rhs.append(Kbnd[flux_bc.w])
        dat_rhs.append(flux_bc.data)

    for flux_bc in M_bnd.inflow_fluxes:
        _, flux_bc_in = split_inflow(flux_bc, c_flux_b)
        row_rhs.append(Kbnd[flux_bc_in.w])
        dat_rhs.append(flux_bc_in.data)
    # right-hand side construction
    return _build_vector(row_rhs, dat_rhs, Nunk)


def solve_steady_pde(M: TPFAStruct,
                     Pb: Problem,
                     reference: Reference | None = None,
                     ) -> xr.DataArray:
    """Solve a steady PDE using a TPFA scheme.

    Parameters
    ----------
    M : TPFAStruct
        Mesh on which to solve the PDE.
    Pb : data_manager.Problem
        Problem to be solved.
    reference : Reference or None, default is None
        Reference solution of the problem.

    Returns
    -------
    xarray.DataArray
        Numerical solution to the problem. The instance has three
        dimensions:

            * `varname`: the names of the quantities which have been
              computed. Currently only one quantity can be computed and
              its name is 'u'.
            * `data_origin`: if an empty `reference` was passed, there
              is only the numerical solution under the name 'approx'. If
              `reference` is not empty, this dimension also has
              'reference' for the discretization of the reference
              solution and 'error' for the absolute value of the
              difference between the two.
            * `space`: the dimension corresponding to the values of each
              quantitity on the corresponding center of `M`.

    See Also
    --------
    xarray.DataArray
    """
    Nunk = M.nvol
    M_bnd = discretize_BC(M, Pb.bndcnd)
    A = assemble_steady_mat(M, Pb.coeffs, M_bnd)
    b = assemble_steady_rhs(M, Pb.coeffs, M_bnd)
    f = _build_vector(*tpfa.source(M, Pb.rhs), Nunk)  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.

    # Resolution of the linear system
    u = spsolve(A, b+f)
    values: list[ValueArray] = [u]
    coords = {'varname': ['u'], 'data_origin': ['approx']}
    dims = ['varname', 'data_origin', 'space']

    # Reference solution
    if reference is not None:
        uexa = M.discretize(reference.u, PRIMAL)  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # DiscreteFunction as a subtype of Discretizable when
        # it is.
        values.append(uexa['centers'])
        coords['data_origin'].append('reference')
    data = np.stack(values)
    data = data.reshape((1,) + data.shape)
    return xr.DataArray(data, coords=coords, dims=dims)

# %% Unsteady tools
#    ==============


def _Euler(M: TPFAStruct, t0: float, tf: float, tau: float,
           U0: ValueArray,
           coeffs_t: Callable[[np.floating], UnsteadyCoeffs],
           M_bnd_t: Callable[[np.floating], BCStructure],
           rhs_t: Callable[[np.floating], DiscreteFunction],
           explicit: bool,
           rebuild_mat: bool, rebuild_rhs: bool, rebuild_f: bool
           ) -> xr.DataArray:
    """Compute an explicit or implicit Euler scheme."""

    def Mat(t: np.floating) -> csr_array:
        return assemble_steady_mat(M, coeffs_t(t), M_bnd_t(t))

    def rhs(t: np.floating) -> ValueArray:
        return assemble_steady_rhs(M, coeffs_t(t), M_bnd_t(t))

    def f(t: np.floating) -> ValueArray:
        return _build_vector(*tpfa.source(M, rhs_t(t)), Nunk)  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # DiscreteFunction as a subtype of Discretizable when
        # it is.

    def InvMass(t: np.floating) -> csr_array:
        Nunk = M.nvol
        row, col, dat = tpfa.volumic(M, coeffs_t(t).d_t)  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # DiscreteFunction as a subtype of Discretizable when
        # it is.
        return csr_array((1/dat[0], (row[0], col[0])), shape=(Nunk, Nunk))
    t = np.arange(t0, tf, tau)
    Nunk = M.nvol
    dims_res = ['varname', 'data_origin', 't', 'space']
    coords_res = {'varname': ['u'], 'data_origin': ['approx'], 't': t}
    res_data = np.zeros((len(t), Nunk), dtype='float')
    Un = U0
    res_data[0] = U0
    if explicit:
        t_enum = enumerate(t[:-1])
    else:
        In = eye_array(Nunk, dtype='float', format='csr')
        t_enum = enumerate(t[1:])
    for (i, tn) in t_enum:
        if i == 0 or rebuild_mat:
            InvMass_t = InvMass(tn)
            A_t = InvMass_t@Mat(tn)
        if i == 0 or rebuild_rhs or rebuild_mat:
            b_t = InvMass_t@rhs(tn)
        if i == 0 or rebuild_f or rebuild_mat:
            f_t = InvMass_t@f(tn)
        if explicit:
            Un = Un-tau*A_t@Un+tau*(b_t+f_t)
        else:
            Un = spsolve(In+tau*A_t, Un+tau*(b_t+f_t))
        res_data[i+1] = Un
    res_data = np.expand_dims(res_data, axis=(0, 1))
    return xr.DataArray(res_data, coords_res, dims_res)


def solve_unsteady_pde(M: TPFAStruct,
                       t0: float,
                       tf: float,
                       dt: tuple[float, float],
                       Pb: UnsteadyProblem,
                       reference: Reference | None = None
                       ) -> xr.DataArray:
    """Solve an unsteady PDE using a TPFA scheme.

    Parameters
    ----------
    M : TPFAStruct
        Mesh on which to solve the PDE.
    t0: float
        Initial time of simulation
    tf: float
        Final time of simulation
    dt: (float, float)
        Time-step used for the simulation. The first float represent the
        initial time-step and the second the smallest time-step
        authorized in an adaptative time-step algorithm.
    Pb : unsteady_data_manager.UnsteadyProblem
        Problem to be solved.
    reference : Reference, default is None
        Reference solution.

    Returns
    -------
    xarray.DataArray
        Numerical solution to the problem. The instance has three
        dimensions:

            * `varname`: the names of the quantities which have been
              computed. Currently only one quantity can be computed and
              its name is 'u'.
            * `data_origin`: if an empty `reference` was passed, there
              is only the numerical solution under the name 'approx'. If
              `reference` is not empty, this dimension also has
              'reference' for the discretization of the reference
              solution and 'error' for the absolute value of the
              difference between the two.
            * `space`: the dimension corresponding to the values of each
              quantitity on the corresponding center of `M`.

    See Also
    --------
    xarray.DataArray
    """
    coeffs = Pb.coeffs
    U0 = M.evaluate(Pb.u0, 'centers')  # type: ignore
    # Because of mypy Issue #2922 mypy does not recognize
    # DiscreteFunction as a subtype of Discretizable when
    # it is.
    reb_mat = 'mat' in Pb.rebuild
    reb_rhs = 'rhs' in Pb.rebuild
    reb_f = 'f' in Pb.rebuild

    def _partialize(c: DiscreteFunction | None, t: np.floating
                    ) -> DiscreteFunction | None:
        if c is None:
            return None
        else:
            return partial(c, T=t)

    def coeff_t(t: np.floating) -> UnsteadyCoeffs:
        return udm.UnsteadyCoeffs(_partialize(coeffs.A, t),
                                  _partialize(coeffs.v, t),
                                  _partialize(coeffs.q, t),
                                  partial(coeffs.d_t, T=t),
                                  schemes=coeffs.schemes)

    def M_bnd_t(t: np.floating) -> BCStructure:
        return discretize_BC(M, Pb.bndcnd, T=t)

    def rhs_t(t: np.floating) -> DiscreteFunction:
        return partial(Pb.rhs, T=t)

    time_scheme = Pb.coeffs.schemes['d_t']
    if time_scheme == "ExplicitEuler":
        explicit = True
    elif time_scheme == 'ImplicitEuler':
        explicit = False
    else:
        raise ValueError("Unknown type of scheme. "
                         + "Must be 'ExplicitEuler' or 'ImplicitEuler' only")
    result = _Euler(M, t0, tf, dt[0], U0,
                    coeff_t, M_bnd_t, rhs_t, explicit,
                    reb_mat, reb_rhs, reb_f)

    if reference:
        dims = ['varname', 'data_origin', 't', 'space']
        coords = {'data_origin': ['reference']}
        t = result.coords['t'].values
        Ue = np.zeros(result.shape)
        for i, tn in enumerate(t):
            Ue[0, 0, i] = M.evaluate(reference.u,  # type: ignore
                                     'centers', T=tn)
            # Because of mypy Issue #2922 mypy does not recognize
            # DiscreteFunction as a subtype of Discretizable when
            # it is.
        result_ref = xr.DataArray(Ue, coords, dims)
        result = xr.concat((result, result_ref), "data_origin")

    return result

# %% Norms for error curves
#    ======================


L2_x = tpfa.norm
H1_x = tpfa.h1norm


def Linf_t_L2_x(M: TPFAStruct, f: xr.DataArray) -> Any:
    r"""Discrete :math:`L^{\infty}_t(L^2_x)` norm."""
    Mnorm = partial(L2_x, M)
    return np.max(xr.apply_ufunc(Mnorm, f, input_core_dims=[['space']]))


def L2_t_H1_x(M: TPFAStruct, f: xr.DataArray) -> Any:
    r"""Discrete :math:`L^2_t(H^1_x)` norm."""
    Mnorm = partial(H1_x, M)
    return np.sqrt(np.sum(
        xr.apply_ufunc(Mnorm, f, input_core_dims=[['space']]))**2)


space_norm = {'L2': L2_x, 'H1': H1_x}
time_space_norm = {'L2': Linf_t_L2_x, 'H1': L2_t_H1_x}


# %% Public tools
#    ============


def run_example() -> None:
    """Run an example XML file from the command line."""
    parser = ArgumentParser(description="Run an example XML file of the "
                            + "resolution of a PDE with the TPFA scheme and "
                            + "the Pynitevolumes library.")
    parser.add_argument('xml_input', type=str,
                        help='XML file descripting the simulation to run')
    parser.add_argument('-o', '--xml_output', type=str,
                        help='XML file descripting the output to be produced',
                        nargs='*',
                        default=[])
    parser.add_argument('-m', '--mesh_dir', type=str,
                        help='directory containing the directory of the family'
                        + ' of mesh needed for the simulation',
                        default=None)
    parser.add_argument('-u', '--unsteady',
                        help='mark the problem as unsteady',
                        action='store_true')
    args = parser.parse_args()
    if args.unsteady:
        run_unsteady_from_files(args.xml_input, args.xml_output, args.mesh_dir)
    else:
        run_steady_from_files(args.xml_input, args.xml_output, args.mesh_dir)
    input('Press any key to end')


def _make_args_path(sim_filename: str | PathLike[Any],
                    out_filenames: Iterable[str | PathLike[Any]] | None = None,
                    mesh_dir: str | PathLike[Any] | None = None,
                    steady: bool = True
                    ) -> tuple[Path, list[Path], Path | Traversable]:

    sim_path = Path(sim_filename)
    sim_path.with_suffix('.xml')
    if not sim_path.is_file():
        XMLin = files('pynitevolumes.schemes.tpfa.XML.input')
        with as_file(XMLin.joinpath(sim_path.name)) as f:
            sim_path = Path(f)
    if not out_filenames:
        if steady:
            out_filenames = ['standard_steady_plot.xml',
                             'space_error_curves.xml']
        else:
            out_filenames = ['standard_unsteady_plot.xml',
                             'time_space_error_curves.xml']

    out_paths: list[Path] = []
    XMLout = files('pynitevolumes.schemes.tpfa.XML.output')
    for out_filename in out_filenames:
        out_path = Path(out_filename)
        out_path.with_suffix('.xml')
        if out_path.is_file():
            out_paths.append(out_path)
        else:
            with as_file(XMLout.joinpath(out_path.name)) as f:
                out_paths.append(Path(f))

    if mesh_dir is None:
        mesh_dir_path = files('pynitevolumes.schemes.mesh_dir')
    else:
        mesh_dir_path = Path(mesh_dir)
    return sim_path, out_paths, mesh_dir_path


def _load_output(out_paths: list[Path]) -> tuple[list[GenericFigure],
                                                 list[ResultFigure],
                                                 dict[str, set[str]]]:

    figures = []
    error_figures = []
    error_data = {}
    for filename in out_paths:
        (file_figures,
         file_error_figures,
         file_error_data) = om.load_output(filename)
        figures.extend(file_figures)
        error_figures.extend(file_error_figures)
        error_data.update(file_error_data)
    return figures, error_figures, error_data


def _print_description(description: dict[str, Any],
                       sim_filename: str | PathLike[str]) -> None:
    name = description.get('name')
    text = description.get('text')
    if name is None:
        name = f"Running example from {sim_filename}"
    ln = len(name)
    print(ln*'=')
    print(name)
    print(ln*'=')
    if text is not None:
        print(text)
        print(ln*'=', '\n')
    else:
        print('\n')


def _load_struct(mesh_dir_path: Path | Traversable, mesh_name: str
                 ) -> TPFAStruct:
    mesh_path = mesh_dir_path.joinpath(mesh_name)
    if not mesh_path.is_file():
        raise ValueError(f'Could not find a file at {mesh_path}')
    if isinstance(mesh_path, Traversable):
        with as_file(mesh_path) as mesh_path_concrete:
            M = loadmesh(mesh_path_concrete)
    else:
        M = loadmesh(mesh_path)
    print(f'Loaded {mesh_path}')

    # Transformation in TPFAStruct
    if isinstance(M, Mesh):
        M = tpfa.TPFAStruct.fromMesh(M)
    else:
        M = tpfa.TPFAStruct.fromMesh(M[0])
    M.name = mesh_name  # type: ignore[attr-defined]
    # I know that a Mesh object does not have a name but it is useful here
    return M


def run_steady_from_files(
        sim_filename: str | PathLike[Any],
        out_filenames: Iterable[str | PathLike[Any]] | None = None,
        mesh_dir: str | PathLike[Any] | None = None) -> None:
    """
    Run an example file of a steady simulation and plot the results.

    Parameters
    ----------
    sim_filename : str or file object
        XML file which describes the simulation being run.
    out_filenames : iterable of str or file object, optional
        Iterable of XML files which describes what kind of output is
        desired. The output from different files are gathered.
        Default output plots various results.
    mesh_dir : str, or file object optional
        Directory containing the relevant family of mesh.
        If omited uses the internal mesh resources.

    Returns
    -------
    None.

    Warning
    -------
    The default output include error curves, so it can only be used on
    simulations that include a reference solution.
    """
    plt.close('all')
    sim_path, out_paths, mesh_dir_path = _make_args_path(sim_filename,
                                                         out_filenames,
                                                         mesh_dir)
    figures, error_figures, error_data = _load_output(out_paths)
    description, space, Pb, reference = dm.load_data(sim_path)

    mesh_list = space.mesh_list
    nb_mesh = len(mesh_list)
    norms = error_data['norms']
    xaxis = error_data['xaxis']
    coords_err = {'norm': list(norms)}
    error_values = np.zeros((len(norms), nb_mesh), dtype='float')

    _print_description(description, sim_filename)
    if 'dof' in error_data['xaxis']:
        dofs = np.zeros(nb_mesh, dtype='int')
    if 'step' in error_data['xaxis']:
        steps = np.zeros(nb_mesh, dtype='float')
    for i in range(nb_mesh):
        M = _load_struct(mesh_dir_path, mesh_list[i])

        # Boundary condition construction
        Nunk = M.nvol
        step = M.size
        if 'dof' in xaxis:
            dofs[i] = Nunk
        if 'step' in xaxis:
            steps[i] = M.size
        print(f'{i=} Number of unknowns={Nunk}')
        print(f'{i=} Step of the mesh={step:1.2e}')

        results = solve_steady_pde(M, Pb, reference)
        sol = {'Mesh': M, 'results': results}

        # Norms
        if norms:
            uf = results.loc['u', 'approx'].values
            ue = results.loc['u', 'reference'].values
            e = np.abs(uf-ue)
            for (n, norm) in enumerate(norms):
                err_value = space_norm[norm](M, e)
                error_values[n, i] = err_value
                print(f"{i=} Error in norm {norm}: {err_value:1.2e}")
        # Visualization
        for figure in figures:
            figure.render(sol)
    error_results = xr.DataArray(error_values, coords_err, ['norm', 'mesh'])
    if 'dof' in xaxis:
        error_results.coords['dof'] = ('mesh', dofs)
    if 'step' in xaxis:
        error_results.coords['step'] = ('mesh', steps)
    if error_figures:
        for figure in error_figures:
            figure.render({'results': error_results})


def run_unsteady_from_files(sim_filename: str | Path,
                            out_filenames: Iterable[str] | None = None,
                            mesh_dir: str | None = None) -> None:
    """
    Run an example file of an unsteady simulation and plot the results.

    Parameters
    ----------
    sim_filename : str or file object
        XML file which describes the simulation being run.
    out_filenames : iterable of str or file object, optional
        Iterable of XML files which describes what kind of output is
        desired. The output from different files are gathered.
        Default output plots various results.
    mesh_dir : str, or file object optional
        Directory containing the relevant family of mesh.
        If omited uses the internal mesh resources.

    Returns
    -------
    None.

    Warning
    -------
    The default output include error curves, so it can only be used on
    simulations that include a reference solution.
    """
    plt.close('all')
    sim_path, out_paths, mesh_dir_path = _make_args_path(sim_filename,
                                                         out_filenames,
                                                         mesh_dir,
                                                         False)
    figures, error_figures, error_data = _load_output(out_paths)
    description, simulation, Pb, reference = udm.load_data(sim_path)
    mesh_list = simulation.space.mesh_list
    first_step = simulation.time.first_step
    max_step = simulation.time.max_step
    nb_mesh = len(mesh_list)
    nb_dt = len(first_step)
    norms = error_data['norms']
    xaxis = error_data['xaxis']
    coords_err = {'norm': list(norms), 'dt': first_step}
    error_values = np.zeros((len(norms), nb_dt, nb_mesh), dtype='float')

    t0 = simulation.time.t0
    tf = simulation.time.tf
    if 'dof' in error_data['xaxis']:
        dofs = np.zeros(nb_mesh, dtype='int')
    if 'step' in error_data['xaxis']:
        steps = np.zeros(nb_mesh, dtype='float')
    _print_description(description, sim_filename)
    for i in range(nb_dt):
        dt = first_step[i]
        dt_max = max_step[i]
        print(f"{i=} Initial time step={dt}")
        for j in range(nb_mesh):
            M = _load_struct(mesh_dir_path, mesh_list[j])

            # Boundary condition construction
            Nunk = M.nvol
            step = M.size
            if 'dof' in xaxis:
                dofs[j] = Nunk
            if 'step' in xaxis:
                steps[j] = M.size
            print(f'{i=}.{j=} Number of unknowns={Nunk}')
            print(f'{i=}.{j=} Step of the mesh={step:1.2e}')

            results = solve_unsteady_pde(M, t0, tf, (dt, dt_max),
                                         Pb, reference)
            sol = {'Mesh': M, 'results': results}
            for figure in figures:
                figure.render(sol)

            if norms:
                uf = results.loc['u', 'approx']
                ue = results.loc['u', 'reference']
                e = np.abs(uf-ue)
                for (n, norm) in enumerate(norms):
                    err_value = time_space_norm[norm](M, e)
                    error_values[n, i, j] = err_value
                    if norm == 'L2':
                        norm_name = "Linf_t(L2_x)"
                    elif norm == 'H1':
                        norm_name = "L2_t(H1_x)"
                    print(f"{i=}.{j=} Error in norm {norm_name}: "
                          + f"{err_value:1.2e}")
    error_results = xr.DataArray(error_values,
                                 coords_err,
                                 ['norm', 'dt', 'mesh'])
    if 'dof' in xaxis:
        error_results.coords['dof'] = ('mesh', dofs)
    if 'step' in xaxis:
        error_results.coords['step'] = ('mesh', steps)
    if error_figures:
        for figure in error_figures:
            figure.render({'results': error_results})


if __name__ == '__main__':
    run_example()
    plt.show()

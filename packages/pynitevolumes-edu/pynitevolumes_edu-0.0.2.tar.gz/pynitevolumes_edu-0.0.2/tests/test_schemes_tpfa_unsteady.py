# -*- coding: utf-8 -*-
"""
=========================
PARABOLIC TESTS AND PLOTS
=========================

In this toy example, we generate parabolic calculation wuth mesh


Created on Wed Apr  8 14:46:06 2020
@author: fhubert
TO DO list
c'est un clone de DDFV_test utiliser pour le nettoyage
"""

import os
import pytest
from numpy.ma.testutils import assert_array_less
from scipy.stats import linregress
import numpy as np
import xarray as xr
import pynitevolumes.schemes.tpfa.unsteady_data_manager as dm
import pynitevolumes.schemes.tpfa as tpfa
from pynitevolumes.schemes.tpfa.run_pvexamples import (solve_unsteady_pde,
                                                       time_space_norm)
from pynitevolumes.mesh.mesh_io import loadmesh


def test_norm_error():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    # Chemin vers le répertoire des fichiers XML
    xml_dir = os.path.join(script_dir, '..', 'src', 'pynitevolumes', 'schemes', 'tpfa', 'XML', 'input')
    mesh_dir = os.path.join(script_dir, '..',  'src', 'pynitevolumes', 'schemes', 'mesh_dir')
    sim_filename = os.path.join(xml_dir, 'heat_dirichlet.xml')

    description, simulation, Pb, reference = dm.load_data(sim_filename)
    space = simulation.space
    time = simulation.time
    t0 = time.t0
    tf = time.tf
    mesh_list = space.mesh_list
    first_step = time.first_step
    max_step = time.max_step
    nb_mesh = len(mesh_list)
    nb_dt = len(first_step)

    norms = ['L2', 'H1']
    coords_err = {'norm': list(norms), 'dt': first_step}
    error_values = np.zeros((len(norms), nb_dt, nb_mesh), dtype='float')
    dofs = np.zeros(nb_mesh, dtype='int')
    steps = np.zeros(nb_mesh, dtype='float')

    for i in range(nb_dt):
        dt = first_step[i]
        dt_max = max_step[i]
        for j in range(nb_mesh):
            path_mesh = os.path.join(mesh_dir, mesh_list[j])
            M = loadmesh(path_mesh)
            M = tpfa.TPFAStruct.fromMesh(M)
            dofs[j] = M.nvol
            steps[j] = M.size

            results = solve_unsteady_pde(M, t0, tf, (dt, dt_max),
                                         Pb, reference)
            uf = results.loc['u', 'approx']
            ue = results.loc['u', 'reference']
            e = np.abs(uf-ue)
            local_err_too_high = "exact and approximation  "
            local_err_too_high += "is locally larger than 0.03"
            assert_array_less(e, 0.03, err_msg=local_err_too_high)
            for (n, norm) in enumerate(norms):
                err_value = time_space_norm[norm](M, e)
                error_values[n, i, j] = err_value

    error_results = xr.DataArray(error_values, coords_err, ['norm', 'dt', 'mesh'])
    error_results.coords['dof'] = ('mesh', dofs)
    error_results.coords['step'] = ('mesh', steps)

    # Order norm LinfL2 in time-space using mesh step and finest dt
    x = steps
    y = error_results.isel(dt=-1).sel(norm='L2').values
    order = linregress(np.log(x), np.log(y)).slope
    assert order == pytest.approx(2.00, abs=0.2)
    # Order norm L2H1 in time-space using mesh step and finest dt
    x = steps
    y = error_results.isel(dt=-1).sel(norm='H1').values
    order = linregress(np.log(x), np.log(y)).slope
    assert order == pytest.approx(1.00, abs=0.2)
    # Order norm LinfL2 in time-space using mesh dofs and finest dt
    x = dofs
    y = error_results.isel(dt=-1).sel(norm='L2').values
    order = -2*linregress(np.log(x), np.log(y)).slope
    assert order == pytest.approx(2.00, abs=0.2)
    # Order norm L2H1 in time-space using mesh dofs and finest dt
    x = dofs
    y = error_results.isel(dt=-1).sel(norm='H1').values
    order = -2*linregress(np.log(x), np.log(y)).slope
    assert order == pytest.approx(1.00, abs=0.2)
    # Order norm LinfL2 in time-space using dt and finest mesh
    x = first_step
    y = error_results.isel(mesh=-1).sel(norm='L2').values
    order = linregress(np.log(x), np.log(y)).slope
    assert order == pytest.approx(1.00, abs=0.2)

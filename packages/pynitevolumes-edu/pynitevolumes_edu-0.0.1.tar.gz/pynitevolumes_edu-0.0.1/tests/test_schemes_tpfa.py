#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============
ELLIPTIC TESTS
==============

In this toy example, we generate elliptic calculation wuth mesh

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
import pynitevolumes.schemes.tpfa.data_manager as dm
import pynitevolumes.schemes.tpfa.output_manager as om
from pynitevolumes.mesh.mesh_io import loadmesh
import pynitevolumes.schemes.tpfa as tpfa
import pynitevolumes.schemes.tpfa.run_pvexamples as run


def test_norm_error():
    # Choose a data file to test
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    # Chemin vers le répertoire des fichiers XML
    xml_dir = os.path.join(script_dir, '..', 'src', 'pynitevolumes', 'schemes', 'tpfa', 'XML', 'input')
    test_dir = os.path.join(script_dir, '.', 'data')
    mesh_dir = os.path.join(script_dir, '..',  'src', 'pynitevolumes', 'schemes', 'mesh_dir')
    sim_filename = 'steady_template.xml'
    sim_filename = os.path.join(xml_dir, sim_filename)
    out_filename = 'steady_test.xml'
    out_filename = os.path.join(test_dir, out_filename)
    description, space, Pb, reference = dm.load_data(sim_filename)
    figures, error_figures, error_data = om.load_output(out_filename)
    space = space
    mesh_list = space.mesh_list
    nb_mesh = len(mesh_list)
    norms = error_data['norms']
    asked_xaxis = error_data['xaxis']
    coords_err = {'norm': list(norms)}
    error_values = np.zeros((len(norms), nb_mesh), dtype='float')
    error_results = xr.DataArray(error_values, coords_err, ['norm', 'mesh'])

    if 'dof' in error_data['xaxis']:
        dofs = np.zeros(nb_mesh, dtype='int')
    if 'step' in error_data['xaxis']:
        steps = np.zeros(nb_mesh, dtype='float')
    for i in range(nb_mesh):
        path_mesh = os.path.join(mesh_dir, mesh_list[i])
        M = loadmesh(path_mesh)
        # Transformation in TPFAStruct
        M = tpfa.TPFAStruct.fromMesh(M)
        M.name = mesh_list[i]

        # Boundary condition construction
        if 'dof' in asked_xaxis:
            dofs[i] = M.nvol
        if 'step' in asked_xaxis:
            steps[i] = M.size

        results = run.solve_steady_pde(M, Pb, reference)

        # Reference solution
        if norms:
            uf = results.loc['u', 'approx'].values
            ue = results.loc['u', 'reference'].values
            e = np.abs(uf-ue)
            for norm in norms:
                err_value = run.space_norm[norm](M, e)
                error_results.loc[norm][i] = err_value
            local_err_too_high = "exact and approximation "
            local_err_too_high += "is locally larger than 0.03"
            assert_array_less(e, 0.03, err_msg=local_err_too_high)
    if 'dof' in asked_xaxis:
        error_results.coords['dof'] = ('mesh', dofs)
    if 'step' in asked_xaxis:
        error_results.coords['step'] = ('mesh', steps)
    if error_figures:
        error = {}
    for xaxis in asked_xaxis:
        for norm in norms:
            xval = error_results.coords[xaxis].values
            yval = error_results.loc[norm].values
            error[xaxis] = xval
            error[norm] = yval
            order = linregress(np.log(xval), np.log(yval)).slope
            if xaxis == 'dof':
                order = -2*order
            error[f'order_{norm}_{xaxis}'] = order
    assert 1.37 == pytest.approx(error['order_L2_step'], abs=0.01)
    assert 1.37 == pytest.approx(error['order_L2_dof'], abs=0.01), \
        "regression L2 is not close to 2.0"
    assert 0.72 == pytest.approx(error['order_H1_step'], abs=0.015)
    assert 0.72 == pytest.approx(error['order_H1_dof'], abs=0.015), \
        "regression H1 is not close to 1.15"

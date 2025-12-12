#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TPFA Finite Volumes Schemes using the edge structure for the mesh.

The purpose of this package is twofold:

* to provide tools to write easily Finite Volume Schemes on meshes that
  respect the Delaunay condition,
* to provide elementary building blocks of schemes on this type of mesh.

The first point is achieved by the `tpfa_struct` submodule and the
second by `tpfa_basics`. Refer to the documentation of these submodules
for detailed information on what they provide.

For convenience, the `tpfa` module provides direct access to some
functionality of these submodules directly.

Attributes
----------
TPFAStruct
check_orthogonality
check_centers_order
build_voronoi_centers
norm
h1norm
diffusion
convection
volumic
source
"""

__all__ = ['TPFAStruct', 'norm', 'h1norm',
           'check_orthogonality',
           'check_centers_order',
           'build_voronoi_centers', 'diffusion_matrix', 'diffusion_rhs',
           'convection_matrix', 'convection_rhs', 'volumic', 'source',
           'build_whole_dirichlet', 'build_whole_neumann']

from importlib.resources import files
from . import tpfa_struct, tpfa_basics
from .tpfa_struct import (TPFAStruct, norm, h1norm,
                          check_orthogonality,
                          check_centers_order,
                          build_voronoi_centers)
from .tpfa_basics import (diffusion_matrix, diffusion_rhs,
                          convection_matrix, convection_rhs, volumic, source,
                          build_whole_dirichlet, build_whole_neumann)

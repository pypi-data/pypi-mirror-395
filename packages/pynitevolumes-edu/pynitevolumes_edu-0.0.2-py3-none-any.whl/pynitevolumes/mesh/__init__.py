"""
Core mesh management tools.

Tools to manage meshes are seperated in categories which get their own
submodules. For convenience, some tools listed below are provided
directly in the `pynitevolumes.mesh`. The submodules are

* base_struct : core mesh management tools
* mesh_io : read/write .pvm mesh filetype or read mesh filetypes from
  external sources
* meshtools : geometric manipulation of meshes
* md : describe abstractly submeshes
* cartesian : grid meshes on rectangle domains
* plotting : plot meshes and discrete functions
* disc : definition of types that can be evaluated on Mesh instances

Refer to the submodule documentation for details.

Attributes
----------
Diamond
Mesh
Cartesian
Discretizable
plotmesh
pcolor_discrete
contour_discrete
contourf_discrete
"""
from .plotting import plotmesh, pcolor_discrete, contour_discrete
from . import base_struct, mesh_io, meshtools, md, cartesian, disc
from .disc import Discretizable
from .meshtools import locate
from .base_struct import Mesh, Diamond
from .cartesian import Cartesian

##############################################################
Pynite Volumes: a library for writing 2D finite volume schemes
##############################################################

***********
Description
***********

This library aims at facilitating the coding of algorithms in the Finite Volumes family. These algorithms are used for computing so-called *numerical solutions* to partial differential equations (PDE).
The Pynite Volumes library provide tools to help writing such algorithms.

Background
==========

There are several ways to use the library depending on your knowledge of Finite Volumes schemes for PDEs.

* If you know about PDEs but know nothing about Finite Volume schemes, you can use the preconstructed tools of the library to rapidly assemble a numerical schemes for a relatively simple (or rather standard/academic) PDE. Use the functions of the library as black boxes.

* If you know about standard Finite Volume schemes (also known as *two-point-fluxes-approximation* or TPFA schemes) you can use the `TPFAStruct` class to write down any scheme that is compatible with this framework.  Even some non linear problems can be approximated, as long as you can write the scheme on paper.

* If you are an expert in Finite Volume schemes and want to implement state-of-the-art, complicated numerical methods, you may rely on the tools of the library to take care of some of the busy work and focus on what matters the most.
  
*****
Usage
*****

At their heart any numerical method for a PDE works by solving a linear system or a sequence of linear systems and as such the numerical methods describes how the matrix and the right-hand side of the linear system are constructed from the data of the problems. Note that the library is concerned with **making** the linear system (matrix and right-hand side) not **solving** the linear system which needs to  be delegated to dedicated libraries such as `Numpy <https://numpy.org>`_ or `Scipy <https://scipy.org>`_.

Let us say that one wants to solve a Laplace (or Poisson) equation with some homogenous Dirichlet boundary conditions

.. math::

   -\Delta u=1\ \mathrm{on}\ \Omega
   
   u=0\ \mathrm{on}\ \partial\Omega

First you would need a mesh of the domain :math:`\Omega`. Details about the mesh are stored inside an object, let us call it `M`.

* If the mesh is "good" (we would rather say *admissible*) and if we want to use the preconstructed tools from the library as black boxes we would do:

  .. code-block:: python

     import numpy as np
     from scipy.sparse import csr_array
     from scipy.sparse.linalg import spsolve
     from pynitevolumes.schemes.tpfa.tpfa_basics import (diffusion_matrix, diffusion_rhs,
		                                         build_whole_dirichlet, source)

     M = ... #  obtain M from various ways

     dof = M.nvol  # the number of unkowns of the system
     
     A = 1.0  #  because the diffusion coefficient in this problem is 1.0

     boundary_condition = build_whole_dirichlet(M, 0.0)  #  the value is 0.0 on the boundary
     
     mat_row_d, mat_col_d, mat_dat_d = diffusion_matrix(M, A, boundary_condition)
     rhs_row_d, rhs_dat_d = diffusion_rhs(M, A, boundary_condition)
     rhs_row_source, rhs_dat_source = source(M, 1.0)  #  the right-hand side is the constant function 1.0

     mat_row = np.concatenate(mat_row_d)
     mat_col = np.concatenate(mat_col_d)
     mat_dat = np.concatenate(mat_dat_d)
     Mat = csr_array((mat_dat, (mat_row, mat_col)), shape=(dof, dof))  # builds the matrix

     # Build the right-hand side
     rhs_row = np.concatenate(rhs_row_d+rhs_row_source)
     rhs_dat = np.concatenate(rhs_dat_d+rhs_dat_source)
     B = csr_array((rhs_dat, (rhs_row, np.zeros(len(rhs_row)))), shape=(dof, 1))  # builds the right-hand side

     U = spsolve(Mat, B) #  obtain the numerical solution!

* If the mesh is again "good" and we want to check that we have understood the standard Finite Volume scheme of TPFA for this problem we could try to build the
  matrix and the right-hand side "by ourselves" in a very detailed way. Then our code could look like that.

  .. code-block:: python
		  
     import numpy as np
     from scipy.sparse import csr_array
     from scipy.sparse.linalg import spsolve

     M = ... #  obtain M from various ways

     dof = M.nvol
     
     A = 1.0  #  because the diffusion coefficient in this problem is 1.0

     mat_row = []
     mat_col = []
     mat_dat = []
     

     # the next two lines are only there to follow classical mathematical notations for this method
     K = M.diam_i.c[0]
     L = M.diam_i.c[1]
     for s in range(M.nin):  # loop over all inner edges/diamonds because this is how data is stored in our framework
         mat_row.extend([K[s], K[s], L[s], L[s]])
	 mat_col.extend([K[s], L[s], K[s], L[s]])
	 val_s = M.len_i[s]/M.dKL_i[s]
	 mat_dat.extend([val_s, -val_s, -val_s, val_s])

     Kbnd = M.diam_b.c
     for s in range(M.nbnd):  # loop now over boundary edges/diamonds
         mat_row.append(Kbnd[s])
	 mat_col.append(Kbnd[s])
	 mat_dat.append(M.len_b[s]/M.dKs_b[s])
     Mat = csr_array((mat_dat, (mat_row, mat_col)), shape=(dof, dof))  # builds the matrix

     B = np.zeros(dof)
     # Build the right-hand side
     for k in range(M.nvol):
         B[k] = M.vol[k]*1.0

     U = spsolve(Mat, B) #  obtain the numerical solution!

  (Of course this particular code could be easily improved by taking advantage of Numpy vectorization capabilities)

* Finally more advanced users can dig in the properties of the object `M` to build more sophisticated examples or even add their own properties to
  create even more advanced numerical schemes.
  
In both cases, assuming for simplicity that :math:`\Omega` is a simple square that has been subdivided into 4x4 subsquares regularly, one would obtain at the end
of the day

>>> print(U)
array([0.0234375, 0.0390625, 0.0390625, 0.0234375, 0.0390625, 0.0703125,
       0.0703125, 0.0390625, 0.0390625, 0.0703125, 0.0703125, 0.0390625,
       0.0234375, 0.0390625, 0.0390625, 0.0234375])

************
Installation
************

For the moment the only way to install the library is from the wheel or the sources available at

`wheel_url <https://plmlab.math.cnrs.fr/pynite_volumes/pynite_volumes/-/releases/>`_
   
**************************
History behind the project
**************************

A unified view of 2D meshes
===========================

Initially this library has been developed to solve two problems issued from teaching considerations:

* Finite Volumes are mathematical algorithms that can be studied in mathematical courses by students who have mostly a mathematical background. Numerical analysis of such algorithms is a fulfilling endeavour in its own right but we have always felt that studying these methods only on paper is lacking from a pedagogical standpoint. On the other hand, we wanted our students to focus on the *numerical analysis* aspects of studying these methods and not be swamped by the programming details of implementing such methods. Moreover, our students mostly know only one programming language which is `Python <https://www.python.org>`_.

* We wanted our students to be able to handle 2D meshes. Usually the crux of a numerical method for a PDE (be it Finite Volumes, Finite Elements or otherwise) can be explained on a 1D problem and those are easy to implement. However, the simplification of the geometry by going from a 2D problem to a 1D problem hides a lot of important details that are important to get if one wants to go even from simple academic problems to more complex *real life* problems espacially in the implementation of the method (some say scientific computation and high-performance computing start in 2D). 2D meshes are complex objects to manipulate and meshing is a scientific field in its own right and once again we wanted our students to be able to focus on other things.

To solve these two problems, we have developed the Pynite Volumes library. It is a library in `Python <https://www.python.org>`_ providing tools to automate the things we want to put under the rug and hopefully allows to focus on the *numerical scheme* aspects  of using these methods. At its core, the library takes a 2D mesh from an outside source (to leave the complicated work of meshing to dedicated tools) and process it into a Python object that allows simple access to the quantity we need from it. Using this object allows to implement easily the equation of the schemes laid out on paper.

Note that to be able to do all that we use a mathematical framework called the *edge structure* or *diamond structure* (you can read to know more about it). This fact alone makes it a complementary library to other library focusing on solving PDE using the Finite Volumes family of algorithms  


A collection of *white boxes*
=============================

As the development of the initial idea grew, we realised that we wanted to expand the uses of our codebase

* for low level teaching : we wanted to be able to to rapidly show the benefits of numerical schemes to people without the mathematical knowledge to write the schemes themselves
* for high level teaching : we wanted students (in internships for instance) to be able to tackle complex problems beyond the standard academic ones and thus focus on the new rather than the known.

This led to the addition into the codebase of functions to take care of the routine aspects of the implementation of the standard methods (specifically, diffusion, convection and volumic terms in the TPFA framework). These are thought of as *white boxes* in the sense that you can use them directly or you can open them and modify them if you need to.

.. to documentation

*************
Documentation
*************

Complete documentation of the library can be found `here <https://pynite_volumes.pages.math.cnrs.fr/pynite_volumes/>`_.

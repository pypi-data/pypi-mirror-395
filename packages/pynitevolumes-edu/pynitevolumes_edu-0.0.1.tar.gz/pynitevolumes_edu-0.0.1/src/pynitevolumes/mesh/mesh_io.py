#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for managing reading and writing meshes from files."""
from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from importlib import import_module
from importlib.resources import files, as_file
import numpy as np
from .base_struct import Mesh, Diamond
from ..tools.geometry import orthocenter, barycenter, wedge, vnorm
if TYPE_CHECKING:
    from typing import Literal, Any
    from collections.abc import Callable
    from numpy.typing import NDArray
    from ._array_types import PointArray, IndexArray

type MeshfileReader = Callable[[Path], Mesh | tuple[Mesh, Any]]
type MeshfileWriter = Callable[[Path, Mesh], None]


# %% Functions for pvm
#    =================

def write_pvm(filename: Path, M: Mesh, *, replace: bool = True,
              compressed: bool = True) -> None:
    """Save the Mesh object to a .pvm file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Filename to which the data is saved.
    M : base_struct.Mesh
        The mesh to be saved.
    replace : bool, optional
        Set to True if you want to allow the replacement of an existing
        file. The default is False.
    compressed : bool, optional
        Uses the NumPy savez_compressed to create the file.
        The default is True.

    Raises
    ------
    FileExistsError
        If a file already exists with the same name this Exception will
        be raised if replace=False.

    Returns
    -------
    None.

    See Also
    --------
    numpy.savez, numpy.savez_compressed

    Notes
    -----
    This function basically renames a file created with the NumPy savez
    or savez_compressed function. This minimizes the risk of arbitrary
    code execution.
    """
    filename = Path(filename).with_suffix('')
    if (not replace) and filename.with_suffix('.pvm').exists():
        raise FileExistsError(f'The file {filename}.pvm already  exists.\n'
                              + 'If you want to replace it,'
                              + ' use replace=True in savemesh')
    if compressed:
        savefun = np.savez_compressed
    else:
        savefun = np.savez
    arrays = {'_saved_type':  np.array([type(M).__module__,
                                        type(M).__qualname__])}
    if '_saved_type' in vars(M):
        raise AttributeError("Mesh object is not allowed to have an " +
                             "attribute '_saved_type'.")
    list_attrs = []
    for a, v in vars(M).items():
        if isinstance(v, np.ndarray):
            arrays[a] = v
        if isinstance(v, list):
            if '_' in a:
                raise AttributeError("List attributes of M cannot contain '_'")
            list_attrs.append(a)
            for i, a_elem in enumerate(v):
                arrays[f'{a}_{i}'] = np.array(a_elem)
    if list_attrs:
        if '_list_attrs' in vars(M):
            raise AttributeError("Mesh object is not allowed to have " +
                                 "an attribute '_list_attr' and " +
                                 "attributes that are lists.")
        arrays['_list_attrs'] = np.array(list_attrs)
    Dic, Div = M.diam_i.unpack()
    Dbc, Dbv = M.diam_b.unpack()
    arrays.update({'Dic': Dic, 'Div': Div, 'Dbc': Dbc, 'Dbv': Dbv})
    savefun(filename, allow_pickle=False, **arrays)
    filename.with_suffix('.npz').rename(filename.with_suffix('.pvm'))


def check_pvm(filename: str | Path) -> None:
    """Check the type saved in a .pvm file."""
    filename = Path(filename).with_suffix('.pvm')
    with np.load(filename, allow_pickle=False) as d:
        print(f"The saved type was {d['_saved_type'][0]}"
              + f".{d['_saved_type'][1]}")


def read_pvm(filename: str | Path) -> Mesh:
    """Load a Mesh object from a .pvm file.

    Parameters
    ----------
    filename : str or pathlib.Path
        The file to be loaded. This file must have been saved via
        savemesh.

    Returns
    -------
    base_struct.Mesh
        The Mesh object contained in filename.

    Notes
    -----
    This function creates an object with the same type as it had when
    savemesh was applied. To do that it imports the module which
    contained the class of the object and as such it is a vulnerability.
    If you want to check which module and which type will be used, use
    `check_pvm` on `filename` before reading the file.
    """
    filename = Path(filename).with_suffix('.pvm')
    info: dict[str, NDArray[Any]] = {}
    with np.load(filename, allow_pickle=False) as d:
        info.update(d)
    if '_saved_type' in info:
        mesh_type = info.pop('_saved_type')
        origin = import_module(mesh_type[0])
        Constructor: type[Mesh] = getattr(origin, mesh_type[1])
    else:
        Constructor = Mesh
    diam_i = Diamond.pack(info.pop('Dic'), info.pop('Div'))
    diam_b = Diamond.pack(info.pop('Dbc'), info.pop('Dbv'))
    centers = info.pop('centers')
    vertices = info.pop('vertices')
    extra: dict[str, list[NDArray[Any]]] = {}
    if '_list_attrs' in info:
        lists_of_arrays = info.pop('_list_attrs')
        for a in lists_of_arrays:
            a_list = [k for k in info if f'{a}_' in k]
            n_a = len(a_list)
            extra[a] = [info.pop(f'{a}_{i}') for i in range(n_a)]
    M = Constructor(centers, vertices, (diam_i, diam_b), **info, **extra)
    return M

# %% Functions for bamg
#    ==================


def write_bamg(filename: Path, M: Mesh, *,
               labels: list[IndexArray] | None = None) -> None:
    """Save the mesh object to a .msh file.

    This format is the FreeFem++ format.

    Parameters
    ----------
    filename : str or pathlib.Path
        Filename to which the data is saved.
    M : base_struct.Mesh
        The mesh to be saved.
    labels : list of arrays, optional
        List of the boundary parts labels. Each array of int contain the
        set of vertices numbers that belong to the same boundary part.
        All boundary vertices must be in one of the array.
        If None, the whole boundary is considered one part.
        The default is None.

    Raises
    ------
    ValueError
        Raised if `M` does not consist only of triangles.

    Returns
    -------
    None.

    """
    filename = Path(filename).with_suffix('.msh')
    nv = M.nvert
    nt = M.nvol
    ne = M.nbnd
    if labels is None:
        labels = [M._find_bound_vert()]
    with open(filename, 'w') as f:
        f.write(f'{nv} {nt} {ne}\n')
        v_labels: dict[int, set[int]] = {}.fromkeys(range(nv), set())
        for s in range(nv):
            label_s = 0
            for num, lab in enumerate(labels, 1):
                if s in lab:
                    label_s = num
                    v_labels[s].add(num)
            f.write(
                f'{M.vertices[s, 0]} {M.vertices[s, 1]} {label_s}\n')
        # for k in range(nt):
        #     f.write('3\n')
        for k in range(nt):
            I, J, Ibnd = M._center_struct(k)
            ei0 = M.diam_i.v[:, I[0]]
            ei1 = M.diam_i.v[:, J[0]]
            eb = M.diam_b.v[:, Ibnd[0]]
            t = np.unique(np.concatenate((ei0, ei1, eb), axis=-1))
            if len(t) != 3:
                raise ValueError("Mesh can only be composed of "
                                 + "triangles.")
            q = M.vertices[t]
            orient = (wedge(q[1]-q[0], q[2]-q[0])
                      / (vnorm(q[1]-q[0])*vnorm(q[2]-q[0])))
            if orient < 0:
                t[[2, 1]] = t[[1, 2]]
            t += 1
            f.write(f'{t[0]} {t[1]} {t[2]} 0\n')
        for s in range(ne):
            V = M.diam_b.v[:, s]
            label_e = (v_labels[V[0]] & v_labels[V[1]]).pop()
            f.write(f'{V[0]} {V[1]} {label_e}\n')


def read_bamg(filename: Path, *,
              centers:
                  Callable[[PointArray, PointArray, PointArray], PointArray] |
                  Literal['orthocenters', 'barycenters'] = 'orthocenters'
              ) -> tuple[Mesh, list[IndexArray]]:
    """Create a `pynitevolumes.Mesh` from a .msh file.

    This function is for meshes obtained through FreeFem++ internal
    mesher BAMG.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to the .msh file.
    centers : Callable or 'orthocenters' or 'barycenters', optional.
        The reconstruction method of the centers from the vertices of
        triangles. If callable, it should be able to take three
        arguments which are all arrays of shape (n, 2) and return an
        array of shape (n, 2) where the center of the triangle of
        vertices v0[i], v1[i], v2[i] has coordinates given by
        centers(v0, v1, v2)[i]. Default method is to compute the
        orthocenters of each triangle as this satisfies half of the
        admissibility condition of Delaunay.

    Returns
    -------
    tuple[base_struct.Mesh, list of IndexArray]
        The first element is the mesh created from the data from the
        in the file. The second element is the boundary parts as a
        list of arrays of int. Each array contain the indices of the
        vertices that belong to the same boundary part.

    Notes
    -----
    Since there is no notion of 'center of a volume' in meshes generated
    through FreeFem++, and since this type of mesh consist only of
    triangles, centers will be constructed as the orthocenter of each
    triangles. In this way, the centers automatically satisfy a
    condition of orthogonality in the sense that the two centers of the
    two control volumes on each side of an inner edge are on a line
    orthogonal to that edge.

    References
    ----------
    Cite Hecht
    """
    if not callable(centers):
        if centers == 'orthocenters':
            centers = orthocenter
        elif centers == 'barycenters':
            centers = barycenter
        else:
            if isinstance(centers, str):
                raise ValueError("Unknown method for centers construction")
            else:
                raise TypeError("centers should be a callable or str")
    infile = Path(filename)
    enc_edges: dict[tuple[int, int], int] = {}

    def treat_edge(s1: int, s2: int) -> None:
        e = (min(s1, s2), max(s1, s2))
        if e in enc_edges:
            ei_0.append(s1)
            ei_1.append(s2)
            Ki.append(enc_edges[e])
            Li.append(i)
            del enc_edges[e]
        else:
            enc_edges[e] = i
    prog = 0
    with open(infile) as f:
        fl = f.readline().strip().split()
        prog += 1
        nvert = int(fl[0])
        nvol = int(fl[1])
        nbnd = int(fl[2])
        cdic = np.zeros((nvol, 2))
        vdic = np.zeros((nvert, 2))
        ei_0: list[int] = []
        ei_1: list[int] = []
        Ki: list[int] = []
        Li: list[int] = []
        eb = np.zeros((2, nbnd), dtype='int64')
        Kb = np.zeros(nbnd, dtype='int64')
        prog += 1
        for i in range(nvert):
            line = f.readline().strip().split()
            vdic[i, :] = np.array([float(line[0]), float(line[1])])
        prog += 1
        for i in range(nvol):
            line = f.readline().strip().split()
            voli = [int(line[0])-1, int(line[1])-1, int(line[2])-1]
            cdic[i, :] = centers(vdic[voli[0]],
                                 vdic[voli[1]],
                                 vdic[voli[2]])
            s1 = voli.pop()
            s1_0 = s1
            while voli:
                s2 = voli.pop()
                treat_edge(s1, s2)
                s1 = s2
            treat_edge(s1, s1_0)
        ei = np.array([ei_0, ei_1])
        prog += 1
        labdic: dict[int, list[int]] = {}
        for i in range(nbnd):
            line = f.readline().strip().split()
            v0, v1 = int(line[0])-1, int(line[1])-1
            eb[0, i] = v0
            eb[1, i] = v1
            lab_i = int(line[2])
            Kb[i] = enc_edges[(min(v0, v1), max(v0, v1))]
            if lab_i in labdic:
                labdic[lab_i].append(i)
            else:
                labdic[lab_i] = [i]
        bnd_pieces_num = max(labdic)
        labels = []
        for n in range(1, bnd_pieces_num+1):
            labels.append(np.array(labdic[n], dtype='int'))
        return (Mesh(cdic, vdic,
                     (Diamond({'c': np.stack((Ki, Li)), 'v': ei}),
                      Diamond({'c': Kb, 'v': eb}))),
                labels)


_known_files: dict[str, tuple[MeshfileReader, MeshfileWriter]]

_known_files = {'.pvm': (read_pvm, write_pvm),
                '.msh': (read_bamg, write_bamg)}


def loadmesh(filename: str | Path, **kwargs: Any) -> Mesh | tuple[Mesh, Any]:
    """
    Create a Mesh file from file.

    Parameters
    ----------
    filename : str or pathlib.Path
        The file containing the data to be read. The files that are
        currently readable are .pvm, .msh. Either give the full path
        to the file or if the file is in the packaged resources,
        one can provide only the name.

    Returns
    -------
    base_struct.Mesh or tuple[base_struct.Mesh, Any]
        If `filename` was a '.pvm' file, return `M` a mesh of the type
        it had when saved. Otherwise `M` will be of type
        `pynitevolumes.mesh.base_struct.Mesh` and the second argument
        will be some metadata associated to the mesh.
    """
    def _load(file: Path) -> Mesh | tuple[Mesh, Any]:
        suff = file.suffix
        if suff in _known_files:
            return _known_files[suff][0](file, **kwargs)
        else:
            raise ValueError("Unknown mesh file type.")

    def _add_mesh_family(file: Path) -> str:
        name = file.name
        mesh_family, underscore, num_and_ext = name.partition('_')
        return mesh_family + '/' + name

    file_path = Path(filename)
    if not file_path.is_file():
        mesh_dir_path = files('pynitevolumes.schemes.mesh_dir')
        file_path_stand_alone = mesh_dir_path.joinpath(file_path.name)
        if file_path_stand_alone.is_file():
            with as_file(file_path_stand_alone) as file:
                return _load(file)
        else:
            file_path_in_fam = mesh_dir_path.joinpath(
                _add_mesh_family(file_path))
            if file_path_in_fam.is_file():
                with as_file(file_path_in_fam) as file:
                    return _load(file)
            else:
                raise ValueError(f"Unable to load {filename}.")
    else:
        return _load(file_path)


def savemesh(filename: str | Path, M: Mesh, **kwargs: Any) -> None:
    """Save the Mesh objecto to a .pvm file."""
    file = Path(filename)
    suff = file.suffix
    if suff in _known_files:
        _known_files[suff][1](file, M, **kwargs)
    else:
        raise ValueError("Unknown mesh file type.")

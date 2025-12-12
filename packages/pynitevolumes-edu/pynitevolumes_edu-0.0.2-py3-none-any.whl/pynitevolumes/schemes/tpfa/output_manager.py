#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module managing the automatic output for TPFA examples."""
from __future__ import annotations
from ast import literal_eval
from warnings import warn
from pathlib import Path
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from defusedxml.ElementTree import parse as parse_xml
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from ...mesh.plotting import (plotmesh, pcolor_discrete, contour_discrete,
                              quiver_discrete, _prepare_plotting)
from pynitevolumes.mesh.md import PREDEFINED_MD
if TYPE_CHECKING:
    from typing import Literal, Any, ClassVar
    from collections.abc import Sequence
    from xml.etree.ElementTree import Element
    from numpy.typing import NDArray
    from xarray import DataArray
    from matplotlib.axes import Axes
    from matplotlib.artist import Artist
    from ...mesh._array_types import ValueArray
    from ...mesh.base_struct import Mesh
    from ...mesh.md import MeshDescription

plt.rcParams['axes.formatter.min_exponent'] = 2
plt.rcParams['font.size'] = 12
plt.rcParams['text.usetex'] = False
plt.rcParams['legend.fontsize'] = 14

_DEF_WIDTH_FIG = 10
_DEF_HEIGHT_FIG = 8


MAX_NVOL = 500

PARAMS_SELECT_TYPE = {'values', 'indexes', 'percents', 'all', 'first', 'last'}


def _filter_params(select_type: str, select: Any, values: DataArray,
                   param_name: str) -> DataArray:
    if select_type == 'values':
        return values.sel({param_name: select}, method='nearest')
    elif select_type == 'indexes':
        return values.isel({param_name: select})
    elif select_type == 'percents':
        nb_other = values.sizes[param_name]
        indexes = [int((nb_other-1)*i) for i in select]
        return values.isel({param_name: indexes})
    elif select_type == 'all':
        return values
    elif select_type == 'first':
        return values.isel({param_name: [0]})
    elif select_type == 'last':
        return values.isel({param_name: [-1]})
    else:
        raise ValueError('Unknown value selection method.' +
                         f'select_type must be one of {PARAMS_SELECT_TYPE}')

# %% Plots
#    =====


class GenericPlot(ABC):
    """Shared properties of every plots.

    Attributes
    ----------
    display : bool
        Whether to actually render the plot or not.
    param : dict[str, Any]
        Extra parameters to pass to the relevant `matplotlib` function.
    """

    def __init__(self, element: Element):
        self.display = literal_eval(element.get('display', 'True'))
        self.param = {k: literal_eval(v) for k, v in element.items()
                      if not hasattr(self, k) and k != 'type'}

    @abstractmethod
    def _render(self, ax: Axes, *args: Any, **kwargs: Any) -> Any:
        ...

    def render(self, ax: Axes, *args: Any, **kwargs: Any) -> Any:
        """Render something."""
        plotobj = None
        if self.display:
            plotobj = self._render(ax, *args, **kwargs)
        return plotobj


class PlotOnMesh(GenericPlot):
    """Shared properties of plots on a mesh.

    Attributes
    ----------
    submesh : str
        Name of the submesh on which the plot occurs.
    title : bool
        Whether to display the name of the quantity being plotted on the
        x axis.
    ylabel : bool
        Whether to display the name of the submesh on the y axis.
    """

    def __init__(self, element: Element) -> None:
        self.submesh = element.get('submesh', 'PRIMAL')
        self.varname = element.get('varname', 'u')
        self.show_colorbar = literal_eval(element.get('show_colorbar',
                                                      'False'))
        self.show_title = literal_eval(element.get('show_title', 'True'))
        self.show_ylabel = literal_eval(element.get('show_ylabel', 'True'))
        super().__init__(element)

    def _specific_render(self, ax: Axes, E: Mesh,
                         md: MeshDescription, u: ValueArray) -> Any:
        pass

    def _render(self, ax: Axes, *, E: Mesh, results: DataArray,
                data_origin: str, extra_title: str | None = None,
                **kwargs: Any) -> Any:
        # E: Mesh = kwargs.get('E')
        # current_data: DataArray = kwargs.get('results')
        # data_origin: str = kwargs.get('data_origin')
        # extra_title: str = kwargs.get('extra_title')
        if extra_title is None:
            extra_title = ''
        md = PREDEFINED_MD[self.submesh]
        if data_origin in {'approx', 'reference'}:
            u = results.loc[dict(varname=self.varname,
                                 data_origin=data_origin)].values
        else:
            ua = results.loc[dict(varname=self.varname,
                                  data_origin='approx')].values
            ue = results.loc[dict(varname=self.varname,
                                  data_origin='reference')].values
            u = np.abs(ua-ue)
        plotobj = self._specific_render(ax, E, md, u)
        if self.show_colorbar:
            plt.colorbar(ax=ax)
        if self.show_title:
            ax.set_title(f"{self.varname} {data_origin} {extra_title}")
        if self.show_ylabel:
            ax.set_ylabel(self.submesh)
        return plotobj


class PlotOfPcolor(PlotOnMesh):
    """Directives to plot a pcolor_discrete."""

    def __init__(self, element: Element) -> None:
        super().__init__(element)

    def _specific_render(self, ax: Axes, E: Mesh, md: MeshDescription,
                         u: ValueArray) -> Any:
        """Render the plot."""
        return pcolor_discrete(E, md, u, ax=ax, **self.param)  # type: ignore
        # Because of mypy Issue #2922 mypy does not recognize
        # ValueArray as a subtype of Discretizable when
        # it is.


class PlotOfContour(PlotOnMesh):
    """Directives to plot contours."""

    def __init__(self, element: Element) -> None:
        levels = element.get('levels', None)
        if levels is None:
            self.levels = None
        else:
            self.levels = literal_eval(levels)
        super().__init__(element)

    def _specific_render(self, ax: Axes, E: Mesh, md: MeshDescription,
                         u: ValueArray) -> Any:
        return contour_discrete(
            E, md, u, levels=self.levels, ax=ax,  # type: ignore
            **self.param)
        # Because of mypy Issue #2922 mypy does not recognize
        # ValueArray as a subtype of Discretizable when
        # it is.


class PlotOfQuiver(PlotOnMesh):
    """Directives to plot quivers."""

    def __init__(self, element: Element) -> None:
        self.colors = element.get('colors', None)
        if self.colors is not None:
            self.colors = literal_eval(self.colors)
        super().__init__(element)

    def _specific_render(self, ax: Axes, E: Mesh, md: MeshDescription,
                         vec: ValueArray) -> Any:
        u = vec[:, 0]
        v = vec[:, 1]
        return quiver_discrete(E, md, u, v, self.colors, ax=ax,  # type: ignore
                               **self.param)
        # Because of mypy Issue #2922 mypy does not recognize
        # ValueArray as a subtype of Discretizable when
        # it is.


class PlotOfMeshStructure(GenericPlot):
    """Directives to plot a mesh.

    Attributes
    ----------
    max_nvol : int or None
        If a mesh has more than `max_nvol` volumes, cuts the display.
        Set to `None` to display in every case.
    """

    def __init__(self, element: Element) -> None:
        self.submesh = element.get('submesh', 'PRIMAL')
        line_kw = element.find('line_parameters')
        if line_kw is None:
            self.line_kw = {}
        else:
            self.line_kw = {k: literal_eval(v) for k, v in line_kw.items()}
        txt_kw = element.find('text_parameters')
        if txt_kw is None:
            self.text_kw = {}
        else:
            self.text_kw = {k: literal_eval(v) for k, v in txt_kw.items()}
        max_nvol = element.get('max_nvol', MAX_NVOL)
        if max_nvol == 'None':
            self.max_nvol = None
        else:
            self.max_nvol = int(max_nvol)
        self.verbose = literal_eval(element.get('verbose', 'False'))
        super().__init__(element)

    def _render(self, ax: Axes, **kwargs: Any) -> Any:
        """Render the mesh."""
        E = kwargs['E']
        submesh = PREDEFINED_MD[self.submesh]
        plotobj = None
        if self.max_nvol is None or (E.nvol < self.max_nvol):
            plotobj = plotmesh(E, submesh, ax=ax,
                               line_kwargs=self.line_kw, text_kw=self.text_kw,
                               **self.param)
        elif self.verbose:
            print('Number of volumes is too high ' +
                  f'({E.nvol} >= {self.max_nvol}). Skipping the plot of the' +
                  ' mesh')
        return plotobj

# %% Error curves
#    ============


class SpaceErrorCurve(GenericPlot):
    """Error curve for a steady numerical scheme.

    Attributes
    ----------
    xaxis : {'step', 'dof'}
        If 'step', the error curve is done relatively to some
        `Mesh.size` parameter. If 'dof', the error curve is done
        relatively to the number of unknowns
    norms : list of str
        What norms to use to evaluate the error.
    axis_names : bool
        Whether to display names along the axes.
    """

    _axis_disp: ClassVar[dict[str, str]] = {'step': 'Mesh size',
                                            'dof': 'Nb of unknowns'}
    _norm_disp: ClassVar[dict[str, str]] = {'L2': r"${L^2}$",
                                            'H1': r"${H^1}$"}

    def __init__(self, element: Element) -> None:
        asked_xaxis = element.get('xaxis')
        if asked_xaxis is None:
            raise TypeError("Need the 'xaxis' attribute")
        else:
            self.xaxis = asked_xaxis
        self.style = element.get('style', 'x')
        asked_norm = element.get('norms')
        if asked_norm is None:
            raise TypeError("Need the 'norms' attribute")
        else:
            if asked_norm == 'all':
                self.norms = ['L2', 'H1']
            else:
                self.norms = [asked_norm]
        self.show_labels = literal_eval(element.get('show_labels', 'True'))
        super().__init__(element)

    def _render(self, ax: Axes, *, results: DataArray,
                **discrete_data: Any) -> Any:
        """Render the error curve."""
        xval = results.coords[self.xaxis].values
        for norm in self.norms:
            yval = results.sel(norm=norm).values
            order = linregress(np.log(xval), np.log(yval)).slope
            if self.xaxis == 'dof':
                order = -2*order
            print(f'Norm {self._norm_disp[norm]} : order ' +
                  f'wrt to {self._axis_disp[self.xaxis]}: {order:1.2f}')
            lab = f"Order in {self._norm_disp[norm]}={order:1.2f}"
            plotobj = ax.loglog(xval, yval, self.style, label=lab, **self.param)
            if self.show_labels:
                ax.set_xlabel(self._axis_disp[self.xaxis])
                ax.set_ylabel('Error norm')
        ax.legend()
        return plotobj


class TimeSpaceErrorCurve(SpaceErrorCurve):
    """Error curve for an unsteady numerical scheme."""

    _axis_disp: ClassVar[dict[str, str]] = {'step': 'Mesh size',
                                            'dof': 'Nb of unknowns',
                                            'dt': 'Time step'}
    _norm_disp: ClassVar[dict[str, str]] = {'L2': r"${L^\infty_t(L^2_x)}$",
                                            'H1': r"${L^2_t(H^1_x)}$"}

    def __init__(self, element: Element, parameters: Element):
        cut_off = parameters.find('cutoff')
        if cut_off is None:
            self.cut_off_display = False
        else:
            self.cut_off_display = literal_eval(cut_off.get('display', 'True'))
            self.cut_off_style = cut_off.get('style', ':')
        self.other_type = parameters.get('type', 'values')
        param_text = parameters.text
        if param_text is not None:
            param_text = param_text.strip()
        if param_text:
            par_vals = literal_eval(param_text.strip())
            if hasattr(par_vals, '__contains__'):
                self.other_par = list(par_vals)
            else:
                self.other_par = [par_vals]
        else:
            self.other_par = []
        super().__init__(element)
        if self.xaxis != 'dt':
            self.other_name = 'dt'
        else:
            self.other_name = parameters.get('name', 'mesh')

    def _render(self, ax: Axes, *, results: DataArray, **discrete_data: Any
                ) -> Any:
        results = _filter_params(self.other_type, self.other_par, results,
                                 self.other_name)
        xval = results.coords[self.xaxis].values
        for norm in self.norms:
            for (par, val) in results.sel(norm=norm).groupby(self.other_name):
                yval = val.values.flatten()
                order = linregress(np.log(xval), np.log(yval)).slope
                if self.xaxis == 'dof':
                    order = -2*order
                print(f'Norm {self._norm_disp[norm]} : order ' +
                      f'wrt to {self._axis_disp[self.xaxis]}: {order:1.2f}' +
                      f' using parameter {self.other_name}={par}')
                lab = (f"Order in {self._norm_disp[norm]}={order:1.2f}, "
                       + f"{self.other_name}={par}")
                p = ax.loglog(xval, yval, self.style, label=lab, **self.param)
                if self.cut_off_display:
                    if self.xaxis != 'dt':
                        co_val = par
                    else:
                        co_val = results.coords['step'].sel(
                            {self.other_name: par}
                            ).values**2
                    ax.axvline(co_val, color=p[0].get_color(),
                               linestyle=self.cut_off_style)
                if self.show_labels:
                    ax.set_xlabel(self._axis_disp[self.xaxis])
                    ax.set_ylabel('Error norm')
        ax.legend()
# %% Axes
#    ====


class GridAxis:
    """Directives to create matplotlib.Axes programatically.

    Attributes
    ----------
    data_origin : str
        Name of the quantity being plotted.
    """

    def __init__(self, axis: Element, plots: Sequence[GenericPlot]) -> None:
        self.posx = literal_eval(axis.get('posx', '0'))
        self.posy = literal_eval(axis.get('posy', '0'))
        self.data_origin = axis.get('data_origin')
        self.display = literal_eval(axis.get('display', 'True'))
        self.param = {k: literal_eval(v) for k, v in axis.items()
                      if not hasattr(self, k) and k != 'type'}
        self.plots = plots

    def render(self, discrete_data: dict[str, Any],
               ax_arr: NDArray[np.object_]) -> Any:
        """Render all the plots in the axis."""
        plotobjs = []
        if self.display:
            ax = ax_arr[self.posy, self.posx]

            for plot in self.plots:
                if isinstance(plot, PlotOfMeshStructure):
                    plotobj = plot.render(ax, E=discrete_data['Mesh'])
                if isinstance(plot, PlotOnMesh):
                    plotobj = plot.render(ax, E=discrete_data['Mesh'],
                                          results=discrete_data['results'],
                                          data_origin=self.data_origin)
                if isinstance(plot, SpaceErrorCurve):
                    plotobj = plot.render(ax, results=discrete_data['results'])
                plotobjs.append(plotobj)
            ax.set(**self.param)
        return plotobjs


class TimedGridAxis(GridAxis):
    """Directives to create a matplotlib.Axes with time data."""

    def __init__(self, axis: Element, plots: Sequence[GenericPlot]):
        snaps = axis.get('snaps')
        if snaps is None:
            raise TypeError("Need the 'snaps' attribute")
        else:
            snaps = literal_eval(snaps)
        if hasattr(snaps, '__contains__'):
            self.snaps = list(snaps)
        else:
            self.snaps = [snaps]
        super().__init__(axis, plots)

    def render(self, discrete_data: dict[str, Any],
               ax_arr: NDArray[np.object_]) -> Any:
        """Render an axis in a figure."""
        if self.display:
            M: Mesh = discrete_data['Mesh']
            R: DataArray = discrete_data['results']
            nb_snaps = len(self.snaps)
            S = R.sel(t=self.snaps, method='nearest')
            match (self.posx, self.posy):
                case ('snaps', py) if isinstance(py, int):
                    ax_iter = ((j, py, S.isel(t=j))
                               for j in range(nb_snaps))
                case (px, 'snaps') if isinstance(px, int):
                    ax_iter = ((px, i, S.isel(t=i))
                               for i in range(nb_snaps))
                case (px, py) if isinstance(px, int) and isinstance(py, int):
                    ax_iter = [(px, py, S.isel(t=0))]
            for j, i, current_data in ax_iter:
                ax = ax_arr[i, j]
                for plot in self.plots:
                    if isinstance(plot, PlotOfMeshStructure):
                        plot.render(ax, E=M)
                    if isinstance(plot, PlotOnMesh):
                        plot.render(ax, E=M,
                                    results=current_data,
                                    data_origin=self.data_origin,
                                    extra_title=f"t={current_data.coords['t'].item()}")
                ax.set(**self.param)

# %% Figures
#    =======


class GenericFigure:
    """Common properties of all figures."""

    def __init__(self, figure: Element) -> None:
        self.display = literal_eval(figure.get('display', 'True'))
        figsize = figure.get('figsize', None)
        if figsize is not None:
            self.width, self.height = literal_eval(figsize)
        else:
            self.width = float(figure.get('width', _DEF_WIDTH_FIG))
            self.height = float(figure.get('height', _DEF_HEIGHT_FIG))
        self.nfig = figure.get('nfig', None)
        if self.nfig is not None:
            self.nfig = literal_eval(self.nfig)
        title = figure.find('title')
        if title is not None:
            self.title = title.text
            self.mesh_name = literal_eval(title.get('mesh_name', 'False'))
        else:
            self.title = None
            self.mesh_name = False
        asked_split = figure.get('split')
        self.split: None | Literal['block'] | float
        if asked_split is None:
            self.split = None
        elif asked_split == 'block':
            self.split = 'block'
        else:
            self.split = float(asked_split)
        clear = figure.get('clear')
        if clear is not None and not literal_eval(clear):
            warn("Figure cannot have clear='False'. Ignoring.")
        self.param = {k: literal_eval(v) for k, v in figure.items()
                      if not hasattr(self, k)}

    def _specific_render(self, fig: Figure,
                         discrete_data: dict[str, Any]) -> None:
        pass

    def render(self, discrete_data: dict[str, Any]) -> Any:
        """Render all the axes inside the Figure."""
        if self.display:
            fig = plt.figure(self.nfig, clear=True, **self.param)
            self._specific_render(fig, discrete_data)
            plt.show(block=False)
            if self.split is not None:
                if self.split == 'block':
                    input('Awaiting input before the next figure.')
                else:
                    plt.pause(self.split)


class ResultFigure(GenericFigure):
    """Directives to create matplotlib.Figure programmatically.

    Parameters
    ----------
    figure : xml.ElementTree.Element
        Description of the figure.
    axs : sequence of GridAxis
        Axes attached to the figure.

    Attributes
    ----------
    nfig : int or None
        Number of the figure.
    title : str or None
        Suptitle of the figure.
    nline, ncol : (int, int)
        Subplots grid shape.
    split : float or None or 'block'
        Duration of a pause between drawing of two figures. If
        `'block'`, user input will be asked before drawing the next
        figure.
    axs : sequence of GenericPlot
        Plots attached to the figure.
    param : dict[str, Any]
        Remaining parameters passed to subplots.
    """

    def __init__(self, figure: Element, axs: Sequence[GridAxis],
                 defm: int = 1,
                 defn: int = 1) -> None:
        self.nline = int(figure.get('nline', defm))
        self.ncol = int(figure.get('ncol', defn))
        subplots_param = figure.find('subplots_parameters')
        if subplots_param is None:
            self.subplots_kw = {}
        else:
            self.subplots_kw = {k: literal_eval(v)
                                for k, v in subplots_param.items()}
        super().__init__(figure)
        self.axs = axs

    def _specific_render(self, fig: Figure,
                         discrete_data: dict[str, Any]) -> None:
        """Render all the plots inside the Figure."""
        m, n = self.nline, self.ncol
        max_height = self.height
        max_width = self.width
        if m >= n:
            height = max_height
            width = n/m*height
        else:
            width = max_width
            height = m/n*width
        fig.set_size_inches(width, height)
        fig.set_layout_engine('constrained')
        ax_arr = fig.subplots(m, n, squeeze=False,
                              subplot_kw=self.subplots_kw)
        nf = fig.number
        if self.title is not None:
            suptitle = self.title
        else:
            suptitle = f"Figure {nf}"
        mesh_name = ''
        if self.mesh_name:
            E = discrete_data['Mesh']
            try:
                mesh_name = f' ({E.name})'
            except AttributeError:
                pass

        suptitle += mesh_name
        fig.suptitle(suptitle, fontsize=16)
        for axe in self.axs:
            axe.render(discrete_data, ax_arr)


class AnimationFigure(GenericFigure):
    """Directives to create a matplotlib.Animation programatically."""

    def __init__(self, figure: Element, anim: Element,
                 plots: Sequence[GenericPlot]):
        self.redraw_needed = []
        self.pcolor = None
        self.plot_of_mesh = None
        for plot in plots:
            if isinstance(plot, PlotOfPcolor):
                self.pcolor = plot
            elif isinstance(plot, PlotOfMeshStructure):
                self.plot_of_mesh = plot
            else:
                self.redraw_needed.append(plot)
        self.plots = plots
        self.data_origin = anim.get('data_origin', 'approx')
        self.varname = anim.get('varname', 'u')
        self.anim_kw = {k: literal_eval(v) for k, v in anim.items()
                        if k not in {'type', 'varname', 'data_origin'}}
        super().__init__(figure)

    def render(self, discrete_data: dict[str, Any]) -> FuncAnimation:
        """Display the animation."""
        M: Mesh = discrete_data['Mesh']
        R: DataArray = discrete_data['results']
        fig = plt.figure(self.nfig, clear=True, **self.param)
        ax = fig.add_subplot()
        plotobjs: list[Any] = []
        pcolor_plot = None
        data = R.isel(t=0)
        if self.pcolor is not None:
            pcolor_plot = self.pcolor.render(ax, E=M,
                                             data_origin=self.data_origin,
                                             results=data)
            submesh = self.pcolor.submesh
            varname = self.pcolor.varname
        if self.plot_of_mesh is not None:
            self.plot_of_mesh.render(ax, E=M)

        def update(t: float) -> list[Artist]:
            data = R.sel(t=t)
            if pcolor_plot is not None:
                fd = _prepare_plotting(
                    M,
                    PREDEFINED_MD[submesh],
                    data.sel(varname=varname,  # type: ignore
                             data_origin=self.data_origin).values)
                # Because of mypy Issue #2922 mypy does not recognize
                # an array as a subtype of Discretizable when
                # it is.
                pcolor_plot.set_array(fd)
                pcolor_plot.changed()
            for plotobj in plotobjs:
                plotobj.remove()
            plotobjs.clear()
            for plot in self.redraw_needed:
                plotobj = plot.render(ax, E=M, data_origin=self.data_origin,
                                      results=data)
                plotobjs.append(plotobj)
            fig.suptitle(f'{t=:.2}')
            return []
        ani = FuncAnimation(fig, update, R.coords['t'].values, **self.anim_kw)
        plt.show(block=True)
        return ani


# %% Public loader
#    =============

def _create_plots(axis: Element) -> list[GenericPlot]:
    plots: list[GenericPlot] = []
    for plot in axis.iterfind('plot'):
        plotfun = plot.get('type')
        if plotfun == 'pcolor':
            plots.append(PlotOfPcolor(plot))
        elif plotfun == 'plotmesh':
            plots.append(PlotOfMeshStructure(plot))
        elif plotfun == 'contour':
            plots.append(PlotOfContour(plot))
        elif plotfun == 'quiver':
            plots.append(PlotOfQuiver(plot))
    return plots


def load_output(filename: Path) -> tuple[list[GenericFigure],
                                         list[ResultFigure],
                                         dict[str, Any]]:
    """Describe how to render the results of a PDE simulation.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to the output file.

    Returns
    -------
    figures : list[GenericFigure]
        `GenericFigure` to be rendered during the computations. It will
        be either a `ResultFigure` or an `AnimationFigure`.
    error_figures : list[ResultFigure]
        `ResultFigure` to be rendered after all computations are done.
    error_data : dict[str, Any]
        Data to be collected during the computations to render the
        figures in `error_figures`. Keys are 'norms' and 'xaxis'.
        'norms' is the set of norms ('L2' or 'H1') to compute the error,
        'xaxis' is the set of mesh parameters to draw the error against
        ('dof' for number of degrees or freedom or 'step' for a
        characteristic length of the mesh).
    """
    out = parse_xml(filename)
    figures: list[GenericFigure] = []

    axis_types = out.find('axis_types')
    if axis_types is not None:
        axis_aliases = {ax_alias.get('name'): ax_alias
                        for ax_alias in axis_types.iterfind('axis')}
    else:
        axis_aliases = {}
    for figure in out.iterfind('figure'):
        m = 0
        n = 0
        axs = []
        anim = figure.find('animation')
        if anim is not None:
            axis_alias = anim.get('type', None)
            if axis_alias is None:
                plots = _create_plots(anim)
            else:
                plots = _create_plots(axis_aliases[axis_alias])
            figures.append(AnimationFigure(figure, anim, plots))
        else:
            for axis in figure.iterfind('axis'):
                axis_alias = axis.get('type', None)
                snaps = axis.get('snaps', None)
                if axis_alias is None:
                    plots = _create_plots(axis)
                else:
                    plots = _create_plots(axis_aliases[axis_alias])
                if snaps is None:
                    newaxis = GridAxis(axis, plots)
                    dm = newaxis.posy
                    dn = newaxis.posx
                else:
                    newaxis = TimedGridAxis(axis, plots)
                    if newaxis.posx == 'snaps':
                        dm = newaxis.posy
                        dn = len(newaxis.snaps)-1
                    elif newaxis.posy == 'snaps':
                        dm = len(newaxis.snaps)-1
                        dn = newaxis.posx
                    else:
                        dm = newaxis.posy
                        dn = newaxis.posx
                m = max(m, dm)
                n = max(n, dn)
                axs.append(newaxis)
            figures.append(ResultFigure(figure, axs, m+1, n+1))
    error_analysis = out.find('error_analysis')
    error_figures = []
    error_data_collection: dict[str, set[str]] = {'norms': set(),
                                                  'xaxis': set()}
    if error_analysis is not None:
        for figure in error_analysis.iterfind('figure'):
            axs = []
            m = 0
            n = 0
            for axis in figure.iterfind('axis'):
                plots = []
                for plot in axis.iterfind('plot'):
                    time_space_ec = plot.find('parameters')
                    if time_space_ec is None:
                        curve = SpaceErrorCurve(plot)
                    else:
                        curve = TimeSpaceErrorCurve(plot, time_space_ec)
                    error_data_collection['norms'].update(curve.norms)
                    error_data_collection['xaxis'].add(curve.xaxis)

                    plots.append(curve)
                newaxis = GridAxis(axis, plots)
                dm = newaxis.posy
                dn = newaxis.posx
                m = max(m, dm)
                n = max(n, dn)
                axs.append(newaxis)
            error_figures.append(ResultFigure(figure, axs, m+1, n+1))
    return figures, error_figures, error_data_collection

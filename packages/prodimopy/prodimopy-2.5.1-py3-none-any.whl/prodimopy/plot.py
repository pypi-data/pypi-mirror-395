import collections
import copy
import math
import warnings

import astropy.units as u
import astropy.constants as const
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy.typing import NDArray
from scipy.interpolate import interp1d

# for now use type_extensions to be compatible with python < 3.13
from typing_extensions import deprecated

import prodimopy.chemistry.network as pchem
import prodimopy.plot_models
import prodimopy.read as pread
import prodimopy.utils as putils


# has to be this way because of circular imports
class Plot(object):
    """
    Plot routines for a single |prodimo| model.
    """

    def __init__(
        self, pdf: PdfPages | None = None, fs_legend: int | None = None, title: str | None = None
    ):
        """
        Attributes
        ----------

        """
        self.pdf: PdfPages | None = pdf
        """ : A :class:`matplotlib.backends.backend_pdf.PdfPages` object for output as pdf, or `None`, for output on screen (notebook etc.). Default: `None` """
        self.fs_legend: int = mpl.rcParams["legend.fontsize"]
        """ : Default font size for the legend in a plot. If not set it is taken from the matplotlib rcParams."""
        if fs_legend is not None:
            self.fs_legend = fs_legend

        self.ncol_legend: int = 5
        """ : Maximum number of columns in the legend. Default: `5`"""
        self.title: str | None = title
        """ : A title for the plot (e.g. the name of the model). Default: `None` (no title) """
        # special colors, forgot the source for it :( somewhere from the internet)
        # FIXME: make an option to activate them
        self.pcolors: dict[str, str] = {
            "blue": "#5DA5DA",
            "orange": "#FAA43A",
            "green": "#60BD68",
            "pink": "#F17CB0",
            "brown": "#B2912F",
            "purple": "#B276B2",
            "yellow": "#DECF3F",
            "red": "#F15854",
            "gray": "#4D4D4D",
        }
        """ : Some nice colors."""

    def _getField2D(
        self, model: pread.Data_ProDiMo, fieldname: str, label: str = "value", log=True
    ) -> tuple[np.ndarray, str, float]:
        """
        Returns quantity with name ``fieldname`` from model.

        Parameters
        ----------

        model : The model to get the field from.

        fieldname : The name of the field to get.

        label : The label to use for the field.

        log : Include log in label or not.

        Returns
        -------

        values : The values of the field from the model.
        label : The label for the field
        zmin : The default value for ``zmin`` to be used e.g. in :func:`~prodimopy.plot.Plot.plot_cont`

        """
        tmpvalues = getattr(model, fieldname, None)
        if tmpvalues is None:
            raise ValueError("ERROR: plot_cont: field %s not found in model" % fieldname)
        # in those cases map the label and zmin

        lab, zmin = self._mapField(fieldname, log)
        if label == "value" or label is None:
            label = lab

        return tmpvalues, label, zmin

    def _mapField(self, fieldname, log=True):
        """
        Maps a field/attribute name from :class:`~prodimopy.read.Data_ProDiMo` to a nice label for the plotting.
        Please not the labels do not include mathrm or similar things. It is recommended to use a matplotlib style file for this.
        E.g. `mathtext.default : regular` or simply use the prodimopy style file.

        Parameters
        ----------

        fieldname : str
          The field name of a quantity in :class:`~prodimopy.read.Data_ProDiMo`.

        log : boolean
          If `True` the label is prepended with `log`. Default: `True`


        Returns
        -------

        str : The label for the field, or the passed fieldname if no mapping is found.
        float : The default min value for the contour plot

        """

        fmap = {
            "AV": (r"$A_\mathrm{V}$", 1.0e-4),
            "AVrad": (r"$A_\mathrm{V,rad}$", 1.0e-5),
            "AVver": (r"$A_\mathrm{V,ver}$", 1.0e-5),
            "Hx": (r"$H_\mathrm{X}\,erg\,{\langle H \rangle}^{-1}]$", 1.0e-32),
            "nHtot": (r"$n_{\langle H \rangle}\,[cm^{-3}]$", 3.0e2),
            "nd": (r"$n_{dust}\,[cm^{-3}]$", 1.0e-10),
            "pressure": (r"$P\,[erg\,cm^{-3}]$", 1.0e-10),
            "rateH2form": (r"$H_2\,form.\,rate\,[s^{-1}]$", 1.0e-15),
            "sdg": (r"$\Sigma_{gas}\,[g\,cm^{-2}]$", 1.0e-10),
            "sdd": (r"$\Sigma_{dust}\,[g\,cm^{-2}]$", 1.0e-12),
            "tg": (r"$T_{gas}\,[K]$", 10),
            "td": (r"$T_{dust}\,[K]$", 10),
            "rhog": (r"$\rho_{gas}\,[g\,cm^{-3}]$", 1.0e-20),
            "rhod": (r"$\rho_{dust}\,[g\,cm^{-3}]$", 1.0e-22),
            "d2g": (r"d/g ratio", 3.0e-6),
            "NHrad": (r"$N_{\langle H \rangle,rad}\,[cm^{-2}]$", 1.0e19),
            "NHver": (r"$N_{\langle H \rangle,ver}\,[cm^{-2}]$", 1.0e19),
            "chi": (r"$\chi\,[Draine\,field]$", 1.0e-6),
            "chiRT": (r"$\chi_\mathrm{RT}\,[Draine\,field]$", 1.0e-6),
            "tauchem": (r"$\tau_{chem}\,[yr]$", 1.0e-2),
            "taucool": (r"$\tau_{cool}\,[yr]$", 1.0e-2),
            "taudiff": (r"$\tau_{diff,vert}\,[yr]$", 1.0e-2),
            "soundspeed": (r"$c_s\,[km\,s^{-1}]$", 1.0e-3),
            "zetaX": (r"$\zeta_{X}\,per\,H\,[s^{-1}]$", 1.0e-21),
            "zetaCR": (r"$\zeta_{CR}\,per\,H_2\,[s^{-1}]$", 1.0e-21),
            "zetaSTCR": (r"$\zeta_{SP}\,per\,H_2\,[s^{-1}]$", 1.0e-21),
            "tauX1": (r"$\tau_{X,1keV}$", 1.0e-5),
            "tauX5": (r"$\tau_{X,5keV}$", 1.0e-5),
            "tauX10": (r"$\tau_{X,10keV}$", 1.0e-5),
            "damean": (r"$\langle a \rangle_\mathrm{grain}\,[\mu m]$", 1.0e-3),
            "da2mean": (r"$\langle a^2\rangle_\mathrm{grain}\,[\mu m]$", 1.0e-4),
            "kappaRoss": (r"$\kappa_{Ross}\,[cm^{-1}]$", 1.0e-21),
            "isoratio_12CO13CO": (r"$^{12}CO/^{13}CO isotop. ratio", 1.0e-3),
            "velocity_xz": (r"$\sqrt{{v_x}^2+{v_z}^2}$ [km/s]", 0),
        }

        if fieldname in fmap:
            label, zmin = fmap[fieldname]
            if log:
                label = r"$\log\,$" + label
        else:
            label = fieldname
            zmin = None

        return label, zmin

    def _legend(self, ax, **kwargs):
        """
        plots the legend, deals with multiple columns
        """
        handles, labels = ax.get_legend_handles_labels()

        if "loc_legend" in kwargs:
            loc = kwargs["loc_legend"]
        else:
            loc = "best"

        if len(labels) > 0:
            ncol = 1
            if self.ncol_legend > 1 and len(labels) > self.ncol_legend:
                ncol = int(len(labels) / self.ncol_legend)

            leg = ax.legend(
                handles, labels, loc=loc, fancybox=False, ncol=ncol, fontsize=self.fs_legend
            )
            lw = mpl.rcParams["axes.linewidth"]
            leg.get_frame().set_linewidth(lw)

    def _dokwargs(self, ax, **kwargs):
        """
        Handles the passed kwargs elements (assumes that defaults are already set)
        TODO: make this a general function ....
        """
        if "ylim" in kwargs:
            ax.set_ylim(kwargs["ylim"])

        if "xlim" in kwargs:
            ax.set_xlim(kwargs["xlim"])

        if "xlog" in kwargs:
            if kwargs["xlog"]:
                ax.semilogx()
            else:
                ax.set_xscale("linear")

        if "ylog" in kwargs:
            if kwargs["ylog"]:
                ax.semilogy()
            else:
                ax.set_yscale("linear")

        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"])

        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"])

        if self.title is not None and ("notitle" not in kwargs):
            if self.title.strip() != "":
                ax.set_title(self.title.strip())

        if "title" in kwargs:
            if kwargs["title"] is not None and kwargs["title"].strip() != "":
                ax.set_title(kwargs["title"].strip())
            else:
                ax.set_title("")

    def _initfig(
        self, ax: mpl.axes.Axes = None, **kwargs
    ) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
        """
        Inits Figure and Axes object.

        If an Axes object is passed, it is returned together with the Figure object.

        This is for a single plot (i.e. only one panel).

        Returns
        -------

        The figure and axes object.

        """

        if ax is not None:
            fig = ax.get_figure()

        else:
            fig, ax = plt.subplots(1, 1, figsize=self._sfigs(**kwargs))

        return fig, ax

    def _closefig(self, fig):
        """
        Save and close the plot (Figure).

        If self.pdf is None than nothing is done and the figure is returned.
        The transparent keyword is set to false in `savefig`.

        ..todo::
          * check why transparent need to be false (maybe performance).

        """
        if self.pdf is not None:
            self.pdf.savefig(figure=fig, transparent=False)
            plt.close(fig)
            return None
        else:
            return fig

    def _sfigs(self, **kwargs):
        """
        Scale the figure size from matplotlibrc by the factors given in the
        array sfigs (in kwargs) the first element is for the width the second for
        the height
        """
        if "sfigs" in kwargs:
            fac = kwargs["sfigs"]
            return scale_figs(fac)
        else:
            return scale_figs([1.0, 1.0])

    def _contourf_fix_white_lines(self, CS):
        """
        This is for fixing the white lines between the contour levels, in pdf output
        to be backward compatible with older matplotlib versions catch a possible attribute error.

        .. todo::
          * remove that at some point, but it seems the white lines are still there in matplotlib 3.10

        """
        try:
            CS.set(edgecolors="face")
        except AttributeError:
            for c in CS.collections:
                c.set_edgecolor("face")

    def plot_grid(self, model, zr=False, ax=None, **kwargs):
        """
        Plots the spatial grid.

        Also all the standard parameter like xlim, ylim etc. can be used.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        zr : boolean
          show the height z as z/r (scaled by the radius)

        """

        print("PLOT: plot_grid ...")

        fig, ax = self._initfig(ax)
        y = model.z
        if zr:
            y = model.z / model.x

        ax.plot(model.x, y, marker="s", ms=0.03, linestyle="None", color=self.pcolors["gray"])

        if "axequal" in kwargs:
            if kwargs["axequal"]:
                ax.axis("equal")
                ax.set_aspect("equal", adjustable="box")

        if not zr:
            ax.semilogy()

        ax.semilogx()
        self._dokwargs(ax, **kwargs)

        ax.set_xlabel("r [au]")
        if zr:
            ax.set_ylabel("z/r")
        else:
            ax.set_ylabel("z [au]")

        return self._closefig(fig)

    def plot_NH(self, model, sdscale=False, muH=None, marker=None, ax=None, **kwargs):
        """
        Plots the total vertical hydrogen column number density
        as a function of radius.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        sdscale : boolean
          show additionally a scale with units in |gcm^-2|


        Returns
        -------
        :class:`~matplotlib.figure.Figure` or `None`
          object if `self.pdf` is `None` the Figure object is returned, otherwise
          otherwise the plot is written directly into the pdf object(file) and
          `None` is returned.
        """
        print("PLOT: plot_NH ...")
        fig, ax = self._initfig(ax, **kwargs)

        if muH is None:
            muH = model.muH

        x = model.x[:, 0]
        y = model.NHver[:, 0]
        ax.plot(x, y, marker=marker, ms=3.0, color="black")

        ax.set_xlim(min(x), max(x))

        ax.semilogy()
        ax.semilogx()

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(r"N$_\mathrm{\langle H \rangle,ver}\,\mathrm{[cm^{-2}]}$")

        self._dokwargs(ax, **kwargs)
        self._legend(ax)

        # second sale on the right
        if sdscale:
            ax2 = ax.twinx()
            y = model.NHver[:, 0] * muH
            # just plot it again, is the easiest way (needs to be the same style etc)
            ax2.plot(x, y, color="black")
            ax2.set_ylabel(r"$\Sigma\,\mathrm{[g\,cm^{-2}]}$")
            # FIXME: does not allow to manually set xlim
            #        need to check if that works with the two scales
            ax2.set_xlim(min(x), max(x))

            # this needs to be done to get the correct scale
            ylim = np.array(ax.get_ylim()) * muH
            ax2.set_ylim(ylim)
            # FIXME: check if this is required!
            ax2.semilogy()

        # ax.yaxis.tick_right()
        # ax.yaxis.set_label_position("right")
        # ax.yaxis.set_ticks_position('both')

        return self._closefig(fig)

    def plot_cont_dion(self, model, zr=True, oconts=None, ax=None, **kwargs):
        """
        Plots the regions where either X-rays, CR or SP are the dominant H2 ionization source.

        .. todo::
          * not really general, should be more flexible (i.e. colors)
          * requires better documentation to make it more general
        """
        values = model.zetaX[:, :] * 0.0
        values[:, :] = np.nan
        values[model.zetaX * 2.0 > (model.zetaCR + model.zetaSTCR)] = 1.0
        values[model.zetaSTCR > (model.zetaCR + model.zetaX * 2.0)] = 0.0
        values[model.zetaCR > (model.zetaSTCR + model.zetaX * 2.0)] = -1.0
        # print(values)

        print("PLOT: plot_cont_dion ...")
        cX = "#F15854"
        cSP = "#5DA5DA"
        cCR = "#4D4D4D"

        x = model.x
        if zr:
            y = model.z / model.x
        else:
            y = np.copy(model.z)
            y[:, 0] = y[:, 0] + 0.05

        # levels=[1.5,0.5,0.0,-0.5,-1.5]
        # levels=MaxNLocator(nbins=4, prune="both").tick_values(-1.0,1.0)
        levels = [-1.2, -0.01, 0.0, 0.01, 1.2]
        ticks = [0.5, 0.0, -0.5]

        # ticks =
        # print(ticks)

        # sclae the figure size if necessary
        # TODO: maybe provide a routine for this, including scaling the figure size
        fig, ax = self._initfig(ax, **kwargs)

        # stupid trick to plot the masked areas
        # plot everything with one color, and than overplot the other stuff.
        valinv = model.zetaX[:, :] * 0.0
        valinv[:, :] = 10
        # valinv[valinv != 10.0]=np.nan
        CS2 = ax.contourf(
            x, y, valinv, levels=[9.0, 10.0, 11.0], colors="0.6", hatches=["////", "////", "////"]
        )

        self._contourf_fix_white_lines(CS2)

        CS = ax.contourf(x, y, values, levels=levels, colors=(cCR, cSP, cSP, cX))
        self._contourf_fix_white_lines(CS2)

        ax.set_ylim([y.min(), y.max()])
        ax.set_xlim([x.min(), x.max()])
        ax.semilogx()

        ax.set_xlabel("r [au]")
        if zr:
            ax.set_ylabel("z/r")
        else:
            ax.set_ylabel("z [au]")

        self._dokwargs(ax, **kwargs)

        if oconts is not None:
            for cont in oconts:
                if cont.filled is True:
                    ax.contourf(
                        x,
                        y,
                        cont.field,
                        levels=cont.levels,
                        colors=cont.colors,
                        linestyles=cont.linestyles,
                        linewidths=cont.linewidths,
                    )
                else:
                    ax.contour(
                        x,
                        y,
                        cont.field,
                        levels=cont.levels,
                        colors=cont.colors,
                        linestyles=cont.linestyles,
                        linewidths=cont.linewidths,
                    )

        CB = fig.colorbar(CS, ax=ax, ticks=ticks, pad=0.01)
        CB.ax.set_yticklabels(["X", "SP", "CR"])
        CB.ax.tick_params(labelsize=self.fs_legend)

        # CB.set_ticks(ticks)
        CB.set_label("dominant ionization source", fontsize=self.fs_legend)

        return self._closefig(fig)

    def plot_cont(
        self,
        model,
        values,
        label="value",
        zlog=True,
        grid=False,
        zlim=[None, None],
        zr=True,
        cmap=None,
        clevels=None,
        clabels=None,
        contour=True,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        showcb=True,
        cb_format="%.1f",
        scalexy=[1, 1],
        patches=None,
        rasterized=False,
        returnFig=False,
        fig=None,
        ax=None,
        movie=False,
        **kwargs,
    ):
        """
        Plot routine for 2D filled contour plots.

        If an `ax` object is passed to this routine, it is use
        use to do the plotting. This is especially useful if you want to use that
        routine together with subplots (e.g. a grid of plots). See for example
        :func:`~prodimopy.plot.Plot.plot_abuncont_grid`.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        values : array_like(float,ndim=2) or str
          a 2D array with numeric values for the plotting. E.g. any 2D array
          of the :class:`~prodimopy.read.Data_ProDiMo` object.
          If a string is passed, it is assumed to be the name of an attribute
          and the corresponding array is used. E.g. Passed value is "tg" -> the array used will be `model.tg`.

        label : str
          The label for the colorbar (color scale). Default: `value`
          Should be the quantity and unit of the field that is shown.

        zlog : boolean
          Using log scaling for the values. Default: True

        grid : boolean
          Use the grid (ix,iz) as spatial coordinates. Default: False

        zlim : array_like(float,ndim=2)
          The minimum and maximum values for the color scale. Default: `[None,None]`

        zr : boolean
          Use z/r as the spatial coordinate for the y-axis. Default: `True`

        cmap : str or :class:`matplotlib.colors.Colormap`
          this is simply passed on to the `contourf` routine of matplotlib
          see :func:`matplotlib.pyplot.contourf` for detail

        clevels : array_like(float,ndim=1)
          The contour levels to plot. Default: `None`
          This will also set the labels shown in the colour bar.
          If `None` the levels are determined by the `MaxNLocator` routine and will be 6.

        clabels : array_like(str,ndim=1)
          Overwrite the labels for the colorbar. Default: `None`

        contour : boolean
          Show contour lines for the `clevels`. Default: `True`

        extend : str
          The extend of the colorbar. Default: `neither` (see :func:`matplotlib.pyplot.colorbar`)

        oconts : array_like(:class:`~prodimopy.plot.Contour`,ndim=1)
          list of :class:`~prodimopy.plot.Contour` objects which will be drawn
          as additional contour levels. See also the example at the top of the page.

        nbins : int
          The number of bins for the color scale. Default: 70

        bgcolor : str
          The background color of the plot. Default: `None`
          Can be useful to set the background color in the plot to `black` for example.

        showcb : boolean
          Show the colorbar or not. Default: `True`

        cb_format : str
          The format string for the colorbar labels. Default: `%.1f`

        scalexy : array_like(float,ndim=1)
          A scaling factor (multiplicative) for the x and y coordinates. Default: `[1,1]`
          W.g. plot in 1000 of au instead of au.

        ax : :class:`matplotlib.axes.Axes`
          a matplotlib axis object which will be used for plotting

        patches : array_like(:class:`matplotlib.patches.Patch`,ndim=1)
          a list of patches objects. For each object in the list, simply ax.add_patch() is called (at the very end of the routine)

        movie : boolean
          Special mode for movies ...


        .. todo::

           * Option for passing a norm (:class:`matplotlib.colors.LogNorm`). But that does not work nicely with contourf and colorbars ... works with imshow and pcolormesh though ... maybe switch to pcolormesh.

        """
        if "nolog" not in kwargs:
            print("PLOT: plot_cont ...")

        # if values is a string try to get the attribute from the model
        if type(values) is str:
            values, label, zmindef = self._getField2D(model, values, label, zlog)
        else:
            zmindef = None

        # prepare the data values and the limits
        if zlog is True:
            pvals = plog(values)
            values[np.isnan(values)] = 0.0
            maxval = np.log10(values.max())
            minval = np.log10(values[values > 0.0].min())
            if zmindef is not None and zmindef > values[values > 0.0].min():
                minval = np.log10(zmindef)
                if extend == "neither":
                    extend = "min"

            if zlim[1] is not None:
                maxval = np.log10(zlim[1])
            if zlim[0] is not None:
                minval = np.log10(zlim[0])
        else:
            pvals = values
            maxval = values.max()
            minval = values.min()
            if zmindef is not None and zmindef > minval:
                minval = zmindef
                if extend == "neither":
                    extend = "min"

            if zlim[1] is not None:
                maxval = zlim[1]
            if zlim[0] is not None:
                minval = zlim[0]

        levels = MaxNLocator(nbins=nbins).tick_values(maxval, minval)

        # if this is true it is assumed that we are in a multiple subplot environment
        # in that case we try a different way to place the colorbar
        if clevels is not None:
            if zlog:
                clevels = np.log10(clevels)
            ticks = clevels
        else:
            ticks = MaxNLocator(nbins=6, prune="both").tick_values(minval, maxval)

        # TODO: maybe provide a routine for this, including scaling the figure size
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=self._sfigs(**kwargs))
        else:
            fig = ax.get_figure()
            returnFig = True

        # prepare the spatial coordinates
        if grid:
            x = model.x[:, :] * 0.0
            y = model.z[:, :] * 0.0
            zr = False

            x = None
            y = None
            ax.set_ylabel("iz ")
            ax.set_xlabel("ir")
            kwargs["xlog"] = False
            kwargs["zlog"] = False
            kwargs["axequal"] = True
        elif zr:
            x = model.x * scalexy[0]
            y = model.z / model.x
            ax.set_ylabel("z/r")
            ax.set_xlabel("r [au]")
        else:
            x = model.x * scalexy[0]
            y = np.copy(model.z) * scalexy[1]
            # if one wants log scale on the y axis (height) avoid problems with
            # z=0.0 in thee prodimo grid.
            if "ylog" in kwargs and kwargs["ylog"]:
                y[:, 0] = y[:, 0] + np.min(y[:, 1]) * scalexy[1]
            ax.set_ylabel("z [au]")
            ax.set_xlabel("r [au]")

        # zorder is needed in case if rasterized is true

        if grid:
            CS = ax.contourf(
                pvals.T,
                levels=levels,
                extend=extend,
                zorder=-20,
                extent=(-0.5, model.nx - 0.5, 0.0, model.nz - 1.0),
                cmap=cmap,
            )
        else:
            CS = ax.contourf(
                x, y, pvals, levels=levels, extend=extend, zorder=-20, origin="image", cmap=cmap
            )

        self._contourf_fix_white_lines(CS)

        # rasterize the filled contours only, text ect. not
        if rasterized:
            ax.set_rasterization_zorder(-19)

        # axis equal needs to be done here already ... at least it seems so
        if "axequal" in kwargs:
            if kwargs["axequal"]:
                ax.axis("equal")
                # this seesm to adapt the figure size
                ax.set_aspect("equal", adjustable="box")

        if not grid:
            ax.set_ylim([y.min(), y.max()])
            ax.set_xlim([x.min(), x.max()])
            # under certain circumstances semilogx can cause problems if later on
            # the scale is changed again. So check if the user actually wants to change it
            if "xlog" not in kwargs:
                ax.semilogx()

            # ax.text(0.27, 0.95,kwargs["title"], horizontalalignment='center',
            #   verticalalignment='center',fontsize=8,
            #   transform=ax.transAxes)

        self._dokwargs(ax, **kwargs)

        if contour:
            if clevels is not None:
                # if zlog: clevels=np.log10(clevels)
                # ticks=clevels
                ax.contour(CS, levels=clevels, colors="white", linestyles="--", linewidths=1.0)
            else:
                ax.contour(CS, levels=ticks, colors="white", linestyles="--", linewidths=1.0)

        if oconts is not None:
            for cont in oconts:
                if grid:
                    ACS = ax.contour(
                        cont.field.T,
                        levels=cont.levels,
                        extent=(-0.5, model.nx - 0.5, 0.0, model.nz - 1.0),
                        colors=cont.colors,
                        linestyles=cont.linestyles,
                        linewidths=cont.linewidths,
                    )
                else:
                    if cont.filled is True:
                        ACS = ax.contourf(
                            x,
                            y,
                            cont.field,
                            levels=cont.levels,
                            colors=cont.colors,
                            linestyles=cont.linestyles,
                            linewidths=cont.linewidths,
                        )
                    else:
                        ACS = ax.contour(
                            x,
                            y,
                            cont.field,
                            levels=cont.levels,
                            colors=cont.colors,
                            linestyles=cont.linestyles,
                            linewidths=cont.linewidths,
                        )
                if cont.showlabels:
                    ax.clabel(
                        ACS,
                        inline=True,
                        inline_spacing=cont.label_inline_spacing,
                        fmt=cont.label_fmt,
                        manual=cont.label_locations,
                        fontsize=cont.label_fontsize,
                    )

        if bgcolor is not None:
            ax.set_axis_bgcolor(bgcolor)

        # Axes divider seems to work much better with multiple subplots
        # but not so well with single plots
        if showcb:
            if len(fig.axes) > 1:
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="4%", pad=0.025)
                CB = fig.colorbar(CS, cax=cax, ticks=ticks, format=cb_format, label=label)

            else:  # for just one axis, this works fine
                CB = fig.colorbar(CS, ax=ax, ticks=ticks, format=cb_format, pad=0.01, label=label)

            # FIXME: this is not very flexible and confusing
            if clabels is not None:
                CB.ax.set_yticklabels(clabels)
            # CB.ax.tick_params(labelsize=self.fs_legend)
            # CB.set_ticks(ticks)

        if patches is not None:
            for patch in patches:
                ax.add_patch(patch)

        if movie:
            return fig, CS

        if returnFig:
            return fig
        else:
            return self._closefig(fig)

    def streamplot_overlay(
        self,
        model: pread.Data_ProDiMo,
        axes: mpl.axes.Axes,
        resolution: float = 0.1,
        use_axlim: bool = True,
        streamprops: dict = {},
    ):
        """
        Creates a streamplot using the plt.streamplot routine from for the vx and vz velocity components of the model.
        Is plotted on top of the passed axes object (e.g. from a contour plot).
        Please note for a "normal" |prodimo| model the vx and vz components are zero and so nothing will be plotted.

        Parameters
        ----------

        model :
            The |prodimo| model data.

        axes :
            The axes object on which the streamplot should be plotted.

        resolution :
          The resolution of the regular grid on which the velocity components are interpolated. Unit: `au`.

        use_axlim :
            If `True` the current axis limits are used to define the grid for the streamplot. So the streamlines are
            only calculated for the visible part. Please note if the axis limits are changed later on, the streamplot will not be updated!
            If `False` the full model grid is used (old behaviour).

        streamprops :
            A dictionary with properties for the streamplot. This is passed on to the :meth:`matplotlib.axes.Axes.streamplot`.
            By default only a few properties of the streamplot are initialised. But most likely those need to be adapted.

        """
        from scipy.interpolate import griddata

        defstreamprops = {"color": "k", "density": 3, "linewidth": 0.4, "arrowsize": 0.5}
        defstreamprops["maxlength"] = np.max(axes.get_ylim()) / 3

        for key in streamprops.keys():
            defstreamprops[key] = streamprops[key]

        if use_axlim:
            rmin = axes.get_xlim()[0]
            rmax = axes.get_xlim()[1]
            zmax = axes.get_ylim()[1]
            rmax = np.max([rmax, zmax])  # always square at the moment

        else:
            rmin = model.x[0, 0]
            rmax = model.x[-1, 0]
            zmax = model.z[-1, -1]
            rmax = np.min([rmax, zmax])  # always square at the moment

        [xC, zC] = np.meshgrid(
            np.arange(rmin, rmax, resolution), np.arange(0, rmax, resolution), indexing="ij"
        )

        points = np.array([model.x.flatten(), model.z.flatten()]).T
        vxC = griddata(points, model.velocity[:, :, 0].flatten(), (xC, zC), method="linear")
        vzC = griddata(points, model.velocity[:, :, 2].flatten(), (xC, zC), method="linear")

        axes.streamplot(xC[:, 0], zC[0, :], vxC.T, vzC.T, **defstreamprops)

    def plot_abuncont(
        self,
        model,
        species="O",
        rel2H=True,
        label=None,
        zlog=True,
        zlim=[None, None],
        zr=True,
        cmap=None,
        clevels=None,
        clabels=None,
        contour=True,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        cb_format="%.1f",
        showcb=True,
        scalexy=[1, 1],
        patches=None,
        rasterized=False,
        ax=None,
        movie=False,
        **kwargs,
    ):
        """
        Plots the 2D abundance structure of a species.

        This is a convenience function and is simply a wrapper for
        :func:`~prodimopy.plot.Plot.plot_cont` routine.

        The routine checks if the species exists, calculates the abundance and sets some
        defaults (e.g. label) for the :func:`~prodimopy.plot.Plot.plot_cont` routine and calls it.
        However, all the defaults can be overwritten by providing the corresponding parameter.

        Contributors: L. Klarmann, Ch. Rab

        .. todo::
          * can be improved with better and smarter default values (e.g. for the colorbar)


        Parameters
        ----------

        model : :class:`prodimopy.read.Data_ProDiMo`
          the model data

        species : str
          the name of the species as given in |prodimo|

        rel2H : boolean
          plot abundances relative to the total H nuclei number density.
          If `False` the number density of the species is plotted

        label : str
          the label for the colorbar. If None the default is plotted


        For all other parameters see :func:`~prodimopy.plot.Plot.plot_cont`

        """
        print("PLOT: plot_abuncont ...")

        values, labelN, zlogN, zlimN, extendN = self._prepareAbunForPlot(
            model, species, label, rel2H, zlog, zlim, extend
        )

        return self.plot_cont(
            model,
            values,
            label=labelN,
            zlog=zlogN,
            zlim=zlimN,
            zr=zr,
            cmap=cmap,
            clevels=clevels,
            clabels=clabels,
            contour=contour,
            extend=extendN,
            oconts=oconts,
            nbins=nbins,
            bgcolor=bgcolor,
            cb_format=cb_format,
            showcb=showcb,
            scalexy=scalexy,
            patches=patches,
            rasterized=rasterized,
            nolog=True,
            ax=ax,
            movie=movie,
            **kwargs,
        )

    def plot_abuncont_grid(
        self,
        model,
        speciesList=["e-", "H2", "CO", "H2O"],
        nrows=2,
        ncols=2,
        rel2H=True,
        label=None,
        zlog=True,
        zlim=[None, None],
        zr=True,
        cmap=None,
        clevels=None,
        clabels=None,
        contour=True,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        cb_format="%.1f",
        scalexy=[1, 1],
        patches=None,
        rasterized=False,
        **kwargs,
    ):
        """
        Convenience routine to plot a grid of abundance plots in the same way as
        :func:`~prodimopy.plot.Plot.plot_abuncont`.

        The number of plots is given by `nrows` times `ncols` and should be equal to
        the number of species in `speciesList`

        Parameters
        ----------

        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        speciesList : array_like(str,ndim=1) :
          a list of species names that should be plotted. The plots will be made
          in order of that list, starting from top left to the bottom right of the grid.

        nrows : int
          how many rows should the subplots grid have.

        ncols : in
          how many columns should teh subplots grid have.

        zlim : array_like
          can either be of the form [zmin,zmax] ore a list of such entries ([zmin1,zmax1],[zmin1,zmax1], ....).
          For the latter the number of entries must be equal to the number of species.


        For the other parameters see :func:`~prodimopy.plot.Plot.plot_abuncont`

        """

        print("PLOT: plot_abuncont_grid ...")

        fig, axes = plt.subplots(nrows, ncols, figsize=scale_figs([ncols, nrows]))

        if zlim is None:
            zlims = [(None, None)] * len(speciesList)
        elif len(np.shape(zlim)) == 1:
            print(zlim)
            zlims = [zlim] * len(speciesList)
        else:
            zlims = zlim

        iax = 0
        for species, zliml in zip(speciesList, zlims):
            if species not in model.spnames:
                print("ERROR: Species " + species + " dose not exist in model.")
                iax = iax + 1
                continue

            values, labelG, zlogG, zlimG, extendG = self._prepareAbunForPlot(
                model, species, label, rel2H, zlog, zliml, extend
            )

            self.plot_cont(
                model,
                values,
                label=labelG,
                zlog=zlogG,
                zlim=zlimG,
                zr=zr,
                cmap=cmap,
                clevels=clevels,
                clabels=clabels,
                contour=contour,
                extend=extendG,
                oconts=oconts,
                nbins=nbins,
                bgcolor=bgcolor,
                cb_format=cb_format,
                scalexy=scalexy,
                patches=patches,
                rasterized=rasterized,
                fig=fig,
                ax=axes.flatten()[iax],
                nolog=True,
                **kwargs,
            )

            iax = iax + 1

        fig.tight_layout()

        return self._closefig(fig)

    def plot_reaccont(
        self,
        model,
        chemana,
        rtype,
        level=1,
        showAbun=False,
        values=None,
        label=None,
        cmap=None,
        zlog=True,
        zlim=[None, None],
        clevels=None,
        clabels=None,
        contour=True,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        cb_format="%.1f",
        patches=None,
        rasterized=True,
        ax=None,
        **kwargs,
    ):
        """
        Make a contour plot with the reactions numbers from chemistry analysis on top.
        As spatial coordinates the indices of the spatial grid are used.

        This is a convenience function and is simply a wrapper for
        :func:`~prodimopy.plot.Plot.plot_cont` routine.

        The same can be achieved by simply using plot_cont and plot the numbers
        on top (see last part of this routine). Then one has more flexibility.

        Parameters
        ----------

        model : :class:`prodimopy.read.Data_ProDiMo`
          the model data

        chemana : class:`prodimopy.read.Chemistry`
          data resulting from `prodimopy.read.analyse_chemistry` on a single species

        rtype : str
          keyword which sets the type of reactions to be shown (destruction or formation)
          must be set to either 'd' (destruction) or 'f' (formation)

        level : int
          1 means most important, 2 second most important etc.

        showAbun : boolean
          Show the abundances of the species that is analysed as filled contours.

        values : array_like(float,ndim=2)
          a 2D array with numeric values for the plotting like in :func:`~prodimopy.plot.Plot.plot_cont`.
          However, it an also be `None` (default) in that case the total formation/destruction rate is plotted.

        sfigs : array_like(float,ndim=2)
          Is part of kwargs. But this one is relevant here as one might need to make
          the figure larger to see the reaction numbers. e.g. just pass `sfigs=[2.,2.]`
        """

        if showAbun:
            values = model.getAbun(chemana.species)
            label = r"$\epsilon(" + spnToLatex(chemana.species) + "$)"
            if zlog:
                label = "log " + label

        if rtype is None or rtype != "d":
            rtype = "f"

        reacs = chemana.get_reac_grid(level, rtype)

        rlabel = "form."
        if rtype == "d":
            rlabel = "dest."

        if values is None:
            if rtype == "d":
                values = chemana.totdrate
            else:
                values = chemana.totdrate

            label = r"(total " + rlabel + " rate) $[cm^{-3} s^{-1}]$"
            if zlog:
                label = "log " + label

        if "title" not in kwargs:
            if level == 1:
                tit = "main " + rlabel + " reactions"
            else:
                tit = str(level).strip() + r"$^{nd}$ " + rlabel + " reactions"

            kwargs["title"] = tit

        fig = self.plot_cont(
            model,
            values,
            label=label,
            zlog=zlog,
            grid=True,
            zlim=zlim,
            zr=False,
            cmap=cmap,
            clevels=clevels,
            clabels=clabels,
            contour=contour,
            extend=extend,
            oconts=oconts,
            acont=None,
            acontl=None,
            nbins=nbins,
            bgcolor=bgcolor,
            cb_format=cb_format,
            scalexy=[1.0, 1.0],
            patches=patches,
            rasterized=rasterized,
            nolog=True,
            ax=ax,
            movie=False,
            returnFig=True,
            **kwargs,
        )

        # this is potentially very slow
        xstart = 0
        xend = model.nx
        ystart = 0
        yend = model.nz - 1
        if "xlim" in kwargs:
            if kwargs["xlim"][0] is not None:
                xstart = kwargs["xlim"][0]

            if kwargs["xlim"][1] is not None:
                xend = kwargs["xlim"][1]

        if "ylim" in kwargs:
            if kwargs["ylim"][0] is not None:
                ystart = kwargs["ylim"][0]

            if kwargs["ylim"][1] is not None:
                yend = kwargs["ylim"][1]

        for i in range(xstart, xend, 1):
            for j in range(ystart, yend, 1):
                if ax is None:
                    ax = fig.axes[0]
                ax.text(
                    i,
                    j,
                    reacs[0][i, j],
                    fontsize=3.0,
                    horizontalalignment="center",
                    verticalalignment="bottom",
                    color="white",
                )

        return fig

    def plot_reac_form_dest(
        self, chemana: pread.Chemistry, level: int = 1, **kwargs
    ) -> mpl.figure.Figure:
        """
        Plot the formation and destruction rates of the most important reactions (or second most etc. )
        for a given chemistry analysis object.

        Parameters
        ----------

        chemana :
            The chemistry analysis object resulting from :func:`~prodimopy.read.analyse_chemistry`.

        level :
            The level of the reactions to be plotted (1 for most important, 2 for second most important etc.).


        .. todo::

          * Currently at most 10 reactions can be plotted (i.e. 10 colors are used).
          * Currently the axes are fixed: ``y=z/r`` and ``x=log(r)`` au.


        """

        sfigs = [2.0, 1.3]
        if "sfigs" in kwargs:
            sfigs = kwargs["sfigs"]

        fig, axes = plt.subplots(1, 2, figsize=(4.0 * sfigs[0], 2.5 * sfigs[1]))

        # the connected model
        m = chemana.model

        font = mpl.font_manager.FontProperties(family="monospace", weight="bold", size="small")
        for reactype, ax in zip(["f", "d"], axes):
            if reactype == "f":
                reacids = chemana.fridxs
            else:
                reacids = chemana.dridxs
            reacs = chemana.get_reac_grid(1, reactype)
            # this is safer, otherwise we might mess up the reacs array
            map = np.copy(reacs[0][0:-1, 0:-1])

            reaclist, reaclist_counts = np.unique(map, return_counts=True)
            nreac = len(reaclist)
            volumes = m.vol[0:-1, 0:-1]
            # sorting just by counts might not be so relevant (e.g. many small pixels)
            vols = [np.sum(volumes[map == reaclist[i]]) for i in range(nreac)]
            sortidx = np.flip(np.argsort(vols))
            sreacsf = reaclist[sortidx]

            # to have better colors we do not use the reacids, but just the index
            # we normalize it by hand
            if nreac > 10:
                print(
                    "WARN: plot_reac_form_dest: more than 10 reactions found, only the first 10 will be plotted, "
                    "The rest will be in white."
                )
                for i in range(10, nreac):
                    map[
                        map == sreacsf[i]
                    ] = -1  # mark as invalid, will be shown in cmap.set_under color
                nreac = 10

            for i in range(nreac):
                map[map == sreacsf[i]] = i

            # this one has 10 colors, so for now we use only 10 reactions
            cmap = mpl.colormaps["tab10"]  # tab20b
            # Take colors at regular intervals spanning the colormap.
            colors = cmap(np.linspace(0, 1, nreac))
            cmap.set_under("white")

            # x and z are actually cell edges, so to make pcolormesh work without warning we need to drop the last row (top) and column (right),
            # this should be fine for such a plot
            ax.pcolormesh(m.x, m.z / m.x, map, linewidth=0, cmap=cmap, rasterized=True, vmin=0)
            ax.semilogx()
            ax.set_xlabel("r [au]")
            ax.set_ylabel("z/r")

            handles = list()
            for i in range(nreac):
                reac = m.chemnet.reactions[reacids[sreacsf[i] - 1] - 1]
                line = ax.scatter(0, 0, marker="s", color=colors[i], label=reacToStr(reac))
                handles.append(line)

            if reactype == "f":
                ax.set_title(chemana.species + " formation ")
                bbox_to_anchor = (0.065, 0, 0.43, 0)
            else:
                ax.set_title(chemana.species + " destruction")
                bbox_to_anchor = (0.065 + 0.505, 0, 0.43, 0)

            # plot the reactions as legend, below the axes
            fig.legend(
                loc="lower right",
                bbox_to_anchor=bbox_to_anchor,
                ncol=2,
                markerscale=0,
                handles=handles,
                labelcolor=colors,
                prop=font,
                columnspacing=-0.5,
                mode="expand",
            )

        fig.subplots_adjust(top=0.93, bottom=0.31, left=0.07, right=0.995)

        return self._closefig(fig)

    def plot_reac_ixiz(
        self,
        ix: int,
        iz: int,
        rtype: str,
        chemanas: list[pread.Chemistry],
        chemana_steadystate: pread.Chemistry | None = None,
        ax=None,
        **kwargs,
    ):
        """
        Plots the rates for the most important reactions at the point ``ix``, ``iz`` for the
        given chemanalysis list, which usually come from a time-dependent |prodimo| disk model (i.e time steps).
        That ages (x-axis) are taken from the model connected the the chemanalysis objects.

        Parameters
        ----------

        ix :
          The ix index of the grid (starts at 0)

        iz :
          The iz index of the grid (starts at 0)

        rtype :
          ``f`` for formation reactions, ``d`` for destruction reactions.

        chemanas :
          A list of chemanalysis objects (e.g. for each
          age in a time-dependent model). All have to be for the same species.

        chemana_steadystate :
          The chemistry analysis of an equivalent steady-state model (i.e. same grid, etc.) for the
          same species. Optional
        """

        # Fixme: Would make sense to have this as a parameter
        nmaxreac = 3

        if rtype == "d":
            tit = "dest. reactions for "
        else:
            tit = "form. reactions for "

        totrates = list()
        reacidx = list()

        ages = list()
        for chemana in chemanas:
            if rtype == "d":
                totrates.append(chemana.totdrate[ix, iz])
                reacs = chemana.gridd[ix, iz, 0]
            else:
                totrates.append(chemana.totfrate[ix, iz])
                reacs = chemana.gridf[ix, iz, 0]

            # figure out what reactions indices I want to plot
            for i in range(nmaxreac):
                if i < len(reacs):
                    reacidx.append(reacs[i])

            ages.append(chemana.model.age)

        reacidx = np.unique(np.array(reacidx))

        reactions = list()
        for ridx in reacidx:
            rates = list()
            for chemana in chemanas:
                if rtype == "d":
                    rate = chemana.gridd[ix, iz, 1][chemana.gridd[ix, iz, 0] == ridx]
                else:
                    rate = chemana.gridf[ix, iz, 1][chemana.gridf[ix, iz, 0] == ridx]

                if len(rate) == 0:
                    rates.append(0.0)
                else:
                    rates.append(rate[0])
            reactions.append(rates)

        fig, ax = self._initfig(ax, **kwargs)
        ax.plot(ages, totrates, label="totrate", color="black", linewidth="3")
        for i in range(len(reacidx)):
            # This assume that all chemanas have the same chemnet in the background, otherwise it would not make much sense
            ax.plot(
                ages,
                reactions[i],
                label=reacToStr(chemanas[0].model.chemnet.reactions[reacidx[i] - 1]),
            )

        # for the steady state model
        if chemana_steadystate is not None:
            reacidxsss = list()
            ratesss = list()
            for i in range(nmaxreac):
                if rtype == "d":
                    if i < len(chemana_steadystate.gridd[ix, iz, 0]):
                        reacidxsss.append(chemana_steadystate.gridd[ix, iz, 0][i])
                        ratesss.append(chemana_steadystate.gridd[ix, iz, 1][i])
                else:
                    if i < len(chemana_steadystate.gridf[ix, iz, 0]):
                        reacidxsss.append(chemana_steadystate.gridf[ix, iz, 0][i])
                        ratesss.append(chemana_steadystate.gridf[ix, iz, 1][i])

            colors = np.arange(0.1, 0.9, 0.7 / nmaxreac)
            for i, (reacidx, rate) in enumerate(zip(reacidxsss, ratesss)):
                ax.scatter(
                    ages[-1] * 1.05,
                    rate,
                    label=reacToStr(chemana_steadystate.model.chemnet.reactions[reacidx - 1]),
                    marker="<",
                    color=str(colors[i]),
                    s=20 / np.log(i + 2),
                )

        ax.legend(
            bbox_to_anchor=(1.01, 1.0), loc="upper left", prop={"family": "monospace", "size": 5}
        )

        ax.semilogx()
        ax.semilogy()
        ax.set_xlabel("age [yr]")
        ax.set_ylabel(r"rate $[cm^{-3}\,s^{-1}]$")
        ax.set_title(tit + " ix={:5d}, iz={:5d}".format(ix, iz))

        self._dokwargs(ax, **kwargs)

        return self._closefig(fig)

    def plot_line_origin(
        self,
        model: pread.Data_ProDiMo,
        lineIdents: list[tuple[str, float]],
        field: NDArray[np.float64] | str,
        label="value",
        showBox=True,
        showRadialLines=True,
        showContOrigin=False,
        showztauD1=True,
        boxcolors=None,
        boxlinewidths=1.5,
        boxlinestyles=None,
        boxhatches=None,
        lineLabels=None,
        showLineLabels=True,
        lineLabelsFontsize=6.0,
        lineLabelsAlign="left",
        zlog=True,
        zlim=[None, None],
        zr=True,
        clevels=None,
        clabels=None,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        cb_format="%.1f",
        scalexy=[1, 1],
        patches=None,
        rasterized=False,
        ax=None,
        **kwargs,
    ):
        """
        Plots the line origins for a list of lineestimates given by their lineIdents
        (["ident",wavelength]).

        Does not give the exact same results as the corresponding idl routine
        as we do not use interpolation here. We rather use the same method for
        calculating the averaged values over the emission area and for plotting
        this area.

        Note most other parameters, especially for plotting styles (line widths), are also
        arrays/lists. Those lists should have the same length as the lineIdents list.

        The routine uses :func:`plot_cont` for plotting, hence a number of parameters have the same meaning as in plot_cont.
        They are just passed through to plot_cont).

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        lineIdents : array_like()
          list of line ids of the form `[("ident",wl),("ident2",wl2)]`. wl is in micron.

        field : array_like(float,ndim=2)
          a 2D array with numeric values for the plotting. E.g. any 2D array, or just the name of that field in
          in a :class:`~prodimopy.read.Data_ProDiMo` object.

        showBox : boolean
          if `True` (default) the box for the emitting region for each line is shown.

        showRadialLines : boolean
          if `True` (default) than two dotted lines are shown for the z15 and z85 values at each radius.
          This is the main line emitting layer at each radius.

        showContOrigin : boolean
          Also show the box for the continuum emitting regions (at the wavelength of the line). Default: `False`.

        showztauD1 : boolean
          show the z_level where taudust_ver=1 for each line. For detail of this quantity see
          :class:`~prodimopy.read.DataLineEstimateRInfo`

        boxcolors : array_like
          list of colors for the boxes for each line one wants to plot (should have the same number of entries as lineIdents).
          If not given the default colors are used.

        boxlinewidths : array_like
          the widths of the line for each box showing the line origin. Can be a
          scalar, in that case all boxes have the same linewidth.

        boxlinestyles : array_like
          the line styles for the boxes (line emitting regions). Can be a scalar, in that case all boxes have the same linestyle.

        boxhatches : array_like
          if given, the origin boxes or the vertical line emitting regions (`showRadialLines=True`), are hatched.
          Hatches are the ones from matplotlib (e.g. `boxhatches=["//"]`).
          See https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html#hatch-style-reference for detail.

        lineLabels : array_like
          list of labels for the lines. If not given the labels are generated from the lineIdents.

        showLineLabels : boolean
          show the labels for the lines. Default: `True`.

        lineLabelsFontsize : float
          fontsize for the line labels. Default: `6.0`.

        lineLabelsAlign : str
          alignment of the line labels. Default: `left`. Other options is `right`.

        """
        if boxcolors is None:
            boxcolors = [
                self.pcolors["red"],
                self.pcolors["orange"],
                self.pcolors["brown"],
                self.pcolors["purple"],
                self.pcolors["gray"],
            ]

        if boxlinestyles is None:
            boxlinestyles = ["-"] * 10
        elif np.isscalar(boxlinestyles):
            boxlinestyles = [boxlinestyles] * 10

        if np.isscalar(boxlinewidths):
            boxlinewidths = [boxlinewidths] * 10

        # if it is only one line (no list of list) make it a list
        if type(lineIdents[0]) is str:
            lineIdents = [lineIdents]

        lestimates = list()
        for id in lineIdents:
            lestimates.append(model.getLineEstimate(id[0], id[1]))

        if patches is None:
            patches = list()

        if len(boxcolors) < len(lestimates) or len(boxlinestyles) < len(lestimates):
            print("Not enough boxcolors or boxlinestyles available! ")
            return

        ibox = 0
        for lesti in lestimates:
            # Security check to avoid stopping of all plotting
            if lesti is None:
                return

            # to be consistent we use the LineOriginMask to determine the box
            # as a result the plotted region is not necessarily the same as in idl
            # as we do not interpolate here
            xmasked = np.ma.masked_array(model.x, mask=model.getLineOriginMask(lesti))
            x15 = np.min(xmasked)
            x85 = np.max(xmasked)
            xi15 = np.argmin(np.abs(model.x[:, 0] - x15))
            xi85 = np.argmin(np.abs(model.x[:, 0] - x85))

            z85s = [[model.x[rp.ix, 0], rp.z85] for rp in lesti.rInfo[xi15 : xi85 + 1]]
            z15s = [[model.x[rp.ix, 0], rp.z15] for rp in lesti.rInfo[xi85 : xi15 - 1 : -1]]
            points = z85s + z15s

            if zr is True:
                for point in points:
                    point[1] = point[1] / point[0]

            if showBox:
                if len(points) > 1:
                    hatch = None
                    if boxhatches is not None:
                        hatch = boxhatches[ibox]

                    patch = mpl.patches.Polygon(
                        points,
                        closed=True,
                        fill=False,
                        color=boxcolors[ibox],
                        linestyle=boxlinestyles[ibox],
                        hatch=hatch,
                        hatch_linewidth=boxlinewidths[ibox] * 0.7,
                        zorder=100,
                        linewidth=boxlinewidths[ibox],
                    )

                    patches.append(patch)
                else:
                    print(
                        "WARN: Unable to calculate a proper region for the line origin: "
                        + str(lesti)
                    )

            if showContOrigin is True:
                if model.sed is not None and model.sed.sedAna is not None:
                    pointsc = self._getSEDana_boxpoints(lesti.wl, model, zr)
                    if len(pointsc) > 1:
                        patchc = mpl.patches.Polygon(
                            pointsc,
                            closed=True,
                            fill=False,
                            color=boxcolors[ibox],
                            zorder=100,
                            linewidth=1.0,
                            linestyle="--",
                        )
                        patches.append(patchc)
                    else:
                        print(
                            "WARN: Unable to calculate a proper region for the continuum origin: "
                            + str(lesti)
                        )

            ibox += 1

        fig = self.plot_cont(
            model,
            field,
            label=label,
            zlog=zlog,
            zlim=zlim,
            zr=zr,
            clevels=clevels,
            clabels=clabels,
            contour=False,
            extend=extend,
            oconts=oconts,
            acont=None,
            acontl=None,
            nbins=nbins,
            bgcolor=bgcolor,
            cb_format=cb_format,
            scalexy=scalexy,
            patches=patches,
            rasterized=rasterized,
            returnFig=True,
            ax=ax,
            **kwargs,
        )

        if ax is None:
            ax = fig.axes[0]

        # show the full emitting layer as function of radius
        # maybe this slows down the pl
        if showRadialLines or showztauD1:
            iest = 0
            r = model.x[:, 0]
            for lesti in lestimates:
                z15 = [rinf.z15 for rinf in lesti.rInfo]
                z85 = [rinf.z85 for rinf in lesti.rInfo]
                if zr is True:
                    z15 = z15 / r
                    z85 = z85 / r

                if showBox is False:
                    lsrad = boxlinestyles[iest]
                else:
                    lsrad = ":"

                if showRadialLines:
                    ax.plot(r, z15, color=boxcolors[iest], linestyle=lsrad, linewidth=1.0)
                    ax.plot(r, z85, color=boxcolors[iest], linestyle=lsrad, linewidth=1.0)
                    if boxhatches is not None:
                        ax.fill_between(
                            r,
                            z15,
                            z85,
                            edgecolor=boxcolors[iest],
                            hatch=boxhatches[iest],
                            facecolor="none",
                            linewidth=0.0,
                        )

                # can be None just check the first entry
                if showztauD1 and lesti.rInfo[0].ztauD1 is not None:
                    ztauD1 = [rinf.ztauD1 for rinf in lesti.rInfo]
                    if zr:
                        ztauD1 = ztauD1 / r

                    ax.plot(r, ztauD1, color=boxcolors[iest], linestyle="--", linewidth=1.0)

                iest += 1

        if showLineLabels:
            ibox = 0
            for idline, lesti in zip(lineIdents, lestimates):
                if lineLabels is not None:
                    label = lineLabels[ibox]
                else:
                    label = (
                        "$"
                        + spnToLatex(idline[0])
                        + "$ "
                        + ("{:10.2f}".format(lesti.wl)).strip()
                        + r" $\mu$m"
                    )

                # FIXME: quick and dirty, ref fontsize =6.0
                vpos = ibox / (18.0 - (lineLabelsFontsize / 6.0 - 1.0) * 12)
                if lineLabelsAlign == "right":
                    ax.text(
                        0.95,
                        0.97 - vpos,
                        label,
                        horizontalalignment="right",
                        verticalalignment="top",
                        fontsize=lineLabelsFontsize,
                        transform=ax.transAxes,
                        color=boxcolors[ibox],
                        bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"),
                        zorder=100,
                    )  # make sure that labels are on top
                else:
                    ax.text(
                        0.02,
                        0.97 - vpos,
                        label,
                        horizontalalignment="left",
                        verticalalignment="top",
                        fontsize=lineLabelsFontsize,
                        transform=ax.transAxes,
                        color=boxcolors[ibox],
                        bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"),
                        zorder=100,
                    )
                ibox += 1

        return self._closefig(fig)

    def plot_ionrates_midplane(self, model, ax=None, **kwargs):
        print("PLOT: plot_ionrates_midplane ...")

        cX = self.pcolors["red"]
        cSP = self.pcolors["blue"]
        cCR = self.pcolors["gray"]

        x = model.x[:, 0]

        #  print pdata.zetaCR[ix,:]
        y1 = model.zetaCR[:, 0]
        y2 = (
            model.zetaX[:, 0] * 2.0
        )  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent
        y3 = model.zetaSTCR[
            :, 0
        ]  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent

        fig, ax = self._initfig(ax, **kwargs)

        ax.plot(x, y2, color=cX, label=r"$\zeta_\mathrm{X}$")
        ax.plot(x, y3, color=cSP, label=r"$\zeta_\mathrm{SP}$")
        ax.plot(x, y1, color=cCR, label=r"$\zeta_\mathrm{CR}$")

        # print ax.get_xlim()

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(r"$\mathrm{\zeta\,per\,H_2\,[s^{-1}]}$")

        ax.semilogy()
        self._dokwargs(ax, **kwargs)
        self._legend(ax)
        # handles, labels = ax.get_legend_handles_labels()
        # ax.legend(handles, labels, loc="best", fancybox=False)

        return self._closefig(fig)

    # FIXME: this routine is also not very general (e.g. colors)
    def plot_ionrates(self, model, r, ax=None, **kwargs):
        cX = self.pcolors["red"]
        cSP = self.pcolors["blue"]
        cCR = self.pcolors["gray"]

        ix = (np.abs(model.x[:, 0] - r)).argmin()
        rstr = "r={:.1f} au".format(model.x[ix, 0])

        old_settings = np.seterr(divide="ignore")
        nhver = np.log10(model.NHver[ix, :])
        np.seterr(**old_settings)  # reset to default
        #  print pdata.zetaCR[ix,:]
        y1 = model.zetaCR[ix, :]
        y2 = (
            model.zetaX[ix, :] * 2.0
        )  # convert to per H2 TODO: maybe do this in ProDiMo already to be consistent
        y3 = model.zetaSTCR[ix, :]

        fig, ax = self._initfig(ax, **kwargs)

        ax.plot(nhver, y2, color=cX, label=r"$\zeta_\mathrm{X}$")
        ax.plot(nhver, y3, color=cSP, label=r"$\zeta_\mathrm{SP}$")
        ax.plot(nhver, y1, color=cCR, label=r"$\zeta_\mathrm{CR}$")

        # set the limits

        ax.set_xlim([17.5, nhver.max()])
        ax.set_ylim([1.0e-21, 1.0e-9])

        ax.set_xlabel(r"$\log$ N$_\mathrm{<H>,ver}$ [cm$^{-2}$]")
        ax.set_ylabel(r"$\zeta$ per H$_2$ [s$^{-1}$]")

        # do axis style
        ax.semilogy()

        # title does not work here
        self._dokwargs(ax, title=None, **kwargs)

        ax2 = ax.twiny()
        ax2.set_xlabel("z/r")
        ax2.set_xlim(ax.get_xlim())
        # ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc="best")
        ax.text(
            0.025,
            0.020,
            rstr,
            verticalalignment="bottom",
            horizontalalignment="left",
            transform=ax.transAxes,
            alpha=0.75,
        )

        return self._closefig(fig)

    def plot_avgabun(self, model, species, ax=None, **kwargs):
        """
        Plots the average abundance for the given species (can be more than one)
        as a function of radius
        """
        print("PLOT: plot_avgabun ...")

        fig, ax = self._initfig(ax, **kwargs)

        iplot = 0
        if type(species) is str:
            species = [species]
        for spec in species:
            # get the species
            if spec in model.spnames:
                y = model.cdnmol[:, 0, model.spnames[spec]]
                y = y / model.NHver[:, 0]
                x = model.x[:, 0]

                style = "-"
                if "#" in spec:
                    style = "--"
                ax.plot(
                    x,
                    y,
                    linestyle=style,
                    marker=None,
                    label=r"$\mathrm{" + spnToLatex(spec) + "}$",
                )

                iplot = iplot + 1

        if iplot == 0:
            print("Species " + species + " not found in any model!")
            return

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(r"average abundance")
        ax.set_xlim([x.min(), x.max()])

        # do axis style
        ax.semilogy()

        self._dokwargs(ax, **kwargs)
        self._legend(ax)

        return self._closefig(fig)

    def plot_radial(self, model, values, ylabel, zidx=0, color=None, ax=None, **kwargs):
        """
        Plots a quantity along the radial grid for the given zidx (from the |prodimo| Array)
        as a function of radius.

        Parameters
        ----------

        values : array_like(float,ndim=2) or array_like(float,ndim=2)
            `values` is any |prodimo| 2D array in the :class:`~prodimopy.read.Data_ProDiMo` object,
            or a 1D array with dim `nx` if `zidx` is `None`.

        ylabel : str
            The lable for the y axis.

        zidx : int
            The index of the z coordinate that should be plotted.
            If zidx is `None` the values array has to be 1D and needs to be filled with the proper values.
            Default: 0 (midplane)

        color : str
            A matplotlib color for the line to plot. Default: `None`

        ax : :class:`matplotlib.axes.Axes`
            A matplotlib axes object that will be use to do the actual plotting. No new instance is created.
            Default: None (make a new figure and axes object).


        """
        print("PLOT: plot_radial ...")
        fig, ax = self._initfig(ax, **kwargs)

        if zidx is None:
            x = np.sqrt(model.x[:, 0] ** 2.0 + model.z[:, 0] ** 2.0)
            y = values
        else:
            x = np.sqrt(model.x[:, zidx] ** 2.0 + model.z[:, zidx] ** 2.0)
            y = values[:, zidx]

        ax.plot(x, y, marker=None, color=color)

        ax.set_xlim(np.nanmin(x), np.nanmax(x))
        ax.set_ylim(np.nanmin(y), np.nanmax(y))
        ax.semilogy()

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(ylabel)

        self._dokwargs(ax, **kwargs)
        # self._legend(ax)

        return self._closefig(fig)

    def plot_cdnmol(
        self,
        model,
        species,
        colors=None,
        styles=None,
        scalefacs=None,
        norm=None,
        normidx=None,
        ylabel=r"$\mathrm{N_{ver}\,[cm^{-2}}]$",
        patches=None,
        ax=None,
        **kwargs,
    ):
        """
        Plots the vertical column densities as a function of radius for the
        given species.

        Parameters
        ----------
        model : :class:`prodimopy.read.Data_ProDiMo`
          the |prodimo| model data.

        species : array_like(str,ndim=1)
          a list of species names that should be plotted.

        scalefacs : array_like(float,ndim=1)
          scale the column density to plot by the given factor.
          `len(scalefacs)` must be equal to `len(species)`.

        norm : float
          an arbitrary normalization factor (i.e. all column density are divided by `norm`)

        normidx : int
          normalize the plotted column densities to the column density given by
          `normidx`. Where `normidx` is the index of any species in the list of species in the model.
          TODO: Could actually just use a species name, would be easier to use.

        """
        print("PLOT: plot_cdnmol ...")

        if colors is None:
            colors = [None] * len(species)

        if styles is None:
            styles = [None] * len(species)

        if type(species) is str:
            species = [species]

        fig, ax = self._initfig(ax, **kwargs)

        x = model.x[:, 0]

        ymin = 1.0e99
        ymax = 1.0e-99

        if scalefacs is None:
            scalefacs = np.ones(len(species))

        if normidx is not None:
            normspec = model.cdnmol[:, 0, normidx]

        iplot = 0
        for spec, fac in zip(species, scalefacs):
            ispec = -1
            try:
                ispec = model.spnames[spec]
            except:  # noqa: E722
                print("WARNING: Could not find species: ", spec)
                continue

            if normidx is not None:
                y = model.cdnmol[:, 0, ispec] / normspec

            y = model.cdnmol[:, 0, ispec] / fac
            if norm is not None:
                y = y / norm

            label = "$" + spnToLatex(spec) + "$"
            if fac != 1.0 and norm is None:
                label += "/" + "{:3.1e}".format(fac)

            ax.plot(x, y, marker=None, linestyle=styles[iplot], color=colors[iplot], label=label)

            ymin = np.min([np.min(y), ymin])
            ymax = np.max([np.max(y), ymax])
            iplot = iplot + 1

        if patches is not None:
            for patch in patches:
                ax.add_patch(copy.copy(patch))

        ax.set_xlim(np.min(x), np.max(x))
        ax.set_ylim(ymin, ymax)
        ax.semilogy()

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(ylabel)

        self._dokwargs(ax, **kwargs)
        self._legend(ax, **kwargs)

        return self._closefig(fig)

    def plot_midplane(self, model, field, ylabel, xRelTo=None, ax=None, **kwargs):
        """
        Plots a quantitiy in in the midplane as a function of radius
        fieldname is any field in Data_ProDiMo

        Parameters
        ----------

        xRelTo : float
          use `x-xRelTo` as the x axis. Default: `None` (no shif)


        FIXME: remove the fieldname stuff passe  the whole array ...
        """
        print("PLOT: plot_midplane ...")
        fig, ax = self._initfig(ax, **kwargs)

        x = model.x[:, 0]
        if xRelTo is not None:
            x = x - xRelTo

        if type(field) is str:
            y = getattr(model, field)[:, 0]
        else:
            y = field[:, 0]

        ax.plot(x, y, marker=None)

        ax.set_xlim(np.min(x), np.max(x))
        ax.set_ylim(np.min(y), np.max(y))
        ax.semilogy()

        if xRelTo is not None:
            ax.set_xlabel("r - {:3.1f} [au]".format(xRelTo))
        else:
            ax.set_xlabel(r"r [au]")
        ax.set_ylabel(ylabel)

        self._dokwargs(ax, **kwargs)
        # self._legend(ax)

        return self._closefig(fig)

    def _prepareAbunForPlot(self, model, species, label, rel2H, zlog, zlim, extend):
        """
        Utility function used in :func:`~prodimopy.plot.Plot.plot_abuncont` and
        :func:`~prodimopy.plot.Plot.plot_abuncont_grid`.
        """
        # Check if species names exists
        try:
            n_rel_index = model.spnames[species]

        except KeyError:
            print(
                "The species "
                + species
                + """you want to access does not exist
             or is spelled incorrectly. Exiting plot_abuncont routine"""
            )
            return

        if rel2H:
            values = model.getAbun(species)

            if label is None:
                label = r"$\mathrm{\epsilon(" + spnToLatex(species) + ")}$"
                if zlog:
                    label = "log " + label

            # define some default lower limit
            if zlim is None or zlim == [None, None]:
                zlim = [3.0e-13, None]
                extend = "both"

        else:
            values = model.nmol[:, :, n_rel_index]
            if label is None:
                label = r"$\mathrm{n(" + spnToLatex(species) + ") [cm^{-3}]}$"
                if zlog:
                    label = "log " + label

        return values, label, zlog, zlim, extend

    def plot_abunvert(
        self,
        model,
        r,
        species,
        useZr=False,
        useNH=True,
        useT=False,
        scaling_fac=None,
        norm=None,
        styles=None,
        colors=None,
        markers=None,
        linewidths=None,
        ax=None,
        **kwargs,
    ):
        """
        Plots the abundances of all the given species as a function of height at
        the given radius.

        If `useZr`, `useNH` and `useT` are all `False` the abundances are plotted
        as function of z in au. By default `useNH=True`.


        FIXME: Make the inferface consistent with plot_vert. Especially
        the treatment of the xaxis (i.e. what should be use to indicate the height)

        Parameters
        ----------
        model : :class:`prodimopy.read.Data_ProDiMo`
          the model data

        r : float
          The radius at which the vertical cut is taken. UNIT: `au`

        species : array_like(str,ndim=1) :
          List of species names to plot.

        useZr : boolean
          plot the abundances as function of z/r: Default: `True`

        useNH : boolean
          plot the abundances as function of vertical column densities
          Default: `False`

        useT : boolean
          plot the abundances as function of dust temperature.


        """

        print("PLOT: plot_abunvert ...")

        if colors is None:
            colors = list(self.pcolors.values())

        rstr = r"r$\approx${:.2f} au".format(r)

        fig, ax = self._initfig(ax, **kwargs)

        ix = (np.abs(model.x[:, 0] - r)).argmin()

        iplot = 0
        ymin = 1.0e100
        ymax = -1.0
        if type(species) is str:
            species = [species]
        for spec in species:
            if useNH:
                old_settings = np.seterr(divide="ignore")
                x = np.log10(model.NHver[ix, :])
                np.seterr(**old_settings)  # reset to default
                xlabelstr = r"$\mathrm{\log\,N_{<H>}\,[cm^{-2}]}$ @" + rstr
            elif useZr:
                x = model.z[ix, :] / model.x[ix, 0]
                xlabelstr = r"z/r @" + rstr
            elif useT:
                x = model.td[ix, :]
                xlabelstr = r"$\mathrm{T_d [K]}$ @" + rstr
            else:
                x = model.z[ix, :]
                xlabelstr = r"z [au] @" + rstr

            # check if list of names in list of names, than sum them up
            if isinstance(spec, (list, tuple, np.ndarray)):
                y = model.nHtot[ix, :] * 0.0  # just to get an array
                for name in spec:
                    y = y + (model.getAbun(name)[ix, :])

            elif spec in model.spnames:
                y = model.nmol[ix, :, model.spnames[spec]] / model.nHtot[ix, :]
            else:
                continue

            if norm is not None:
                y = y / norm

            if scaling_fac is not None:
                y = y * scaling_fac[iplot]

            # FIXME: add proper treatment for styles and colors
            if styles is None:
                style = "-"
                if "#" in spec:
                    style = "--"
            else:
                style = styles[iplot]

            color = colors[iplot]

            marker = None
            if markers is not None:
                marker = markers[iplot]

            lines = ax.plot(
                x,
                y,
                marker=marker,
                ms=4,
                markeredgecolor=color,
                markerfacecolor=color,
                linestyle=style,
                color=color,
                label=r"$\mathrm{" + spnToLatex(spec) + "}$",
            )

            if linewidths is not None:
                if linewidths[iplot] is not None:
                    lines[-1].set_linewidth(linewidths[iplot])

            iplot = iplot + 1
            if min(y) < ymin:
                ymin = min(y)
            if max(y) > ymax:
                ymax = max(y)

        if useT:
            ax.set_xlim([30, 5])
        elif useNH:
            ax.set_xlim([17.5, x.max()])
        else:
            ax.invert_xaxis()  # (z/r=0 on the right)
        ax.set_ylim(ymin, ymax)
        ax.semilogy()

        #     ax2 = ax.twiny()
        #     ax2.set_xlabel("z/r")
        #     ax2.set_xlim(ax.get_xlim())
        #     #ax2.set_xticks(ax.get_xticks())
        #     ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

        ax.set_xlabel(xlabelstr)
        ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

        self._dokwargs(ax, **kwargs)
        self._legend(ax, **kwargs)
        return self._closefig(fig)

    def plot_abunrad(
        self,
        model,
        species,
        useNH=True,
        norm=None,
        styles=None,
        colors=None,
        markers=None,
        linewidths=None,
        ax=None,
        **kwargs,
    ):
        """
        Plots species abundances as function of radius in the midplane (z=0)
        Similar to :func:`plot_abunvert` but radially is more useful for e.g. envelope structures.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        species : array_like(str,ndim=1) :
          List of species names to plot.

        useNH : boolean
          plot the abundances as function of radial column densities
          Default: `False`

        norm : float
          normalize the y values by the given number (i.e. y=y/norm)
          Default: `None` (i.e. no normalisation)

        """

        print("PLOT: plot_abunrad ...")

        fig, ax = self._initfig(ax, **kwargs)

        iplot = 0
        ymin = 1.0e100
        ymax = -1.0
        if type(species) is str:
            species = [species]
        for spec in species:
            if useNH:
                old_settings = np.seterr(divide="ignore")
                x = np.log10(model.NHrad[:, 0])
                np.seterr(**old_settings)  # reset to defaul
            else:
                x = model.x[:, 0]

            if spec in model.spnames:
                y = model.nmol[:, 0, model.spnames[spec]] / model.nHtot[:, 0]
                if norm is not None:
                    y = y / norm

                # FIXME: add proper treatment for styles and colors
                if styles is None:
                    style = "-"
                    if "#" in spec:
                        style = "--"
                else:
                    style = styles[iplot]

                color = None
                if colors is not None:
                    color = colors[iplot]

                marker = None
                if markers is not None:
                    marker = markers[iplot]

                lines = ax.plot(
                    x,
                    y,
                    marker=marker,
                    ms=4,
                    markeredgecolor=color,
                    markerfacecolor=color,
                    linestyle=style,
                    color=color,
                    label=r"$\mathrm{" + spnToLatex(spec) + "}$",
                )

                if linewidths is not None:
                    if linewidths[iplot] is not None:
                        lines[-1].set_linewidth(linewidths[iplot])

                iplot = iplot + 1
                if min(y) < ymin:
                    ymin = min(y)
                if max(y) > ymax:
                    ymax = max(y)

        if useNH:
            ax.set_xlim([17.5, x.max()])
        ax.set_ylim(ymin, ymax)
        ax.semilogy()

        #     ax2 = ax.twiny()
        #     ax2.set_xlabel("z/r")
        #     ax2.set_xlim(ax.get_xlim())
        #     #ax2.set_xticks(ax.get_xticks())
        #     ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ix, ax.get_xticks(), model)])

        if useNH:
            ax.set_xlabel(r"$\mathrm{\log\,N_{<H,rad>}\,[cm^{-2}]}$")
        else:
            ax.set_xlabel(r"r [au]")
        ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

        self._dokwargs(ax, **kwargs)
        self._legend(ax)
        return self._closefig(fig)

    def plot_abun_midp(
        self, model, species, norm=None, styles=None, colors=None, ax=None, **kwargs
    ):
        """
        Plots the abundances in the midplane for the given species (can be more than one)

        Parameters
        ----------
        model : :class:`prodimopy.read.Data_ProDiMo`
          the model data

        species : array_like(str,ndim=1) :
          List of species names to plot.

        norm : float
          normalize the y values by the given number (i.e. y=y/norm)
          Default: `None` (i.e. no normalisation)

        """

        print("PLOT: plot_abun_midp ...")
        fig, ax = self._initfig(ax, **kwargs)

        iplot = 0
        xmin = 1.0e100
        xmax = 0
        ymin = 1.0e100
        ymax = -1.0e00
        if type(species) is str:
            species = [species]
        for spec in species:
            if spec not in model.spnames:
                print("WARN: Species " + spec + " not found")
                continue

            x = model.x[:, 0]
            y = model.nmol[:, 0, model.spnames[spec]] / model.nHtot[:, 0]
            if norm is not None:
                y = y / norm

            # FIXME: add proper treatment for styles and colors

            if styles is None:
                style = "-"
                if "#" in spec:
                    style = "--"
            else:
                style = styles[iplot]

            if colors is None:
                color = None
            else:
                color = colors[iplot]

            ax.plot(
                x,
                y,
                marker=None,
                linestyle=style,
                color=color,
                label=r"$\mathrm{" + spnToLatex(spec) + "}$",
            )

            iplot = iplot + 1

            if min(x) < xmin:
                xmin = min(x)
            if max(x) > xmax:
                xmax = max(x)
            if min(y) < ymin:
                ymin = min(y)
            if max(y) > ymax:
                ymax = max(y)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.semilogy()
        ax.set_xlabel("r [au]")
        ax.set_ylabel(r"$\mathrm{\epsilon(X)}$")

        self._dokwargs(ax, **kwargs)
        self._legend(ax)

        return self._closefig(fig)

    def plot_dust_opac(self, model, dust=None, ax=None, pseudoaniso=False, **kwargs):
        """
        Plots the dust opacities (dust_opac.out) or the data given in the
        dust object

        Parameters
        ----------

        pseudoaniso : boolean
          Use the pseudo anisotropic scattering opacity (Default: `False`).

        """
        print("PLOT: dust opacities ...")

        fig, ax = self._initfig(ax, **kwargs)

        x = model.dust.lam

        if dust is None:
            dust = model.dust

        ax.plot(x, dust.kabs, label="absorption")
        if pseudoaniso:
            ax.plot(x, dust.ksca_an, label="scattering")
            ax.plot(x, dust.kabs + dust.ksca_an, label="extinction")
        else:
            ax.plot(x, dust.ksca, label="scattering")
            ax.plot(x, dust.kext, label="extinction")
        ax.set_xlabel(r"wavelength $\mathrm{[\mu m]}$")
        ax.set_ylabel(r"opacity $\mathrm{[cm^2 g(dust)^{-1}]}$")

        ax.set_xlim(np.min(x), np.max(x))
        # ax.set_ylim(1.e-2,None)

        ax.semilogx()
        ax.semilogy()

        self._dokwargs(ax, **kwargs)
        self._legend(ax)
        return self._closefig(fig)

    def plot_opac(
        self, model: pread.Data_ProDiMo, xunit: str = "micron", ax: mpl.axes.Axes = None, **kwargs
    )-> mpl.figure.Figure:
        """
        Plots gas and dust opacity data.

        The unit is per hydrogen, to make it comparable.
        see `Rab+ (2018) <https://scixplorer.org/abs/2018A&A...609A..91R/>`_ .

        Parameters
        ----------

        model : 
            the model data.

        xunit : 
            The unit for the x-axis. Options are `eV` or `micron`.

        ax : 
            A matplotlib axes object that will be use to do the actual plotting. No new instance is created.

        """
        if model.gas is None:
            print("WARNING: No gas opacity data found in the model, cannot plot gas opacities!")

        # approximate, here it should be unsettled
        # TODO provide also a paramter to fix this
        #   nd_nH=pd.nd[0,0]/pd.nHtot[0,0]
        rhod_nH = model.rhod[0, 0] / model.nHtot[0, 0]

        # dust stuff
        if xunit == "eV":
            xd = model.dust.lam * (u.micrometer).cgs
            xd = ((const.h.cgs * const.c.cgs / xd).to(u.eV)).value
            if model.gas is not None:
                xg = model.gas.energy
        else:
            xd = model.dust.lam
            if model.gas is not None:
                xg = model.gas.lam

        ydabs = model.dust.kabs * rhod_nH
        ydsca = model.dust.ksca * rhod_nH
        ydscaan = model.dust.ksca_an * rhod_nH

        # gas data
        if model.gas is not None:
            ygabs = model.gas.abs_cs
            ygsca = model.gas.sca_cs

        fig, ax = self._initfig(ax, **kwargs)

        if model.gas is not None:
            ax.plot(
                xg,
                (ygabs + ygsca) * 1.0e21,
                label="gas ext (pa)",
                color=self.pcolors["gray"],
                linestyle="-",
            )
            ax.plot(
                xg,
                ygsca * 1.0e21,
                label="gas sca (pa)",
                color=self.pcolors["gray"],
                linestyle="--",
                dashes=(4, 4),
            )

        # if scaan and sca are the same don't plot it
        #print(np.allclose(ydscaan, ydsca, atol=np.min([ydscaan.min(), ydsca.min()]) * 1.0e-2))

        if not np.allclose(ydscaan, ydsca, atol=np.min([ydscaan.min(), ydsca.min()]) * 1.0e-2):
            ax.plot(
                xd,
                (ydabs + ydscaan) * 1.0e21,
                label="dust ext (pa)",
                color=self.pcolors["blue"],
                linestyle="-",
            )
            ax.plot(
                xd,
                ydscaan * 1.0e21,
                label="dust sca (pa)",
                color=self.pcolors["blue"],
                linestyle="--",
                dashes=(4, 4),
            )

        ax.plot(
            xd,
            (ydabs + ydsca) * 1.0e21,
            label="dust ext",
            color=self.pcolors["red"],
            linestyle="-",
        )
        ax.plot(
            xd,
            ydsca * 1.0e21,
            label="dust sca",
            color=self.pcolors["red"],
            linestyle="--",
            dashes=(4, 4),
        )

        # for simplicity
        if model.gas is None:
            xg=xd

        if xunit == "eV":
            # the gas defines the max x axis, dust opacities are calculate for even higher eV
            # but are not used
            ax.set_xlim(np.min([xd.min(), xg.min()]), xg.max())
            ax.set_xlabel("energy [eV]")
        else:
            ax.set_xlim(xg.min(), np.max([xg.max(), xd.max()]))
            ax.set_xlabel(r"wavelength [$\mathrm{\mu}$m]")


        ax.set_ylabel(r"cross-section $\mathrm{[10^{-21} cm^2 H^{-1}]}$")

        ax.semilogx()
        ax.semilogy()

        self._dokwargs(ax, **kwargs)
        self._legend(ax, **kwargs)
        return self._closefig(fig)

    def plot_vertical(
        self, model, r, values, ylabel, zr=True, xfield="zr", marker=None, ax=None, **kwargs
    ):
        """
        Plots a quantity (values) as a function of height at a certain radius
        radius.

        values : array_like(float,ndim=2)
          a 2D array with numeric values for the plotting. E.g. any 2D array
          of the :class:`~prodimopy.read.Data_ProDiMo` object.

        xfield : str
          What field should be used a x-axis. Options are
          `zr`,`NHver`,`tg`,`AVver` .


        FIXME: Make the inferface consistent with plot_abunvert. Especially
        the treatment of the xaxis (i.e. what should be use to indicate the height)

        """
        print("PLOT: plot_vertical ...")
        rstr = r"r$\approx${:.1f} au".format(r)

        fig, ax = self._initfig(ax, **kwargs)

        ix = (np.abs(model.x[:, 0] - r)).argmin()

        if zr and xfield == "zr":
            x = model.z[ix, :] / model.x[ix, 0]
        elif xfield == "NHver" or xfield == "nH":  # nH ist just for backward compatibility
            old_settings = np.seterr(divide="ignore")
            x = np.log10(model.NHver[ix, :])
            np.seterr(**old_settings)  # reset to defaul
            zr = False
        elif xfield == "tg":
            x = model.tg[ix, :]
            zr = False
        elif xfield == "AVver":
            old_settings = np.seterr(divide="ignore")
            x = np.log10(model.AVver[ix, :])
            np.seterr(**old_settings)
            zr = False
        elif xfield == "grid":
            x = np.range(model.nz)
            print(x)
        else:
            x = model.z[ix, :]

        y = values[ix, :]

        ax.plot(x, y, marker=marker, ms=4)

        if zr:
            ax.invert_xaxis()
            ax.set_xlabel(r"z/r @ " + rstr)
        elif xfield == "NHver" or xfield == "nH":  # nH ist just for backward compatibility
            ax.set_xlabel(r"$\mathrm{\log\,N_{<H>}\,[cm^{-2}]}$ @" + rstr)
        elif xfield == "AVver":
            ax.set_xlabel(r"$\mathrm{\log\,A_{V,ver}}$ @" + rstr)
        elif xfield == "tg":
            ax.set_xlabel(r"$\mathrm{\log\,T_{gas}\,[K]}$ @" + rstr)
            ax.invert_xaxis()
        else:
            ax.set_xlabel(r"z [au] @ " + rstr)
            ax.invert_xaxis()

        ax.set_ylabel(ylabel)

        self._dokwargs(ax, **kwargs)
        self._legend(ax)

        return self._closefig(fig)

    def plot_taus(self, model, r, ax=None, **kwargs):
        """
        Plot's taus (A_V, X-rays) as a function of vertical column density
        """
        ir = (np.abs(model.x[:, 0] - r)).argmin()
        rstr = "r={:.2f} au".format(model.x[ir, 0])

        fig, ax = self._initfig(ax, **kwargs)

        old_settings = np.seterr(divide="ignore")

        x = np.log10(model.NHver[ir, :])

        ax.plot(x, model.tauX1[ir, :], color="blue", label=r"$\mathrm{\tau_{1\;keV}}$")
        ax.plot(x, model.tauX10[ir, :], "--", color="blue", label=r"$\mathrm{\tau_{10\;keV}}$")
        ax.plot(x, model.AVrad[ir, :], color="red", label=r"$\mathrm{A_V,rad}}$")
        ax.plot(x, model.AVver[ir, :], "--", color="red", label=r"$\mathrm{A_{V,ver}}$")

        ax.set_xlim(17.5, x.max())
        ax.set_ylim(1.0e-2, np.max([model.AVver[ir, :].max(), 2.0]))

        np.seterr(**old_settings)  # reset to default

        ax.hlines(1.0, ax.get_xlim()[0], ax.get_xlim()[1], linestyle=":")

        ax2 = ax.twiny()
        ax2.set_xlabel("z/r")
        ax2.set_xlim(ax.get_xlim())
        # ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(["{:.2f}".format(x) for x in nhver_to_zr(ir, ax.get_xticks(), model)])

        ax.set_xlabel(r"$\log$ N$_\mathrm{H}$ [cm$^{-2}$]")
        ax.set_ylabel(r"$\mathrm{A_V, \tau}$")

        # do axis style
        ax.semilogy()

        self._dokwargs(ax, **kwargs)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc="best", fancybox=False)
        ax.text(
            0.025,
            0.025,
            rstr,
            verticalalignment="bottom",
            horizontalalignment="left",
            transform=ax.transAxes,
            alpha=0.75,
        )

        return self._closefig(fig)

    def plot_starspec(
        self,
        model: pread.Data_ProDiMo,
        step: int = 10,
        xunit: str = "micron",
        nuInu: bool = True,
        second_xaxis: bool = False,
        showInuInterpol: bool = False,
        showInuBand: bool = False,
        ax: mpl.axes.Axes = None,
        **kwargs,
    ) -> mpl.figure.Figure:
        r"""
        Plots the full Stellar Spectrum.

        Parameters
        ----------

        model :
            The model to plot.

        step :
          only every `step` point is plotted from the Stellar Spectrum (makes is less dense)

        xunit :
          the unit for the x-axes. Current options are `micron` or `eV`.

        nuInu :
            Plot :math:`\nu` times :math:`I_\nu` instead of :math:`I_\nu` only.

        second_xaxis :
            If `True` add a second x-axis showing the corresponding energy/wl in eV/micron.

        showInuInterpol :
            If `True` also plot the interpolated stellar spectrum used in the radiative transfer (from `RTinterpolation.out`).

        showInuBand :
            If `True` also plot the band-averaged stellar spectrum used in the radiative transfer (from `RTinterpolation.out`).

        ax :
            The axes object to plot the spectra on. Default: `None` (new figure)

        """
        print("PLOT: plot_starspec ...")
        fig, ax = self._initfig(ax, **kwargs)

        if showInuInterpol and model.star.InuInterpol is None:
            print("WARN: No RTinterpolation data found in the model, cannot plot it.")
            showInuInterpol = False

        if showInuBand and model.star.InuBand is None:
            print("WARN: No RTinterpolation band data found in the model, cannot plot it.")
            showInuBand = False

        x = model.star.lam[0::step]
        if xunit == "eV":
            x = (x * u.micron).to(u.eV, equivalencies=u.spectral()).value
            # switch the axes
            xmin = (1000.0 * u.micron).to(u.eV, equivalencies=u.spectral()).value
            xmax = x.max()
            xlabel = r"energy [eV]"
        else:
            xmin = x.min()
            xmax = 1000.0
            xlabel = r"wavelength [$\mu$m]"

        y = (model.star.Inu)[0::step]
        if nuInu:
            y = y * model.star.nu[0::step]

        ymin = np.min(y[y>0])
        ymax = np.max(y) * 1.5

        ax.plot(x, y, color="black", label="Spectrum")

        if showInuInterpol:
            yInterpol = model.star.InuInterpol
            xInterpol = model.star.wlInterpol
            if nuInu:
                nuInterpol=(xInterpol* u.micron).to(u.Hz, equivalencies=u.spectral()).value
                yInterpol = yInterpol *nuInterpol
            if xunit=="eV":
                xInterpol = (xInterpol* u.micron).to(u.eV, equivalencies=u.spectral()).value                        
                
            ax.plot(
                xInterpol,
                yInterpol,
                color=self.pcolors["red"],
                linestyle="-",
                linewidth=0.75,
                label="Interpolated",
            )

        if showInuBand:            
            yBand = model.star.InuBand
            if nuInu:
                yBand = yBand * (model.lams * u.micron).to(u.Hz, equivalencies=u.spectral()).value
            
            xBand = model.lambs            
            xCenter = model.lams
            if xunit == "eV":
                xBand = (xBand * u.micron).to(u.eV, equivalencies=u.spectral()).value
                xCenter = (xCenter * u.micron).to(u.eV, equivalencies=u.spectral()).value

            # if the bands go beyon the sellar specturm
            xmax=np.max([xBand.max(),xmax])
            xmin=np.min([xBand.min(),xmin])
            ymin=np.min([(yBand[yBand>0]/2.).min(),ymin])
            
            # it is rather complicated, as there can be gaps in the bands. 
            # FIXME: not very elegant, and hardcoded
            # if Xray_Emin is very close to 13.6eV assume there is no hole
            # additionally the Starspectrum should also be zero
            # find the index closest to 0.0912 micron 
            iUVedge=np.argmin(np.abs(model.lambs - 0.0912))
            iUV=np.where(model.lams>0.0912)[0][0]

            # this one we always have
            ranges=[(iUVedge,len(model.lambs),iUV,len(model.lams))]           
            labels=["Band-averaged",] 

            if iUV>0: # have also Xrays
                XrayEmin=float(model.params["XRAY_EMIN"])*1000.
                if np.abs(XrayEmin - 13.6) < 1.0e-4:
                    ranges=[(0,len(model.lambs),0,len(model.lams))]           
                else:
                    # Holes detected, plot things twice
                    ranges.append((0,iUVedge,0,iUV-1))
                    labels.append(None)
                                                    
            for r,label in zip(ranges,labels):
                i0e=r[0]
                i1e=r[1]
                i0=r[2]
                i1=r[3]
                ax.stairs(
                    yBand[i0:i1],
                    xBand[i0e:i1e],
                    color=self.pcolors["blue"],
                    linestyle="-",
                    label=label,
                    fill=True,
                    alpha=0.2
                )
                # plot it twice once with a low alpha and once just for the lines
                ax.stairs(
                    yBand[i0:i1],
                    xBand[i0e:i1e],
                    color=self.pcolors["blue"],
                    linestyle="-"
                )
                ax.scatter(
                    xCenter[i0:i1], yBand[i0:i1], marker="|", color=self.pcolors["blue"], s=50, linewidths=1.0
                )
                # include vertical lines       
                # need ymin already here
                if "ylim" in kwargs:
                    ymin=kwargs["ylim"]
                    if (len(ymin)==2):
                        ymin=ymin[0]

                ax.vlines(xBand[i0e:i1e], ymin, np.append(yBand[i0:i1],yBand[i1-1]), colors=self.pcolors["blue"],linewidth=0.5,zorder=-10)

        # set defaults, can be overwritten by the kwargs
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        ax.semilogx()
        ax.semilogy()
        ax.set_xlabel(xlabel)
        if nuInu:
            ax.set_ylabel(r"$\nu \mathrm{I}_\nu\,\mathrm{[erg\,cm^{-2}\,s^{-1}\,sr^{-1}]}$")
        else:
            ax.set_ylabel(r"$\mathrm{I}_\nu\,\mathrm{[erg\,cm^{-2}\,s^{-1}\,sr^{-1}\,Hz^{-1}]}$")

        if second_xaxis:
            ax.tick_params(axis="x", which="both", top=False, bottom=True)

            def eV_to_micron(x):
                return (x * u.eV).to(u.micron, equivalencies=u.spectral()).value

            def micron_to_eV(x):
                return (x * u.micron).to(u.eV, equivalencies=u.spectral()).value

            if xunit == "eV":
                secax = ax.secondary_xaxis("top", functions=(eV_to_micron, micron_to_eV))
                secax.set_xlabel(r"wavelength [$\mu$m]")
            else:
                secax = ax.secondary_xaxis("top", functions=(micron_to_eV, eV_to_micron))
                secax.set_xlabel(r"energy [eV]")

        if showInuBand or showInuInterpol:
            self._legend(ax, **kwargs)

        self._dokwargs(ax, **kwargs)

        return self._closefig(fig)

    def plot_sed(
        self,
        model,
        plot_starSpec=True,
        incidx=0,
        unit="erg",
        sedObs=None,
        reddening=False,
        ax=None,
        **kwargs,
    ):
        """
        Plots the sed(s) including the stellar spectrum and observations (last two are optional).

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data. Only required if wl,ident and or lineObs are passed.

        plot_starSpec : boolean
          also show the (unobscured) stellar spectrum. Default: True

        incidx : int or array_like(ndim=1)
          which inclination (index) should be used for plotting (0 is the first one and default).
          If it is a single value only the profile for that inclination index is plotted.

          If it is an array of values all profiles for that chosen inclinations are plotted.
          If `incidx=[]` profiles for all inclinations will be plotted. Test

        unit : str
          in what unit should the sed be plotted. Possible values: `erg`, `W`, `Jy`, `mJy`

        sedObs : :class:`~prodimopy.read.DataContinuumObs`
          if  :attr:`~prodimopy.read.Data_ProDiMo.sedObs` (e.g. sedObs=model.sedOBS) is provided
          also the observational data is plotted. But in principal can be any object of type
          :class:`~prodimopy.read.DataContinuumObs`.

        reddening : boolean or str
          If True also apply the reddening of the SED using the given A_V value from the
          provided observational data (`sedObs`). If `reddening` is a string the according extinction
          model is used in :func:`~prodimopy.read.DataSED.extinction`.

        """
        print("PLOT: plot_sed ...")
        fig, ax = self._initfig(ax, **kwargs)

        xmin = 0.1
        if model.sed is None:
            return

        if not isinstance(incidx, (collections.abc.Sequence, np.ndarray)):
            incidx = [incidx]
        # just for convenience if it is an empty array take all the inclinations
        elif len(incidx) == 0:  # empty array, plot all inclinations
            # need the line for that
            incidx = np.arange(len(model.sed._inclinations))
        else:
            # make sure that in that case only one inclinations is done
            incidx = [0]

        dist = ((model.sed.distance * u.pc).to(u.cm)).value

        if plot_starSpec:
            # scale input Stellar Spectrum to the distance for comparison to the SED
            r = ((model.star.r * u.R_sun).to(u.cm)).value

            xStar = model.star.lam[0::1]
            yStar = (model.star.nu * model.star.Inu)[0::1]
            yStar = yStar * (r**2.0 * math.pi * dist ** (-2.0))

            if unit == "W":
                yStar = (yStar * u.erg / (u.s * u.cm**2)).to(u.Watt / u.m**2).value
            elif "Jy" in unit:
                yStar = (model.star.Inu)[0::1]
                yStar = yStar * (r**2.0 * math.pi * dist ** (-2.0))
                yStar = (yStar * u.erg / (u.s * u.cm**2 * u.Hz)).to(u.Jy).value
                if unit == "mJy":
                    yStar = yStar * 1000

            ax.plot(xStar, yStar, color="black")

        # plot it for all selected inclinations
        for iinc in incidx:
            # to be sure we have the right inclination
            model.sedinc(incidx=iinc)

            incstr = r"$i=" + "{:3.1f}".format(model.sed.inclination) + r"^\degree$"

            # only use every 5 element to speed up plotting
            x = model.sed.lam
            if unit == "W":
                y = model.sed.nuFnuW
            elif "Jy" in unit:
                y = model.sed.fnuJy
                if unit == "mJy":
                    y = y * 1000
            else:
                y = model.sed.nu * model.sed.fnuErg

            ymin = np.min(y[model.sed.lam > 1])

            if (
                reddening
                or type(reddening) is str
                and sedObs is not None
                and sedObs.A_V is not None
            ):
                if type(reddening) is str:
                    y = y * model.sed.extinction(sedObs, extmodel=reddening)
                else:
                    y = y * model.sed.extinction(sedObs)

            # plot the SED
            ax.plot(x, y, marker=None, label=incstr)

        if sedObs is not None:
            okidx = np.where(sedObs.flag == "ok")

            xsedObs = sedObs.lam
            ysedObs = sedObs.nu * sedObs.fnuErg
            ysedObsErr = sedObs.nu * sedObs.fnuErgErr

            if unit == "W":
                ysedObs = sedObs.nu * ((sedObs.fnuJy * u.Jy).si.value)
                ysedObsErr = sedObs.nu * ((sedObs.fnuJyErr * u.Jy).si.value)
            elif "Jy" in unit:
                ysedObs = sedObs.fnuJy
                ysedObsErr = sedObs.fnuJyErr
                if unit == "mJy":
                    ysedObs = ysedObs * 1000
                    ysedObsErr = ysedObsErr * 1000

            # ax.plot(sedObs.lam[okidx],sedObs.nu[okidx]*sedObs.fnuErg[okidx],linestyle="",marker="x",color="0.5",ms=3)
            ax.errorbar(
                xsedObs[okidx],
                ysedObs[okidx],
                yerr=ysedObsErr[okidx],
                fmt="o",
                color="0.5",
                ms=2,
                linewidth=1.0,
                zorder=0,
            )

            ulidx = np.where(sedObs.flag == "ul")
            ax.plot(xsedObs[ulidx], ysedObs[ulidx], linestyle="", marker="v", color="0.5", ms=2.0)

            if sedObs.specs is not None:
                for spec in sedObs.specs:
                    if unit == "W":
                        nu = (spec[:, 0] * u.micrometer).to(u.Hz, equivalencies=u.spectral()).value
                        f = (spec[:, 1] * u.Jy).si.value
                        fErr = (spec[:, 2] * u.Jy).si.value
                    elif "Jy" in unit:
                        f = spec[:, 1]
                        fErr = spec[:, 2]
                        if unit == "mJy":
                            f = f * 1000
                            fErr = fErr * 1000
                    else:
                        nu = (spec[:, 0] * u.micrometer).to(u.Hz, equivalencies=u.spectral()).value
                        f = (spec[:, 1] * u.Jy).cgs.value
                        fErr = (spec[:, 2] * u.Jy).cgs.value

                    # set fErr to a fraction of f if it is zero, otherwise the fill betweeen is not working
                    fErr[fErr == 0] = f[fErr == 0] * 1.0e-4
                    lowf = f - fErr
                    highf = f + fErr

                    if unit == "W" or unit == "erg":
                        lowf = lowf * nu
                        highf = highf * nu
                        f = f * nu

                    # use a combination of fill_between and plot, works better than errorbar
                    ax.fill_between(spec[:, 0], lowf, highf, color="0.8")
                    ax.plot(spec[:, 0], f, linestyle="-", linewidth=0.5, color="0.5", zorder=2000)

        # set defaults, can be overwritten by the kwargs
        ax.set_xlim([xmin, None])
        ax.set_ylim([ymin, None])
        ax.semilogx()
        ax.semilogy()
        ax.set_xlabel(r"wavelength [$\mathrm{\mu}$m]")
        if unit == "W":
            ax.set_ylabel(r"$\mathrm{\lambda F_{\lambda}\,[W\,m^{-2}]}$")
        elif unit == "Jy":
            ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")
        elif unit == "mJy":
            ax.set_ylabel(r"$\mathrm{flux\,[mJy]}$")
        else:
            ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")
        #    ax.yaxis.tick_right()
        #    ax.yaxis.set_label_position("right")
        if len(incidx) > 1:  # backward compatibility, dont show lables if only one inclination
            ax.legend()

        self._dokwargs(ax, **kwargs)

        return self._closefig(fig)

    def _getSEDana_boxpoints(self, lam, model, zr=True):
        """
        Creates an array of (x,y) coordinates representing the emission origin for
        the SEDana which can be used or the given wavelength. Those coordinates can
        be used to draw a box on a plot (e.g. can be passed to a matplotlib Polygon)
        to draw a box (Polygon).

        Parameters
        ----------
        lam : float
          the wavelength for which the emission origin should be calculated

        model : :class:`prodimopy.read.Data_ProDiMo`
          the |prodimo| model including the SED analysis data (SEDana)

        zr : boolean
          If `zr==True` (default) then the z coordinate of the points is returned in
          z/r units. Optional parameter.

        Returns
        -------
        array_like(float,ndim=1) :
          list of (x,y) points (in au). if zr=True the z coordinate is in z/r units.


        TODO: maybe merge somehow with :func:`~prodimopy.Data_ProDiMo.getSEDAnaMask`
        """
        # interpolate
        sedAna = model.sed.sedAna

        r15 = interp1d(sedAna.lams, sedAna.r15, bounds_error=False, fill_value=0.0, kind="linear")(
            lam
        )
        r85 = interp1d(sedAna.lams, sedAna.r85, bounds_error=False, fill_value=0.0, kind="linear")(
            lam
        )
        xi15 = np.argmin(np.abs(model.x[:, 0] - r15))
        xi85 = np.argmin(np.abs(model.x[:, 0] - r85))

        z85s = [
            [
                model.x[ix, 0],
                interp1d(
                    sedAna.lams,
                    sedAna.z85[:, ix],
                    bounds_error=False,
                    fill_value=0.0,
                    kind="linear",
                )(lam),
            ]
            for ix in range(xi15, xi85)
        ]
        z15s = [
            [
                model.x[ix, 0],
                interp1d(
                    sedAna.lams,
                    sedAna.z15[:, ix],
                    bounds_error=False,
                    fill_value=0.0,
                    kind="linear",
                )(lam),
            ]
            for ix in range(xi85 - 1, xi15 - 1, -1)
        ]
        points = z85s + z15s

        for point in points:
            if zr is True:
                point[1] = point[1] / point[0]

        return points

    def plot_sedAna(
        self,
        model,
        lams=[1.0, 3.0, 6.0, 10.0, 30.0, 60.0, 100.0, 200.0, 1000.0],
        field=None,
        label=None,
        boxcolors=None,
        zlog=True,
        zlim=[None, None],
        zr=True,
        clevels=None,
        clabels=None,
        extend="neither",
        oconts=None,
        nbins=70,
        bgcolor=None,
        cb_format="%.1f",
        scalexy=[1, 1],
        patches=None,
        rasterized=False,
        ax=None,
        **kwargs,
    ):
        """
        Plots the SED analysis stuff (origin of the emission).

        Parameters
        ----------
        model : :class:`prodimopy.read.Data_ProDiMo`
          the |prodimo| model.

        lams : array_like(float,ndim=1)
          list of wavelengths in micrometer.

        field : array_like(float,ndim=2)
          And array with dimension (nx,nz) with values that should be plotted as filled contours.
          `DEFAULT:` the `nHtot` field of :class:`prodimopy.read.Data_ProDiMo`.


        """
        print("PLOT: plot_sedAna ...")

        if boxcolors is None:
            boxcolors = list(self.pcolors.values())

        if patches is None:
            patches = list()

        ibox = 0
        for lam in lams:
            points = self._getSEDana_boxpoints(lam, model, zr=True)
            if len(points) > 0:
                patch = mpl.patches.Polygon(
                    points,
                    closed=True,
                    fill=False,
                    color=boxcolors[ibox],
                    zorder=100,
                    linewidth=2.0,
                )
                patches.append(patch)
            else:
                print("WARN: Could not create box for lam=", str(lam))
            ibox += 1

        if field is None:
            field = "nHtot"
            oconts = [Contour(model.AV, [1], linestyles="--", colors=self.pcolors["gray"])]

        fig = self.plot_cont(
            model,
            field,
            label=label,
            zlog=zlog,
            zlim=zlim,
            zr=zr,
            clevels=clevels,
            clabels=clabels,
            contour=False,
            extend=extend,
            oconts=oconts,
            nbins=nbins,
            bgcolor=bgcolor,
            cb_format=cb_format,
            scalexy=scalexy,
            patches=patches,
            rasterized=rasterized,
            returnFig=True,
            ax=ax,
            **kwargs,
        )

        ax = fig.axes[0]

        ibox = 0
        for lam in lams:
            ax.text(
                0.02,
                0.92 - ibox / 18.0,
                "$" + "{:5.1f}".format(lam) + r"\,\mathrm{\mu m}$",
                horizontalalignment="left",
                verticalalignment="bottom",
                fontsize=6,
                transform=ax.transAxes,
                color=boxcolors[ibox],
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"),
            )
            ibox += 1

        self._dokwargs(ax, **kwargs)

        return self._closefig(fig)

    def plot_taulines(self, model, lineIdents, showCont=True, ax=None, **kwargs):
        """
        Plots the line optical depth as a function of radius for the given lines.
        The lines are identified via a list of lineIdents containt of an array with
        ident and wavelength of the line e.g. ["CO",1300.0].
        It searches for the closest lines.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        lineIdents : array_like()
          list of line identifactors of the form `[["ident",wl],["ident2",wl2]]`.

        TODO: there are no options for linestyles and colors yet (the defaults are used).
        """
        print("PLOT: plot_taulines ...")
        fig, ax = self._initfig(ax, **kwargs)

        # if it is only one line (no list of list) make it a list
        if type(lineIdents[0]) is str:
            lineIdents = [lineIdents]

        xmin = 1.0e100
        xmax = 0

        iplot = 0
        for lineIdent in lineIdents:
            x = model.x[:, 0]
            lineEstimate = model.getLineEstimate(lineIdent[0], lineIdent[1])

            ax.axhline(y=1.0, linestyle="-", color="black", linewidth=0.5)
            label = (
                r"$\mathrm{"
                + spnToLatex(lineEstimate.ident)
                + "}$ "
                + "{:.2f}".format(lineEstimate.wl)
                + r" $\mathrm{\mu m}$"
            )

            (line,) = ax.plot(
                x, [dum.tauLine for dum in lineEstimate.rInfo], marker=None, label=label
            )

            if showCont:
                ax.plot(
                    x,
                    [dum.tauDust for dum in lineEstimate.rInfo],
                    marker=None,
                    linestyle="--",
                    color=line.get_color(),
                )

            iplot = iplot + 1

            if min(x) < xmin:
                xmin = min(x)
            if max(x) > xmax:
                xmax = max(x)

        ax.set_xlim(xmin, xmax)

        ax.semilogx()
        ax.semilogy()

        ax.set_xlabel(r"r [au]")
        ax.set_ylabel(r"$\mathrm{\tau_{line}}$")

        self._dokwargs(ax, **kwargs)
        self._legend(ax, **kwargs)

        return self._closefig(fig)

    def plot_lineprofile(
        self,
        model: pread.Data_ProDiMo | None = None,
        wl: float | None = None,
        ident: str | None = None,
        lineObj: pread.DataLine | None = None,
        linetxt=None,
        lineObs=None,
        incidx=0,
        lw=None,
        line_styles: list[str] | str | None = None,
        unit: str | None = None,
        normalized=False,
        convolved=False,
        removecont=True,
        style=None,
        color=None,
        ax=None,
        **kwargs,
    ):
        """
        Plots the line profile for the given line (id wavelength and optionally the line ident)

        Parameters
        ----------
        model :
          The model data. Required if ``wl``,``ident`` and/or ``lineObs`` are passed.

        wl :
          The wavelength of the line in micrometer. The line closest to `wl` is plotted.

        ident :
          The optional line ident which is additionally use to identify the line.

        lineObj :
          The full line data. In that case ``model``, ``wl`` and ``ident`` are ignored

        linetxt : str
          A string that is used as the label for the line.

        lineObs : array_like(ndim=1)
          list of :class:`~prodimopy.read.DataLineObs` objects. Must be consistent with the list of
          lines from the line radiative transfer.

        incidx : int or array_like(ndim=1)
          which inclination (index) should be used for plotting (0 is the first one and default).
          If it is a single value only the profile for that inclination index is plotted.

          If it is an array of values all profiles for that chosen inclinations are plotted.
          If `normalized=True` the profiles will be normalized to the first one, in that case.
          If `incidx=[]` profiles for all inclinations will be plotted.

          If lineObj is passed only one inclination (the one set in that obj) will be plotted.

        lw : float
          The line width of the plotted profiles. Default: `None` (i.e. use default value).
          Can be usefull for multiple inclinations plots, where the default value might be to thick.

        line_styles :
          The line style of the plotted profiles. Default: `None` (i.e. use default value).
          If a scalar style is applied to all lines. If it is an array the styles are applied in order
          to the plotted lines (i.e. must have the same length as `incidx`).

        unit : str
          In what unit should the line flux be plotted (see :func:`~prodimopy.read.DataLineProfile.flux_unit`).
          if ``None`` the current unit of the line profile is used.

        normalized : boolean
          if `True` normalize the profile to the peak flux

        convolved : boolean
          if `True` plot the convolved profile.

        removecont : boolean
          if `True` remove the continuum from the profile. Default: `True`

        color : str
          the color for the plotted profile.

        style : str
          if style is `step` the profile is plotted as a step function assuming
          the values are the mid point of the bin.

        """
        print("PLOT: plot_line_profile ...")
        fig, ax = self._initfig(ax, **kwargs)

        # first need a line object to properly init incidx.
        # if lineObj is passed incidx is ignored
        if lineObj is None:
            line = model.getLine(wl, ident=ident)
            if line is None:
                print("WARN: line " + str(ident) + " at " + str(line.wl) + " micron not found")

            if not isinstance(incidx, (collections.abc.Sequence, np.ndarray)):
                incidx = [incidx]
            # just for convenience if it is an empty array take all the inclinations
            elif len(incidx) == 0:
                # need the line for that
                incidx = np.arange(len(line._inclinations))
        else:
            # make sure that in that case only one inclinations is done
            incidx = [0]

        # ignore the color attribute in that case.
        # could also use an array of colors to allow the user to chose, but
        # for now color is only used if a single profile is used.
        if len(incidx) > 1:
            color = None

        if line_styles is not None:
            if not isinstance(line_styles, list):
                line_styles = [line_styles] * len(incidx)
            elif len(line_styles) != len(incidx):
                print(
                    "WARN: number of line styles does not match number of inclinations, ignoring line styles"
                )
                line_styles = None

        # plot it for all selected inclinations
        for i, iinc in enumerate(incidx):
            if lineObj is None:
                line = model.getLine(wl, ident=ident, incidx=iinc)
                if line is None:
                    print("WARN: line " + str(ident) + " at " + str(line.wl) + " micron not found")
            else:
                line = lineObj

            incstr = f"$i={line.inclination:.4g}^\\degree$"

            x = line.profile.velo
            old_flux_unit = line.profile.flux_unit
            if unit is not None and not normalized:
                line.profile.flux_unit = unit

            if convolved:
                y = line.profile.flux_conv
                if removecont:
                    y = y - line.profile.flux_conv[0]
            else:
                y = line.profile.flux
                if removecont:
                    y = y - line.profile.flux[0]

            if normalized:
                if i == 0:  # always normalize to the first inclination
                    norm = np.max(y)
                y = y / norm

            if linetxt is None:
                if ident is not None:
                    linetxt = ident
                else:
                    linetxt = line.species
                linetxt = linetxt + "@" + "{:.2f}".format(line.wl) + r" $\mathrm{\mu m}$"

            if line_styles is not None:
                style = line_styles[i]
            else:
                style = None

            if style == "step":
                ax.step(x, y, marker=None, label=incstr, where="mid", color=color, lw=lw, ls=style)
            else:
                ax.plot(x, y, marker=None, label=incstr, color=color, lw=lw, ls=style)

            # set back the flux unit
            line.profile.flux_unit = old_flux_unit

        # plot the observed line profile if it exists
        if lineObs is not None:
            lineIdx = model._getLineIdx(wl, ident=ident)

            lineO = lineObs[lineIdx]
            if lineO.profile is not None:
                x = lineO.profile.velo

                old_flux_unit_obs = lineO.profile.flux_unit
                if unit is not None:
                    lineO.profile.flux_unit = unit

                y = lineO.profile.flux  # remove the continuum

                if normalized:
                    y = y / np.max(y)

                # FIXME: also need a conversion for profileErr
                if lineO.profileErr is not None:
                    ax.fill_between(
                        x, y - lineO.profileErr, y + lineO.profileErr, color="0.8", zorder=0
                    )

                ax.plot(x, y, marker=None, color="black", label="Obs. ", zorder=0)
                lineO.profile.flux_unit = old_flux_unit_obs

        if normalized:
            ax.set_ylabel("normalized flux")
        else:
            # FIXME: find a nicer solution (maybe some function to string for the units)
            if line.profile.flux_unit == "ErgAng":
                ax.set_ylabel(r"$\mathrm{flux\,[erg s^{-1}cm^{-2}\AA^{-1}]}$")
            elif line.profile.flux_unit == "mJy":
                ax.set_ylabel(r"$\mathrm{flux\,[mJy]}$")
            else:
                ax.set_ylabel(r"$\mathrm{flux\,[Jy]}$")

        ax.set_xlabel("velocity [km/s]")

        ax.text(
            0.03,
            0.955,
            linetxt,
            fontsize=7.0,
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
            color=self.pcolors["gray"],
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="0"),
        )

        self._dokwargs(ax, **kwargs)
        self._legend(ax, **kwargs)

        return self._closefig(fig)

    def plot_lines(
        self,
        model,
        lineIdents,
        useLineEstimate=True,
        jansky=False,
        showBoxes=True,
        lineObs=None,
        lineObsLabel="Obs.",
        peakFlux=False,
        showCont=False,
        xLabelGHz=False,
        showGrid=True,
        **kwargs,
    ):
        """
        Plots a selection of lines or lineEstimates.

        See :func:`~prodimopy.plot.PlotModels.plot_lines` for more details.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        lineIdents : array_like
          a list of line identifiers. Each entry should contain `["ident",wl]`
          (e.g. `["CO",1300],["CO",800]]`. Those values are passed to
          :func:`~prodimopy.Data_ProDiMo.getLineEstimate`. The order of the lineIdents also
          defines the plotting order of the lines (from left to right)


        """
        print("PLOT: plot_lines ...")

        # need the instance
        ppm = prodimopy.plot_models.PlotModels(None, markers=["x"])
        fig = ppm.plot_lines(
            [model],
            lineIdents,
            useLineEstimate=useLineEstimate,
            jansky=jansky,
            showBoxes=showBoxes,
            lineObs=lineObs,
            lineObsLabel=lineObsLabel,
            peakFlux=peakFlux,
            showCont=showCont,
            xLabelGHz=xLabelGHz,
            showGrid=showGrid,
            **kwargs,
        )

        return self._closefig(fig)

    def plot_heat_cool(self, model, zr=True, oconts=None, showidx=(0, 0), **kwargs):
        """
        Plots the dominant heating and cooling processes.

        The initial python code for this routine is from Frank Backs

        Parameters
        ----------

        model : :class:`~prodimopy.read.Data_ProDiMo`
          the model data

        zr : boolean
          use z/r for y axis Default: True

        oconts : array_like(:class:`~prodimopy.plot.Contour`,ndim=1)
          list of :class:`~prodimopy.plot.Contour` objects which will be drawn
          contours (like in :func:`~prodimopy.plot.Plot.plot_cont`.

        showidx : tuple(ndim=1)
          Default is (0,0): will show the most dominant heating and cooling process.
          For example (1,1) will show the second most dominant heating and cooling process.
          For example (-1,-1) will show the least dominant heating and cooling process.


        .. todo::

          * possibility to have different oconts for the heating and cooling figures
          * possibility to map certain heating/cooling processes always to the same color

        """
        print("PLOT: plot_heat_cool ...")

        colors = np.array(
            [
                (230, 25, 75),
                (60, 180, 75),
                (255, 225, 25),
                (0, 130, 200),
                (245, 130, 48),
                (145, 30, 180),
                (70, 240, 240),
                (240, 50, 230),
                (210, 245, 60),
                (250, 190, 190),
                (0, 128, 128),
                (230, 190, 255),
                (170, 110, 40),
                (255, 250, 200),
                (128, 0, 0),
                (170, 255, 95),
                (128, 128, 0),
                (255, 215, 180),
                (0, 0, 128),
                (128, 128, 128),
                (0, 0, 0),
                (220, 220, 220),
            ],
            dtype=float,
        )
        colors /= 255

        if zr:
            z = model.z / model.x
        else:
            z = model.z

        # used for plotting
        max_idx = np.zeros(shape=(model.nx, model.nz), dtype="int16")

        # heat_mainidx=model.heat_mainidx
        # cool_mainidx=model.cool_mainidx

        # sort the heat/cool .. this allows to also plot e.g. the second most
        # important etc. i.e. differently to using heat_mainidx from ProDiMo.out

        # sortidx is  most important one first +1 to be consistent with
        # model_heatmainidx from ProDiMo.out ... makes checking easier
        heat_mainidx = np.flip(np.argsort(model.heat, axis=2), axis=2)[:, :, showidx[0]] + 1
        cool_mainidx = np.flip(np.argsort(model.cool, axis=2), axis=2)[:, :, showidx[1]] + 1

        # list of all the dominant heating processes

        idxlisth, idxlisth_counts = np.unique(heat_mainidx, return_counts=True)
        idxlistc, idxlistc_counts = np.unique(cool_mainidx, return_counts=True)

        # sort it descending
        idxlisth = idxlisth[np.argsort(idxlisth_counts)[::-1]]
        idxlistc = idxlistc[np.argsort(idxlistc_counts)[::-1]]

        sfigs = [2.0, 1.6]
        if "sfigs" in kwargs:
            sfigs = kwargs["sfigs"]

        # build title strings
        titles = list()
        for idx, tit in zip(showidx, ["heating processes", "cooling processes"]):
            # FIXME: (somehow) least impo
            if idx == -1:
                titles.append("least important " + tit)
            elif idx == 0:
                titles.append("dominant " + tit)
            elif idx > 0 and idx < 3:
                titles.append(str(idx + 1) + "nd most dominant " + tit)
            elif idx >= 3:
                titles.append(str(idx + 1) + "th most dominant " + tit)
            else:
                titles.append(str(idx) + " (idx) " + tit)

        fig, axarr = plt.subplots(1, 2, figsize=self._sfigs(sfigs=sfigs))
        plt.subplots_adjust(bottom=0.32)
        axh = axarr[0]
        axc = axarr[1]

        if len(idxlisth) > len(colors):
            print("WARN: too many heating processes, do not show the least important ones:")
            for i in range(len(colors), len(idxlisth)):
                print("   ", model.heat_names[idxlisth[i] - 1])

        # this if for the labels, and also maps the colors to the names
        for i in range(min(len(idxlisth), len(colors))):
            # -1 because python starts at zero
            axh.scatter(0, 0, marker="s", color=colors[i], label=model.heat_names[idxlisth[i] - 1])

            # this is necessary to have the fields with increasing number without
            # gaps, otherwhise the colormapping in pcolormesh does not work
            max_idx[heat_mainidx == idxlisth[i]] = i

        cMap = mpl.colors.ListedColormap(colors[0 : len(idxlisth) - 1])
        with warnings.catch_warnings():
            # ignore this warning, as the plot looks fine
            warnings.filterwarnings(
                "ignore",
                category=Warning,
                message=r".*to pcolormesh are interpreted as cell centers, but.*",
            )
            axh.pcolormesh(model.x, z, max_idx, linewidth=0, cmap=cMap, rasterized=True)
        axh.legend(
            loc="upper center", bbox_to_anchor=(0.5, -0.175), ncol=2, frameon=False, fontsize=5.5
        )

        axh.set_title(titles[0])

        # now for the cooling
        if len(idxlistc) > len(colors):
            print("WARN: too many cooling processes, do not show the least important ones:")
            for i in range(len(colors), len(idxlistc)):
                print("   ", model.cool_names[idxlistc[i] - 1])

        # this if for the labels, and also maps the colors to the names
        for i in range(min(len(idxlistc), len(colors))):
            # -1 because python starts at zeror
            axc.scatter(0, 0, marker="s", color=colors[i], label=model.cool_names[idxlistc[i] - 1])

            # this is necessary to have the fields with increasing number without
            # gaps, otherwhise the colormapping in pcolormesh does not work
            max_idx[cool_mainidx == idxlistc[i]] = i

        cMap = mpl.colors.ListedColormap(colors[0 : len(idxlistc) - 1])
        with warnings.catch_warnings():
            # ignore this warning, as the plot looks fine
            warnings.filterwarnings(
                "ignore",
                category=Warning,
                message=r".*to pcolormesh are interpreted as cell centers, but.*",
            )
            axc.pcolormesh(model.x, z, max_idx, linewidth=0, cmap=cMap, rasterized=True)

        axc.legend(
            loc="upper center", bbox_to_anchor=(0.5, -0.175), ncol=2, frameon=False, fontsize=5.5
        )
        axc.set_title(titles[1])

        for ax in [axh, axc]:
            # axis equal needs to be done here already ... at least it seems so
            if "axequal" in kwargs:
                if kwargs["axequal"]:
                    ax.axis("equal")

            ax.set_xlim(np.min(model.x), None)
            ax.semilogx()
            ax.set_xlabel("r [au]")
            if zr:
                ax.set_ylim(0, None)
                ax.set_ylabel("z/r")
            else:
                ax.set_ylabel("z [au]")

            # Additional Contours, plot for both plots at the moment
            if oconts is not None:
                for cont in oconts:
                    ACS = ax.contour(
                        model.x,
                        z,
                        cont.field,
                        levels=cont.levels,
                        colors=cont.colors,
                        linestyles=cont.linestyles,
                        linewidths=cont.linewidths,
                    )
                    if cont.showlabels:
                        ax.clabel(
                            ACS,
                            inline=True,
                            inline_spacing=cont.label_inline_spacing,
                            fmt=cont.label_fmt,
                            manual=cont.label_locations,
                            fontsize=cont.label_fontsize,
                        )

        # need to remove the title, as it does not fit here
        if self.title is not None:
            if self.title.strip() != "":
                fig.suptitle(self.title.strip())

        # remove title so that it does not show up onthe individual panels
        self._dokwargs(axh, notitle=True, **kwargs)
        self._dokwargs(axc, notitle=True, **kwargs)

        return self._closefig(fig)

    def plot_contImage(
        self,
        model,
        wl,
        iinc=0,
        zlim=[None, None],
        cmap="inferno",
        rlim=[None, None],
        cb_show=True,
        cb_fraction=0.15,
        ax=None,
        **kwargs,
    ):
        """
        Simple plot for the continuum Images as produced by PRoDiMo.
        (The output in image.out).

        The scale is fixed to LogNorm at the moment.

        Parameters
        ----------
        model : :class:`~prodimopy.read.Data_ProDiMo`
          The model data.

        wl : float
          The wavelength in micron for which we should plot the image. The routine simple
          selected the closest one to the given image.

        iinc : int
          the inclination index in case of multiple inclinations. Default ``iinc=0``

        zlim : array_like(ndim=1)
          the min and max value for the data to plot. Optional.

        rlim : array_like(ndim=1)
          the extension of the image eg. rlim[-1,1] plot the x and y coordinate from
          -1 to 1 au. Optional

        cmap : str
          The name of a matplotlib colormap. Optional.

        cb_show : boolean
          show colorbar or not. Optional.

        cb_fraction : float
          fractoin of the image use for the colorbar. Useful for subplots. Optional

        """
        contImages = model.contImages
        x,y,tmpImg, wl = contImages.getImage(wl, iinc=iinc)
        image = np.copy(tmpImg)

        # not very elegant, but need to extend the array otherwise the contourf routine is not "closing" the image
        x = np.hstack((x, x[:, 0:1]))
        y = np.hstack((y, y[:, 0:1]))
        imagepl = np.hstack((image, image[:, 0:1]))

        vmin = zlim[0]
        vmax = zlim[1]

        # set some default values if required
        if vmax is None:
            vmax = np.max(imagepl) / 2.0
        if vmin is None:
            vmin = np.max([np.min(imagepl), vmax / 1.0e6])

        fig, ax = self._initfig(ax, **kwargs)

        norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
        levels = np.logspace(np.log10(vmin), np.log10(vmax), 100)

        CS = ax.contourf(x, y, imagepl, norm=norm, cmap=cmap, levels=levels, extend="both")

        # FIXME: that might not work for all colormaps
        ax.set_facecolor("black")
        ax.axis("equal")
        ax.set_xlim(rlim)
        ax.set_ylim(rlim)
        ax.set_aspect("equal", "box")
        ax.set_xlabel("x [au]")
        ax.set_ylabel("y [au]")
        # FIXME: not good to directly access _inclinations
        ax.set_title(
            r"$\lambda= {:6.2f}\, \mu m; \, i={:3.1f}^\circ$".format(
                wl, contImages._inclinations[iinc]
            ),
            pad=0,
        )

        for spine in ax.spines.values():
            spine.set_color("white")
        ax.tick_params(color="white", which="both")

        if cb_show:
            axcb = np.array(fig.get_axes()).ravel().tolist()
            CB = fig.colorbar(CS, ax=axcb, pad=0.01, format="%3.1e", fraction=cb_fraction)
            CB.set_label(r"$I_\mathrm{\nu}\,[erg/cm^2/s/Hz/sr]$")

        self._dokwargs(ax, **kwargs)

        return self._closefig(fig)

    def plot_sled(self, models, lineIdents, units="W", ax=None, title="SLED", **kwargs):
        """
        Plots the Spectral Line Energy Distribution

        Parameters
        ----------
        models : list(:class:`~prodimopy.read.Data_ProDiMo`)
                or a single model
          the model(s) to plot

        lineIdents : array_like
          a list of line identifiers. Examples

          `lineIdents = ['CO']`

          `lineIdents = ['CO', 'o-H2', 'p-H2O']`

        units : str, optional
          In which units should be plotted.
          Allowed values: `erg` [erg/s/cm^2], `W` [W/m^2]
          default : `W`

        Example
        -------

        In the directory of the |prodimo| model

        .. code-block:: python

           from matplotlib.backends.backend_pdf import PdfPages
           import prodimopy.plot as pplot
           import prodimopy.read as pread

           outfile = "out_test.pdf"
           model=pread.read_prodimo()

           with PdfPages(outfile) as pdf:
             pp=pplot.Plot(pdf, title=model.name)
             pp.plot_sled(model, ["CO", "o-H2"])
        """

        print("PLOT: plot_sled ...")

        if not isinstance(models, list):
            models = [models]

        if units == "erg":
            # 1 erg/s/cm2 = 1000 W/m2
            flux_correction = 1e3
        else:
            flux_correction = 1.0

        fig, ax = self._initfig(ax, **kwargs)

        iplot = 0
        xmin = 1.0e100
        xmax = 0
        ymin = 1.0e100
        ymax = -1.0e00
        for model in models:
            for sp in lineIdents:
                lests = model.selectLineEstimates(sp)
                if lests != "":
                    lam, flux = [], []
                    for lest in lests:
                        lam.append(lest.wl)
                        flux.append(lest.flux)

                x = np.array(lam)  # micron
                y = np.array(flux) * flux_correction  # u.W / u.m**2

                # line flux estimates can be negative
                # aka absorption lines
                ythres = 1e-30
                wneg = y <= 0.0
                y[wneg] = ythres

                # if we only have one ident, but mutliple models the name of the model is more useful
                if len(lineIdents) == 1:
                    label = model.name
                else:
                    label = sp

                ax.scatter(x, y, s=1, alpha=0.5, label=label)

                if min(x) < xmin:
                    xmin = 0.5 * min(x)
                if max(x) > xmax:
                    xmax = 5.0 * max(x)
                if min(y) < ymin:
                    ymin = 0.5 * min(y)
                if max(y) > ymax:
                    ymax = 10.0 * max(y)

            iplot = iplot + 1
            if iplot == 0:
                return

            # set defaults, can be overwritten by the kwargs
            if ymin < 1e-30:
                ymin = ythres
            ax.set_xlim(xmin, xmax)
            ax.set_ylim([ymin, ymax])
            ax.semilogx()
            ax.semilogy()
            ax.set_title(title)
            ax.set_xlabel(r"wavelength [$\mu$m]")
            if units == "W":
                ax.set_ylabel(r"$\mathrm{\lambda F_{\lambda}\,[W\,m^{-2}]}$")
            else:
                ax.set_ylabel(r"$\mathrm{\nu F_{\nu}\,[erg\,cm^{-2}\,s^{-1}]}$")

        self._dokwargs(ax, **kwargs)

        self._legend(ax, **kwargs)

        return self._closefig(fig)

    @deprecated("This routine is deprected please use plot_reaccont instead.")
    def plot_reac(
        self,
        model,
        chemistry,
        rtype,
        level=1,
        plot_size=10,
        lograte=True,
        grid=True,
        with_abun=False,
        vmin=None,
        **kwargs,
    ):
        """
        Plots the 2D main formation/destruction reaction structure for a given species,
        in each grid point. Each number corresponds to the reaction indices in
        `prodimo.read.chemistry.sorted_form_info` or `prodimo.read.chemistry.sorted_form_info`

        By default it is plotted along the 2D main formation/reaction rate structure, but it
        can also be plotted along the abundance of the species.

        The routine checks if the reaction type is set
        plots the data (lograte, rate or abundance) as an image, and fills in the reaction
        indices for each grid point.

        An index of 0 means that the total rate at that point was so low it didn't get
        registered in chemanalysis.out (in |prodimo|)

        Contributors: G. Chaparro, Ch. Rab

        Parameters
        ----------
        model : :class:`prodimopy.read.Data_ProDiMo`
          the model data

        chemistry : class:`prodimopy.read.Chemistry`
          data resulting from `prodimopy.read.analise_chemistry` on a single species

        rtype : str
          keyword which sets the type of reactions to be shown (destruction or formation)
          must be set to either 'd' (destruction) or 'f' (formation)

        level : int
          1 means most important, 2 second most important etc.

        plot_size : int
          plot size, it is set to square for now

        lograte : bool
          plot log rate instead of rate, default to True (the difference are more noticeable)

        grid : bool
          plot nx,ny instead of r, z, default to False

        with_abun : bool
          plot abundance instead of formation or destruction rate, overrides lograte,
          default to False

        vmin : float
          sets the minimum value for `plt.imshow` (abundance, rate or lograte)
          default min(array)

        """
        print("PLOT: plot_reac ...")
        print("WARN: this routine is deprected please use plot_reaccont instead.")

        fig, ax = plt.subplots(figsize=(plot_size, plot_size))

        # label='main '
        # label+=r"$\mathrm{"+spnToLatex(chemistry.species)+"}$"
        splabel = r"$\mathrm{" + spnToLatex(chemistry.species) + "}$"

        if rtype == "f":
            # data=chemistry.farray.T
            data = chemistry.totfrate.T  # transpose because of imshow
            reacs = chemistry.get_reac_grid(level, "f")[0]
            label = r"(total formation rate) $[cm^{-3} s^{-1}]$"
            # label+=' formation rate '
            # ax.set_title('Main formation reaction: '+chemistry.sorted_form_info[0][23:].replace(" ",""))
            ax.set_title(splabel + " main formation reactions")
        elif rtype == "d":
            # data=chemistry.darray.T
            data = chemistry.totdrate.T  # transpose because of imshow
            reacs = chemistry.get_reac_grid(level, "d")[0]
            label = r"(total destruction rate) $[cm^{-3} s^{-1}]$"
            ax.set_title(splabel + " main destruction reactions")
            # label+=' destruction rate '
            # ax.set_title('Main destruction reaction: '+chemistry.sorted_dest_info[0][23:].replace(" ",""))
        else:
            print("ERROR: Unknown rtype.")
            return

        if with_abun:
            label = r"$\mathrm{\epsilon(" + spnToLatex(chemistry.species) + ")}$"
            label = "log " + label
            data = np.log10(model.getAbun(chemistry.species).T)
            lograte = False

        if lograte:
            label = "log " + label
            data = np.log10(data)
            # label+='* [s] '
        #    else:
        #      if not(with_abun):
        #        label=r'[$\mathrm{s}^{-1}$]'

        for i in range(model.nx):
            for j in range(model.nz)[::-1]:
                ax.text(i + 1 - 1.2, j + 1 - 1.2, reacs[i, j])

        if vmin is None:
            vmin = np.min(data)

        im = ax.imshow(data, vmin=vmin)
        CB = fig.colorbar(im, ax=ax, fraction=0.047, pad=0.01)
        CB.set_label(label)

        if grid:
            ax.set_xlim(-0.5, model.nx - 0.5)
            ax.set_ylim(-0.5, model.nz - 0.5)
            ax.set_xlabel("ix")
            ax.set_ylabel("iz")

        else:
            ax.set_ylim(-0.5, model.nz - 0.5)

            xticks = ax.get_xticks()[1:]
            xticks[-1] = model.nx - 1
            ax.set_xticks(xticks)

            xticks_l = list(model.x[:, 0][xticks.astype(int)])
            xticks_l = [np.around(item, 4) for item in xticks_l]
            ax.set_xticklabels(xticks_l)

            yticks = ax.get_yticks()[1:]
            yticks[-1] = model.nz - 1
            ax.set_yticks(yticks)

            yticks_l = list(model.z[0, :][yticks.astype(int)])
            yticks_l = [np.around(item, 3) for item in yticks_l]
            ax.set_yticklabels(yticks_l)

            ax.set_xlabel("r [au]")
            ax.set_ylabel("z [au]")

        self._dokwargs(ax, **kwargs)
        # self._legend(ax)

        return self._closefig(fig)


class Contour(object):
    """
    Define a contour line that can be used in the contour plotting routines. Something like the visual exctinction of unity in a plot
    for the 2D dust temperature distribution.
    Objects of this class can be passed to e.g. the :func:`~prodimopy.plot.Plot.plot_cont` routine and will be drawn their.

    Example
    -------

        .. code-block:: python

            # define some contours for the dust temperature
            tdcont=Contour(model.td,[10,20,30,100])
            # we also want to show the AV=1 line
            avcont=Contour(model.AV,[1],color="red",showlabels=True,label_fmt=r"A$_V$=%1.0f")
            # use them with plot_cont
            pp.plot_cont(model, "td", oconts=[tdcont,avcont])

    .. todo::

        * provide a field for label strings (arbitrary values) need to be the same size as levels

    """

    def __init__(
        self,
        field,
        levels,
        colors="white",
        linestyles="solid",
        linewidths=1.5,
        showlabels=False,
        label_locations=None,
        label_fmt="%.1f",
        label_fontsize=7,
        label_inline_spacing=5,
        filled=False,
    ):
        """
        Attributes
        ----------

        """
        self.field: NDArray[np.float64] = field
        """ : A 2D array of values used for the Contours. Needs to have the same
            dimensions as the array used for the contour plotting routine. So any
            2D array of the :class:`~prodimopy.read.Data_ProDiMo` will do.
        """
        self.levels: list[float] = levels
        """ : list of values for which contour lines should be drawn.
        """
        self.colors: str | list[str] = colors
        """ : List of colors for the idividual contours. If only a single value is
            provided (i.e. no array/list) this value is applied to all contours.
            The values of colors can be given in the syntax as for matplotlib.
        """
        self.linestyles: str | list[str] = linestyles
        """ : Linestyles for the contours. Works like the `colors` parameter.
            Any style that matplotlib understands will work.
        """
        self.linewidths: float | list[float] = linewidths
        """ : linewidths for the individual contour levels. Works like the `colors` parameter. """
        self.showlabels: bool = showlabels
        """ : show text label for each level or not """
        self.label_locations: list[tuple[float, float]] | None = label_locations
        """ : Locations for the labels if shown. If None, default locations are used e.g. `[(0.3,2),(0.4,2)]`. """
        self.label_fmt: str = label_fmt
        """ : Format string for the labels if shown, e.g. ``r"A$_V$=%1.0f"``"""
        self.label_fontsize: float = label_fontsize
        """ : The fontsize of the contour level label if enabled """
        self.label_inline_spacing: float = label_inline_spacing
        """ : Control the space around the contour label (i.e. if it overlaps with the line) """
        self.filled: bool = filled
        """ : Use filled contours (contourf) instead of lines. Can be usefull sometimes.
            But not supported everywhere (just try).
        """


def spnToLatex(spname):
    """
    Utilitiy function to convert species names to proper latex math strings.

    The returned string can directly be embedded in a latex $ $ statement.
    """
    # use string in case it is a binary format (python 3 comaptibility)
    name = str(spname)
    # TODO: make this a bit smarter
    if str(spname) == "HN2+":
        name = "N2H+"
    if str(spname) == "C18O":
        return "C^{18}O"
    if str(spname) == "13CO":
        return "^{13}CO"
    if str(spname) == "H13CO+":
        return "H^{13}CO^+"
    if str(spname) == "PHOTON":
        return r"\gamma"
    if str(spname) == "dust":
        return "\u26ab"

    newname = ""
    previous_char = None
    for c in name:
        if c.isdigit():
            # case for large melecues two digits ... not nice
            if previous_char is not None and previous_char.isdigit():
                newname = newname[0:-2] + "_{" + previous_char + c + "}"
            else:
                newname += "_" + c
        # deal with ortho and para (o-, p-) species
        elif c == "-" and not (
            previous_char == "o" or previous_char == "p" or previous_char == "-"
        ):
            newname += "^-"
        elif c == "+" and not previous_char == "+":
            newname += "^+"
        elif c == "#":
            newname += r"\#"
        else:
            newname += c

        previous_char = c

    # for line names (species)
    if "_H" in newname:
        newname = newname.replace("_H", r"\_H")

    if "_C" in newname:
        newname = newname.replace("_C", r"\_C")

    # repair the double ionized case
    if "^++" in newname:
        newname = newname.replace("^++", "^{++}")
    # repair the triple ionized case
    if "^+++" in newname:
        newname = newname.replace("^+++", "^{+++}")
    # repair the double ionized case
    if "^--" in newname:
        newname = newname.replace("^--", "^{--}")
    # repair the triple ionized case
    if "^---" in newname:
        newname = newname.replace("^---", "^{---}")

    return newname


def reacToStr(reaction: pchem.Reaction) -> str:
    """
    Builds a string representation for a reactions.
    Usefull to put it on plots or in legends.
    """
    # a utility function to produce a str for the Reaction that can be use in the legend
    out = rf"{reaction.id:>4d}$\,{reaction.type.strip()}\!:\,"
    out += r"\!+\!".join([spnToLatex(reac) for reac in reaction.reactants])
    out += r"\,\mathregular{\rightarrow}\,"
    out += "+".join([spnToLatex(prod) for prod in reaction.products])
    out += "$"
    return out


def nhver_to_zr(ir, nhver, model, log=True):
    zrs = model.z[ir, :] / model.x[ir, :]

    if log:
        old_settings = np.seterr(divide="ignore")
        ipol = interp1d(
            np.log10(model.NHver[ir, :]), zrs, bounds_error=False, fill_value=0.0, kind="linear"
        )
        np.seterr(**old_settings)  # reset to default
    else:
        ipol = interp1d(model.NHver[ir, :], zrs, bounds_error=False, fill_value=0.0, kind="linear")

    # return 0
    return ipol(nhver)


def plog(array):
    # ignore divide by zero in log10
    old_settings = np.seterr(divide="ignore")
    array = np.log10(array)
    np.seterr(**old_settings)  # reset to default
    return array


def scale_figs(scale):
    """
    Scale the figure size from matplotlibrc by the factors given in the
    array scale the first element is for the width the second for
    the heigth.
    """
    figsize = mpl.rcParams["figure.figsize"]

    return (figsize[0] * scale[0], figsize[1] * scale[1])


def load_style(style="prodimopy"):
    """
    Simple wrapper that calls :func:`~prodimopy.utils.load_mplstyle` with the given style.

    Parameters
    ----------
    style : str
      The name of the style to load. Default: "prodimopy"

    """
    putils.load_mplstyle(style)

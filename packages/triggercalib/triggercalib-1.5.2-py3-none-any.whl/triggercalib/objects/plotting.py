###############################################################################
# (c) Copyright 2024-2025 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

from lhcbstyle import LHCbStyle
import matplotlib.pyplot as plt
import mplhep as hep  # Import mplhep for HEP style plotting
import numpy as np
import os
import ROOT as R

from triggercalib.utils import core, types

has_zfit = core.zfit_installed()
if has_zfit:
    import zfit


class Plot:
    """Class for trigger efficiency plots

    This class provides functionality to create and save plots of fits to discriminating variable,
    supporting both RooFit and zFit backends. It handles the plotting of data and fitted PDFs (with
    their components if relevant), with appropriate styling for LHCb publications.
    """

    def __init__(
        self,
        name: str,
        observable: types.observable,
        data: types.data,
        pdf: types.pdf,
        plot_kwargs: dict = {},
        extension: str = ".pdf",
    ):
        """Initialize a new Plot instance

        Args:
            name: Name of the plot, used to define the filename
            observable: Variable being plotted (ROOT.RooAbsReal or zfit.Space)
            data: Dataset to plot (ROOT.RooDataSet or zfit.Data)
            pdf: Probability density function (ROOT.RooAbsPdf or zfit.pdf.BasePDF)
            extension: File extension for saved plots (default: .pdf)
            backend: Fitting backend to use ('roofit' or 'zfit')
        """

        self.name = name
        self.observable = observable
        self.data = data
        self.pdf = pdf
        self.extension = extension
        self.plot_kwargs = plot_kwargs

        if isinstance(self.observable, R.RooAbsReal) and isinstance(
            self.pdf, R.RooAbsPdf
        ):
            self._roofit_plot()
        elif (
            has_zfit
            and isinstance(self.observable, zfit.Space)
            and isinstance(self.pdf, zfit.pdf.BasePDF)
        ):
            self._zfit_plot()

        return

    def _roofit_plot(self):
        # TODO: write docstring

        with LHCbStyle():
            # Delete canvas if already exists
            _c = R.gROOT.GetListOfCanvases().FindObject(f"{self.name}_canvas")
            if isinstance(_c, R.TCanvas):
                _c.Destructor()

            self.fig = R.TCanvas(f"{self.name}_canvas")
            self.fig.cd()

            frame = self.observable.frame()
            self.data.plotOn(frame)
            if hasattr(self.pdf, "coefList") and callable(
                getattr(self.pdf, "coefList")
            ):
                colors = ["r", "g", "b", "o"]

                for pdf_i, color in zip(self.pdf.pdfList(), colors):
                    self.pdf.plotOn(
                        frame,
                        Components=[pdf_i],
                        LineStyle="--",
                        LineColor=color,
                    )
            self.pdf.plotOn(frame)

            frame.Draw()

        return self.fig

    def _zfit_plot(self):
        # TODO: write docstring

        default_kwargs = {
            "aspect": (12, 9),
            "xlabel": self.observable.obs[0],
            "ylabel": "Candidates per bin",
            "ylog": False,
            "title": "",
            "units": "",
            "lhcb_label": "Preliminary",
            "lhcb_rlabel": "",
            "pulls": True,  # <- Make this actually do something
        }

        colors = ["#ff2244", "#f1c15b", "#8fbc5c", "#5587a3", "#263a82"]
        styles = ["solid", "dashed", "dotted"]

        plot_kwargs = self.plot_kwargs.copy()
        for kwarg, value in default_kwargs.items():
            if kwarg not in plot_kwargs:
                plot_kwargs[kwarg] = value

        data = self.data.value(self.observable).numpy().ravel()
        weights = (
            self.data.weights.numpy()
            if self.data.weights is not None
            else np.ones(np.shape(data))
        )

        plot_xlims = (
            data.min(),
            data.max(),
        )  # has to be set relative to data to get the normalisation right
        if "xlims" not in plot_kwargs:
            plot_kwargs["xlims"] = plot_xlims
        if "bins" not in plot_kwargs:
            plot_kwargs["bins"] = 100
        bin_edges = np.linspace(*plot_xlims, plot_kwargs["bins"] + 1)
        bin_width = bin_edges[1] - bin_edges[0]

        # +===========+ #
        # Create figure #
        # +===========+ #
        hep.style.use("LHCb2")
        if plot_kwargs["pulls"]:
            self.fig, (plot_ax, pull_ax) = plt.subplots(
                2,
                1,
                figsize=plot_kwargs["aspect"],
                gridspec_kw={"height_ratios": [4, 1], "hspace": 0.035},
                sharex=True,
            )
        else:
            self.fig, plot_ax = plt.subplots(1, 1, figsize=plot_kwargs["aspect"])

        data_yvals, data_edges = np.histogram(data, bins=bin_edges, weights=weights)
        data_xerrs = np.diff(data_edges) / 2
        data_xvals = data_edges[:-1] + data_xerrs

        # +===============+ #
        # Plot data and fit #
        # +===============+ #
        plot_ax.errorbar(
            data_xvals,
            data_yvals,
            xerr=data_xerrs,
            yerr=np.sqrt(data_yvals),
            marker="o",
            markersize=3,
            linestyle="none",
            label="Data",
            color="black",
            capsize=2,
            elinewidth=1,
        )

        pdf_xvals = np.linspace(*plot_xlims, 1000)
        total_yield = self.pdf.get_yield().numpy()
        component_min = total_yield
        for n, component in enumerate(self.pdf.pdfs):
            component_yield = component.get_yield().numpy()
            component_yvals = (
                component.pdf(pdf_xvals)
                * component_yield
                * (bin_edges[1] - bin_edges[0])
            )
            plot_ax.plot(
                pdf_xvals,
                component_yvals,
                label=component.name,
                marker="none",
                color=colors[n % len(colors)],
                lw=2,
                ls=styles[n % len(styles)],
            )
            component_min = min(component_min, min(component_yvals))

        pdf_yvals = (
            self.pdf.pdf(pdf_xvals) * total_yield * (bin_edges[1] - bin_edges[0])
        )

        plot_ax.plot(
            pdf_xvals,
            pdf_yvals,
            label=self.pdf.name,
            marker="none",
            color="#606060",
            lw=2,
        )

        if plot_kwargs["pulls"]:
            # +========+ #
            # Pulls plot #
            # +========+ #

            pulls_yvals = (
                data_yvals - self.pdf.pdf(data_xvals) * total_yield * bin_width
            ) / np.sqrt(data_yvals)

            for n in (-3, -1, 1, 3):
                pull_ax.plot(
                    plot_kwargs["xlims"],
                    [n, n],
                    color="#d4d4d4",
                    lw=2,
                    ls="dashed",
                )
            pull_ax.bar(
                data_xvals,
                pulls_yvals,
                width=bin_width,
                label=self.pdf.name,
                color="#d4d4d4",
            )
            pull_ax.plot(
                plot_kwargs["xlims"],
                [0, 0],
                color="k",
                lw=2,
            )
            pull_ax.set_ylim(-4.5, 4.5)

        plot_ax.legend()
        plot_ax.set_xlim(*plot_kwargs["xlims"])

        if plot_kwargs["ylog"]:
            plot_ax.set_yscale("log")
        else:
            plot_ax.set_ylim(0, 1.1 * max(pdf_yvals))

        # +========+ #
        # Set labels #
        # +========+ #

        plot_ax.set_title(plot_kwargs["title"])

        xlabel = plot_kwargs["xlabel"]
        if plot_kwargs["units"]:
            xlabel = xlabel.replace("UNITS", plot_kwargs["units"])
        xlabel = xlabel.replace("BIN_WIDTH", f"{bin_width:.1f}")

        ylabel = plot_kwargs["ylabel"]
        if plot_kwargs["units"]:
            ylabel = ylabel.replace("UNITS", plot_kwargs["units"])
        ylabel = ylabel.replace("BIN_WIDTH", f"{bin_width:.1f}")

        plot_ax.set_ylabel(ylabel)

        if plot_kwargs["pulls"]:

            pull_ax.set_xlabel(xlabel)
            pull_ax.set_ylabel("Pulls")
        else:
            plot_ax.set_xlabel(xlabel)

        hep.lhcb.label(
            loc=1,
            ax=plot_ax,
            label=plot_kwargs["lhcb_label"],
            data=plot_kwargs["lhcb_label"].lower() != "simulation",
            rlabel=plot_kwargs["lhcb_rlabel"],
        )

        return

    def save(self, plot_path: str):
        """Save the plot to a file

        Args:
            plot_path: Directory path where the plot should be saved. The filename will
                       be constructed from the configured name and extension
        """
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)

        path = os.path.join(plot_path, self.name)

        if isinstance(self.fig, R.TCanvas):
            self.fig.SaveAs(f"{path}{self.extension}")
        elif has_zfit and isinstance(self.fig, plt.Figure):
            self.fig.savefig(f"{path}{self.extension}")
            plt.close(self.fig)

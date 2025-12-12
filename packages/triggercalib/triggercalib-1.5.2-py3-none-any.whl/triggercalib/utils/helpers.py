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

from array import array
from ctypes import c_double
import itertools as it
import re
from typing import Annotated, Dict, List, Literal, Union

import numpy as np
import ROOT as R

from triggercalib.utils import core, types

has_zfit = core.zfit_installed()
if has_zfit:
    import zfit


def bins_from_taxis(axis, as_array=False, as_np=True):
    """Extract bin edges from a ROOT TAxis object

    Args:
        axis: ROOT TAxis object to extract bins from
        as_array: Whether to return bins as a ROOT array
        as_np: Whether to return bins as a numpy array

    Returns:
        list or array: List/ROOT/numpy array of bin edges
    """
    bins = [axis.GetBinLowEdge(0)] + [
        axis.GetBinUpEdge(i) for i in range(1, axis.GetNbins() + 1)
    ]

    if as_array:
        if as_np:
            raise RuntimeError("'as_array' and 'as_np' may not both be set")
        return array("d", bins)
    elif as_np:
        return np.array(bins)
    return bins


def bin_nums_from_hist(hist):

    xbins = range(1, hist.GetNbinsX() + 1)
    if isinstance(hist, R.TH2):
        ybins = range(1, hist.GetNbinsY() + 1)
        bin_indices = it.product(xbins, ybins)
    else:
        bin_indices = [(b,) for b in xbins]

    return [hist.GetBin(*b) for b in bin_indices]


def sum_bins(hist):
    contents = []
    errors = []

    bin_nums = bin_nums_from_hist(hist)
    for n_bin in bin_nums:
        contents.append(hist.GetBinContent(n_bin))
        errors.append(hist.GetBinError(n_bin))

    sum_content = np.sum(contents)
    sum_error = np.sqrt(np.sum(np.array(errors) ** 2))

    return sum_content, sum_error


def tgraph_to_th(
    graph, name="", title="", error_type: Literal["mean", "lower", "upper"] = "mean"
):
    """Convert a ROOT TGraph(2D)AsymmErrors to a TH1(2)D

    Args:
        graph: ROOT TGraph(2D)AsymmErrors to convert
        name: Optional name for output histogram
        title: Optional title for output histogram
        error_type: Which error to use (`mean`, `lower` or `upper`), defaults to `mean`

    Returns:
        TH1D or TH2D: Histogram containing graph points with symmetric errors
    """

    x = c_double(0)
    y = c_double(0)
    z = c_double(0)

    x_edges = []
    y_edges = []

    x_vals = []
    y_vals = []
    values = []
    errors = []

    for n in range(graph.GetN()):
        if isinstance(graph, R.TGraph2DAsymmErrors):
            graph.GetPoint(n, x, y, z)
        else:
            graph.GetPoint(n, x, y)

        x_edges.append(x.value - graph.GetErrorXlow(n))
        x_edges.append(x.value + graph.GetErrorXhigh(n))

        x_vals.append(x.value)
        if isinstance(graph, R.TGraph2DAsymmErrors):
            y_edges.append(y.value - graph.GetErrorYlow(n))
            y_edges.append(y.value + graph.GetErrorYhigh(n))

            y_vals.append(y.value)
            values.append(z.value)
            if error_type == "lower":
                errors.append(graph.GetErrorZlow(n))
            elif error_type == "upper":
                errors.append(graph.GetErrorZhigh(n))
            else:
                errors.append(graph.GetErrorZ(n))
        else:
            values.append(y.value)
            if error_type == "lower":
                errors.append(graph.GetErrorYlow(n))
            elif error_type == "upper":
                errors.append(graph.GetErrorYhigh(n))
            else:
                errors.append(graph.GetErrorY(n))

    x_edges = np.array(sorted(list(set(x_edges))))
    y_edges = np.array(sorted(list(set(y_edges))))

    if isinstance(graph, R.TGraph2DAsymmErrors):
        hist = R.TH2D(
            name if name else f"{graph.GetName()}_TH2D",
            title if title else f"{graph.GetTitle()}_TH2D",
            len(x_edges) - 1,
            x_edges,
            len(y_edges) - 1,
            y_edges,
        )
        for x_val, y_val, value, error in zip(x_vals, y_vals, values, errors):
            n = hist.FindBin(x_val, y_val)
            hist.SetBinContent(n, value)
            hist.SetBinError(n, error)
    else:
        hist = R.TH1D(
            name if name else f"{graph.GetName()}_TH1D",
            title if title else f"{graph.GetTitle()}_TH1D",
            len(x_edges) - 1,
            x_edges,
        )
        for x_val, value, error in zip(x_vals, values, errors):
            n = hist.FindBin(x_val)
            hist.SetBinContent(n, value)
            hist.SetBinError(n, error)

    return hist


def th_to_np(th, xscale: float = 1.0, yscale: float = 1.0, zscale: float = 1):
    """Convert a ROOT TH1(2)D to numpy objects

    Args:
        th: ROOT TH1(2)D to convert
        xscale: Scale factor for x-axis
        yscale: Scale factor for y-axis
        zscale: Scale factor for z-axis

    Returns:
        x_vals: x-axis bin centres
        y_vals: values in each bin if TH1D given, otherwise y-axis bin centres
        z_vals (only if TH2D given): values in each bin
        x_errors: x-axis bin widths
        y_errors: errors in each bin if TH1D given, otherwise y-axis bin widths
        z_errors (only if TH2D given): errors in each bin
    """

    dims = 2 if isinstance(th, R.TH2) else 1

    x_edges = bins_from_taxis(th.GetXaxis(), as_np=True) * xscale
    x_vals = (x_edges[1:] + x_edges[:-1]) / 2
    x_errors = (x_edges[1:] - x_edges[:-1]) / 2

    shape = [len(x_edges) - 1]

    if dims > 1:
        y_edges = bins_from_taxis(th.GetYaxis(), as_np=True) * yscale
        y_vals = (y_edges[1:] + y_edges[:-1]) / 2
        y_errors = (y_edges[1:] - y_edges[:-1]) / 2

        shape.append(len(y_edges) - 1)

    n_bins = bin_nums_from_hist(th)

    values = []
    errors = []
    for n_bin in n_bins:
        values.append(th.GetBinContent(n_bin))
        errors.append(th.GetBinError(n_bin))

    values = np.reshape(values, shape)
    errors = np.reshape(errors, shape)

    if dims == 1:
        return x_vals, values, x_errors, errors
    elif dims == 2:
        return x_vals, y_vals, values, x_errors, y_errors, errors
    raise NotImplementedError


def tgraph_to_np(
    tgraph,
    xscale: float = 1.0,
    yscale: float = 1.0,
    zscale: float = 1.0,
    symmetric_uncertainties=False,
):
    """Convert a ROOT TGraph(2D)(AsymmErrors) to numpy objects

    Args:
        th: ROOT TH1(2)D to convert
        xscale: Scale factor for x-axis
        yscale: Scale factor for y-axis
        zscale: Scale factor for z-axis
        symmetric_uncertainties: Whether to report uncertainties as the mean of the lower and upper uncertainties

    Returns:
        x_vals: x-axis bin centres
        y_vals: values in each bin if TH1D given, otherwise y-axis bin centres
        z_vals (only if TH2D given): values in each bin
        x_errors: x-axis bin widths
        y_errors: errors in each bin if TH1D given, otherwise y-axis bin widths
        z_errors (only if TH2D given): errors in each bin
    """

    if (
        not (isinstance(tgraph, (R.TGraphAsymmErrors, R.TGraph2DAsymmErrors)))
        or symmetric_uncertainties
    ):
        th = tgraph_to_th(tgraph)
        return th_to_np(th, xscale=xscale, yscale=yscale, zscale=zscale)

    th_low = tgraph_to_th(tgraph, error_type="lower")
    low_as_np = list(th_to_np(th_low, xscale=xscale, yscale=yscale, zscale=zscale))

    th_high = tgraph_to_th(tgraph, error_type="upper")
    high_as_np = th_to_np(th_high, xscale=xscale, yscale=yscale, zscale=zscale)

    low_as_np[-1] = [low_as_np[-1], high_as_np[-1]]

    return low_as_np


def get_backend(data=None, observable=None, pdf=None):
    # TODO: write docstring

    roofit_objects = []
    zfit_objects = []

    if data is None and observable is None and pdf is None:
        return None

    if data is not None:
        if isinstance(data, R.RooAbsData):
            roofit_objects.append(data)
        elif has_zfit and isinstance(data, zfit.Data):
            zfit_objects.append(data)

    if observable is not None:
        if isinstance(observable, R.RooAbsReal):
            roofit_objects.append(observable)
        elif has_zfit and isinstance(observable, zfit.Space):
            zfit_objects.append(observable)

    if pdf is not None:
        if isinstance(pdf, R.RooAbsPdf):
            roofit_objects.append(pdf)
        elif has_zfit and isinstance(pdf, zfit.pdf.BasePDF):
            zfit_objects.append(pdf)

    if len(roofit_objects) > 0 and len(zfit_objects) > 0:
        raise ValueError(
            f"Unsupported combination of fitting objects. These must be either both RooFit objects or both zFit objects. RooFit objects: {roofit_objects}, zFit objects: {zfit_objects}"
        )

    if len(roofit_objects) > 0:
        return "roofit"
    elif len(zfit_objects) > 0:
        return "zfit"

    raise ValueError(
        f"Unsupported combination of fitting objects. These must be either both RooFit objects or both zFit objects. RooFit objects: {roofit_objects}, zFit objects: {zfit_objects}"
    )


def construct_variable(
    name,
    backend,
    value: float = None,
    limits: Annotated[List[float], 2] = None,
    title: str = None,
):
    # TODO: write docstring

    if title is None:
        title = name

    if backend == "roofit":
        if limits:
            if value:
                return R.RooRealVar(name, title, value, *limits)
            return R.RooRealVar(name, title, *limits)
        elif value:
            return R.RooRealVar(name, title, value)
        return R.RooRealVar(name, title, -np.inf, np.inf)
    elif has_zfit and backend == "zfit":
        # TODO: <- Inform user that value is ignored when creating a zfit Space
        if limits is None:
            limits = (-np.inf, np.inf)
        return zfit.Space(name, limits=limits)

    raise ValueError(
        f"Backend '{backend}' not recognised. Variable '{name}' could not be constructed."
    )


def create_dataset(
    data: Dict[str, np.ndarray],
    observable: types.observable,
    weight="",
):
    # TODO: write docstring

    observables = observable if isinstance(observable, List) else [observable]

    backends = [get_backend(observable=observable) for observable in observables]
    if len(set(backends)) == 1:
        backend = backends[0]
    else:
        raise ValueError(
            f"Unsupported combination of observables. These must be either all ROOT RooAbsReal or all zFit Spaces. Observables: {observables}"
        )

    if weight and not any(get_variable_name(obs) for obs in observables):
        observables.append(construct_variable(weight, backend))

    if backend == "roofit":
        return R.RooDataSet.from_numpy(data, observables, weight_name=weight)

    elif has_zfit and backend == "zfit":
        np_dataset = np.array(
            [
                branch
                for branch_name, branch in data.items()
                if branch_name in [get_variable_name(obs) for obs in observables]
            ]
        ).T
        return zfit.Data.from_numpy(
            obs=zfit.dimension.combine_spaces(*observables),
            array=np_dataset,
            weights=data[weight] if weight else None,
        )


def fit_result_to_string(fit_result):
    # TODO: write docstring
    _width = 48

    result_string = "=" * _width + "\n"
    if isinstance(fit_result, R.RooFitResult):
        result_string += f"Fit performed with RooFit from ROOT {R.__version__}\n"
        result_string += "\nInitial parameters:\n"
        for var in fit_result.floatParsInit():
            result_string += f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"
        result_string += "\nFinal parameters:\n"
        for var in fit_result.floatParsFinal():
            result_string += f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"

        if len(fit_result.constPars()) > 0:
            result_string += "\nConstant parameters:\n"
            for var in fit_result.constPars():
                result_string += f"{var.GetName()}: {var.getVal()}\n"
        result_string += f"\nCovariance quality: {fit_result.covQual()}\n"
        result_string += f"Fit status: {fit_result.status()}\n"
        result_string += f"Minimum value: {fit_result.minNll()}\n"
        result_string += "=" * _width + "\n"

        return result_string

    elif has_zfit and isinstance(fit_result, zfit.minimizers.fitresult.FitResult):
        result_string += f"Fit performed with zfit {zfit.__version__}"
        result_string += "\nFinal parameters:\n"
        for param, param_info in fit_result.params.items():
            result_string += f"{param.name}: {param_info['value']} +/- {param_info['hesse']['error']}\n"
        result_string += f"\nValid: {fit_result.valid}\n"
        result_string += f"Converged: {fit_result.converged}\n"
        result_string += f"Fit status: {fit_result.status}\n"
        result_string += f"Minimum value: {fit_result.fmin}\n"
        result_string += "=" * _width + "\n"

        return result_string

    raise TypeError(
        f"Unrecognised type '{type(fit_result)}' for 'fit_result'. 'fit_result' must be of type 'ROOT.RooFitResult' or 'zfit.minimizers.fitresult.FitResult'."
    )


def write_fit_result(fit_result, path, verbose=False):
    # TODO: write docstring

    result_string = fit_result_to_string(fit_result)
    if verbose:
        print(result_string)

    with open(path, "w") as result_file:
        result_file.write(result_string)

    return


def get_variable_name(observable: types.observable):
    # TODO: write docstring

    if isinstance(observable, R.RooAbsReal):
        return observable.GetName()
    elif has_zfit and isinstance(observable, zfit.Space):
        return observable.obs[0]
    raise NotImplementedError(
        f"Could not determine name for observable of type '{type(observable)}'"
    )


def parse_selection(
    particle: str,
    lines: Union[str, List[str]],
    category: Literal["", "TIS", "TOS"],
    branches: List[str],
):
    """Parse trigger selection strings into ROOT cut expressions

    Args:
        particle: Particle to seek TIS/TOS branches for
        lines: Trigger line(s) to create selection for
        category: Optional trigger outcome category (TIS/TOS) to append
        branches: List of branches to compare against

    Returns:
        str: ROOT cut expression combining the selections
    """

    if isinstance(lines, str):
        # If only a string given, use regex match to get branches
        search_string = (
            f"{particle}_{lines}Decision_{category}" if category else f"{lines}Decision"
        )
        search = re.compile(search_string)
        lines = set()
        for branch in branches:
            if search.fullmatch(branch):
                branch = branch.replace("Decision", "")
                if category:
                    branch = branch.split(f"{particle}_", 1)[1]
                    branch = branch.rsplit(f"_{category}", 1)[0]
                lines.update({branch})
        if len(lines) == 0:
            RuntimeError(f"No branches found matching '{search_string}'")
        lines = list(lines)
        lines.sort()

    for line in lines:
        branch_name = (
            f"{particle}_{line}Decision_{category}" if category else f"{line}Decision"
        )
        if branch_name not in branches:
            raise RuntimeError(f"Branch '{branch_name}' could not be found")

    cuts = []
    for level in ("Hlt1", "Hlt2"):
        cut = " || ".join(
            (f"{particle}_{line}Decision_{category}" if category else f"{line}Decision")
            for line in lines
            if line.startswith(level)
        )
        if cut:
            cuts += [f"({cut})"]

    return " && ".join(cuts)


def empty_histogram(name, binning):
    """Create an empty ROOT.TH1D with specified binning scheme

    Args:
        name: Name for the histogram
        binning: binning scheme of interest

    Returns:
        TH1D or TH2D: Empty histogram with appropriate binning
    """
    bin_vars = list(binning.keys())
    if len(bin_vars) == 1:
        return R.TH1D(
            name,
            name,
            len(binning[bin_vars[0]]) - 1,
            array("d", binning[bin_vars[0]]),
        )
    elif len(bin_vars) == 2:
        return R.TH2D(
            name,
            name,
            len(binning[bin_vars[0]]) - 1,
            array("d", binning[bin_vars[0]]),
            len(binning[bin_vars[1]]) - 1,
            array("d", binning[bin_vars[1]]),
        )
    raise NotImplementedError(
        "Construction of empty histograms above 2D not yet implemented in TriggerCalib"
    )

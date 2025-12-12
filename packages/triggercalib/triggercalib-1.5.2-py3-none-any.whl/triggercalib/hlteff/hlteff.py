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

import numpy as np
import ROOT as R
from hepstats.splot import compute_sweights

from array import array
import itertools as it
import logging
import os
from typing import Dict, List, Literal, Union
import uproot as up

from triggercalib.objects import Fit, Plot, Sideband
from triggercalib.utils import helpers, io, stats, types


class HltEff:
    """Class for calculating trigger efficiencies

    This class provides functionality for calculating trigger efficiencies using
    either RooFit or zFit as the backend. It supports various methods of efficiency
    calculation including direct counting and fitting methods. It also handles
    different trigger categories (TIS, TOS, TISTOS) and provides utilities for
    binning, plotting, and saving results.
    """

    # Magic methods #

    def __init__(  # <- TODO: order the arguments!
        self,
        name: str,
        path: Union[str, List[str]],  # <- TODO: add direct passing of RDataFrame object
        tos: Union[str, List[str]],  # <- line(s) to be used as TOS
        tis: Union[str, List[str]],  # <- line(s) to be used as TIS
        particle: str,
        binning: Union[
            str, Dict[str, Dict[str, Union[List[float], str]]]
        ] = {},  # <- provide binning directly as dict or as path to .json/.yaml file
        cut: Union[str, List[str]] = "",
        friend: Union[str, List[str]] = None,
        observable: types.observable = None,
        pdf: types.pdf = None,
        sideband: Union[Dict[str, List[float]], str, Sideband] = None,
        sweights: str = False,
        expert_mode: bool = False,
        lazy: bool = False,
        max_fit_attempts: int = 5,
        min_fit_entries: int = 50,
        plots: bool = True,  # <- TODO: implement central plotting framework
        fit_kwargs: Dict = {},
        plot_kwargs: Dict = {},
        prefix: str = "",
        output_path: str = "",
        trig_effs: bool = True,  # Disable to calculate only TIS|TOS and TOS|TIS efficiencies
        uncertainty_method: Literal[
            "poisson", "generalised_wilson", "standard_wilson"
        ] = "generalised_wilson",
        weight: Union[str, List[str]] = "",
        silent: bool = False,
    ):
        """Initialize a new HltEff instance

        Args:
            name: Unique identifier for this efficiency calculation
            path: Path(s) to the input data file(s) or RDataFrame, of the form <path>:<tree>
            tos: Trigger selection (line(s)) of interest (taken as TOS)
            tis: Reference trigger selection used to define the TIS category
            particle: Name of particle chosen as signal
            binning: Binning scheme as dict or path to binning config .json/.yaml file
            cut: Additional selection criteria to apply to both tis and tos samples
            friend: Path to additional input file to use friend tree, of the form <path>:tree
            observable: Variable for fitting, as a RooAbsReal or zfit.Space object
            pdf: Probability density function for fitting, as a RooAbsPdf or zfit.pdf
            sideband: Sideband regions for sideband subtraction
            sweights: Name of coefficient from which corresponding sWeights will be used
            expert_mode: Enable advanced features and controls, and disable convergence checks
            max_fit_attempts: Maximum number of attempts at fit for fit to converge
            min_fit_entries: Minimum number of entries required in each bin for fit to be performed
            lazy: Defer computation until explicitly requested
            plots: Generate plots when performing fitting
            prefix: Prefix to prepend to names of counts/error TH and TGraph objects
            output_path: Directory to which fit results should be saved
            trig_effs: Enables calculation of "trig" efficiencies as well as TIS|TOS and TOS|TIS
            uncertainty_method: Method to be used for propagation of statistical uncertainties
            weight: Branch in input sample(s) to be used as per events weights
            silent: Disables printed outputs from HltEff
        """

        self.silent = silent
        self.logger = logging.getLogger(__name__)
        if silent:
            self.logger.propagate = False
        self.logger.info(f"Initialising HltEff object {name}")

        self.name = name
        self.particle = particle

        # Configure options for the I/O
        if isinstance(path, str):
            path = [path]
        self.tree, self.path = io.split_paths(path, require_same_tree=True)
        self.cut = [cut] if isinstance(cut, str) and len(cut) > 0 else cut
        # Normalize friend input
        if friend is not None:
            if isinstance(friend, str):
                friend = [friend]
            self.friend_tree, self.friend_path = io.split_paths(
                friend, require_same_tree=True
            )
        else:
            self.friend_tree, self.friend_path = None, None
        self.rdf = self._load_rdf()

        weight_branches = weight if isinstance(weight, List) else [weight]
        self.weight = (
            {
                f"per_event_weight__{''.join(weight_branches)}".replace(
                    ".", "_"
                ): weight_branches
            }
            if weight
            else None
        )

        # Configure selection categories
        self.trig_effs = trig_effs
        self._categories = (
            ("tis", "tos", "tistos", "trig")
            if self.trig_effs
            else ("tis", "tos", "tistos")
        )
        self.tis = self._parse_selection(tis, "TIS")
        self.tos = self._parse_selection(tos, "TOS")
        self.selection = self._parse_selection(tos) if self.trig_effs else None

        if isinstance(binning, str):
            binning = io.load_config(binning)
        self.set_binning(binning)

        self.observable = observable
        self.pdf = pdf
        self.backend = helpers.get_backend(observable=self.observable, pdf=self.pdf)

        if self.backend == "zfit":
            self.logger.info(
                f"Enabled zFit backend for {name}, this functionality is currently experimental"
            )
            self.fit_kwargs = {}
        else:
            default_fit_kwargs = {
                "Extended": True,
                "Save": True,
            }
            self.fit_kwargs = {**default_fit_kwargs, **fit_kwargs}
            if not self.fit_kwargs["Extended"]:
                raise ValueError("RooFit keyword argument 'Extended' must be True")
            if not self.fit_kwargs["Save"]:
                raise ValueError("RooFit keyword argument 'Save' must be True")

        if sweights and (
            (
                self.backend == "roofit"
                and not any(sweights == coef.GetName() for coef in pdf.coefList())
            )
            or (
                self.backend == "zfit"
                and not any(
                    sweights == component.extended.name for component in pdf.pdfs
                )
            )
        ):
            raise ValueError(f"Yield '{sweights}' could not be found in '{pdf}'")

        if bool(sideband) and bool(pdf):
            ValueError("Sideband and fit model cannot both be provided")

        self.expert_mode = expert_mode
        self.max_fit_attempts = max_fit_attempts
        self.min_fit_entries = min_fit_entries
        self.plot_kwargs = plot_kwargs
        self.sweights = sweights
        self.uncertainty_method = uncertainty_method

        self.method = "raw"

        if sideband:
            self.method = "sideband"
            if isinstance(sideband, Sideband):
                self.sideband = sideband
            else:
                # Construct Sideband from dict
                if isinstance(sideband, str):
                    sideband = io.load_config(sideband)
                self.set_binning(binning)

                sideband_var = list(sideband.keys())[0]

                if (
                    "signal" not in sideband[sideband_var]
                    or "sidebands" not in sideband[sideband_var]
                ):
                    raise RuntimeError(
                        "Sideband must be specified with 'signal' and 'sidebands' entries"
                    )

                _signal = sideband[sideband_var]["signal"]
                _sidebands = sideband[sideband_var]["sidebands"]

                self.sideband = Sideband(sideband_var, _signal, _sidebands)
        else:
            self.sideband = None
            if pdf:
                self.method = "sweights" if self.sweights else "fit_count"
            else:
                if not expert_mode:
                    raise RuntimeError(
                        "Expert mode must be enabled to use 'raw' count mode"
                    )
        self.logger.info(f"Count mode '{self.method}' chosen")

        self.output_path = output_path
        if output_path and self.method not in ("raw", "sideband"):
            os.makedirs(output_path, exist_ok=True)

            self.fit_path = os.path.join(output_path, "fits")
            os.makedirs(self.fit_path, exist_ok=True)

            if plots:
                self.plot_path = os.path.join(output_path, "plots")
                os.makedirs(self.plot_path, exist_ok=True)
            else:
                self.plot_path = None
        else:
            self.fit_path = None
            self.plot_path = None

        if lazy:
            self._counts = {}
            self._efficiencies = {}
            self._sweights = {}
        else:
            if not self.binning:
                raise RuntimeError(
                    "Binning must be provided at initialisation unless running in lazy mode, i.e. lazy = True"
                )
            self.counts(prefix)
            self.efficiencies(prefix)

    def __getitem__(self, key):
        # TODO: write docstring

        if key not in ("counts", "efficiencies"):
            raise ValueError("Can only obtain 'counts' or 'efficiencies' objects")
        if key == "counts":
            return self._counts
        return self._efficiencies

    def get_count(self, name):
        # TODO: write docstring

        if name not in self._counts:
            raise KeyError(f"Count '{name}' not found in counts")
        return self._counts[name]

    def get_eff(self, name: str, as_th: bool = False):
        # TODO: write docstring

        if name not in self._efficiencies:
            raise KeyError(f"Efficiency '{name}' not found in efficiencies")
        _eff = self._efficiencies[name]

        if as_th:
            self.logger.info(
                "Conversion of efficiency from TGraph(2D)AsymErrors will combine asymmetric errors"
            )
            return helpers.tgraph_to_th(_eff, name=name)

        return _eff

    def set_binning(
        self,
        scheme: Dict[str, Union[List[float], float, str]],
        compute_bins: bool = False,
        bin_cut: Union[
            str, List[str]
        ] = "",  # Only applied when binning is being generated (i.e., scheme["bins"] is not a Dict)
    ):
        # TODO: write docstring

        if any("bins" not in entry for entry in scheme.values()):
            raise ValueError("Binning scheme does not contain argument 'bins'")
        if compute_bins:
            self.binning_scheme = {}
            # Compute bins if a list of bins is given instead of the bins themselves
            rdf = self.rdf

            if bin_cut and len(bin_cut) > 0:
                if isinstance(bin_cut, str):
                    bin_cut = [bin_cut]
                for bin_cut_i in bin_cut:
                    rdf = rdf.Filter(bin_cut_i)

            # Before computing bins, apply cuts on each dimension
            for var, entry in scheme.items():
                if isinstance(entry["bins"], List):
                    _, lower, upper = entry["bins"]
                    rdf = rdf.Filter(f"({var} > {lower}) & ({var} < {upper})")

            df = rdf.AsNumpy((var for var in scheme.keys()))
            for var, entry in scheme.items():
                if isinstance(entry["bins"], float):
                    nbins = entry["bins"]
                    lower = np.min(df[var])
                    upper = np.max(df[var])
                else:
                    nbins, lower, upper = entry["bins"]

                edges = np.quantile(df[var], np.arange(1, nbins) / nbins)
                edges = np.append((lower,), np.append(edges, (upper,)))
                self.binning_scheme[var] = {
                    "bins": edges.tolist(),
                    "label": entry["label"] if "label" in scheme else var,
                }

            self.set_binning(self.binning_scheme)
        else:
            self.binning_scheme = scheme
            self.binning = {
                var: entry["bins"] for var, entry in self.binning_scheme.items()
            }
            if any(
                bins[n + 1] <= bins[n]
                for bins in self.binning.values()
                for n in range(len(bins) - 1)
            ):
                raise ValueError("Bins must be increasing")
            self.variables = {
                var: entry["label"] if "label" in entry else var
                for var, entry in self.binning_scheme.items()
            }
            self.midpoints = [
                (np.array(axis_bins[1:]) + np.array(axis_bins[:-1])) / 2
                for axis_bins in self.binning.values()
            ]  # TODO: replace this with bin indices
            self.nbins = np.prod([len(b) for b in self.midpoints])

        self.logger.info(
            f"Binning scheme set for variables '{', '.join(self.variables.keys())}'"
        )

        for variable, bins in self.binning.items():
            self.rdf = self.rdf.Filter(
                f"{variable} > {bins[0]} && {variable} < {bins[-1]}"
            )

    def counts(self, prefix=""):
        # TODO: write docstring

        var_names = list(self.variables.keys())

        self._counts = {}
        if not self.binning or not self.path or not self.tree:
            raise ValueError(
                "Path, tree and binning must all be set before calculating counts"
            )

        self._counts = {}
        prefix = f"{prefix}_" if prefix else ""

        if self.method == "fit_count":  # <- TODO: require fit model
            self._counts = self._fit_count(prefix)
        else:
            self._counts = self._hist_count(prefix)

        for category in ("tis", "tos"):
            category_name = f"{prefix}{category}_only_count_{'_'.join(var_names)}"
            self._counts[category_name] = self._counts[
                f"{prefix}{category}_count_{'_'.join(var_names)}"
            ].Clone(category_name)
            self._counts[category_name].SetTitle(category_name)
            self._counts[category_name].Add(
                self._counts[f"{prefix}tistos_count_{'_'.join(var_names)}"], -1
            )

        if self.trig_effs:
            # Compute estimate of selected efficiency, the denominator of the trig. efficiency
            sel_hist_name = f"{prefix}sel_count_{'_'.join(var_names)}"
            self._counts[sel_hist_name] = self._empty_histogram(sel_hist_name)

            bin_nums = helpers.bin_nums_from_hist(self._counts[sel_hist_name])
            for n_bin in bin_nums:
                _tistos_name = sel_hist_name.replace("sel", "tistos")
                tistos_n = self._counts[_tistos_name].GetBinContent(n_bin)
                tistos_s = self._counts[_tistos_name].GetBinError(n_bin)

                _tis_name = sel_hist_name.replace("sel", "tis")
                tis_n = self._counts[_tis_name].GetBinContent(n_bin)
                tis_s = self._counts[_tis_name].GetBinError(n_bin)

                _tos_name = sel_hist_name.replace("sel", "tos")
                tos_n = self._counts[_tos_name].GetBinContent(n_bin)
                tos_s = self._counts[_tos_name].GetBinError(n_bin)

                if tistos_n > 0:
                    bin_value = tis_n * tos_n / tistos_n
                    bin_error = np.sqrt(
                        np.abs(tos_n / tistos_n) ** 2 * (tis_s**2 - tistos_s**2)
                        + np.abs(tis_n / tistos_n) ** 2 * (tos_s**2 - tistos_s**2)
                        + np.abs(
                            1 - (tis_n - tistos_n) * (tos_n - tistos_n) / tistos_n**2
                        )
                        ** 2
                        * tistos_s**2
                    )
                else:
                    bin_value = 0
                    bin_error = 0

                self._counts[sel_hist_name].SetBinContent(n_bin, bin_value)
                self._counts[sel_hist_name].SetBinError(n_bin, abs(bin_error))

        additional_parts = [self.sideband.variable] if self.sideband else []
        for count_label, count_hist in dict(self._counts).items():
            if self._to_project(count_label, additional_parts=additional_parts):
                self._counts[
                    count_label.replace("_".join(var_names), list(var_names)[0])
                ] = count_hist.ProjectionX()
                self._counts[
                    count_label.replace("_".join(var_names), list(var_names)[1])
                ] = count_hist.ProjectionY()

        return self._counts

    def efficiencies(self, prefix=""):
        # TODO: write docstring

        self.logger.info("Calculating TIS, TOS and Trig efficiencies")

        self._efficiencies = {}
        _counts = self._counts
        prefix = f"{prefix}_" if prefix else ""

        _efficiencies = {}
        axes = [None, 0, 1]
        suffixes = (
            [
                "_".join(self.variables.keys()),
                list(self.variables.keys())[0],
                list(self.variables.keys())[1],
            ]
            if len(self.variables.keys()) > 1
            else ["_".join(self.variables.keys())]
        )

        for (
            (axis, suffix),
            total,
            (efficiency_category, numerator_category, denominator_category),
        ) in it.product(
            zip(axes, suffixes),
            ("", "total_"),
            zip(
                ("tos", "tis", "trig"),
                ("tistos", "tistos", "trig"),
                ("tis", "tos", "sel"),
            ),
        ):

            if (
                not bool(total)
                or axis
                is None  # Skips integrated efficiencies in each axis (the 1D and 2D integrated efficiencies are equivalent)
            ) and (
                numerator_category != "trig"
                or self.trig_effs  # Only compute trigger efficiencies if self.trig_effs is True
            ):
                _efficiencies[
                    f"{prefix}{efficiency_category}_{total}efficiency_{suffix}"
                ] = self._base_efficiency(
                    f"{prefix}{efficiency_category}_{total}efficiency_{suffix}",
                    _counts[f"{prefix}{numerator_category}_count_{suffix}"],
                    _counts[f"{prefix}{denominator_category}_count_{suffix}"],
                    axis=axis,
                    integrated=bool(total),
                )

        self._efficiencies = _efficiencies
        return self._efficiencies

    def write(self, path, mode="RECREATE", prefix=""):
        if not path.endswith(".root"):
            raise ValueError("Path to write HltEff output to must end with '.root'")
        prefix = f"{prefix}_" if prefix else ""
        if "/" in path and not os.path.exists(path.rsplit("/", 1)[0]):
            os.makedirs(path.rsplit("/", 1)[0])

        output_file = R.TFile.Open(path, mode)
        _results = {
            f"{prefix}counts": self._counts,
            f"{prefix}efficiencies": self._efficiencies,
        }
        for name, results in _results.items():
            if results:
                output_dir = output_file.mkdir(name)
                output_dir.cd()
                for key, hist in results.items():
                    hist.Write(key)

        output_file.Close()

    def write_bins(self, path: str):
        if self.binning_scheme:
            return io.write_config(self.binning_scheme, path)
        raise RuntimeError("Binning scheme has not been set")

    def _load_rdf(self):
        """Create and store ROOT RDataFrame object from the input files

        Returns:
            RDataFrame: Loaded data with any specified cuts applied
        """
        self.logger.info(
            f"Creating RDF from tree '{self.tree}' in path(s) '{self.path}'"
        )
        rdf = R.RDataFrame(self.tree, self.path)
        # Attach any friend trees
        if self.friend_path:
            # Create a TChain from the main tree
            self.logger.info(
                f"Attaching friend tree '{self.friend_tree}' in path(s) '{self.friend_path}'"
            )
            if len(self.path) != 1 or len(self.friend_path) != 1:
                raise RuntimeError("Friend feature works only with 1 file")
            self.file = R.TFile(self.path[0])
            tree = self.file.Get(self.tree)
            tree.ResetBit(R.TTree.kEntriesReshuffled)
            self.file_friend = R.TFile(self.friend_path[0])
            tree_friend = self.file_friend.Get(self.friend_tree)
            tree.AddFriend(tree_friend)

            # Create RDataFrame from the TChain
            rdf = R.RDataFrame(tree)

        if self.cut and len(self.cut) > 0:
            for cut in self.cut:
                rdf = rdf.Filter(cut)

        return rdf

    def _parse_selection(
        self, selection: Union[str, List[str]], category: Literal["", "TIS", "TOS"] = ""
    ):
        branches = {str(b) for b in self.rdf.GetColumnNames()}
        return helpers.parse_selection(self.particle, selection, category, branches)

    def _empty_histogram(self, name):

        return helpers.empty_histogram(name, self.binning)

    def _rdf_histo(self, rdf, name, weight="", binning=None):
        """Create a histogram from a branch in a given RDataFrame object

        Args:
            rdf: Input RDataFrame
            name: Name for the histogram
            weight: Optional weight branch
            binning: Optional binning scheme

        Returns:
            Pointer to booked RDataFrame histogram (1D or 2D)
        """
        if not (binning):
            binning = self.binning

        bin_vars = list(binning.keys())

        if len(bin_vars) == 1:
            args = [
                (
                    name,
                    name,
                    len(binning[bin_vars[0]]) - 1,
                    array("d", binning[bin_vars[0]]),
                ),
                bin_vars[0],
            ]
            if weight:
                args += [weight]

            return rdf.Histo1D(*args)
        elif len(bin_vars) == 2:
            args = [
                (
                    name,
                    name,
                    len(binning[bin_vars[0]]) - 1,
                    array("d", binning[bin_vars[0]]),
                    len(binning[bin_vars[1]]) - 1,
                    array("d", binning[bin_vars[1]]),
                ),
                bin_vars[0],
                bin_vars[1],
            ]
            if weight:
                args += [weight]

            return rdf.Histo2D(*args)
        raise RuntimeError("Calculations can only be performed in 1D or 2D")

    def _trigger_cut(self, category):
        """Obtain ROOT cut string for a trigger outcome category

        Args:
            category: One of 'tis', 'tos', 'tistos', or 'trig'

        Returns:
            str: ROOT cut expression for the specified trigger outcome category

        Raises:
            ValueError: If category is not one of the allowed values
        """
        if category == "tis":
            return self.tis
        elif category == "tos":
            return self.tos
        elif category == "tistos":
            return f"({self.tis}) && ({self.tos})"
        elif category == "trig":
            return self.selection
        raise ValueError("Category must be one of 'tis', 'tos', 'tistos' or 'trig'")

    def _to_project(self, label, bin_requirement=True, additional_parts=[]):
        """Check if a histogram should be projected, based on its label

        Args:
            label: Histogram label to check
            bin_requirement: Whether to require binning variables
            include_mass: Whether to include mass in the check

        Returns:
            bool: True if the histogram should be projected
        """
        test_parts = [f"_{var}" for var in self.variables.keys()]
        if additional_parts:
            test_parts += additional_parts
        return (len(self.variables.keys()) > 1 or not bin_requirement) and not any(
            l in label and "_".join(self.variables.keys()) not in label
            for l in test_parts
        )

    def _fit_count(self, prefix=""):
        """Perform fit-based counting of events to fill histograms

        Args:
            prefix: Optional prefix for histogram names

        Returns:
            dict: Dictionary of histograms containing fit yields for different trigger outcome categories
        """
        rdf = self.rdf

        dataset_ptrs = {}
        pdfs = {}
        _counts = {}

        if self.weight:
            weight_branch = list(self.weight.keys())[0]
            weight_sub_branches = list(self.weight.values())[0]
        else:
            weight_branch = None

        for category in self._categories:
            _counts[f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"] = (
                self._empty_histogram(
                    f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"
                )
            )

            count_rdf = (
                rdf.Filter(self._trigger_cut(category)) if category != "sel" else rdf
            )

            observables_list = [helpers.get_variable_name(self.observable)]
            if self.weight:
                count_rdf = count_rdf.Define(
                    weight_branch, "*".join(weight_sub_branches)
                )
                observables_list += [weight_branch] + weight_sub_branches

            for midpoint_coords in it.product(*self.midpoints):
                xaxis = _counts[
                    f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"
                ].GetXaxis()
                xbin = xaxis.FindBin(midpoint_coords[0])
                x_low = xaxis.GetBinLowEdge(xbin)
                x_up = xaxis.GetBinUpEdge(xbin)

                bin_cut = f"({list(self.variables.keys())[0]}>{x_low} && {list(self.variables.keys())[0]}<{x_up})"
                dataset_name = f"{prefix}{category}_dataset_bin_{xbin}"

                if len(midpoint_coords) > 1:
                    yaxis = _counts[
                        f"{prefix}{category}_count_{'_'.join(self.variables)}"
                    ].GetYaxis()
                    ybin = yaxis.FindBin(midpoint_coords[1])
                    y_low = yaxis.GetBinLowEdge(ybin)
                    y_up = yaxis.GetBinUpEdge(ybin)

                    bin_cut = f"{bin_cut} && ({list(self.variables.keys())[1]} > {y_low} && {list(self.variables.keys())[1]} < {y_up})"
                    dataset_name = f"{dataset_name}_{ybin}"

                bin_rdf = count_rdf.Filter(bin_cut)

                pdf_name = dataset_name.replace("_dataset_", "_pdf_")
                if self.backend == "roofit":
                    pdfs[pdf_name] = self.pdf.cloneTree(pdf_name)
                    R.SetOwnership(pdfs[pdf_name], False)
                elif self.backend == "zfit":
                    pdfs[pdf_name] = self.pdf

                dataset_ptrs[dataset_name] = bin_rdf.AsNumpy(
                    observables_list, lazy=True
                )

        results = {}
        for category in self._categories:
            hist = _counts[f"{prefix}{category}_count_{'_'.join(self.variables)}"]

            for midpoint_coords in it.product(*self.midpoints):
                nbin = hist.FindBin(*midpoint_coords)
                xaxis = hist.GetXaxis()
                xbin = xaxis.FindBin(midpoint_coords[0])
                dataset_name = f"{prefix}{category}_dataset_bin_{xbin}"
                if len(midpoint_coords) > 1:
                    yaxis = hist.GetYaxis()
                    ybin = yaxis.FindBin(midpoint_coords[1])
                    dataset_name = f"{dataset_name}_{ybin}"

                data = helpers.create_dataset(
                    dataset_ptrs[dataset_name].GetValue(),
                    self.observable,
                    weight=weight_branch,
                )
                pdf = (
                    pdfs[dataset_name.replace("_dataset_", "_pdf_")]
                    if self.backend == "roofit"
                    else self.pdf if self.backend == "zfit" else None
                )
                fit = Fit(
                    pdf,
                    data,
                    fit_kwargs=self.fit_kwargs,
                    min_entries=self.min_fit_entries,
                    max_attempts=self.max_fit_attempts,
                    require_convergence=not self.expert_mode,
                )
                converged = fit.converged
                results[dataset_name.replace("_dataset_", "_result_")] = fit.result

                if self.fit_path is not None:
                    fit_result_path = os.path.join(
                        self.fit_path,
                        dataset_name.replace("_dataset_", "_") + "_fit.txt",
                    )
                    helpers.write_fit_result(
                        fit.result, fit_result_path, verbose=not self.silent
                    )
                if not self.expert_mode and not converged:
                    raise RuntimeError(
                        "Fit did not converge, please reconfigure fit and try again"
                    )

                if self.plot_path:
                    plot_name = dataset_name.replace("_dataset_", "_").replace(
                        ".root", "_plot"
                    )

                    plot = Plot(
                        plot_name,
                        self.observable,
                        data,
                        pdf,
                        plot_kwargs=self.plot_kwargs,
                    )
                    plot.save(self.plot_path)

                if self.backend == "roofit":
                    pdf_yields = {coef.GetName(): coef for coef in pdf.coefList()}
                elif self.backend == "zfit":
                    pdf_yields = {
                        component.extended.name: fit.result.params[
                            component.extended.name
                        ]
                        for component in self.pdf.pdfs
                    }

                for coef_name, coef in pdf_yields.items():
                    count_name = f"{prefix}{category}_{coef_name}_count_{'_'.join(self.variables)}"
                    if (
                        f"{prefix}{category}_{coef_name}_count_{'_'.join(self.variables)}"
                        not in _counts
                    ):
                        _counts[count_name] = hist.Clone(count_name)
                        _counts[count_name].SetTitle(count_name)
                    temp_hist = _counts[count_name]
                    if self.backend == "roofit":
                        temp_hist.SetBinContent(nbin, coef.getVal())
                        temp_hist.SetBinError(
                            nbin, np.abs(coef.getPropagatedError(fit.result))
                        )
                    elif self.backend == "zfit":
                        temp_hist.SetBinContent(nbin, coef["value"])
                        temp_hist.SetBinError(nbin, np.abs(coef["hesse"]["error"]))

                signal_count = list(pdf_yields.values())[0]
                if self.backend == "roofit":
                    hist.SetBinContent(nbin, signal_count.getVal())
                    hist.SetBinError(nbin, np.abs(signal_count.getError()))
                elif self.backend == "zfit":
                    hist.SetBinContent(nbin, signal_count["value"])
                    hist.SetBinError(nbin, np.abs(signal_count["hesse"]["error"]))

        for category in ("tis", "tos"):
            category_name = f"{prefix}{category}_only_count_{'_'.join(self.variables)}"
            _counts[category_name] = _counts[
                f"{prefix}{category}_count_{'_'.join(self.variables)}"
            ].Clone(category_name)
            _counts[category_name].SetTitle(category_name)
            _counts[category_name].Add(
                _counts[f"{prefix}tistos_count_{'_'.join(self.variables)}"], -1
            )

        return _counts

    def _calculate_sweights(self, rdf, prefix=""):
        """Calculate sWeights for background mitigation

        Args:
            rdf: Input RDataFrame
            prefix: Optional prefix for output names

        Returns:
            dict: Dictionary containing sWeights for each trigger outcome category
        """
        dataset_ptrs = {}
        pdfs = {}

        observables = [self.observable] + [
            helpers.construct_variable(var, self.backend, limits=(bins[0], bins[-1]))
            for var, bins in self.binning.items()
        ]

        if self.weight:
            weight_branch = list(self.weight.keys())[0]
            observables.append(helpers.construct_variable(weight_branch, self.backend))
        else:
            weight_branch = None

        for category in self._categories:
            category_rdf = (
                rdf.Filter(self._trigger_cut(category)) if category != "sel" else rdf
            )

            if self.backend == "roofit":
                pdf_name = f"{prefix}{category}_pdf"
                pdfs[pdf_name] = self.pdf.cloneTree(pdf_name)

            dataset_name = f"{prefix}{category}_dataset"
            dataset_ptrs[dataset_name] = category_rdf.AsNumpy(
                [helpers.get_variable_name(obs) for obs in observables], lazy=True
            )

        sweight_path = os.path.join(self.output_path, "sweighted_data.root")
        sweights = {}
        for category in self._categories:
            data = helpers.create_dataset(
                dataset_ptrs[f"{prefix}{category}_dataset"].GetValue(),
                observables,
                weight=weight_branch,
            )
            pdf = (
                pdfs[f"{prefix}{category}_pdf"]
                if self.backend == "roofit"
                else self.pdf
            )

            fit = Fit(
                pdf,
                data,
                fit_kwargs=self.fit_kwargs,
                min_entries=self.min_fit_entries,
                max_attempts=self.max_fit_attempts,
                require_convergence=not self.expert_mode,
            )

            # TODO: <- replace with fit.write() (when that exists)
            if self.fit_path is not None:
                fit_result_path = os.path.join(
                    self.fit_path,
                    f"{prefix}{category}_fit.txt",
                )
                helpers.write_fit_result(
                    fit.result, fit_result_path, verbose=not self.silent
                )

            if self.plot_path:
                plot_name = f"{prefix}{category}_plot"

                plot = Plot(
                    plot_name, self.observable, data, pdf, plot_kwargs=self.plot_kwargs
                )
                plot.save(self.plot_path)

            if self.backend == "roofit":
                splot = R.RooStats.SPlot(
                    f"{prefix}{category}_sdata",
                    f"{prefix}{category}_sdata",
                    data,
                    pdf,
                    pdf.coefList(),
                )
                sdata = splot.GetSDataSet()
                sweights[category] = sdata.GetClonedTree()
                sweights[category].SetName(f"{prefix}{category.capitalize()}")
            else:
                if self.weight:
                    raise NotImplementedError(
                        "sWeights method with weighted data is not implemented for the zFit backend."
                    )
                data_no_sweights = {obs: data.value(obs).numpy() for obs in data.obs}
                sweights[category] = data_no_sweights | {  # Corresponding sWeights
                    f"{key.name}_sw": value
                    for key, value in compute_sweights(
                        pdf,
                        data_no_sweights[helpers.get_variable_name(self.observable)],
                    ).items()
                }

        if self.backend == "roofit":
            with R.TFile.Open(sweight_path, "RECREATE") as sweight_file:
                sweight_file.cd()
                for category, tree in sweights.items():
                    category_dir = sweight_file.mkdir(
                        f"{prefix}{category.capitalize()}"
                    )
                    category_dir.cd()
                    tree.Write("DecayTree")

        elif self.backend == "zfit":
            with up.recreate(sweight_path) as sweights_tuple:
                for category, category_sweighted_data in sweights.items():
                    sweights_tuple[f"{prefix}{category.capitalize()}/DecayTree"] = (
                        category_sweighted_data
                    )

        return sweight_path

    def _hist_count(self, prefix=""):
        """Perform direct counting of events to fill histograms

        Args:
            prefix: Optional prefix for histogram names

        Returns:
            dict: Dictionary of histograms containing counts for different trigger outcome categories
        """
        rdf = self.rdf
        ptrs = {}

        if self.weight:
            weight_branch = list(self.weight.keys())[0]
            weight_sub_branches = list(self.weight.values())[0]
            rdf = rdf.Define(weight_branch, "*".join(weight_sub_branches))
        else:
            weight_branch = None

        if self.sweights:
            sweight_path = self._calculate_sweights(rdf, prefix=prefix)

        for category in self._categories:
            if self.sweights:
                _count_rdf = R.RDataFrame(
                    f"{prefix}{category.capitalize()}/DecayTree", sweight_path
                )
            else:
                _count_rdf = (
                    rdf.Filter(self._trigger_cut(category))
                    if category != "sel"
                    else rdf
                )

            if self.sideband:  # <- TODO make loop over cuts
                mass_binning = {
                    self.sideband.variable: np.linspace(
                        self.sideband.lower, self.sideband.upper, 200
                    )
                }
                for cut_label, cut in zip(
                    ("all", "signal", "sideband"),
                    (
                        self.sideband.range_cut(),
                        self.sideband.signal_cut(),
                        self.sideband.sideband_cut(),
                    ),
                ):
                    _temp_rdf = _count_rdf.Filter(cut)
                    ptrs[
                        f"{prefix}{category}_{cut_label}_count_{'_'.join(self.variables)}"
                    ] = self._rdf_histo(
                        _temp_rdf,
                        f"{prefix}{category}_{cut_label}_count_{'_'.join(self.variables)}",
                        weight=weight_branch,
                    )
                    ptrs[f"{prefix}{category}_{cut_label}_{self.sideband.variable}"] = (
                        self._rdf_histo(
                            _temp_rdf,
                            f"{prefix}{category}_{cut_label}_{self.sideband.variable}",
                            weight=weight_branch,
                            binning=mass_binning,
                        )
                    )
            else:
                if self.sweights:
                    ptrs[
                        f"{prefix}{category}_no_sweights_count_{'_'.join(self.variables)}"
                    ] = self._rdf_histo(
                        _count_rdf,
                        f"{prefix}{category}_no_sweights_count_{'_'.join(self.variables)}",
                    )
                ptrs[f"{prefix}{category}_count_{'_'.join(self.variables)}"] = (
                    self._rdf_histo(
                        _count_rdf,
                        f"{prefix}{category}_count_{'_'.join(self.variables)}",
                        weight=(
                            f"{self.sweights}_sw"
                            if self.sweights
                            else weight_branch if weight_branch else ""
                        ),
                    )
                )

        R.RDF.RunGraphs(list(ptrs.values()))

        _counts = {}
        additional_parts = [self.sideband.variable] if self.sideband else []
        for key, count in ptrs.items():
            hist = count.GetValue()
            _counts[key] = hist
            if self._to_project(key, additional_parts=additional_parts):
                _counts[
                    key.replace(
                        "_".join(self.variables), list(self.variables.keys())[0]
                    )
                ] = hist.ProjectionX()
                _counts[
                    key.replace(
                        "_".join(self.variables), list(self.variables.keys())[1]
                    )
                ] = hist.ProjectionY()

        if self.sideband:
            for key in list(_counts.keys()):
                if self._to_project(key, bin_requirement=False) and "_signal_" in key:
                    new_key = key.replace("_signal_", "_")
                    _counts[new_key] = _counts[key].Clone(new_key)
                    _counts[new_key].SetTitle(new_key)

                    _subtract_hist = _counts[
                        key.replace("_signal_", "_sideband_")
                    ].Clone(f"{new_key}_subtract_hist")

                    if "count" in key:
                        _counts[new_key].Add(_subtract_hist, -1 * self.sideband.scale())
                    else:
                        _sideband_count = _counts[
                            key.replace("_signal_", "_sideband_")
                        ].GetEntries()

                        if _subtract_hist.GetNbinsY() > 1:
                            bin_nums = it.product(
                                (
                                    list(range(1, _subtract_hist.GetNbinsX() + 1)),
                                    list(range(1, _subtract_hist.GetNbinsY() + 1)),
                                )
                            )
                        else:
                            bin_nums = zip(
                                list(range(1, _subtract_hist.GetNbinsX() + 1))
                            )

                        for b in bin_nums:
                            n_bin = _subtract_hist.GetBin(*b)
                            if (
                                _subtract_hist.GetBinCenter(n_bin)
                                > self.sideband.signal[0]
                                and _subtract_hist.GetBinCenter(n_bin)
                                < self.sideband.signal[1]
                            ):
                                width = (
                                    _subtract_hist.GetBinWidth(n_bin)
                                    if "count" not in key
                                    else None
                                )
                                _subtract_hist.SetBinContent(
                                    n_bin, _sideband_count * self.sideband.scale(width)
                                )
                            else:
                                _subtract_hist.SetBinContent(n_bin, 0)

                        _counts[new_key].Add(_subtract_hist, -1)

        return _counts

    def _base_efficiency(
        self, name, numerator_hist, denominator_hist, axis=None, integrated=False
    ):
        """Calculate efficiency from two histograms for the TIS or TOS trigger outcome categories

        Args:
            name: Name for the efficiency histogram
            numerator_hist: Histogram of passing events
            denominator_hist: Histogram of total events
            axis: Optional axis to project onto
            integrated: Whether to calculate as an integrated efficiency

        Returns:
            TGraphAsymmErrors or TGraph2DAsymmErrors: Efficiency histogram (in 1D or 2D)
        """
        _is_2D = isinstance(numerator_hist, R.TH2)
        xaxis = numerator_hist.GetXaxis()

        if _is_2D:
            yaxis = numerator_hist.GetYaxis()
            eff = R.TGraph2DAsymmErrors()
        else:
            eff = R.TGraphAsymmErrors()

        if integrated:
            numerator_value, numerator_error = helpers.sum_bins(numerator_hist)
            denominator_value, denominator_error = helpers.sum_bins(denominator_hist)
            if numerator_value > denominator_value:
                self.logger.info(
                    "Bin contains more passing events than total events (efficiency > 1), setting N(passing) to N(total)"
                )
                numerator_value = denominator_value

            if "wilson" in self.uncertainty_method:
                eff_value, eff_low, eff_up = stats.wilson(
                    numerator_value,
                    denominator_value,
                    passed_error=(
                        numerator_error
                        if "generalised" in self.uncertainty_method
                        else None
                    ),
                    total_error=(
                        denominator_error
                        if "generalised" in self.uncertainty_method
                        else None
                    ),
                )
            else:
                eff_value, eff_low, eff_up = stats.poisson(
                    numerator_value,
                    denominator_value,
                    passed_error=numerator_error,
                    total_error=denominator_error,
                )

            x_min = xaxis.GetXmin()
            x_max = xaxis.GetXmax()
            x_center = (x_min + x_max) / 2
            x_low = x_center - x_min
            x_up = x_max - x_center

            if _is_2D:
                yaxis = numerator_hist.GetYaxis()
                y_min = yaxis.GetXmin()
                y_max = yaxis.GetXmax()
                y_center = (y_min + y_max) / 2
                y_low = y_center - y_min
                y_up = y_max - y_center

                eff.AddPoint(x_center, y_center, eff_value)
                eff.SetPointError(0, x_low, x_up, y_low, y_up, eff_low, eff_up)
            else:
                eff.AddPoint(x_center, eff_value)
                eff.SetPointError(0, x_low, x_up, eff_low, eff_up)

        else:
            for n, midpoint_coords in enumerate(it.product(*self.midpoints)):
                coords = [midpoint_coords[axis]] if axis else midpoint_coords

                numerator_bin_num = numerator_hist.FindBin(*coords)
                numerator_value = numerator_hist.GetBinContent(numerator_bin_num)
                numerator_error = numerator_hist.GetBinError(numerator_bin_num)

                denominator_bin_num = denominator_hist.FindBin(*coords)
                denominator_value = denominator_hist.GetBinContent(denominator_bin_num)
                denominator_error = denominator_hist.GetBinError(denominator_bin_num)
                if numerator_value > denominator_value:
                    self.logger.info(
                        "Bin contains more passing events than total events (efficiency > 1), setting N(passing) to N(total)"
                    )
                    numerator_value = denominator_value

                if "wilson" in self.uncertainty_method:
                    eff_value, eff_low, eff_up = stats.wilson(
                        numerator_value,
                        denominator_value,
                        passed_error=(
                            numerator_error
                            if "generalised" in self.uncertainty_method
                            else None
                        ),
                        total_error=(
                            denominator_error
                            if "generalised" in self.uncertainty_method
                            else None
                        ),
                    )
                else:
                    eff_value, eff_low, eff_up = stats.poisson(
                        numerator_value,
                        denominator_value,
                        passed_error=numerator_error,
                        total_error=denominator_error,
                    )

                xbin = xaxis.FindBin(coords[0])
                x_center = xaxis.GetBinCenter(xbin)
                x_low = x_center - xaxis.GetBinLowEdge(xbin)
                x_up = xaxis.GetBinUpEdge(xbin) - x_center

                if _is_2D:
                    ybin = yaxis.FindBin(coords[1])
                    y_center = yaxis.GetBinCenter(ybin)
                    y_low = y_center - yaxis.GetBinLowEdge(ybin)
                    y_up = yaxis.GetBinUpEdge(ybin) - y_center

                    eff.AddPoint(x_center, y_center, eff_value)
                    eff.SetPointError(n, x_low, x_up, y_low, y_up, eff_low, eff_up)
                else:
                    eff.AddPoint(x_center, eff_value)
                    eff.SetPointError(n, x_low, x_up, eff_low, eff_up)

            eff.SetName(name)
            eff.SetTitle(name)

        return eff

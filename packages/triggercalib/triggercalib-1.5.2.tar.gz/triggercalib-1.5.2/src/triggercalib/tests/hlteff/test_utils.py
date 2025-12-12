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

from ctypes import c_double
import json
import os

import matplotlib.pyplot as plt
import mplhep as hep

import ROOT as R

hep.style.use("LHCb2")

R.gROOT.SetBatch(True)

os.makedirs("results", exist_ok=True)


def test_bins_io_json(example_file_hlteff):
    import json
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    h1 = HltEff(
        "test_write_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    h1.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h1.write_bins("results/test_bins_io_binning.json")

    # Read in binning scheme
    with open("results/test_bins_io_binning.json", "r") as binning_file:
        binning = json.load(binning_file)

    h2 = HltEff(
        "test_read_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        binning=binning,
        expert_mode=True,
        lazy=True,
    )

    assert h1.binning_scheme == h2.binning_scheme


def test_bins_io_yaml(example_file_hlteff):
    import yaml
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    h1 = HltEff(
        "test_write_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    h1.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h1.write_bins("results/test_bins_io_binning.yaml")

    # Read in binning scheme
    with open("results/test_bins_io_binning.yaml", "r") as binning_file:
        binning = yaml.safe_load(binning_file)

    h2 = HltEff(
        "test_read_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        binning=binning,
        expert_mode=True,
        lazy=True,
    )

    assert h1.binning_scheme == h2.binning_scheme


def test_bins_io_yaml(example_file_hlteff):
    import yaml
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    h1 = HltEff(
        "test_write_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    h1.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h1.write_bins("results/test_bins_io_binning.yaml")

    # Read in binning scheme
    with open("results/test_bins_io_binning.yaml", "r") as binning_file:
        binning = yaml.safe_load(binning_file)

    h2 = HltEff(
        "test_read_bins",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        binning=binning,
        expert_mode=True,
        lazy=True,
    )

    assert h1.binning_scheme == h2.binning_scheme


def test_conversion_to_th1(example_file_hlteff):
    from triggercalib import HltEff
    from triggercalib.utils.helpers import tgraph_to_np, th_to_np

    tree, path = example_file_hlteff

    hlteff = HltEff(
        "test_conversion_to_th1",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    hlteff.set_binning(
        {
            "observ1": {"label": "Observable 1", "bins": [4, 0, 8]},
        },
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )

    hlteff.counts("conversion_th1")
    hlteff.efficiencies("conversion_th1")

    # Test th_to_np
    xvals, yvals, xerrs, yerrs = th_to_np(
        hlteff["counts"]["conversion_th1_trig_count_observ1"]
    )

    hist_tgraph = hlteff.get_eff("conversion_th1_trig_efficiency_observ1", as_th=False)
    hist_th = hlteff.get_eff("conversion_th1_trig_efficiency_observ1", as_th=True)

    # Sum values/errors in tgraph
    tgraph_sum_vals = 0
    tgraph_sum_errs = 0

    # Sum values/errors in th1
    th_sum_vals = 0
    th_sum_errs = 0

    x = c_double(0)
    y = c_double(0)
    for point in range(hist_tgraph.GetN()):
        hist_tgraph.GetPoint(point, x, y)
        tgraph_sum_vals += y.value
        tgraph_sum_errs += hist_tgraph.GetErrorY(point)

        bin_n = hist_th.FindBin(x)
        th_sum_vals += hist_th.GetBinContent(bin_n)
        th_sum_errs += hist_th.GetBinError(bin_n)

    assert (
        tgraph_sum_vals == th_sum_vals
        and th_sum_vals == hist_th.GetSumOfWeights()
        and tgraph_sum_errs == th_sum_errs
    )

    # Test tgraph_to_np
    xvals, yvals, xerrs, (ylow_errs, yhigh_errs) = tgraph_to_np(hist_tgraph)


def test_conversion_to_th2(example_file_hlteff):
    from triggercalib import HltEff
    from triggercalib.utils.helpers import tgraph_to_np, th_to_np

    tree, path = example_file_hlteff

    hlteff = HltEff(
        "test_conversion_to_th2",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    hlteff.set_binning(
        {
            "observ1": {"label": "Observable 1", "bins": [4, 0, 8]},
            "observ2": {"label": "Observable 2", "bins": [4, -18, 12]},
        },
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("conversion_th2")
    hlteff.efficiencies("conversion_th2")

    xvals, yvals, zvals, xerrs, yerrs, zerrs = th_to_np(
        hlteff["counts"]["conversion_th2_trig_count_observ1_observ2"]
    )

    hist_tgraph = hlteff.get_eff(
        "conversion_th2_trig_efficiency_observ1_observ2", as_th=False
    )
    hist_th = hlteff.get_eff(
        "conversion_th2_trig_efficiency_observ1_observ2", as_th=True
    )

    # Sum values/errors in tgraph
    tgraph_sum_vals = 0
    tgraph_sum_errs = 0

    # Sum values/errors in th1
    th_sum_vals = 0
    th_sum_errs = 0

    x = c_double(0)
    y = c_double(0)
    z = c_double(0)
    for point in range(hist_tgraph.GetN()):
        hist_tgraph.GetPoint(point, x, y, z)
        tgraph_sum_vals += z.value
        tgraph_sum_errs += hist_tgraph.GetErrorZ(point)

        bin_n = hist_th.FindBin(x, y)
        th_sum_vals += hist_th.GetBinContent(bin_n)
        th_sum_errs += hist_th.GetBinError(bin_n)

    xvals, yvals, zvals, xerrs, yvals, (zlow_errs, zhigh_errs) = tgraph_to_np(
        hist_tgraph
    )


def test_regex(example_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    hlteff_regex = HltEff(
        "test_regex",
        tis="Hlt1.*",
        tos="Hlt1.*One",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )

    hlteff_explicit = HltEff(
        "test_explicit",
        tis=["Hlt1DummyOne", "Hlt1DummyTwo"],
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )

    assert hlteff_regex.tis == hlteff_explicit.tis
    assert hlteff_regex.tos == hlteff_explicit.tos


def test_uncertainty_methods(example_file_hlteff):
    import yaml
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    hlteff_poisson_errors = HltEff(
        "test_poisson_errors",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        uncertainty_method="poisson",
        lazy=True,
    )
    hlteff_poisson_errors.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff_poisson_errors.counts()
    hlteff_poisson_errors.efficiencies()

    hlteff_generalised_wilson_errors = HltEff(
        "test_generalised_wilson_errors",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        uncertainty_method="generalised_wilson",
        lazy=True,
    )
    hlteff_generalised_wilson_errors.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff_generalised_wilson_errors.counts()
    hlteff_generalised_wilson_errors.efficiencies()

    hlteff_standard_wilson_errors = HltEff(
        "test_standard_wilson_errors",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        uncertainty_method="standard_wilson",
        lazy=True,
    )
    hlteff_standard_wilson_errors.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff_standard_wilson_errors.counts()
    hlteff_standard_wilson_errors.efficiencies()

    x = c_double(0)
    y = c_double(0)
    values = {
        "x": [],
        "poisson": [],
        "poisson_error": [],
        "generalised_wilson": [],
        "generalised_wilson_error": [],
        "standard_wilson": [],
        "standard_wilson_error": [],
    }

    for label, hlteff in zip(
        ("poisson", "generalised_wilson", "standard_wilson"),
        (
            hlteff_poisson_errors,
            hlteff_generalised_wilson_errors,
            hlteff_standard_wilson_errors,
        ),
    ):
        hist_tgraph = hlteff.get_eff("trig_efficiency_observ1")
        for point in range(hist_tgraph.GetN()):
            hist_tgraph.GetPoint(point, x, y)
            if label == "poisson":
                values["x"].append(x.value)
            values[label].append(y.value)
            values[f"{label}_error"].append(hist_tgraph.GetErrorY(point))

    with open("results/test_uncertainty_methods_results.json", "w") as outfile:
        json.dump(values, outfile, indent=4)

    plt.figure()
    for label, capsize in zip(
        ("poisson", "generalised_wilson", "standard_wilson"), (12, 9, 6)
    ):
        plt.errorbar(
            values["x"],
            values[label],
            yerr=values[f"{label}_error"],
            label=label,
            capsize=capsize,
        )
    plt.xlabel("Observable 1")
    plt.ylabel("Efficiency")
    plt.legend()
    plt.savefig("results/test_uncertainty_methods_results.png")

    assert (
        values["poisson"] == values["generalised_wilson"]
        and values["poisson"] == values["standard_wilson"]
    )

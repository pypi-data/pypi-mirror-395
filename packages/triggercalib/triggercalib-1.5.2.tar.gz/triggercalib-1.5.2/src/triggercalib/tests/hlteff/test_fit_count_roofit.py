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

import ROOT as R

R.gROOT.SetBatch(True)

from triggercalib.utils.tests import check_result


def test_fit_count_roofit(example_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    ws = R.RooWorkspace("ws")
    obs = ws.factory("discrim[4800, 5600]")
    ws.factory(
        "BreitWigner::signal_pdf(discrim, signal_mean[5195, 5175, 5225], signal_width[8, 4, 24])"
    )
    ws.factory(
        "Exponential::combinatorial_pdf(discrim, combinatorial_exponent[-0.001, -0.01, 0])"
    )
    pdf = ws.factory(
        "SUM::pdf(signal_yield[10000, 0, 100000]*signal_pdf, combinatorial_yield[1000, 0, 100000]*combinatorial_pdf)"
    )

    hlteff = HltEff(
        "test_fit_count_roofit",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/fit_count_roofit/",
    )

    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5000 && discrim < 5400 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )

    hlteff.counts("fit_count_roofit")
    hlteff.efficiencies("fit_count_roofit")
    hlteff.write("results/output_test_fit_count_roofit.root")

    hist = hlteff.get_eff("fit_count_roofit_trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    result_okay, (true, lower, upper) = check_result(
        val,
        (err_low, err_high),
        sample=f"{path}:{tree}",
        cut="discrim > 5100 && discrim < 5300 && observ1 > 0 && observ1 < 8",
    )
    if not result_okay:
        print(f"Computed efficiency out of bounds: {true} not in ({lower}-{upper})")
        raise RuntimeError


def test_fit_count_roofit_weighted(example_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    ws = R.RooWorkspace("ws")
    obs = ws.factory("discrim[4800, 5600]")
    ws.factory(
        "BreitWigner::signal_pdf(discrim, signal_mean[5195, 5175, 5225], signal_width[8, 4, 24])"
    )
    ws.factory(
        "Exponential::combinatorial_pdf(discrim, combinatorial_exponent[-0.001, -0.01, 0])"
    )
    pdf = ws.factory(
        "SUM::pdf(signal_yield[10000, 0, 100000]*signal_pdf, combinatorial_yield[1000, 0, 100000]*combinatorial_pdf)"
    )

    hlteff = HltEff(
        "test_fit_count_roofit_weighted",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/fit_count_roofit_weighted/",
        weight="event_weight",
    )

    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5000 && discrim < 5400 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )

    hlteff.counts("fit_count_roofit_weighted")
    hlteff.efficiencies("fit_count_roofit_weighted")
    hlteff.write("results/output_test_fit_count_roofit_weighted.root")

    hist = hlteff.get_eff("fit_count_roofit_weighted_trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    result_okay, (true, lower, upper) = check_result(
        val,
        (err_low, err_high),
        sample=f"{path}:{tree}",
        cut="discrim > 5100 && discrim < 5300 && observ1 > 0 && observ1 < 8",
    )
    if not result_okay:
        print(f"Computed efficiency out of bounds: {true} not in ({lower}-{upper})")
        raise RuntimeError

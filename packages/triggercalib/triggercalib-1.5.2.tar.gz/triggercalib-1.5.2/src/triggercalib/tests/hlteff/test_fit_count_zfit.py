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


from triggercalib.utils import core

if core.zfit_installed():
    import ROOT as R

    R.gROOT.SetBatch(True)

    from triggercalib.utils.tests import check_result

    def test_fit_count_zfit(example_file_hlteff, zfit_model):

        from triggercalib import HltEff

        tree, path = example_file_hlteff
        obs, pdf = zfit_model

        hlteff = HltEff(
            "test_fit_count_zfit",
            tis="Hlt1DummyOne",
            tos="Hlt1DummyOne",
            particle="P",
            path=f"{path}:{tree}",
            lazy=True,
            observable=obs,
            pdf=pdf,
            output_path="results/fit_count_zfit/",
            expert_mode=True,
            plot_kwargs={"ylog": True, "pulls": False},
        )

        hlteff.set_binning(
            {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
            compute_bins=True,
            bin_cut="discrim > 5000 && discrim < 5400 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
        )

        hlteff.counts("fit_count_zfit")
        hlteff.efficiencies("fit_count_zfit")
        hlteff.write("results/output_test_fit_count_zfit.root")

        hist = hlteff.get_eff("fit_count_zfit_trig_total_efficiency_observ1")
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

    def test_fit_count_zfit_weighted(example_file_hlteff, zfit_model):

        from triggercalib import HltEff

        tree, path = example_file_hlteff
        obs, pdf = zfit_model

        hlteff = HltEff(
            "test_fit_count_zfit_weighted",
            tis="Hlt1DummyOne",
            tos="Hlt1DummyOne",
            particle="P",
            path=f"{path}:{tree}",
            lazy=True,
            observable=obs,
            pdf=pdf,
            output_path="results/fit_count_zfit_weighted/",
            expert_mode=True,
            plot_kwargs={"ylog": True, "pulls": False},
            weight="event_weight",
        )

        hlteff.set_binning(
            {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
            compute_bins=True,
            bin_cut="discrim > 5000 && discrim < 5400 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
        )

        hlteff.counts("fit_count_zfit_weighted")
        hlteff.efficiencies("fit_count_zfit_weighted")
        hlteff.write("results/output_test_fit_count_zfit_weighted.root")

        hist = hlteff.get_eff("fit_count_zfit_weighted_trig_total_efficiency_observ1")
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

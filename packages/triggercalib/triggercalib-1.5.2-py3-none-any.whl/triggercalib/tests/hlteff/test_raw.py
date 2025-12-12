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


def test_raw(example_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    hlteff = HltEff(
        "test_raw",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        expert_mode=True,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("raw")
    hlteff.efficiencies("raw")
    hlteff.write("results/output_test_raw.root")


def test_raw_weighted(example_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff

    hlteff = HltEff(
        "test_raw_weighted",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        expert_mode=True,
        weight="event_weight",
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("raw")
    hlteff.efficiencies("raw")
    hlteff.write("results/output_test_raw_weighted.root")


def test_raw_friend_weighted(example_file_hlteff, example_friend_file_hlteff):
    from triggercalib import HltEff

    tree, path = example_file_hlteff
    friend_tree, friend_path = example_friend_file_hlteff

    hlteff = HltEff(
        "test_raw_weighted",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        friend=f"{friend_path}:{friend_tree}",
        lazy=True,
        expert_mode=True,
        weight=f"{friend_tree.rsplit('/',1)[1]}.event_weight",
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("raw")
    hlteff.efficiencies("raw")
    hlteff.write("results/output_test_raw_weighted.root")

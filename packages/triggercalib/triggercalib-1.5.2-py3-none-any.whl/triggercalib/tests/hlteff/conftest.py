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
import numpy as np
import pytest
import ROOT as R


@pytest.fixture
def example_file_hlteff(N_events=100_000):
    """Create an example ROOT file for testing

    Creates a ROOT file containing signal and background events with known trigger
    efficiencies for testing the HltEff class

    Args:
        N_events: Total number of events to generate

    Returns:
        str: Path to generated ROOT file
    """

    path = "example_file.root"

    one_signal_efficiencies = {"trig": 0.8, "tos": 0.7, "tis": 0.2}
    two_signal_efficiencies = {"trig": 0.7, "tos": 0.65, "tis": 0.1}

    one_background_efficiencies = {"trig": 0.2, "tos": 0.18, "tis": 0.3}
    two_background_efficiencies = {"trig": 0.05, "tos": 0.04, "tis": 0.2}

    weights = {"signal": 0.9, "background": 0.5}

    purity = 4 / (
        one_signal_efficiencies["trig"] / one_background_efficiencies["trig"]
    )  # p = S / B
    background_yield = N_events / (1 + purity)
    signal_yield = purity * background_yield

    ws = R.RooWorkspace("ws_{hash}")

    discrim_var = ws.factory("discrim[5000, 4800, 5800]")
    observ1_var = ws.factory("observ1[0, -10, 10]")
    observ2_var = ws.factory("observ2[0, -50, 50]")

    ws.factory(
        "BreitWigner::signal_discrim_pdf(discrim, signal_discrim_mean[5200, 5200, 5200], signal_discrim_width[16, 16, 16])"
    )
    ws.factory(
        "BreitWigner::signal_observ1_pdf(observ1, signal_observ1_mean[4, 4, 4], signal_observ1_width[1, 1, 1])"
    )
    ws.factory(
        "Gaussian::signal_observ2_pdf(observ2, signal_observ2_mean[-1, -1, -1], signal_observ2_width[4, 4, 4])"
    )
    signal_pdf = ws.factory(
        "PROD::signal_pdf(signal_discrim_pdf, signal_observ1_pdf, signal_observ2_pdf)"
    )

    ws.factory(
        "Exponential::background_discrim_pdf(discrim, background_discrim_lambda[-0.001, -0.001, -0.001])"
    )
    ws.factory(
        "Gaussian::background_observ1_pdf(observ1, background_observ1_mean[-2, -2, -2], background_observ1_width[8, 8, 8])"
    )
    ws.factory("Uniform::background_observ2_pdf(observ2)")
    background_pdf = ws.factory(
        "PROD::background_pdf(background_discrim_pdf, background_observ1_pdf, background_observ2_pdf)"
    )

    tree_list = R.TList()

    signal_data = signal_pdf.generate(
        {discrim_var, observ1_var, observ2_var}, signal_yield
    )
    signal_data.convertToTreeStore()
    signal_tree = signal_data.tree()
    tree_list.Add(signal_tree)
    signal_n = signal_tree.GetEntries()

    signal_issignal = array("b", [0])
    signal_issignal_branch = signal_tree.Branch(
        "isSignal", signal_issignal, "isSignal/O"
    )

    signal_weight = array("d", [0])
    signal_weight_branch = signal_tree.Branch(
        "event_weight", signal_weight, "event_weight/D"
    )

    for line, signal_efficiencies in zip(
        ("Hlt1DummyOne", "Hlt1DummyTwo"),
        (one_signal_efficiencies, two_signal_efficiencies),
    ):

        signal_dec = array("b", [0])
        signal_dec_branch = signal_tree.Branch(
            f"{line}Decision", signal_dec, f"{line}Decision/O"
        )

        signal_tis = array("b", [0])
        signal_tis_branch = signal_tree.Branch(
            f"P_{line}Decision_TIS", signal_tis, f"P_{line}Decision_TIS/O"
        )

        signal_tos = array("b", [0])
        signal_tos_branch = signal_tree.Branch(
            f"P_{line}Decision_TOS", signal_tos, f"P_{line}Decision_TOS/O"
        )

        for _ in range(signal_n):
            signal_issignal[0] = 1
            signal_dec[0] = np.random.uniform() < signal_efficiencies["trig"]
            signal_tis[0] = np.random.uniform() < signal_efficiencies["tis"]
            signal_tos[0] = np.random.uniform() < signal_efficiencies["tos"]
            signal_weight[0] = weights["signal"]

            signal_issignal_branch.Fill()
            signal_dec_branch.Fill()
            signal_tis_branch.Fill()
            signal_tos_branch.Fill()
            signal_weight_branch.Fill()

    background_data = background_pdf.generate(
        {discrim_var, observ1_var, observ2_var}, background_yield
    )
    background_data.convertToTreeStore()
    background_tree = background_data.tree()
    tree_list.Add(background_tree)
    background_n = background_tree.GetEntries()

    background_issignal = array("b", [0])
    background_issignal_branch = background_tree.Branch(
        "isSignal", background_issignal, "isSignal/O"
    )

    background_weight = array("d", [0])
    background_weight_branch = background_tree.Branch(
        "event_weight", background_weight, "event_weight/D"
    )

    for line, background_efficiencies in zip(
        ("Hlt1DummyOne", "Hlt1DummyTwo"),
        (one_background_efficiencies, two_background_efficiencies),
    ):

        background_dec = array("b", [0])
        background_dec_branch = background_tree.Branch(
            f"{line}Decision", background_dec, f"{line}Decision/O"
        )

        background_tis = array("b", [0])
        background_tis_branch = background_tree.Branch(
            f"P_{line}Decision_TIS", background_tis, f"P_{line}Decision_TIS/O"
        )

        background_tos = array("b", [0])
        background_tos_branch = background_tree.Branch(
            f"P_{line}Decision_TOS", background_tos, f"P_{line}Decision_TOS/O"
        )

        for _ in range(background_n):
            background_issignal[0] = 0
            background_dec[0] = np.random.uniform() < background_efficiencies["trig"]
            background_tis[0] = np.random.uniform() < background_efficiencies["tis"]
            background_tos[0] = np.random.uniform() < background_efficiencies["tos"]
            background_weight[0] = weights["background"]

            background_issignal_branch.Fill()
            background_dec_branch.Fill()
            background_tis_branch.Fill()
            background_tos_branch.Fill()
            background_weight_branch.Fill()

    output_tree = R.TTree.MergeTrees(tree_list)
    with R.TFile(path, "RECREATE") as outfile:
        tree_dir = outfile.mkdir("Test")
        tree_dir.WriteObject(output_tree, "DecayTree")

    return "Test/DecayTree", path


@pytest.fixture
def example_friend_file_hlteff(example_file_hlteff, N_events=100_000):
    """Create an example ROOT file for testing friend functionality

    Args:
        N_events: Total number of events to generate

    Returns:
        str: Path to generated ROOT file
    """

    tree = "Test/FriendTree"
    path = "example_friend_file.root"

    original_treename, original_path = example_file_hlteff

    original_file = R.TFile.Open(original_path)
    original_tree = original_file.Get("Test").Get("DecayTree")
    original_tree.SetBranchStatus("*", 0)
    original_tree.SetBranchStatus("event_weight", 1)

    new_file = R.TFile(path, "RECREATE")
    new_tree = original_tree.CloneTree(0)
    new_tree.SetName("FriendTree")
    new_tree.CopyEntries(original_tree)

    tree_dir = new_file.mkdir("Test")
    tree_dir.WriteObject(new_tree, "FriendTree")

    return "Test/FriendTree", path

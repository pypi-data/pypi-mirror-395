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

import pytest
import ROOT as R


@pytest.fixture
def example_files_factorisable():
    """Create example ROOT files with factorisable distributions

    Creates signal and background ROOT files where the discriminating and control
    variables are independent (factorisable) for testing factorisation tests

    Returns:
        tuple: Paths to signal and background ROOT files
    """

    tree = "Hlt2Test/DecayTree"
    signal_path = "example_factorisable_signal_file.root"
    background_path = "example_factorisable_background_file.root"

    ws = R.RooWorkspace("ws_{hash}")
    discrim_var = ws.factory("discrim[5000, 4800, 5600]")
    observ1_var = ws.factory("observ1[0, -10, 10]")

    ws.factory(
        "BreitWigner::signal_discrim_pdf(discrim, signal_discrim_mean[5220], signal_discrim_width[32])"
    )
    ws.factory(
        "BreitWigner::signal_observ1_pdf(observ1, signal_observ1_mean[4], signal_observ1_width[1])"
    )
    signal_pdf = ws.factory("PROD::signal_pdf(signal_discrim_pdf, signal_observ1_pdf)")

    signal_data = signal_pdf.generate({discrim_var, observ1_var}, 20_000)
    signal_data.convertToTreeStore()
    signal_tree = signal_data.tree()

    with R.TFile.Open(signal_path, "RECREATE") as outfile:
        sig_out_dir = outfile.mkdir("Hlt2Test")
        sig_out_dir.WriteObject(signal_tree, "DecayTree")

    ws.factory(
        "Exponential::background_discrim_pdf(discrim, background_discrim_lambda[-0.001, -0.001])"
    )
    ws.factory(
        "Gaussian::background_observ1_pdf(observ1, background_observ1_mean[-2, -2, -2], background_observ1_width[8, 8, 8])"
    )
    background_pdf = ws.factory(
        "PROD::background_pdf(background_discrim_pdf, background_observ1_pdf)"
    )
    background_data = background_pdf.generate({discrim_var, observ1_var}, 20_000)
    background_data.convertToTreeStore()
    background_tree = background_data.tree()

    with R.TFile.Open(background_path, "RECREATE") as outfile:
        bkg_out_dir = outfile.mkdir("Hlt2Test")
        bkg_out_dir.WriteObject(background_tree, "DecayTree")

    return tree, signal_path, background_path


@pytest.fixture
def example_files_non_factorisable(example_files_factorisable):
    """Create example ROOT files with non-factorisable distributions

    Creates signal and background ROOT files where the discriminating and control
    variables are correlated (non-factorisable) for testing factorisation tests

    Args:
        example_files_factorisable: Fixture providing base files to modify

    Returns:
        tuple: Paths to signal and background ROOT files
    """

    tree, signal_path, background_path = example_files_factorisable
    non_factorisable_signal_path = signal_path.replace(
        "factorisable", "non_factorisable"
    )

    # Create dependence of discrim on observ1
    signal_rdf = R.RDataFrame(tree, signal_path)
    signal_rdf = signal_rdf.Redefine("discrim", "discrim + 12 * observ1")
    signal_rdf.Snapshot(tree, non_factorisable_signal_path)

    return tree, non_factorisable_signal_path, background_path

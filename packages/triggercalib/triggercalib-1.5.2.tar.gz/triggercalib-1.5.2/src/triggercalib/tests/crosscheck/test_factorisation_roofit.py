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

from triggercalib.utils.tests import factorisation_summary


def test_factorisable_factorisation_roofit(example_files_factorisable):
    from triggercalib.crosscheck import Factorisation

    tree, signal_path, background_path = example_files_factorisable

    ws = R.RooWorkspace("ws")
    discrim_var = ws.factory("discrim[4800, 5600]")
    ws.factory(
        "BreitWigner::signal_pdf(discrim, signal_mean[5200, 5175, 5225], signal_width[32, 24, 40])"
    )
    ws.factory(
        "Exponential::combinatorial_pdf(discrim, combinatorial_exponent[-0.001, -0.01, 0])"
    )
    pdf = ws.factory(
        "SUM::pdf(signal_yield[10000, 0, 100000]*signal_pdf, combinatorial_yield[1000, 0, 100000]*combinatorial_pdf)"
    )

    factorisation_test = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
        threads=1,
        verbose=True,
    )

    factorisation_summary(factorisation_test)
    if not factorisation_test.factorisable:
        raise RuntimeError


def test_non_factorisable_factorisation_roofit(example_files_non_factorisable):
    from triggercalib.crosscheck import Factorisation

    tree, signal_path, background_path = example_files_non_factorisable

    ws = R.RooWorkspace("ws")
    discrim_var = ws.factory("discrim[4800, 5600]")
    ws.factory(
        "BreitWigner::signal_pdf(discrim, signal_mean[5200, 5175, 5225], signal_width[32, 24, 40])"
    )
    ws.factory(
        "Exponential::combinatorial_pdf(discrim, combinatorial_exponent[-0.001, -0.01, 0])"
    )
    pdf = ws.factory(
        "SUM::pdf(signal_yield[10000, 0, 100000]*signal_pdf, combinatorial_yield[1000, 0, 100000]*combinatorial_pdf)"
    )

    factorisation_test = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
        threads=1,
        verbose=True,
    )

    factorisation_summary(factorisation_test)
    if factorisation_test.factorisable:
        raise RuntimeError

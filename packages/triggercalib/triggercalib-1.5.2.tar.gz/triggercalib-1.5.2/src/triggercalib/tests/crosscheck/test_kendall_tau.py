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


def test_factorisable_kendall_tau(example_files_factorisable):

    from triggercalib.crosscheck import KendallTau

    tree, signal_path, background_path = example_files_factorisable

    kt = KendallTau(
        "discrim", "observ1", f"{signal_path}:{tree}", f"{background_path}:{tree}"
    )

    assert kt.factorisable


def test_non_factorisable_kendall_tau(example_files_non_factorisable):

    from triggercalib.crosscheck import KendallTau

    tree, signal_path, background_path = example_files_non_factorisable

    kt = KendallTau(
        "discrim", "observ1", f"{signal_path}:{tree}", f"{background_path}:{tree}"
    )

    assert not kt.factorisable

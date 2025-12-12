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

    from triggercalib.utils.tests import factorisation_summary

    def test_factorisable_factorisation_zfit(example_files_factorisable, zfit_model):
        from triggercalib.crosscheck import Factorisation

        tree, signal_path, background_path = example_files_factorisable
        discrim_var, pdf = zfit_model

        factorisation_test = Factorisation(
            discrim_var,
            "observ1",
            [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
            pdf,
        )

        factorisation_summary(factorisation_test)
        if not factorisation_test.factorisable:
            raise RuntimeError

    def test_non_factorisable_factorisation_zfit(
        example_files_non_factorisable, zfit_model
    ):
        from triggercalib.crosscheck import Factorisation

        tree, signal_path, background_path = example_files_non_factorisable
        discrim_var, pdf = zfit_model

        factorisation_test = Factorisation(
            discrim_var,
            "observ1",
            [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
            pdf,
        )

        factorisation_summary(factorisation_test)
        if factorisation_test.factorisable:
            raise RuntimeError

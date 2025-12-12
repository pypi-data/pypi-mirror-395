###############################################################################
# (c) Copyright 2025 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import pytest

import numpy as np
import ROOT as R

from triggercalib.utils.helpers import parse_selection


R.gROOT.SetBatch(True)


def _check_selection(selection, lines, category):

    if category:
        correct = (
            selection.replace(" ", "")
            == f"({'||'.join(f'P_{line}Decision_{category}' for line in lines)})"
        )
    else:
        correct = (
            selection.replace(" ", "")
            == f"({'||'.join(f'{line}Decision' for line in lines)})"
        )

    if not correct:
        print(
            f"Selection '{selection}' was not produced correctly, instead as '{selection}"
        )
        raise RuntimeError
    return


def test_parse_selection_no_trig():

    lines = ("Hlt1DummyOne", "Hlt1DummyTwo")
    branches = {
        "Hlt1DummyOneDecision",
        "P_Hlt1DummyOneDecision_TOS",
        "P_Hlt1DummyOneDecision_TIS",
        "P_Hlt1DummyTwoDecision_TOS",
        "P_Hlt1DummyTwoDecision_TIS",
    }

    for category in ("TIS", "TOS"):
        selection = parse_selection(
            "P",
            lines,
            category,
            branches,
        )
        _check_selection(selection, lines, category)

    with pytest.raises(RuntimeError):
        parse_selection(
            "P",
            lines,
            "",
            branches,
        )


def test_parse_selection_with_trig():

    lines = ("Hlt1DummyOne", "Hlt1DummyTwo")
    branches = {
        "Hlt1DummyOneDecision",
        "P_Hlt1DummyOneDecision_TOS",
        "P_Hlt1DummyOneDecision_TIS",
        "Hlt1DummyTwoDecision",
        "P_Hlt1DummyTwoDecision_TOS",
        "P_Hlt1DummyTwoDecision_TIS",
    }

    for category in ("TIS", "TOS", ""):
        selection = parse_selection("P", lines, category, branches)
        _check_selection(selection, lines, category)


def test_parse_selection_regex_with_trig():

    lines = "Hlt1Dummy.*"
    branches = {
        "Hlt1DummyOneDecision",
        "P_Hlt1DummyOneDecision_TOS",
        "P_Hlt1DummyOneDecision_TIS",
        "Hlt1DummyTwoDecision",
        "P_Hlt1DummyTwoDecision_TOS",
        "P_Hlt1DummyTwoDecision_TIS",
    }

    for category in ("TIS", "TOS", ""):
        selection = parse_selection("P", lines, category, branches)
        _check_selection(selection, ["Hlt1DummyOne", "Hlt1DummyTwo"], category)

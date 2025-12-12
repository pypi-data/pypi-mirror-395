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

import numpy as np
import ROOT as R

from triggercalib.utils.stats import wilson


import matplotlib.pyplot as plt

R.gROOT.SetBatch(True)


def test_wilson():

    total = 100
    passed = np.arange(0, total + 1)

    _, lower_error, upper_error = wilson(passed, total)
    wilson(list(passed), total)

    lower_interval = np.vectorize(lambda x: R.TEfficiency.Wilson(total, x, 0.68, False))
    upper_interval = np.vectorize(lambda x: R.TEfficiency.Wilson(total, x, 0.68, True))

    tefficiency_lower_error = passed / total - lower_interval(passed)
    tefficiency_upper_error = upper_interval(passed) - passed / total

    plt.figure()
    plt.scatter(lower_error, tefficiency_lower_error)

    plt.savefig("A.pdf")

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    if not np.allclose(lower_error, tefficiency_lower_error) or not np.allclose(
        upper_error, tefficiency_upper_error
    ):
        print(
            "triggercalib.utils.stats.wilson interval and ROOT.TEfficiency.Wilson disagree"
        )
        raise RuntimeError

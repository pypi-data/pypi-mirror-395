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

from enum import Enum
from typing import Union

import ROOT as R

from triggercalib.utils import core

backend = Enum("backend", ["roofit", "zfit"])

if core.zfit_installed():
    import zfit

    data = Union[R.RooDataSet, zfit.Data]
    nll = zfit.loss.ExtendedUnbinnedNLL
    observable = Union[R.RooAbsReal, zfit.Space]
    pdf = Union[R.RooAbsPdf, zfit.pdf.BasePDF]
else:
    data = R.RooDataSet
    nll = None
    observable = R.RooAbsReal
    pdf = R.RooAbsPdf

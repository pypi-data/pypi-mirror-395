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

"""TriggerCalib: Trigger efficiency calculation and validation package

This package provides tools for calculating trigger efficiencies in HEP experiments
and validating the calculations through various statistical tests. It includes:

- HltEff: Main class for trigger efficiency calculations
- Factorisation: Tests for validating sWeight factorisation assumptions
- KendallTau: Non-parametric tests of variable independence
"""

import ROOT  # Required to ensure compatibility with tensorflow (if required)

from triggercalib.hlteff import HltEff

__all__ = ["HltEff"]

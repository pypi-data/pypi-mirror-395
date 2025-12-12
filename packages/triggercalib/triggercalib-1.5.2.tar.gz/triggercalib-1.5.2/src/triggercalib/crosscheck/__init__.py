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

"""Statistical validation tests for trigger efficiency calculations

This module provides tools for validating the assumptions underlying trigger
efficiency calculations, particularly for sWeight-based methods:

- Factorisation: Tests for validating sWeight factorisation assumptions
- KendallTau: Non-parametric tests of variable independence
"""

from .factorisation import Factorisation
from .kendall_tau import KendallTau

__all__ = ["Factorisation", "KendallTau"]

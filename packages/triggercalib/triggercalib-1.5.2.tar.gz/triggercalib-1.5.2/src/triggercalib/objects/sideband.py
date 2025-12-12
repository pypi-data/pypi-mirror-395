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

import numpy as np

from typing import Annotated, List


class Sideband:
    """Handler for sidebands in the sideband subtraction mitigation method

    This class manages the definition and manipulation of signal and sideband regions
    for background subtraction in trigger efficiency calculations. It provides methods
    to define cuts and the appropriate scale factor to estimate the number of background
    events in a given width.
    """

    def __init__(
        self,
        variable: str,
        signal: Annotated[List[float], 2],
        sidebands: List[Annotated[List[float], 2]],
    ):
        """Initialize a new Sideband instance

        Args:
            variable: Name of the variable used for sideband subtraction
            signal: Range in which to subtract background
            sidebands: Range defining the sideband regions [lower, upper]
        """

        self.variable = variable
        self.signal = signal
        self.sidebands = sidebands

        # Find minimum and maximum bounds for the variable, and check for non-overlapping windows
        self.lower = None
        self.upper = None
        for lower, upper in self.sidebands + [self.signal]:
            for _sideband in self.sidebands:
                if lower > _sideband[0] and upper < _sideband[1]:
                    raise ValueError(
                        "Sideband and signal windows should be defined such that they do not overlap"
                    )
            if self.lower is None or lower < self.lower:
                self.lower = lower
            if self.upper is None or upper > self.upper:
                self.upper = upper

        return

    def scale(self, width=None):
        """Calculate the scaling factor for sideband subtraction

        Args:
            width: Optional width to use instead of signal region width

        Returns:
            float: Scaling factor for sideband subtraction, calculated as
                  signal_width / (lower_sideband_width + upper_sideband_width)
        """
        if not (width):
            width = np.diff(self.signal)
        return width / sum(np.diff(self.sidebands))

    def range_cut(self):
        """Generate a cut string for the full variable range

        Returns:
            str: Cut string in ROOT format selecting events in the full range
        """

        return f"({self.variable} > {self.lower}) && ({self.variable} < {self.upper})"

    def sideband_cut(self):
        """Generate a cut string for the sideband regions

        Returns:
            str: Cut string in ROOT format selecting events in both lower and upper sidebands
        """

        return " || ".join(
            f"(({self.variable} > {lower}) && ({self.variable} < {upper}))"
            for (lower, upper) in self.sidebands
        )

    def signal_cut(self):
        """Generate a cut string for the signal region

        Returns:
            str: Cut string in ROOT format selecting events in the signal region
        """

        return f"({self.variable} > {self.signal[0]}) && ({self.variable} < {self.signal[1]})"

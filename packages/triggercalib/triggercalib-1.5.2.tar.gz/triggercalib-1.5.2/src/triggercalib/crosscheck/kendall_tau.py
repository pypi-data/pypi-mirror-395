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

# A special thanks is given to Hans Dembinski for his help and input on the sWeight checks.   #
# In particular, KendallTau is heavily influenced by Hans' notebook on sWeight factorisation: #
# - https://github.com/sweights/sweights/blob/main/doc/notebooks/factorization_test.ipynb     #

from sweights.independence import kendall_tau
import ROOT as R

from triggercalib.utils import io


class KendallTau:
    """Class for performing the Kendall's tau independence test

    This class implements Kendall's tau test to validate sWeight calculations by checking
    if the discriminating variable is independent of control variables in both signal
    and background samples. It uses the sweights package implementation of the test.
    """

    def __init__(
        self,
        discriminating_var: str,
        control_var: str,
        signal_sample: str,
        background_sample: str,
        bkg_discriminating_var: str = "",
        bkg_control_var: str = "",
        threshold: float = 0.01,
    ):
        """Initialize a new KendallTau instance

        Args:
            discriminating_var: Variable used for discrimination in signal sample
            control_var: Variable to test for independence in signal sample
            signal_sample: Path to signal sample, of the form <path>:<tree>
            background_sample: Path to background sample, of the form <path>:<tree>
            bkg_discriminating_var: Variable used for discrimination in background sample
            bkg_control_var: Variable to test for independence in background sample
            threshold: (arbitrary) threshold for independence test
        """
        self.discriminating_var = discriminating_var
        self.control_var = control_var

        self.bkg_discriminating_var = (
            bkg_discriminating_var if bkg_discriminating_var else discriminating_var
        )
        self.bkg_control_var = bkg_control_var if bkg_control_var else control_var

        self.threshold = threshold

        if signal_sample.count(":") != 1 or background_sample.count(":") != 1:
            raise ValueError("Sample names must be of the form {path}:{tree}")

        _signal_rdf = R.RDataFrame(*io.split_paths(signal_sample))
        _background_rdf = R.RDataFrame(*io.split_paths(background_sample))

        _signal_df = _signal_rdf.AsNumpy((self.discriminating_var, self.control_var))
        _background_df = _background_rdf.AsNumpy(
            (self.bkg_discriminating_var, self.bkg_control_var)
        )

        signal_tau, signal_tau_err, signal_pvalue = kendall_tau(
            _signal_df[self.discriminating_var], _signal_df[self.control_var]
        )
        background_tau, background_tau_err, background_pvalue = kendall_tau(
            _background_df[self.bkg_discriminating_var],
            _background_df[self.bkg_control_var],
        )

        self.results = {
            "signal_tau": signal_tau,
            "signal_tau_err": signal_tau_err,
            "signal_pvalue": signal_pvalue,
            "background_tau": background_tau,
            "background_tau_err": background_tau_err,
            "background_pvalue": background_pvalue,
            "threshold": threshold,
        }
        self.factorisable = signal_pvalue > threshold and background_pvalue > threshold

        return

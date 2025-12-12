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
    import pytest
    import zfit

    @pytest.fixture
    def zfit_model():
        """Create a zfit model for testing

        Returns:
            tuple: zfit Space and PDF for testing
        """
        # zfit model with BasePDF objects
        observable = zfit.Space("discrim", limits=(4800, 5600))

        # signal-gaussian extended
        mu = zfit.Parameter("signal_mu", 5200, 5150, 5300)
        sigma = zfit.Parameter("signal_sigma", 32, 0.01, 64)
        signal_yield = zfit.Parameter("signal_yield", 10_000, 0, 100_000)

        signal_pdf = zfit.pdf.Cauchy(obs=observable, m=mu, gamma=sigma)
        extended_sig = signal_pdf.create_extended(signal_yield, name="Signal")

        # bkg-exponential extended
        lambda_bkg = zfit.Parameter("background_exponent", -0.001, -0.01, 0)
        background_yield = zfit.Parameter("background_yield", 10_000, 0, 100_000)
        background_pdf = zfit.pdf.Exponential(lambda_bkg, obs=observable)
        extended_bkg = background_pdf.create_extended(background_yield, "Background")

        # SumPDF combines the signal and background with their respective yields
        pdf = zfit.pdf.SumPDF([extended_sig, extended_bkg], name="PDF", label="PDF")

        # Ensure the pdf is indeed a zfit.BasePDF object
        assert isinstance(
            pdf, zfit.pdf.BasePDF
        ), "The pdf must be a zfit.BasePDF instance"

        return observable, pdf

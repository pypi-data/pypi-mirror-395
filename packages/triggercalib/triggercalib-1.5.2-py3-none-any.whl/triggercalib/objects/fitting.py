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

# from lhcbstyle import LHCbStyle
# import matplotlib.pyplot as plt
# import mplhep as hep  # Import mplhep for HEP style plotting
import numpy as np

# import os
import ROOT as R
from typing import Dict

from triggercalib.utils import core, helpers, types

if core.zfit_installed():
    import zfit


def has_converged(result):
    # TODO: write docstring

    if isinstance(result, R.RooFitResult):
        return result.status() == 0 and result.covQual() == 3
    elif isinstance(result, zfit.minimizers.fitresult.FitResult):
        minimizer = zfit.minimize.Minuit()
        criterion = minimizer.create_criterion(result.loss, result.params)
        return criterion.converged(result)

    raise RuntimeError


def run_fit(
    pdf: types.pdf = None,
    data: types.data = None,
    nll: types.nll = None,
    fit_kwargs: Dict = {},
    max_attempts=1,
    require_convergence=True,
):
    # TODO: write docstring

    if nll is not None and (pdf is not None or data is not None):
        raise ValueError("Cannot specify both NLL and pdf/data.")

    attempts = 0
    backend = "zfit" if nll else helpers.get_backend(data=data, pdf=pdf)
    converged = False

    while attempts < max_attempts and not converged:
        if backend == "roofit":
            result = pdf.fitTo(
                data,
                **fit_kwargs,
            )
        elif backend == "zfit":
            if nll is None:
                nll = zfit.loss.ExtendedUnbinnedNLL(model=pdf, data=data)
            minimizer = zfit.minimize.Minuit()
            result = minimizer.minimize(nll)
            result.hesse()

        converged = has_converged(result)
        attempts += 1

    if not converged and require_convergence:
        raise RuntimeError("Fit did not converge, please check input parameters")

    return result


class Fit:
    """Initialize a new Fit instance

    Args:
        pdf: PDF model
        data: Data to fit
        fit_kwargs: Keyword arguments for run_fit
        lazy: Whether to perform the fit lazily (i.e., not perform the fit
            until `fit` is called)
        min_entries: Minimum number of events required for the fit
        max_attempts: Maximum number of attempts to perform the fit
        require_convergence: Whether to require the fit to converge
    """

    def __init__(
        self,
        pdf: types.pdf,
        data: types.data,
        fit_kwargs: Dict = {},
        lazy: bool = False,
        min_entries: float = -1,
        max_attempts: int = 5,
        require_convergence: bool = True,
    ):
        # TODO: write docstring

        self.pdf = pdf
        self.data = data
        self.backend = helpers.get_backend(data=self.data, pdf=self.pdf)

        self.fit_kwargs = fit_kwargs
        self.max_attempts = max_attempts
        self.require_convergence = require_convergence

        num_events = (
            data.sumEntries()
            if self.backend == "roofit"
            else np.sum(data.weights) if data.weights is not None else len(data)
        )

        if num_events < min_entries:
            raise RuntimeError(
                f"Insufficient events to perform the fit: {num_events} events < '{min_entries}' events"
            )

        if not lazy:
            self.fit()

        return

    def fit(self):
        # TODO: write docstring

        self.result = run_fit(
            self.pdf,
            self.data,
            fit_kwargs=self.fit_kwargs,
            max_attempts=self.max_attempts,
            require_convergence=self.require_convergence,
        )
        self.converged = has_converged(self.result)
        return

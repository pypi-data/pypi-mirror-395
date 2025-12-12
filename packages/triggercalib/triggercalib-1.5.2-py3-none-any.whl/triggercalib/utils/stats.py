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

from typing import List, Union
from statistics import NormalDist

import numpy as np


def poisson(
    passed: Union[float, List[float], np.ndarray[float]],
    total: Union[float, List[float], np.ndarray[float]],
    passed_error: Union[float, List[float], np.ndarray[float]] = None,
    total_error: Union[float, List[float], np.ndarray[float]] = None,
):
    """
    Calculate the efficiency and symmetric uncertainty based on propagation of Poisson-like errors

    Args:
        passed: int or array of int
            Number of events passing a criteria (numerator of the efficiency).
        total: int or array of int
            Total number of events (denominator of the efficiency).
        passed_error: int or array of int, optional
            Uncertainty on the number of events that pass some criteria if not strictly Poissonian;
            defaults to Poissonian uncertainty, `sqrt(passed)`, if not specified.
        total_error: int or array of int, optional
            Uncertainty on the total number of events if not strictly Poissonian;
            defaults to Poissonian uncertainty, `sqrt(total)`, if not specified.

    Returns:
        value: float or array of float
            The raw efficiency (passed / total).
        lower_error: float or array of float
            The symmetric error on the efficiency
        upper_error: float or array of float
            The upper error on the efficiency (same as lower error, since uncertainty is symmetric)

    Notes:
        This function implements the propagation of Poisson-like uncertainties as detailed in Eq. 14 of LHCb-PUB-2014-039 (https://cds.cern.ch/record/1701134/).
    """

    if passed_error is None:
        passed_error = np.sqrt(passed)
    if total_error is None:
        total_error = np.sqrt(total)

    failed = total - passed
    failed_error = np.sqrt(total_error**2 - passed_error**2)

    value = passed / total
    error = np.sqrt(
        (failed / total**2) ** 2 * passed_error**2
        + (passed / total**2) ** 2 * failed_error**2
    )

    return value, error, error


def wilson(
    passed: Union[float, List[float], np.ndarray[float]],
    total: Union[float, List[float], np.ndarray[float]],
    confidence: float = 0.68,
    passed_error: Union[float, List[float], np.ndarray[float]] = None,
    total_error: Union[float, List[float], np.ndarray[float]] = None,
):
    """
    Calculate the efficiency and lower/upper uncertainties based on a generalised Wilson interval.

    Args:
        passed: float or array of float
            Number of events passing a critera (numerator of the efficiency)
        total: float or array of float
            Total number of events (denominator of the efficiency)
        confidence: float, optional
            Confidence level for the interval; defaults to 0.68 (1 sigma), per the recommendation of the LHCb Statistics guidelines
        passed_error: int or array of int, optional
            Uncertainty on the number of events that pass some criteria if not strictly Poissonian; defaults to Poissonian uncertainty, `sqrt(passed)`, if not specified
        total_error: int or array of int, optional
            Uncertainty on the total number of events if not strictly Poissonian; defaults to Poissonian uncertainty, `sqrt(total)`, if not specified

    Returns:
        efficiency: float or array of float
            The raw efficiency (passed / total)
        lower_error: float or array of float
            The lower error on the efficiency from the Wilson interval
        upper_error: float or array of float
            The upper error on the efficiency from the Wilson interval

    Notes:
        This function implements the generalised Wilson interval of H. Dembinski and M. Schmelling, 2022 (https://arxiv.org/pdf/2110.00294).
    """

    if isinstance(passed, List) and not isinstance(passed, np.ndarray):
        passed = np.array(passed)
    if isinstance(total, List) and not isinstance(total, np.ndarray):
        total = np.array(total)

    if passed_error is None:
        passed_error = np.sqrt(passed)
    elif isinstance(passed_error, List) and not isinstance(passed_error, np.ndarray):
        passed_error = np.array(passed_error)

    if total_error is None:
        total_error = np.sqrt(total)
    elif isinstance(total_error, List) and not isinstance(total_error, np.ndarray):
        total_error = np.array(total_error)

    passed_nonpoisson_variance = np.nan_to_num(
        passed_error**2 - passed
    )  # non-Poisson term in variance on n(passed)
    if isinstance(passed_nonpoisson_variance, (List, np.ndarray)):
        passed_nonpoisson_variance[passed_nonpoisson_variance < 1e-12] = 0
    elif passed_nonpoisson_variance < 1e-12:
        passed_nonpoisson_variance = 0

    failed_nonpoisson_variance = np.nan_to_num(
        total_error**2 - passed_error**2 - total + passed
    )
    if isinstance(failed_nonpoisson_variance, (List, np.ndarray)):
        failed_nonpoisson_variance[failed_nonpoisson_variance < 1e-12] = 0
    elif failed_nonpoisson_variance < 1e-12:
        failed_nonpoisson_variance = 0

    # Define terms in line with the notation of the paper where possible
    n = total
    p = passed / total if total > 0 else 0
    z = NormalDist().inv_cdf((1 + confidence) / 2)

    # Calculate the lower and upper limits of the interval
    prefactor = (
        1
        / (
            1
            + (z**2 / n)
            * (1 - (passed_nonpoisson_variance + failed_nonpoisson_variance) / n)
        )
        if n > 0
        else 0
    )
    positive_term = (
        p + (z**2 / (2 * n)) * (1 - 2 * passed_nonpoisson_variance / n) if n > 0 else 0
    )
    plusminus_term = (
        (
            z
            / n
            * np.sqrt(
                p**2 * (passed_nonpoisson_variance + failed_nonpoisson_variance - n)
                + p * (n - 2 * passed_nonpoisson_variance)
                + passed_nonpoisson_variance
                + z**2
                / 4
                * (
                    1
                    - 4 * passed_nonpoisson_variance * failed_nonpoisson_variance / n**2
                )
            )
        )
        if n > 0
        else 0
    )

    lower_limit = np.maximum(
        np.nan_to_num(prefactor * (positive_term - plusminus_term)), 0
    )
    upper_limit = np.minimum(
        np.nan_to_num(prefactor * (positive_term + plusminus_term)), 1
    )

    return p, p - lower_limit, upper_limit - p

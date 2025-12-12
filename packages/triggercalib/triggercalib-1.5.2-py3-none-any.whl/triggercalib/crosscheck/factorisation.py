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

# Another special thanks is given to Maxim Lysenko, on whose work the implementation of the   #
# factorisation tests (particularly in zFit) is based                                         #

import logging
from typing import Annotated, List, Literal, Union

import numpy as np
import ROOT as R
from scipy.stats import chi2

from triggercalib.objects import Fit  # , Plot
from triggercalib.objects.fitting import run_fit
from triggercalib.utils import core, helpers, io, types

has_zfit = core.zfit_installed()
if has_zfit:
    import zfit


class Factorisation:
    """Class for performing factorisation tests on sWeight calculations

    This class implements factorisation tests to validate sWeight calculations by checking
    if the discriminating variable is independent of control variables. It supports both
    RooFit and zFit backends.
    """

    def __init__(
        self,
        discriminating_obs: types.observable,
        control_var: str,
        sample: Union[List[str], str],
        pdf: types.pdf,
        cut: Union[List[str], str] = "",
        max_attempts: int = 3,
        name: str = "",
        weight: str = "",
        threshold: float = 0.05,
        threads: int = 8,
        expert_mode: bool = False,
        verbose: bool = False,
        split_params: Union[List[str], Literal["all"]] = "all",
    ):
        """Initialize a new Factorisation instance

        Args:
            discriminating_obs: Discriminating variable used in sWeight calculation
            control_var: Control variable to test for independence
            sample: Path(s) to the input data file(s), of the form <path>:<tree>
            pdf: PDF model used for sWeight calculation
            cut: Additional selection criteria to apply
            max_attempts: Maximum number of attempts for fit
            threshold: p-value threshold for independence test
            threads: Number of threads to use for parallel processing
            split_params: Names of parameters to be split in simultaneous fit (in addition to yields), or "all" to split all floating parameters
        """
        self.discriminating_obs = discriminating_obs
        self.control_var = control_var
        self.weight = weight

        self.max_attempts = max_attempts
        self.threshold = threshold
        self.threads = threads
        self.expert_mode = expert_mode
        self.split_params = split_params

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

        self.backend = helpers.get_backend(
            observable=self.discriminating_obs,
            pdf=pdf,
        )

        if self.backend == "roofit":
            _range = f"{discriminating_obs.GetName()} > {discriminating_obs.getMin()} && {discriminating_obs.GetName()} < {discriminating_obs.getMax()}"
        elif self.backend == "zfit":
            self.logger.info(
                f"Enabled zFit backend for {name}, this functionality is currently experimental"
            )
            _range = " && ".join(
                f"({name} > {lower[0]} && {name} < {upper[0]})"
                for name, lower, upper in zip(
                    discriminating_obs.obs,
                    discriminating_obs.lower,
                    discriminating_obs.upper,
                )
            )

        self.rdf = R.RDataFrame(*io.split_paths(sample))
        self.rdf = self.rdf.Filter(_range)
        if cut:
            self.rdf = self.rdf.Filter(",".join(cut))

        low_data, high_data = self._create_datasets()

        self.split_fit_result = self._fit(
            (low_data, high_data), pdf, simultaneous=False
        )
        if verbose:
            print(helpers.fit_result_to_string(self.split_fit_result))

        self.simultaneous_fit_result = self._fit(
            (low_data, high_data), pdf, simultaneous=True
        )
        if verbose:
            print(helpers.fit_result_to_string(self.simultaneous_fit_result))

        # Compare likelihoods
        if self.backend == "roofit":
            self.split_nll = self.split_fit_result.minNll()
            self.split_nparams = len(
                [
                    param
                    for param in self.split_fit_result.floatParsFinal()
                    if param.getMin() != param.getMax()
                ]
            )

            self.simultaneous_nll = self.simultaneous_fit_result.minNll()
            self.simultaneous_nparams = len(
                [
                    param
                    for param in self.simultaneous_fit_result.floatParsFinal()
                    if param.getMin() != param.getMax()
                ]
            )

        elif self.backend == "zfit":
            self.split_nll = self.split_fit_result.fmin
            self.split_nparams = len(self.split_fit_result.params)

            self.simultaneous_nll = self.simultaneous_fit_result.fmin
            self.simultaneous_nparams = len(self.simultaneous_fit_result.params)

        self.ndof = self.split_nparams - self.simultaneous_nparams
        self.q_statistic = self.simultaneous_nll - self.split_nll
        self.p_value = chi2(self.ndof).sf(self.q_statistic)

        self.factorisable = self.p_value > self.threshold

        return

    def _create_datasets(self):
        """Create datasets for factorisation test

        Returns:
            tuple: Low and high datasets
        """

        # First event loop to get the cut value
        var_array = self.rdf.AsNumpy((self.control_var,))
        median = np.median(var_array[self.control_var])

        data_observables = (
            list(self.discriminating_obs.obs)
            if self.backend == "zfit"
            else [self.discriminating_obs.GetName()]
        )
        if self.weight:
            data_observables.append(self.weight)

        low_data_ptr = self.rdf.Filter(f"{self.control_var} < {median}").AsNumpy(
            data_observables, lazy=True
        )
        high_data_ptr = self.rdf.Filter(f"{self.control_var} >= {median}").AsNumpy(
            data_observables, lazy=True
        )

        low_data = helpers.create_dataset(
            low_data_ptr.GetValue(), self.discriminating_obs, weight=self.weight
        )
        high_data = helpers.create_dataset(
            high_data_ptr.GetValue(), self.discriminating_obs, weight=self.weight
        )

        return low_data, high_data

    def _fit(
        self,
        datasets: Annotated[List[types.data], 2],
        pdf: types.pdf,
        simultaneous: bool = False,
    ):
        """Perform fit to data

        Args:
            datasets: Low and high datasets
            pdf: PDF model
            simultaneous: Whether to perform simultaneous fit
            split_params: Names of parameters to be split in simultaneous fit (in addition to yields)

        Returns:
            fit_result: Fit result
        """

        if self.backend == "roofit":
            category = R.RooCategory("category", "category")
            category.defineType("low")
            category.defineType("high")

            low_dataset, high_dataset = datasets
            data = R.RooDataSet(
                "data",
                "data",
                {self.discriminating_obs},
                Index=category,
                Import={"low": low_dataset, "high": high_dataset},
            )

            ws = R.RooWorkspace(f"{pdf.GetName()}_ws")
            ws.Import(data)
            ws.Import(pdf)

            split_params = {y.GetName() for y in pdf.coefList()}
            if isinstance(self.split_params, List):
                split_params.update(self.split_params)

            if not simultaneous:
                for each_pdf in pdf.pdfList():
                    for param in each_pdf.getParameters(data):
                        if not param.isConstant():
                            if self.split_params == "all":
                                split_params.add(param.GetName())
                        else:
                            if param.GetName() in split_params:
                                raise Warning(
                                    f"Parameter '{param.GetName()}' is constant; splitting this parameter has no effect."
                                )
            sim_pdf = ws.factory(
                f"SIMCLONE::sim_{pdf.GetName()}({pdf.GetName()}, $SplitParam({{{','.join(split_params)}}},category))"
            )

            fit_kwargs = {
                "Extended": True,
                "EvalBackend": "cpu",
                "EvalErrorWall": False,
                "Minimizer": ("Minuit2", "minimize"),
                "NumCPU": self.threads,
                "Optimize": True,
                "Save": True,
                "Strategy": 2,
                "SumW2Error": False,
            }

            fit = Fit(
                pdf=sim_pdf,
                data=data,
                fit_kwargs=fit_kwargs,
                max_attempts=self.max_attempts,
                require_convergence=not self.expert_mode,
            )
            result = fit.result
        elif has_zfit and self.backend == "zfit":
            low_pdfs = []
            high_pdfs = []
            for _pdf in pdf.pdfs:
                _yield = _pdf.get_yield()

                _name = _yield.name
                _value = _yield.value()
                _lower = _yield.lower
                _upper = _yield.upper

                if simultaneous:
                    _low_params = list(_pdf.get_params(is_yield=False)) + [_pdf.obs]
                    _high_params = list(_pdf.get_params(is_yield=False)) + [_pdf.obs]
                else:
                    _low_params = []
                    _high_params = []
                    for _param in _pdf.get_params(is_yield=False):
                        _low_params.append(
                            zfit.Parameter(
                                f"low_{_param.name}",
                                _param.value(),
                                _param.lower,
                                _param.upper,
                            )
                        )
                        _high_params.append(
                            zfit.Parameter(
                                f"high_{_param.name}",
                                _param.value(),
                                _param.lower,
                                _param.upper,
                            )
                        )
                    _low_params.append(_pdf.obs)
                    _high_params.append(_pdf.obs)

                _low_pdf = type(_pdf)(*_low_params, **{"norm": _pdf.norm})
                _low_yield = zfit.Parameter(f"low_{_name}", _value, _lower, _upper)
                low_pdfs.append(_low_pdf.create_extended(_low_yield))

                _high_pdf = type(_pdf)(*_high_params, **{"norm": _pdf.norm})
                _high_yield = zfit.Parameter(f"high_{_name}", _value, _lower, _upper)
                high_pdfs.append(_high_pdf.create_extended(_high_yield))

            low_pdf = zfit.pdf.SumPDF(low_pdfs)
            low_nll = zfit.loss.ExtendedUnbinnedNLL(model=low_pdf, data=datasets[0])

            high_pdf = zfit.pdf.SumPDF(high_pdfs)
            high_nll = zfit.loss.ExtendedUnbinnedNLL(model=high_pdf, data=datasets[1])

            nll = low_nll + high_nll
            result = run_fit(
                nll=nll,
                max_attempts=self.max_attempts,
                require_convergence=not self.expert_mode,
            )
        else:
            return ValueError(f"Backend '{self.backend}' not recognised")

        return result

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

import ROOT as R
from typing import Annotated, List

distributions = {
    "breitwigner": "BreitWigner",
    "doublecrystalball": "CrystalBall",
    "exponential": "Exponential",
    "gauss": "Gaussian",
}


def build_component(ws, name, observable, component):
    """Build a RooFit PDF component

    Args:
        ws: RooWorkspace to build component in
        name: Name for the component
        observable: Observable to build PDF for
        component: Component configuration dictionary

    Returns:
        RooAbsPdf: Built PDF component
    """
    distribution = distributions[component["model"]]
    expanded_vars = ", ".join(
        f"{name}_{variable}[{', '.join(str(value) for value in values)}]"
        for variable, values in component["variables"].items()
    )
    expanded_vars = f"{observable}, {expanded_vars}"

    ws.factory(f"{distribution}::{name}_pdf({expanded_vars})")

    return ws


def check_result(
    value: float,
    error: Annotated[List[float], 2],
    sample: str = "example_file.root:Hlt2Test/DecayTree",
    cut: str = "",
    line: str = "Hlt1DummyOne",
    threshold: float = 5.0,
):
    """Check if a test result matches expectations

    Args:
        value: Measured value to check
        error: List of lower and upper uncertainties
        sample: Path to input ROOT file and tree
        cut: Additional selection criteria
        line: Trigger line to check
        threshold: Maximum allowed deviation in percent

    Returns:
        bool: Whether result matches expectations within threshold
    """
    sample_rdf = R.RDataFrame(*reversed(sample.rsplit(":", 1)))
    sample_rdf = sample_rdf.Filter(cut)
    sample_rdf = sample_rdf.Filter("isSignal")
    denominator = sample_rdf.Count()
    numerator = sample_rdf.Filter(f"{line}Decision").Count()
    R.RDF.RunGraphs((numerator, denominator))

    true_efficiency = numerator.GetValue() / denominator.GetValue()

    result_okay = (
        true_efficiency > value - threshold * error[0]
        and true_efficiency < value + threshold * error[1]
    )
    if not result_okay:
        print(
            f"True efficiency '{true_efficiency:.4f}' does not lie within window [{value - threshold * error[0]:.4f} - {value + threshold * error[1]:.4f}] ({threshold:.1f} sigma threshold)"
        )

    return result_okay, (
        true_efficiency,
        value - threshold * error[0],
        value + threshold * error[1],
    )


def factorisation_summary(factorisation_test, verbose=True):
    # TODO: write docstring

    output_string = f"Split NLL: {factorisation_test.split_nll}"
    output_string += f"Simultaneous NLL: {factorisation_test.simultaneous_nll}"
    output_string += f"q-statistic: {factorisation_test.q_statistic}"
    output_string += f"p-value: {factorisation_test.p_value}"

    if verbose:
        print(output_string)
    return output_string

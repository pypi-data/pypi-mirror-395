# TriggerCalib - Tooling for trigger efficiencies

This repository contains tools developed for calculating trigger efficiencies in LHCb analyses and studies.
The full documenation for the `TriggerCalib` tools can be found here: [**https://triggercalib.docs.cern.ch/**](https://triggercalib.docs.cern.ch/).

At the core of these tools is the `HltEff` class, which implements the TISTOS method (as laid out in [LHCb-PUB-2014-039](https://cds.cern.ch/record/1701134/files/LHCb-PUB-2014-039.pdf)) to produce trigger efficiencies in ROOT `TH1`/`TH2` histograms.
This will be extended in the near future by a `.yaml`-configurable interface to the class, with the aim of being familiar to users of the [`HltEfficiencyChecker`](https://gitlab.cern.ch/lhcb/DaVinci/-/tree/master/HltEfficiencyChecker) tool for studying MC efficiencies in simulation. 
An additional tool, currently in planning, further extend this functionality by providing users with trigger efficiency correction tables (à la [`PIDCalib2`](https://gitlab.cern.ch/lhcb-rta/pidcalib2)) in key control channels.

If you wish to contribute to TriggerCalib, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgements

We acknowledge funding from the European Union Horizon 2020 research and innovation programme, call H2020-MSCA-ITN-2020, under Grant Agreement n. 956086

<a href="https://www.smarthep.org/">
    <img src="https://www.smarthep.org/wp-content/uploads/2022/11/SmartHEP-Logo-Full-Colour.jpg" alt="SMARTHEP logo" height="64"/>
</a>
<a href="https://www.smarthep.org/">
    <img src="https://www.smarthep.org/wp-content/uploads/2022/11/EU-Logo.jpg" alt="EU flag" height="64"/>
</a>
<a href="https://www.smarthep.org/">
    <img src="https://www.smarthep.org/wp-content/uploads/2022/11/marie_curie_logo-300x182-1.png" alt="MSCA logo" height="64"/>
</a>
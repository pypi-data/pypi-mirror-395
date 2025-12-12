---
hide:
    - toc
---

# TriggerCalib tutorials
The following tutorials work through from the simplest case of a trigger efficiency calculation, a simple efficiency of a single HLT1 line, up to a complex selection involving multiple lines at both.
The tutorials also demonstrate all three background mitigation method.
The tutorials all take the form of Jupyter notebooks, which can be found [in the GitLab repository](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/tree/master/docs/guide/tutorials) and worked through directly.
Requests for additional tutorials are very welcome and should be opened as [issues](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues).

The following tutorials are currently available:

<div class="grid cards" markdown>

- [:material-numeric-1-box: __Calculating the efficiency of a single HLT1 line__](hlt1.ipynb)
- [:material-chart-bell-curve: __Applying fit-and-count to mitigate background__](fit-and-count.ipynb)
- [:material-chart-bell-curve-cumulative: __Applying _sWeights_ to mitigate background__](sweights.ipynb)
- [:material-land-plots-circle: __Calculating efficiencies with a 2D binning scheme__](2d-binning.ipynb)
- [:material-plus-box: __Combined efficiency of multiple HLT1 lines__](combined.md)
- [:material-numeric-2-box: __Calculating HLT2 efficiencies in spruced samples__](hlt2.md)
- [:material-texture-box: __Efficiency of a combined HLT1 and HLT2 selection__](hlt1-and-hlt2.md)

</div>
# Contributing to TriggerCalib

Contributions to TriggerCalib are very welcome! Bug reports, feature requests and code contributions are encouraged: bug reports and feature requests can be submitted as [issues](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues); code contributions can be proposed in [merge requests](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/merge_requests). Details on how to submit these are provided below.

For more information and to ask questions, we recommend joining the [TriggerCalib Mattermost channel](https://mattermost.web.cern.ch/lhcb/channels/triggercalib).

## Submitting bug reports/feature requests

To submit a bug report or feature request, please open an [issue](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues).
Bug reports should contain a description of the bug and the circumstances in which the bug was discovered.
If possible, a [minimal reproducible example](https://en.wikipedia.org/wiki/Minimal_reproducible_example) should be included.
Feature requests should contain a description of the requested feature, an explanation of why this is required.
Feature requests can be supplemented with information on how to approach implementing the feature or with a corresponding merge request (see [Developing TriggerCalib](#Developing%20TriggerCalib)).

We kindly ask that you add the `bug` or `feature` label to your issue so that we can keep track.


## Developing TriggerCalib

Developments to TriggerCalib are encouraged and can be proposed in a [merge request](https://gitlab.cern.ch/lhcb-rta/triggercalib/-/merge_requests).
Merge requests should ideally aim to close a raised issue (see [Submitting bug reports/feature requests](#Submitting%20bug%20reports%2Ffeature%20requests)).
When a merge request is ready for review, please assign Jamie ([@jagoodin](https://gitlab.cern.ch/jagoodin)) as a reviewer.
For a merge request to be merged it must:

- Pass the CI pipeline (see [Running the tests](#Running%20the%20tests) and [Fixing the formatting](#Fixing%20the%20formatting) for troubleshooting)
- Have received an approval

A few labels currently exist to help track merge requests; please use these if they cover an aspect of the code under development.

To develop TriggerCalib locally:
1. Clone the repository
2. Source `LbEnv`:
    ```
    source /cvmfs/lhcb.cern.ch/lib/LbEnv
    ```
3. Create a virtual environment
    ```
    lb-conda-dev virtual-env default/2024-06-08 .venv
    ```
4. Install the packages required for development:
    ```
    .venv/run pip install -r requirements-dev.txt
    ```

### Running the tests

The CI pipeline job `testing` runs a set of tests in `pytest`.
These tests can be run locally by running `pytest` from the top level of the repository.

### Fixing the formatting

The CI pipeline applies a formatting check with `black`.
Fixes to the formatting can be made by running `black src` from the top level of the repository

### Building the documentation

The documentation is built with `mkdocs`, using the environment defined in `environment-docs.yml`.
To build the documentation locally for the first time, run `source build-docs.sh` from the top level of the repository.
After this, you can view the documentation locally by running `python -m mkdocs serve` and open the documentation in your browser at http://127.0.0.1:8000 (or http://127.0.0.0:8000).
# legend-daq2lh5

[![PyPI](https://img.shields.io/pypi/v/legend-daq2lh5?logo=pypi)](https://pypi.org/project/legend-daq2lh5/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/legend-exp/legend-daq2lh5?logo=git)
[![GitHub Workflow Status](https://img.shields.io/github/checks-status/legend-exp/legend-daq2lh5/main?label=main%20branch&logo=github)](https://github.com/legend-exp/legend-daq2lh5/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Codecov](https://img.shields.io/codecov/c/github/legend-exp/legend-daq2lh5?logo=codecov)](https://app.codecov.io/gh/legend-exp/legend-daq2lh5)
![GitHub issues](https://img.shields.io/github/issues/legend-exp/legend-daq2lh5?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr/legend-exp/legend-daq2lh5?logo=github)
![License](https://img.shields.io/github/license/legend-exp/legend-daq2lh5)
[![Read the Docs](https://img.shields.io/readthedocs/legend-daq2lh5?logo=readthedocs)](https://legend-daq2lh5.readthedocs.io)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10721223.svg)](https://doi.org/10.5281/zenodo.10721223)

JSON-configurable conversion of digitized data into
[LEGEND HDF5](https://legend-exp.github.io/legend-data-format-specs/dev/hdf5/),
with optional data pre-processing via [dspeed](https://dspeed.readthedocs.io)
and data compression via [legend-pydataobj](https://legend-pydataobj.readthedocs.io).

Currently supported DAQ data formats:
* [FlashCam](https://www.mizzi-computer.de/home)
* [CoMPASS](https://www.caen.it/products/compass)
* [ORCA](https://github.com/unc-enap/Orca), reading out:
  - FlashCam
  - [Struck SIS3302](https://www.struck.de/sis3302.htm)
  - [Struck SIS3316](https://www.struck.de/sis3316.html)

If you are using this software, consider
[citing](https://doi.org/10.5281/zenodo.10721223)!

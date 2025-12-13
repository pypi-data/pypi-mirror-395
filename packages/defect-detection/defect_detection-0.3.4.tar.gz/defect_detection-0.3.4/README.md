# defect_detection

[![PyPI](https://img.shields.io/pypi/v/defect_detection)](https://pypi.org/project/defect_detection/)
[![Build](https://github.com/lovaslin/defect_detection/actions/workflows/cd.yml/badge.svg)](https://github.com/lovaslin/defect_detection/actions)

This packge provides a basic API to implement defect detection algorithms.
These algorithms can be tune in order to automatically detect any defects in a PCB or other components.

## Requirement

The following package are required :
- numpy
- opencv-python
- torch
- scikit-learn

Recommended python version >= 3.8

## Installation

To install the latest stable release from PyPI :
```bash
pip install defect_detection
```

For developper who wants to work with a local and editable version :
```bash
git clone https://github.com/lovaslin/defect_detection.git
cd defect_detection
pip install -e .
```

For the local install, you should of course run the commands using a clean python environment.
I recommend to use `venv` to setup a pip-friendly environemnt.

## Usage

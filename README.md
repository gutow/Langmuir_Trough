# Trough Controller
This software is a custom controller for the research Langmuir trough in the
Gutow Lab at UW Oshkosh. It is written in Python and expects to run in a
Jupyter notebook environment. However, all of the parts that are not elements
of the user interface should work in a vanilla Python environment.

Hardware requirements:
Raspberry Pi compatible system with a Pi-Plates DAQC2 data acquisition plate.

## Usage

## Installation

## Change Log
* 0.1.0 First pypi compatible package version.

## Development
### Ideas/Things to do
* Switch to returning fraction open for barrier position rather than volts.
* Function that clears all the data deques rather than having to call `.clear()`
  on each of them separately.
* 

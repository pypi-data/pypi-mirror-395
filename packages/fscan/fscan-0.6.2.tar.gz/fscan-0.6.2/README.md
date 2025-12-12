# Fscan

[![PyPI version](https://badge.fury.io/py/fscan.svg)](https://badge.fury.io/py/fscan)
![Conda](https://img.shields.io/conda/v/conda-forge/fscan?label=conda-forge)
![PyPI - License](https://img.shields.io/pypi/l/fscan)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fscan)

Fscan pipeline for characterizing persistent narrowband spectral artifacts in gravitational wave detector data

## Installation

On Unix systems, Fscan can be installed easily using conda:

```shell
conda install -c conda-forge fscan
```

Or from PyPI:

```shell
pip install fscan
```

`LALPulsar` and `lalframe` are required for running but optional dependencies. You may either install it into the environment using

```shell
conda install -c conda-forge fscan[conda]
```

or install `LALSuite` [from source](https://git.ligo.org/lscsoft/lalsuite). 

## Running Fscan

Fscan runs on LIGO site computing resources (LHO, LLO, or CIT) by accessing the frame files directly on-disk (not via NDS).
The main way to run Fscan is using the `FscanDriver` program on the command line together with arguments that tell Fscan how to run.

One key argument is the channel configuration file.
This file contains the information needed on how the Fscan program finds and processes data on an individual channel basis.
Example channel configuration files may be [found here](https://git.ligo.org/CW/instrumental/fscan-configuration).

### Example running Fscan

Run the `FscanDriver <args>` exectuable with appropriate arguments (see `FscanDriver -h` for additional details). For example at CIT:

```shell
FscanDriver --chan-opts=fscan-configuration/configuration/examples/example_ch_info.yml --SFTpath=. --create-sfts=1 --plot-output=1 --accounting-group=ligo.dev.o4.detchar.linefind.fscan --accounting-group-user=albert.einstein --analysisStart=20200229 --analysisDuration=1day --averageDuration=1day
```

### Another example (using a configuration file)

Running from the Fscan source directory,

```shell
FscanDriver --config configuration/example.config
```

Be sure to edit the arguments in `example.config` to reflect the locations of your lalsuite and fscan installations.

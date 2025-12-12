.. Fscan documentation master file, created by
   sphinx-quickstart on Wed Oct 22 17:05:15 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================
Fscan documentation
===================

Fscan is a package that allows creating high-resolution spectra, spectrograms,
persistency figure of merit, and coherence plots for gravitational wave
detector strain data and auxiliary channels. This enables characterization of
detector strain data for persistent narrowband artifacts and pathways for
mitigation efforts.

.. image:: https://badge.fury.io/py/fscan.svg
    :target: https://badge.fury.io/py/fscan
    :alt: Fscan PyPI version badge
.. image:: https://img.shields.io/conda/vn/conda-forge/fscan.svg
    :target: https://anaconda.org/conda-forge/fscan/
    :alt: Fscan Conda-forge version badge
.. image:: https://img.shields.io/pypi/l/fscan.svg
    :target: https://choosealicense.com/licenses/gpl-3.0/
    :alt: Fscan license badge
.. image:: https://img.shields.io/pypi/pyversions/fscan.svg
    :alt: Fscan python version badge


---------------
Getting started
---------------

.. toctree::
    :maxdepth: 1

    Installing Fscan <install>


-----------
Using Fscan
-----------

.. include:: usage.rst


---------------------
Command line programs
---------------------

.. toctree::
    :maxdepth: 2

    fscan


---
API
---

Fscan has a number of functions that are useful when running investigations of narrow spectral artifacts.
The LVK CW/Stochastic/DetChar line investigations team utilizes many of these functions when running `bespoke scripts <https://git.ligo.org/CW/instrumental/line-investigations>`__.

Further information on the Fscan API to interface with these functions may be found below:

.. toctree::
    :maxdepth: 1
    :caption: Batch processing

    batch

.. toctree::
    :maxdepth: 2
    :caption: Plotting

    plot/index

.. toctree::
    :maxdepth: 2
    :caption: Processing data

    process/index

.. toctree::
    :maxdepth: 2
    :caption: Utility functions

    utils/index


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

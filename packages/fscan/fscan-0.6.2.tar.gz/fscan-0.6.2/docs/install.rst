================
Installing Fscan
================

.. _fscan-install-conda:

The recommended way of installing Fscan is with `Conda <https://conda.io>`__:

.. code-block:: bash

   conda install -c conda-forge fscan

Alternatively, Fscan can be installed using ``pip``

.. _fscan-install-pip:

.. code-block:: bash

    python -m pip install fscan

---------------------
Dependencies
---------------------

The Fscan workflow depends on ``lalpulsar`` programs.
These are optional dependencies because one may choose to install ``LALSuite`` `from source <https://git.ligo.org/lscsoft/lalsuite>`__.
To install from ``conda`` simply run

.. code-block:: bash

   conda install -c conda-forge fscan[conda]

Otherwise, please refer to the ``LALSuite`` `building from source <https://git.ligo.org/lscsoft/lalsuite/-/blob/master/README.md?ref_type=heads#building-from-source>`__.
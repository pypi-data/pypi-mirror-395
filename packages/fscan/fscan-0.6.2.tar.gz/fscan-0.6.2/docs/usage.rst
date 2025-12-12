Fscan runs on LIGO site computing resources (LHO, LLO, or CIT) by accessing the frame files directly on-disk (not via NDS).
The main way to run Fscan is using the ``FscanDriver`` program on the command line together with arguments that tell Fscan how to run.

One key argument is the channel configuration file.
This file contains the information needed on how the Fscan program finds and processes data on an individual channel basis::

    - {channel: H1:CAL-DELTAL_EXTERNAL_DQ, frametype: H1_R, plot_sub_band: 100, segment_type: H1:DMT-ANALYSIS_READY, freq_res: 0.1, persist_avg_sec: 14400, auto_track: 0.5}
    - {channel: H1:PEM-EX_MAG_VEA_FLOOR_X_DQ, frametype: H1_R, plot_sub_band: 100, segment_type: H1:DMT-ANALYSIS_READY, freq_res: 0.1, coherence: H1:CAL-DELTAL_EXTERNAL_DQ, persist_avg_sec: 14400, auto_track: 0.5}
    - {channel: H1:PEM-EX_MAG_VEA_FLOOR_X_DQ, frametype: H1_R, plot_sub_band: 100, segment_type: ALL, freq_res: 0.1, include_extra_sub_band: no, persist_avg_opt: 1}

Examples and production running files may be `found here <https://git.ligo.org/CW/instrumental/fscan-configuration>`__.

Other ``FscanDriver`` options may be found by the help output

.. code-block:: bash

    FscanDriver --help

An example command for running ``FscanDriver`` may look like:

.. code-block:: bash

    FscanDriver --create-sfts=1 --plot-output=1 --accounting-group=ligo.dev.o4.detchar.linefind.fscan --full-band-avg=1 --analysisStart=20251102 --analysisDuration=1day --averageDuration=1day --seek-existing-sfts=0 --chan-opts=chanopts.yaml --SFTpath=~/public_html/fscan/ --intersect-data=1 --delete-ascii=1 --run=0 --make-sft-dag-path=/home/pulsar/gitrepos/lalsuite/_inst/bin --make-sft-path=/home/pulsar/gitrepos/lalsuite/_inst/bin --spec-tools-path=/home/pulsar/gitrepos/lalsuite/_inst/bin --postproc-path=/home/pulsar/.conda/envs/fscan-py3.10/bin --allow-skipping=1 --accounting-group-user=albert.einstein

Fscan will process the channels listed in the channel configuration yaml file.
The output of Fscan will be a webpage with plots of spectra, spectrograms, and other figures of merit in the Summary Page style.

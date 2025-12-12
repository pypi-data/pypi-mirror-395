# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#               Ansel Neunzert (2023)
#
# This file is part of fscan

import os
from pathlib import Path
import subprocess

from .batch import MakeSFTJob, ProcessSFTs, SummaryJob, write_workflow
from .utils import dtutils as dt
from .utils.config import CustomConfParser, MultiConfParser
from .utils.io import read_channel_config
from .utils.reuse import use_existing_sfts
from .utils.utils import channels_per_segments, epseg_setup
from .utils.utils import epoch_info as ep_info


def epoch_info(args):
    """
    This builds a list of dictionaries that have the epoch list and variable
    information
    """
    gps_intervals, duration_tags, epoch_tags = dt.args_to_intervals(
        analysisStart=args.analysisStart,
        analysisEnd=args.analysisEnd,
        analysisDuration=args.analysisDuration,
        averageDuration=args.averageDuration,
        snapToLast=args.snapToLast,
        greedy=args.greedy,
    )

    out = ep_info(gps_intervals, duration_tags, epoch_tags,
                  args.Tsft, args.overlap_fraction)

    return out


def main():
    parser = CustomConfParser(
        description='This is the top-level management of Fscans',
    )
    parser.add_argument('-O', '--observing-run', type=int, default=100,
                        help='For public SFTs, observing run data the SFTs are'
                             ' generated from, or (in the case of mock data '
                             'challenge data) the observing run on which the '
                             'data is most closely based')
    parser.add_argument('-K', '--observing-kind', type=str,
                        choices=['RUN', 'AUX', 'SIM', 'DEV'], default='AUX',
                        help='For public SFTs, one of: "RUN" for production '
                             'SFTs of h(t) channels; "AUX" for SFTs of non-'
                             'h(t) channels; "SIM" for mock data challenge or '
                             'other simulated data; or "DEV" for development/'
                             'testing purposes')
    parser.add_argument('-R', '--observing-revision', type=int, default=1,
                        help='For public SFTs: revision number starts at 1, '
                             'and should be incremented once SFTs have been '
                             'widely distributed across clusters, advertised '
                             'as being ready for use, etc.  For example, if '
                             'mistakes are found in the initial SFT production'
                             ' run after they have been published, regenerated'
                             ' SFTs should have a revision number of at least '
                             '2')
    parser.add_argument('-y', '--chan-opts', required=True, type=Path,
                        help='yml file containing list of channels, frametype,'
                             ' etc. to run over multiple')
    parser.add_argument('-f', '--SFTpath', required=True, type=Path,
                        help='base path to SFTs (either already existing or '
                             'where to output them); appended will be <EPOCH> '
                             '/ <CHANNEL>')
    parser.add_argument('-C', '--create-sfts', type='bool', default=False,
                        help='create the SFTs !!! (/tmp will be appended to '
                             'the sft-path and SFTs will be generated there!)')
    parser.add_argument('--seek-existing-sfts', type='bool', default=True,
                        help='look in other average-duration folders within '
                             'the same path for idential SFTs and symlink them'
                             ' instead of regenerating.')
    parser.add_argument('-I', '--intersect-data', type='bool', default=False,
                        help='Run gw_data_find with the --show-times option to'
                             ' find times data exist, and use LIGOtools '
                             ' segexpr to intersect this with the segments.')
    parser.add_argument('-P', '--plot-output', required=True, type='bool',
                        help='if given then Python jobs run and put output '
                             'plots and data in the same directory as the '
                             'averaged spectra.')
    parser.add_argument('--include-extra-sub-band', type='bool', default=True,
                        help='include any remaining subband beyond the 100 Hz '
                             'chunks')
    parser.add_argument('--tracked-line-list', type=Path, default=None,
                        help='File containing a reference list of known lines '
                             'for annotation')
    parser.add_argument('--tracked-line-tag', type=str, default=None,
                        help="Short tag for the tracked line entries, e.g. "
                             "'O3'")
    parser.add_argument('--delete-ascii', type='bool', default=False,
                        help="delete ascii files after conversion to npz")
    parser.add_argument('-A', '--accounting-group', type=str,
                        default='ligo.prod.o4.detchar.linefind.fscan',
                        help='accounting group tag to be added to the condor '
                             'submit files.')
    parser.add_argument('-U', '--accounting-group-user', type=str,
                        default='evan.goetz',
                        help='accounting group albert.einstein username to be '
                             'added to the condor submit files.')
    parser.add_argument('-Y', '--request-memory', type=int, default=2048,
                        help='memory allocation in MB to request from condor '
                             'for lalpulsar_MakeSFTs step')
    parser.add_argument('--request-disk', type=int, default=4096,
                        help='disk space allocation in MB to request from '
                             'condor for lalpulsar_MakeSFTs step')
    parser.add_argument('-n', '--max-jobs', type=int, default=100,
                        help='gives -maxjobs to use with condor_submit_dag')
    parser.add_argument('-B', '--full-band-avg', type='bool', default=True,
                        help='If provided, save full band average (using '
                             'lalpulsar_spec_avg_long)')
    parser.add_argument('-W', '--html-path', type=Path,
                        help='base path to output html file that displays '
                             'output plots and data; appended will be <EPOCH> '
                             '/ <CHANNEL> / index.html')
    parser.add_argument('-X', '--misc-desc', type=str,
                        help='misc. part of the SFT description field in the '
                             'filename (also used if -D option is > 0)')
    parser.add_argument('--run', type='bool', default=False,
                        help='For a trial run do NOT give this option! When '
                             'given this code will run condor_submit_dag! '
                             'Otherwise this script generates the .dag file '
                             'and then stops!')
    parser.add_argument('-s', '--make-sft-dag-path', type=Path,
                        default='/home/pulsar/gitrepos/lalsuite/_inst/bin',
                        help='Path to the installation of lalpulsar_MakeSFTDAG'
                        )
    parser.add_argument('-S', '--make-sft-path', type=Path,
                        default='/home/pulsar/gitrepos/lalsuite/_inst/bin',
                        help='Path to the installation of lalpulsar_MakeSFTs')
    parser.add_argument('-a', '--spec-tools-path', type=Path,
                        default='/home/pulsar/gitrepos/lalsuite/_inst/bin',
                        help='Path to the installation of lalpulsar_spec_avg '
                             'and lalpulsar_spec_avg_long')
    parser.add_argument('-p', '--postproc-path', type=Path,
                        default='/home/pulsar/.conda/envs/fscan-py3.10/bin',
                        help='Path to the conda environment for running '
                             'postProcess')
    parser.add_argument('-T', '--Tsft', type=int, default=1800,
                        help='SFT coherence length')
    parser.add_argument('--fmin', type=int, default=10,
                        help='Start frequency')
    parser.add_argument('--band', type=int, default=1990,
                        help='Frequency band')
    parser.add_argument('--hp-filter-knee-freq', type=float, default=7,
                        help='Knee frequency of the high pass filter')
    parser.add_argument('-w', '--window-type', type=str, default='hann',
                        help='type of windowing of time-domain to do before '
                             'generating SFTs, e.g. "rectangular", "hann", '
                             '"tukey:<parameter>"')
    parser.add_argument('--overlap-fraction', type=float, default=0.5,
                        help='overlap fraction (for use with windows; e.g., '
                             'use --overlap-fraction=0.5 with -w "hann")')
    parser = dt.add_dtlargs(parser)
    parser.add_argument('--allow-skipping', type='bool', default=True,
                        help='Allow Fscan to skip channels without errors if '
                             'the channel sampling frequency is too low or is '
                             'not present in frames')

    initial_parser = MultiConfParser(subsequentParser=parser)
    multi_conf_args = initial_parser.parse_args()

    for args in multi_conf_args:
        # parse the yaml file with channel specific information
        all_ch_info = read_channel_config(args.chan_opts)

        # Here's the sorted dictionary of segment types and channels
        segtype_info = channels_per_segments(all_ch_info)

        # Here's the dictionary of useful values for each epoch
        epochs_info = epoch_info(args)

        # loop over segment types
        for segtype_idx, (segtype, channels) in enumerate(
                segtype_info.items()):

            # loop over epochs
            for ep_idx, ep in enumerate(epochs_info):
                # create a new dictionary which inherits information from both
                # the epoch and the segment. This also creates the segment file
                # if it does not already exist. (Has to be done before summary
                # page generation in order to get the GPS time stamps in plot
                # filenames correct.)
                epseg_info = epseg_setup(
                    args.SFTpath, ep, segtype, channels,
                    intersect_data=args.intersect_data)

                # analysis workflow

                # make SFTs (if requested and there is data available)
                if args.create_sfts and epseg_info['havesegs']:
                    # loop over frame types
                    for frametype_idx, fr_chans in enumerate(channels.items()):
                        sft_job = MakeSFTJob(args, epseg_info, fr_chans)
                        # write_make_sft_dag might fail if there are no
                        # segments available in the seg file. This happens if
                        # there is no usable data in the given epoch. Skip the
                        # epoch.
                        if sft_job.run_make_sft_dag() != 0:
                            break

                if epseg_info['havesegs']:
                    chans = [
                        ch for frchans in channels.values()
                        for (ch_idx, ch) in frchans
                    ]
                    chans_idx = [
                        ch_idx for frchans in channels.values()
                        for (ch_idx, ch) in frchans
                    ]
                    # process SFTs for each channel
                    processing = ProcessSFTs(
                        args, epseg_info['epoch_path'], chans,
                        epseg_info['duration']
                    )
                    processing.write_condor_band_sub()
                    # full band average (if requested)
                    if args.full_band_avg:
                        processing.write_condor_full_band_sub()
                    # plot/post-processing processed SFTs (if requested)
                    if args.plot_output:
                        processing.write_condor_plots_sub()
                    # loop over all channels of this segment type
                    # compute and plot coherence (if requested)
                    coherence_sub = False
                    for ch_idx in chans_idx:
                        if ('coherence' in all_ch_info[ch_idx]
                                and not coherence_sub):
                            processing.write_condor_coherence_sub()
                            coherence_sub = True

                # prepare summary page job for dag
                if args.plot_output:
                    summary_job = SummaryJob(args, epseg_info)
                    summary_job.write_condor_work_sub()

                # Write a DAG file that will run everything together:
                # Create SFTs, if needed
                # Normalize and average data, if needed
                # Make plots, if needed
                # Compute coherences, if needed
                # Create summary page, if needed
                write_workflow(args, epseg_info, channels, all_ch_info)

                # If requested, reuse SFTs. Note that we do this AFTER dag
                # creation because we *may* need to edit SUPERDAG to remove
                # the splicing of the SFT dag.
                if args.seek_existing_sfts:
                    use_existing_sfts(epseg_info, channels)

                # Submit condor jobs for this epoch, if needed
                if args.run:
                    dagfile = os.path.join(
                        epseg_info['epoch_path'], 'SUPERDAG.dag')
                    cmd = ['condor_submit_dag',
                           '-maxjobs', f'{args.max_jobs}',
                           dagfile]
                    print(f"Submitting {dagfile}")
                    subprocess.run(cmd,
                                   check=True,
                                   cwd=os.path.dirname(dagfile))


if __name__ == "__main__":
    main()

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2023)
#
# This file is part of fscan

import argparse
import numpy as np
from pathlib import Path

from .plot import finetoothplot, static, linecount
from .process.autotag import autotag
from .utils import io
from .utils import dtutils as dtl
from .utils.utils import str_to_bool


def main():
    parser = argparse.ArgumentParser()
    parser.register('type', 'bool', str_to_bool)
    parser.add_argument("--parentPathInput", type=Path, required=True,
                        help="Path to the channel directory containing output "
                             "files from lalpulsar Fscan programs")
    parser.add_argument("--convert-txt-to-npz", type='bool', default=True,
                        help="Convert txt files to npz files")
    parser.add_argument("--delete-converted-text", type='bool', default=False,
                        help="Delete ASCII text files")
    parser.add_argument("--plot-static", type='bool', default=True,
                        help="Make static plots")
    parser.add_argument("--plot-interactive", type=str, nargs='*',
                        choices=['timeaverage', 'speclong', 'persist',
                                 'coherence'],
                        help="Make interactive plots")
    parser.add_argument("--static-plot-sub-band", type=int, default=100,
                        help="Plot frequency bands are rounded to nearest"
                             " integer of this size")
    parser.add_argument("--interactive-plot-sub-band", type=int, default=300,
                        help="Plot frequency bands are rounded to nearest"
                             " integer of this size")
    parser.add_argument("--find-lines-combs", type='bool', default=False,
                        help="Find lines and combs")
    parser.add_argument("--autoline-FAR", type=float, default=0.001,
                        help="(very) approximate target per-bin false alarm "
                             "rate for linefinding")
    parser.add_argument("--autoline-window", type=float, default=0.05,
                        help="window for running statistics in Hz")
    parser.add_argument("--tracked-line-list", type=Path, nargs="+",
                        default=None, help="Reference list for line tracking")
    parser.add_argument("--tracked-line-tag", type=str, default=None,
                        help="The tag string for tagged lines")
    args = parser.parse_args()

    # Make the file path nicer
    args.parentPathInput = args.parentPathInput.expanduser().absolute()

    # work out the segment type and epoch paths from parent path
    # search backwards in the filepath to find the segment type folder
    epoch_path = args.parentPathInput.parent
    segtype_path = epoch_path.parent.parent

    # ==============================
    # Figure out what plots to make
    # and save data
    # ==============================

    # Convert ASCII txt files to npz files
    if args.convert_txt_to_npz:
        errnum1 = errnum2 = errnum3 = errnum4 = 0
        if len(sorted(args.parentPathInput.glob(
                "spec_*_timeaverage.txt"))) > 0:
            errnum1 = io.convert_fscan_txt_to_npz(
                args.parentPathInput, "spec_*_timeaverage.txt"
            )
        if len(sorted(args.parentPathInput.glob(
                "spec_*_spectrogram.txt"))) > 0:
            errnum2 = io.convert_fscan_txt_to_npz(
                args.parentPathInput, "spec_*_spectrogram.txt"
            )
        if len(sorted(args.parentPathInput.glob("spec_*_coh.txt"))) > 0:
            errnum3 = io.convert_fscan_txt_to_npz(
                args.parentPathInput, "spec_*_coh.txt"
            )
        if len(sorted(args.parentPathInput.glob("speclong_*.txt"))) > 0:
            errnum4 = io.convert_fscan_txt_to_npz(
                args.parentPathInput, "speclong_*.txt"
            )

        if np.any([errnum1, errnum2, errnum3, errnum4]):
            Path(args.parentPathInput / 'sfts' / 'zerosfts').touch()
            print('WARNING: input data is either all zeros or nans. Exiting.')
            return

    # Figure out which plots should be made based on which npz files are
    # available
    which_plots = []
    if len(sorted(args.parentPathInput.glob("*_timeaverage.npz"))) > 0:
        which_plots.append('timeaverage')
    if len(sorted(args.parentPathInput.glob("*_spectrogram.npz"))) > 0:
        which_plots.append('spectrogram')
    if len(sorted(args.parentPathInput.glob("*_coherence.npz"))) > 0:
        which_plots.append('coherence')
    if len(sorted(args.parentPathInput.glob("*_speclong.npz"))) > 0:
        which_plots.append('speclong')

    # ==========
    # Make plots
    # ==========

    # Static plots (time average, spectrogram, coherence, persistency)
    if args.plot_static:
        for plt_type in which_plots:
            if plt_type == 'speclong':
                static.make_all_plots(args.parentPathInput,
                                      args.static_plot_sub_band,
                                      ptype='persist',
                                      )
            else:
                static.make_all_plots(args.parentPathInput,
                                      args.static_plot_sub_band,
                                      ptype=plt_type,
                                      )

    # =====================
    # Line and comb finding, line count history
    # =====================

    if (args.find_lines_combs and
            ('speclong' in which_plots or 'timeaverage' in which_plots)):
        # prioritize speclong file
        if 'speclong' in which_plots:
            datafile = sorted(args.parentPathInput.glob(
                "fullspect*_speclong.npz"))[0]
        else:
            datafile = sorted(args.parentPathInput.glob(
                "fullspect*_timeaverage.npz"))[0]
        metadata = io.get_metadata_from_fscan_npz(datafile)
        epoch_dt = dtl.datestr_to_datetime(metadata['epoch'])
        duration_td = dtl.deltastr_to_relativedelta(metadata['duration'])
        sfreq, sval, _ = io.load_spect_data(
            datafile,
            fmin=metadata['fmin'],
            fmax=metadata['fmax'],
        )
        # this epoch lines and combs tagging
        autotag(sfreq, sval,
                tracked_list=args.tracked_line_list,
                tracked_tag=args.tracked_line_tag,
                annotated_only_outfile=(
                        args.parentPathInput / "autolines_annotated_only.txt"),
                complete_outfile=(
                        args.parentPathInput / "autolines_complete.txt"),
                lf_far=args.autoline_FAR,
                lf_win=args.autoline_window,
                )
        # line count history
        if args.plot_static:
            endpt = (epoch_dt + duration_td).strftime("%Y%m%d-%H%M%S")
            # TODO: when we don't have access to /home, this will need to be
            #  changed
            linecount.linecount_plots(
                segtype_path,
                metadata['channel'],
                Path(args.parentPathInput) / "heatmap.png",
                Path(args.parentPathInput) / "linecount.png",
                f_bins=None,
                numSFTsCutoff=6,
                dataPtsInHistory=30,
                autolinesType="complete",
                analysisStart=None,
                analysisEnd=endpt,
                analysisDuration='3months',
                averageDuration=metadata['duration'],
                snapToLast='',
                greedy=None,
            )

    # =====================
    # interactive plots
    # =====================

    if len(args.plot_interactive) > 0:
        fstep = args.interactive_plot_sub_band
        for plt_type in which_plots:
            if plt_type in args.plot_interactive:
                datafile = sorted(args.parentPathInput.glob(
                    f"*_{plt_type}.npz"))[0]
                metadata = io.get_metadata_from_fscan_npz(datafile)
                epoch_dt = dtl.datestr_to_datetime(metadata['epoch'])

                # Plot specific options
                # for coherence, also make a coherence-specific line finding
                # file
                plt_opts = {}
                if plt_type == 'timeaverage':
                    plt_opts['yaxlabel'] = "Normalized average power"
                    plt_opts['ylog'] = True
                    plt_opts['linesfile'] = [
                        args.parentPathInput / "autolines_annotated_only.txt",
                    ]
                    plt_opts['title'] = (
                        f"{metadata['channel']} "
                        f"{epoch_dt.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                elif plt_type == 'speclong':
                    plt_opts['yaxlabel'] = "Average power"
                    plt_opts['ylog'] = True
                    plt_opts['linesfile'] = [
                        args.parentPathInput / "autolines_annotated_only.txt",
                    ]
                    plt_opts['title'] = (
                        f"{metadata['channel']} "
                        f"{epoch_dt.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                elif plt_type == 'coherence':
                    plt_opts['yaxlabel'] = "Coherence"
                    plt_opts['ylog'] = False
                    # Use the annotated only lines file from the reference
                    # channel
                    # TODO: when we don't have access to /home, this will need
                    #  to be changed
                    if 'Undefined' not in metadata['channelA']:
                        ref_linesfile = (
                                epoch_path /
                                metadata['channelA'].replace(":", "_", 1) /
                                "autolines_annotated_only.txt"
                        )
                    else:
                        print(f"{metadata['channelA']}: guessing channel A "
                              "is CAL-DELTAL_EXTERNAL_DQ")
                        ref_linesfile = (
                                epoch_path /
                                ''.join([metadata['channelB'].split(":")[0],
                                         "_CAL-DELTAL_EXTERNAL_DQ"]) /
                                'autolines_annotated_only.txt'
                        )
                    plt_opts['linesfile'] = [ref_linesfile]
                    plt_opts['title'] = (
                        f"{metadata['channelB']}/"
                        f"{metadata['channelA']} "
                        f"{epoch_dt.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    if not ref_linesfile.is_file():
                        raise Exception(
                            f"Couldn't find line file at {ref_linesfile}")

                    # List of top 1000 values in coherence
                    # TODO: EG changed this from a line finding algorithm
                    #  because the line finding didn't work very well on
                    #  coherence. For now just look at the top 1000 coherence
                    #  values
                    f, coh, mdata = io.load_spect_from_fscan_npz(datafile)
                    indices = np.argsort(coh)[::-1][:1000]
                    indices_sorted = np.sort(indices)
                    with open(args.parentPathInput /
                              "top_coherence.txt", 'w') as cohf:
                        cohf.write("# Frequency coherence\n")  # header
                        for freq, co in zip(f[indices_sorted],
                                            coh[indices_sorted]):
                            cohf.write(f"{freq:.6f} {co:.4f}\n")
                    with open(args.parentPathInput /
                              "top_coherence_sorted.txt", 'w') as cohf:
                        cohf.write("# Frequency coherence\n")  # header
                        for freq, co in zip(f[indices], coh[indices]):
                            cohf.write(f"{freq:.6f} {co:.4f}\n")

                for fmin in np.arange(0, metadata['fmax'], fstep):
                    ftag = f"{int(fmin):04}to{int(fmin + fstep):04}Hz"
                    finetoothplot.make_interactive_plot(
                        datafile,
                        fmin,
                        fmin + fstep,
                        (args.parentPathInput /
                         f"visual_overview_{plt_type}_{ftag}.html"),
                        legend=True,
                        annotate=False,
                        colorcode_group_min=3,
                        **plt_opts,
                    )
                if ('persist' in args.plot_interactive and
                        plt_type == 'speclong'):
                    finetoothplot.make_interactive_plot(
                        datafile,
                        metadata['fmin'],
                        metadata['fmax'],
                        args.parentPathInput / "visual_overview_persist.html",
                        datacolname='persist',
                        legend=True,
                        title=(
                            f"{metadata['channel']}"
                            f" {epoch_dt.strftime('%Y-%m-%d')}"),
                        yaxlabel="Persistence",
                        ylog=False,
                        annotate=False,
                        linesfile=[
                            (args.parentPathInput /
                             "autolines_annotated_only.txt")
                        ],
                        colorcode_group_min=3
                    )

    # Finally, delete the txt files if requested
    if args.delete_converted_text:
        try:
            io.delete_ascii(args.parentPathInput, "spec*.txt")
        except FileNotFoundError:
            pass

    if len(which_plots) == 0:
        Path(args.parentPathInput / 'sfts' / 'nosfts').touch()
        print('WARNING: no data available. Exiting.')
        return

    Path(args.parentPathInput / 'postProcess_success').touch()
    print("Completed postProcess successfully")


if __name__ == "__main__":
    main()

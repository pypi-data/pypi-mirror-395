# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2025)
#
# This file is part of fscan

import argparse
import numpy as np
from pathlib import Path
from ..utils import dtutils as dtl
from ..utils import io


def compile_linecount_history(segtypePath, channel, autolinesType='complete',
                              **kwargs):
    """
    Combine the linecount history values into a dictionary

    Parameters
    ----------
    segtypePath : Path, str
        path to the segment type used for the history
    channel : str
        name of the channel used for the history
    autolinesType : str, optional
        kind of autolines file; either 'complete' or 'annotated'
    kwargs :
        additional arguements to pass to args_to_intervals, available_epochs

    Returns
    -------
    data_dict : dict
        Dictionary containing keys 'dates', 'lines_{date}', 'numsfts_{date}'
    """

    # get a list of available epochs
    epochs = dtl.available_epochs(segtypePath, **kwargs)

    data_dict = {
        'dates': np.array([ep.name for ep in epochs], dtype=str),
    }
    for date, epoch_path in zip(data_dict['dates'], epochs):
        data_dict[f'lines_{date}'] = np.array([])
        data_dict[f'numsfts_{date}'] = np.array([0])
        try:
            mdata = dtl.parse_filepath(epoch_path / channel.replace(':', '_'))
        except AssertionError:
            print(f'WARNING: {channel} does not exist for date {date}')
            continue
        try:
            linesfile = mdata[f"autolines-{autolinesType}-path"]
        except KeyError:
            print(f'WARNING: line file "{autolinesType}" does not exist for '
                  f'date {date}')
            data_dict[f'numsfts_{date}'] = np.array(
                [mdata['num-sfts-expected-per-channel']]
            )
            continue
        if not Path(linesfile).exists():
            print(f'WARNING: {linesfile} does not exist')
            data_dict[f'numsfts_{date}'] = np.array(
                [mdata['num-sfts-expected-per-channel']]
            )
        else:
            data_dict[f'lines_{date}'], _ = io.load_lines_from_linesfile(
                linesfile
            )
            data_dict[f'numsfts_{date}'] = np.array(
                [mdata['num-sfts-expected-per-channel']]
            )

    return data_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--segtypePath", type=Path, required=True,
                        help='Path to data used to create heatmap')
    parser.add_argument("--channel", type=str, required=True,
                        help="Channel of data to create heatmap of, e.g., "
                             "H1:GDS-CALIB_STRAIN_CLEAN")
    parser.add_argument("-o", "--outfile", type=Path, required=True,
                        help="File to write output to")
    parser.add_argument("--autolinesType", type=str, default="complete",
                        choices=['complete', 'annotated'],
                        help="Choose 'complete' for all lines found by line "
                             "count. Choose 'annotated' to only plot lines "
                             "identified as belonging to combs")
    parser = dtl.add_dtlargs(parser)
    args = parser.parse_args()

    data_dict = compile_linecount_history(
        args.segtypePath,
        args.channel,
        autolinesType=args.autolinesType,
        analysisStart=args.analysisStart,
        analysisEnd=args.analysisEnd,
        analysisDuration=args.analysisDuration,
        averageDuration=args.averageDuration,
        snapToLast=args.snapToLast,
        greedy=args.greedy,
    )

    io.save_compiled_linecount_history(data_dict, args.outfile)


if __name__ == "__main__":
    main()

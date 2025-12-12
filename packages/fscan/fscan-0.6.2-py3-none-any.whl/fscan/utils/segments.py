# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023-2025)
#
# This file is part of fscan

import numpy as np
from pathlib import Path
from gwpy.segments import Segment, SegmentList, DataQualityDict
from gwdatafind import find_urls
from gwdatafind.utils import file_segment


def find_segments(gps_start, gps_end, dqflags, to_file,
                  Tsft=1800, overlap_fraction=0.5,
                  intersect_data=False, frametypes=None):
    """
    This queries the segment database for the specified segment type.

    If `to_file` does not exist, this function will create it. If it already
    exists, it will just use the file, so if a user wanted custom segments,
    one could do this by just creating that file separately and then naming it
    the file name the Fscan workflow is looking for.
    TODO: need an easier way to do this for custom segments.

    Parameters
    ----------
    gps_start : int
        GPS start time of the segment database query
    gps_end : int
        GPS end time of the segment database query
    dqflags : list of str
        DQ flags to query
    to_file : Path or str
        File to save the segments list to
    Tsft : int, optional
        Length of SFTs
    overlap_fraction : float, optional
        Fraction to overlap SFTs between 0 and 1 (0 is no overlap)
    intersect_data : bool, optional
        Indicate whether we want to intersect the segments with available data
    frametypes : list of str, optional
        List of frame types needed when intersecting with available data

    Returns
    -------
    span_start : int
    span_end : int
    """
    sft_gps_start = gps_start  # initial value, may be amended later
    step = Tsft * (1 - overlap_fraction)
    span_start = span_end = None

    # If there's already a segment file, we don't need to make one.
    # We'll just read from it
    if Path(to_file).exists():
        # Read from the segment file to return the updated start and
        # end GPS (this will be necessary to correctly name plots and
        # configure summary pages).
        segdat = np.genfromtxt(to_file, dtype='int')
        if len(segdat) == 0:
            return None, None
        else:
            segdat = np.atleast_2d(segdat)
            return segdat[0][0], segdat[-1][-1]
    else:
        if dqflags == ['ALL']:
            print("Using all available data with no segment type restriction")
            segs = SegmentList([Segment(gps_start, gps_end)])

        # If no segment file given, and segment type isn't 'ALL',
        # then query the segment database
        else:
            if 'ALL' in dqflags:
                dqflags.remove('ALL')

            print("Querying segments")
            dqdict = DataQualityDict.query_dqsegdb(
                    dqflags,
                    gps_start,
                    gps_end)
            segs = dqdict.intersection().active
            if len(segs) == 0:
                Path(to_file).touch(exist_ok=True)
                return None, None
            # If the earliest segment goes all the way to the starting
            # cutoff point, look back 1 week. We are looking for the point
            # where the flag actually became active
            lookback_window = 7*24*60*60  # TODO: handle smarter
            if segs[0][0] <= gps_start:
                prev_epoch_segs = DataQualityDict.query_dqsegdb(
                    dqflags,
                    gps_start - lookback_window,
                    gps_start).intersection().active

                prev_epoch_segstart = int(prev_epoch_segs[-1][0])

                # Align the segments to an integer multiple of 'step'
                # counting from the point where the flag became active
                sft_gps_start = (
                    gps_start +
                    (step - (gps_start - prev_epoch_segstart) %
                     step))
                sft_gps_start = int(sft_gps_start)
                print(
                    f"Aligning segments to a new start time: {sft_gps_start}"
                )

        # If requested, here we find the data first and check if it is
        # available and intersect with the requested segments
        if intersect_data:
            for frametype in frametypes:
                # query for the data of this frametype, spit out a warning if
                # some data is not available
                urls = find_urls(
                    frametype[0], frametype, sft_gps_start, gps_end,
                    on_missing='warn',
                )

                # create a segment list from each of the frame files
                data_segs = SegmentList()
                for url in urls:
                    data_segs.append(Segment(file_segment(url)))

                # merge (coalesce) the data file segments
                data_segs.coalesce()

                # remove any segments with length less than Tsft
                data_segs_copy = data_segs.copy()
                for seg in data_segs:
                    if abs(seg) < Tsft:
                        data_segs_copy.remove(seg)
                data_segs = data_segs_copy.copy()

                # adjust data segments beyond the first to start an integer
                # number of steps after the SFT GPS start time. segments are
                # required to be of length Tsft or longer to be added to the
                # modified data segments list
                modified_data_segs = SegmentList()
                for seg in data_segs:
                    # numsteps should always be 0 or larger
                    numsteps = max(
                        0, int(np.ceil((seg[0] - sft_gps_start)/step)))
                    newseg = Segment(sft_gps_start + numsteps*step, seg[1])
                    if abs(newseg) >= Tsft:
                        modified_data_segs.append(newseg)

                # intersect with original data quality segs
                segs &= modified_data_segs

        with open(to_file, 'w') as f:
            for seg in segs:

                # This is done for 2 reasons:
                # (a) because dqsegdb2 has historically returned
                # GPS times outside the range requested, and (b)
                # because the sft_gps_start is adjusted (possibly moved
                # later) relative to the gpsstart that was initially
                # used to query the segments.
                if int(seg[0]) < sft_gps_start:
                    seg = Segment(sft_gps_start, seg[1])

                # This is just compensating for the dqsegdb2 issue
                # described above
                if int(seg[1]) > gps_end:
                    seg = Segment(seg[0], gps_end)

                # Don't use this segment if it is less than Tsft long
                if abs(seg) < Tsft:
                    continue

                # This is because any extra time around the SFTs will
                # cause lalpulsar_MakeSFTDAG to "center" the SFTs in a
                # way that causes inconsistencies between avg durations
                nsteps = int(np.floor((abs(seg) - Tsft) / step))
                seg = Segment(seg[0],
                              seg[0] + (nsteps * step) + Tsft)

                # write this segment to the segment file
                f.write(f"{int(seg[0])} {int(seg[1])}\n")

                # set span start and end
                if not span_start:
                    span_start = int(seg[0])
                span_end = int(seg[-1])

    # Return None, None if no data or segments are longer than Tsft
    # otherwise return start of first segment and end of last segment
    return span_start, span_end

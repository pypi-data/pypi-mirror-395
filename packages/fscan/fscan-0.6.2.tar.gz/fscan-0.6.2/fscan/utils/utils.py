# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2023)
#
# This file is part of fscan

from pathlib import Path
from numpy import arange
import re

from .segments import find_segments


# simple snippet to handle various ways of specifying True
def str_to_bool(choice):
    """ Convert string to boolean """
    return bool(str(choice).lower() in ('yes', 'y', 'true', 't', '1'))


def sft_vals_from_makesft_dag_vars(vars_line):
    """ Get SFT information from MakeSFTDAG dag file VARS line """

    obs = int(re.search('-O (\\d+)', vars_line).group(1))
    kind = re.search('-K ([a-zA-Z]+)', vars_line).group(1)
    rev = int(re.search('-R (\\d+)', vars_line).group(1))
    gpsstart = int(re.search('-s (\\d+)', vars_line).group(1))
    Tsft = int(re.search('-t (\\d+)', vars_line).group(1))
    window = re.search('-w ([a-zA-Z]+)', vars_line).group(1)
    channels = vars_line.split(" -N ")[1].split(" ")[0].split(",")
    sftpaths = vars_line.split(' -p ')[-1].split()[0].split(',')

    return obs, kind, rev, gpsstart, Tsft, window, channels, sftpaths


def sft_name_from_vars(obs, kind, rev, gpsstart, Tsft, window, channel):
    """ Create SFT file name from specification """

    return (
        f"{channel[0]}-1_{channel[:2]}_"
        f"{Tsft}SFT_O{obs}{kind}+R{rev}+"
        f"C{channel[3:].replace('-', '').replace('_', '')}+"
        f"W{window.upper()}-{gpsstart}-{Tsft}.sft")


def epoch_info(gps_intervals, duration_tags, epoch_tags, Tsft,
               overlap_fraction):
    """
    This builds a list of dictionaries that have the epoch list and variable
    information
    """

    out = []

    for idx, epoch_tag in enumerate(epoch_tags):
        this_ep = {'GPSstart': gps_intervals[idx][0],
                   'GPSend': gps_intervals[idx][1],
                   'duration': gps_intervals[idx][1] - gps_intervals[idx][0],
                   'duration_tag': duration_tags[idx],  # ex. "day" or "4hours"
                   'epoch_tag': epoch_tag,  # ex. "20220101", "20220101-000000"
                   'Tsft': Tsft,
                   'overlap_fraction': overlap_fraction}
        if this_ep['duration_tag'] in ['day', 'week', 'month']:
            this_ep['summary_page_mode'] = this_ep['duration_tag']
        else:
            this_ep['summary_page_mode'] = 'gps'

        out.append(this_ep)

    return out


def epseg_setup(SFTpath, ep_info, segtype, channels, intersect_data=False):
    """
    Creates a dictionary of info that is specific to each *combination* of an
    epoch and a segment type. That is, specific to each folder of the form
    basepath/Tsft/segment-type/avg-duration/timestamp
    e.g.
    basepath/1800s/H1_DMT-ANALYSIS-READY/day/20220101

    This includes (a) inheriting all properties from the epoch info, and then
    (b) calculating necessary paths, and (c) checking for a segment file and
    creating it if none is found.
    """

    # record the segment type
    epseg = {'segtype': segtype}

    # make sure the segtype is a list
    if not isinstance(epseg['segtype'], list):
        epseg['segtype'] = epseg['segtype'].split(",")

    # inherit epoch information
    for key in ep_info.keys():
        epseg[key] = ep_info[key]

    # Next, setting up some paths...
    # basepath/Tsft/segment-type
    epseg['segtype_path'] = (Path(SFTpath).absolute() /
                             f"{ep_info['Tsft']}s" /
                             '__'.join([x.replace(':', '_')
                                        for x in epseg['segtype']]))

    # basepath/Tsft/segment-type/duration/timestamp
    epseg['epoch_path'] = (epseg['segtype_path'] /
                           ep_info['duration_tag'] /
                           ep_info['epoch_tag'])

    # make the epoch path directory here
    epseg['epoch_path'].mkdir(parents=True, exist_ok=True)

    # basepath/Tsft/segment-type/duration/timestamp/segments.txt
    epseg['segfile'] = epseg['epoch_path'] / 'segments.txt'

    # list all of the frame types associated with this epoch and segment group
    epseg['frametypes'] = list(channels.keys())

    # get the segments, create the segfile, and record the
    # modified start and end times which the SFTs will be constrained to
    # (this is for SFT alignment and easy reuse)
    epseg['SFTGPSstart'], epseg['SFTGPSend'] = find_segments(
        ep_info['GPSstart'],
        ep_info['GPSend'],
        epseg['segtype'],
        epseg['segfile'],
        Tsft=ep_info['Tsft'],
        overlap_fraction=ep_info['overlap_fraction'],
        intersect_data=intersect_data,
        frametypes=epseg['frametypes'],
    )

    # Record whether we have data or not
    if epseg['SFTGPSstart'] is None and epseg['SFTGPSend'] is None:
        epseg['havesegs'] = False
    else:
        epseg['havesegs'] = True

    return epseg


def channels_per_segments(ch_info):
    """
    This builds a dictionary that each entry has the key of the DQ flags used
    for the segments and values that is the list of channels associated with
    that set of DQ flags

    Each entry in the dictionary has a list of tuples representing:
    - the index in the channel yaml file
    - the channel name
    - the frametype
    """

    out = {}
    for idx, ch in enumerate(ch_info):
        # Default to DMT-ANALYSIS_READY
        if ('segment_type' not in ch or
                (ch['segment_type'] in ch and ch['segment_type'] == '')):
            this_ch_seg_type = f"{ch['channel'][0:2]}:DMT-ANALYSIS_READY"
        else:
            this_ch_seg_type = ch['segment_type']
        if this_ch_seg_type not in out.keys():
            out[this_ch_seg_type] = {}

        this_ch_frametype = ch['frametype']
        if this_ch_frametype not in out[this_ch_seg_type].keys():
            out[this_ch_seg_type][this_ch_frametype] = []
        out[this_ch_seg_type][this_ch_frametype].append((idx, ch['channel']))

    return out


def numdecs(res, maxtry=15):
    """
    Small utility function that will determine the appropriate number
    of decimal places to use for a given spectral resolution
    """
    f = arange(0, res*5, res)
    for i in range(maxtry+1):
        test = [f"{j:.{i}f}" for j in f]
        if len(set(test)) == len(test):
            return i
    return maxtry

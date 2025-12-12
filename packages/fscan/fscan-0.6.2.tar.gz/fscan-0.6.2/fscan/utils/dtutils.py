# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2023)
#
# This file is part of fscan

import numpy as np
from gpstime import gpstime
from datetime import datetime
try:
    from datetime import UTC
except ImportError:
    from datetime import timezone
    UTC = timezone.utc
# for smarter calendar-based manipulations...
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
import argparse
import re
from igwn_segments import segment, segmentlist
from .utils import str_to_bool, numdecs
from pathlib import Path


SHORTCUTS = {
    'y': 'years',
    'M': 'months',
    'w': 'weeks',
    'd': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds',
}


def datestr_to_datetime(datestr):
    """
    Accept a string and parse it into a datetime if it fits any of a list of
    formats. Interpret "now" as the moment the program is run.

    Parameters
    ----------
    datestr : str
        A string of the format "%Y-%m-%d-%H:%M:%S", "%Y%m%d-%H%M%S",
        "%Y-%m-%d", "%Y%m%d", "%Y-%m", or "%Y%m"

    Returns
    -------
    dt : datetime
        A `datetime` object

    Notes
    -----
    The datetime output is always in UTC timezone format
    """

    if datestr.lower().endswith("ago"):
        now = datetime.now(UTC).replace(microsecond=0)
        deltastr = datestr[:-3]
        rdelta = deltastr_to_relativedelta(deltastr)
        return now - rdelta

    if datestr == "now":
        now = datetime.now(UTC).replace(microsecond=0)
        return now

    fmts = [
        "%Y-%m-%d-%H:%M:%S",
        "%Y%m%d-%H%M%S",
        "%Y-%m-%d",
        "%Y%m%d",
        "%Y-%m",
        "%Y%m"][::-1]

    for fmt in fmts:
        try:
            dt = datetime.strptime(datestr, fmt).replace(tzinfo=UTC)
            return dt
        except Exception:
            pass

    raise ValueError(f"{datestr} is in some format which is not accepted. "
                     f"Accepted formats: {fmts}")


def datetime_to_gps(dt):
    """
    Turn a python datetime object into a GPS time stamp

    Parameters
    ----------
    dt : datetime

    Returns
    -------
    int :
        GPS time
    """
    dt = dt.replace(tzinfo=UTC)
    return int(gpstime.fromdatetime(dt).gps())


def datestr_to_gps(datestr):
    """
    Small utility function that just sticks together two other functions.

    Parameters
    ----------
    datestr : str
        A string of the format "%Y-%m-%d-%H:%M:%S", "%Y%m%d-%H%M%S",
        "%Y-%m-%d", "%Y%m%d", "%Y-%m", or "%Y%m"

    Returns
    -------
    int :
        GPS time
    """
    dt = datestr_to_datetime(datestr)
    return datetime_to_gps(dt)


def relativedelta_to_tag(rel):
    """
    Convert a relativedelta object to an Fscan "duration tag"

    Parameters
    ----------
    rel : relativedelta
        A `dateutil.relativedelta.relativedelta` object

    Returns
    -------
    tag : str
        A formatted string for the relative duration length
    """
    # In some special cases we might like to reformat things to look pretty
    # and fit with the standard Fscan naming scheme. This info can be used for
    # epoch naming later.
    # example: "1weeks" goes to "week".

    # In non-special cases, we just save the ugly looking tag.
    tag = ""
    for t in SHORTCUTS.values():
        val = getattr(rel, t)

        # In relativedelta objects, 7 days and 1 week are equivalent and both
        # return non-zero for the given 7-day / 1-week period. To solve this
        # issue, we instead use weeks and the remainder of days as the tag.
        # It's possible there may be some other sneaky combination that could
        # trigger some mistake, but my testing indicates this seems to work
        # for our needs.
        if t == SHORTCUTS['d']:
            val %= 7

        # Add to the tag anything that is non-zero, using singular when the
        # value = 1, plural otherwise.
        if val == 0:
            pass
        elif val == 1:
            tag += f"{val}{t.strip('s')}"
        else:
            tag += f"{val}{t}"

    # If the tag was a simple duration, compress it
    remap = {"1day": "day",
             "24hours": "day",
             "1week": "week",
             "7days": "week",  # Maybe not needed, but keeping just to be safe
             "1month": "month",
             "1year": "year",
             "12months": "year",
             }
    if tag in remap.keys():
        tag = remap[tag]

    return tag


def deltastr_to_relativedelta(deltastr):
    """
    Takes a string and parses it into a time interval (specifically a
    *relativedelta*, not a regular timedelta)

    Examples of valid input strings might include "1week", "36hours", "1h30m",
    and many more. You can use abbreviations or not, can use plurals or not.
    When using abbreviations "m" means "minute" and "M" means "month".

    Parameters
    ----------
    deltastr : str
        String containing the time inverval

    Returns
    -------
    relativedelta :
        A `dateutil.relativedelta.relativedelta` object
    """

    # This breaks the input up into sub-strings ("blocks"). It breaks whenever
    # it finds something numeric following something non-numeric.
    # example: "1hour30m" goes to ["1hour", "30m"]

    argstring = ""
    blocks = []
    for i in range(len(deltastr)):
        if (deltastr[i].isnumeric() and i != 0 and not
                deltastr[i-1].isnumeric()):
            blocks += [argstring]
            argstring = deltastr[i]
        else:
            argstring += deltastr[i]
    blocks += [argstring]

    # Having broken it up into blocks, we then separate out the numeric and
    # non-numeric parts of each block, creating a dict (td_args) of arguments.
    # Since `td_args` will be used as input to `relativedelta`, we also fix up
    # the dictionary so that all the keys will be valid arguments for
    # `relativedelta`.
    # example: ["1hour", "30m"] goes to {"hours": 1,"minutes": 30}

    td_args = {}
    for block in blocks:
        for i in range(len(block)):  # look through the block
            # when the numeric part ends, we found the splitting point
            if not block[i].isnumeric():
                k = block[i:]
                a = block[:i]
                if k in SHORTCUTS.keys():  # check for abbreviations
                    k = SHORTCUTS[k]
                # check for singular instead of plural
                elif (t := f"{k.lower()}s") in SHORTCUTS.values():
                    k = t
                    if a == '':
                        a = 1
                # check for nonsense
                # TODO: is this logic correct? the last and seems weird
                elif (len(k) == 0 or len(a) == 0 or
                      k not in SHORTCUTS.keys() and
                      k.lower() not in SHORTCUTS.values()):
                    raise ValueError(f"\n\'{deltastr}\' is in some format "
                                     "which is not accepted. In particular, "
                                     f"\'{block}\' cannot be parsed.")
                td_args[k] = int(a)  # turn the numeric part into an int
                break

    return relativedelta(**td_args)


def snap_to_midnight(dt):
    """
    Accept a datetime and "snap" to the most recent UTC midnight (backwards)

    Parameters
    ----------
    dt : datetime
        A `datetime` object

    Returns
    -------
    dt : datetime
        A `datetime` object of the most recent midnight
    """
    return dt + relativedelta(hour=0, minute=0, second=0)


def snap_to_day(dt, day):
    """
    Shift to the most recent occurrence of a given day of the week, e.g.,
    Wednesday

    Parameters
    ----------
    dt : datetime
    day : str
        A day of the week, e.g., 'wednesday'

    Returns
    -------
    dt : datetime
        A `datetime` object of the most recent occurance for that day

    Notes
    -----
    This function doesn't change the hour/minute/second, use with
    snap_to_midnight if you want that!
    """
    # dictionary of days:relativedelta
    daysDict = {"monday": MO(-1),
                "tuesday": TU(-1),
                "wednesday": WE(-1),
                "thursday": TH(-1),
                "friday": FR(-1),
                "saturday": SA(-1),
                "sunday": SU(-1)}

    # iterate through dictionary of days to match correct argument for
    # relativedelta, {"monday":MO(-1) ...}
    for key in daysDict:
        if key in day:
            return dt + relativedelta(weekday=daysDict[key])


def snap_to_monthstart(dt):
    """
    Shift a datetime to the most recent first day of the current month

    Parameters
    ----------
    dt : datetime

    Returns
    -------
    dt : datetime
        Shifted to the most recent first day of the current month

    Notes
    -----
    This function doesn't change the hour/minute/second, use with
    snap_to_midnight if you want that!
    """
    return dt + relativedelta(day=1)


def snap_to(time, snap_to):
    """
    Combine snapping to different epochs

    Parameters
    ----------
    time : datetime
        The original starting datetime
    snap_to : list str
        List of strings that we are snapping to

    Returns
    -------
    time : datetime
        The modified `datetime` object
    """

    # if the user said to snap, do the thing
    if "month" in snap_to:
        time = snap_to_monthstart(time)

    # snap to day if a day is in args.snapToLast
    days = ["monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday"]
    for day_name in days:
        if day_name in snap_to:
            time = snap_to_day(time, snap_to)

    if "midnight" in snap_to:
        time = snap_to_midnight(time)

    return time


def subfolder_format(durationtag, t):
    """
    Return a string for the epoch tag given the averaging duration and epoch
    datetime

    Parameters
    ----------
    durationtag : str
    t : datetime

    Returns
    -------
    epochtag : str
    """
    # if we're starting at UTC midnight on the 1st of the month and we're
    # doing a monthly average
    if ((t.second == 0 and t.minute == 0 and t.hour == 0 and t.day == 1) and
            durationtag == "month"):
        epochtag = t.strftime("%Y%m")  # label with month only
    # if we're starting at UTC midnight and in a mode that doesn't care about
    # hour/min/sec
    elif (t.second == 0 and t.minute == 0 and t.hour == 0) and all(
            [x not in durationtag for x in ["hour", "minute", "second"]]):
        epochtag = t.strftime("%Y%m%d")  # label with date only
    else:
        epochtag = t.strftime("%Y%m%d-%H%M%S")  # otherwise label time
    return epochtag


def args_to_intervals(**kwargs):
    """
    This is the real important part: it takes all the input arguments and
    computes GPS time intervals, as well as a list of epoch labels in
    duration/starttime format.

    Parameters
    ----------
    kwargs
        Options for keyword arguments are: analysisStart, analysisEnd,
        analysisDuration, averageDuration, snapToLast, and greedy. At minimum,
        exactly two of analysisStart, analysisEnd, analysisDuration must be
        specified.

    Returns
    -------
    gps_intervals : list
    durationtags : list
    epochtags : list
    """

    analysisStart, analysisEnd, averageDuration = dtl_args_to_startenddur(
        **kwargs)
    durationtag = relativedelta_to_tag(averageDuration)

    # set up the lists we want to append to
    gps_intervals = segmentlist()
    durationtags = []
    epochtags = []

    # initialize the time
    epochStart = analysisStart

    # start looping
    while (epochEnd := epochStart + averageDuration) <= analysisEnd:

        epochtags.append(subfolder_format(durationtag, epochStart))
        durationtags.append(durationtag)

        # get the GPS times for this interval
        gpsStart = datetime_to_gps(epochStart)
        gpsEnd = datetime_to_gps(epochEnd)

        gps_intervals.append(segment(gpsStart, gpsEnd))  # save the GPS times

        # Issue a warning if the 'greedy' argument made us go into the future.
        # Not an exception, though - it wouldn't be ridiculous to set up a
        # future run for testing.
        if gpsEnd > datetime_to_gps(datetime.now(UTC).replace(microsecond=0)):
            print("\n***Careful! The last calculated interval extends into "
                  "the future.***")

        # increment epoch start
        epochStart += averageDuration

    return gps_intervals, durationtags, epochtags


def find_specific_SFT(sftname, parentDir, channel, mode=None, exclude=None):
    """
    Return the path to an SFT file for a given SFT name, parent directory, and
    channel

    Parameters
    ----------
    sftname : str
        Name of the SFT file
    parentDir : Path, str
        segment type path
    channel : str
        channel name
    mode : str, optional
        Mode of searching (default: None). Options are None, 'daily-first', and
        'daily-only'
    exclude : list, optional
        List of strings for average durations meant to be excluded from the
        search

    Returns
    -------
    path : str
        Path to the SFT file
    """
    parentDir = Path(parentDir).absolute()

    SFTgpsStart = int(sftname.split('-')[-2])
    SFTgpsEnd = SFTgpsStart + int(sftname.split('-')[-1].replace('.sft', ''))
    SFTstart = gpstime.fromgps(SFTgpsStart)
    SFTend = gpstime.fromgps(SFTgpsEnd)

    chformat = channel.replace(":", "_")

    avgDurs = [x.name for x in parentDir.glob("*")]

    # mode daily-first or daily-only
    if mode == 'daily-first' and 'day' in avgDurs:
        avgDurs.remove('day')
        avgDurs.insert(0, 'day')
    elif mode == 'daily-only':
        assert 'day' in avgDurs
        avgDurs = ['day']

    # Exclude searching in any average durations listed in exclude
    if exclude is None:
        exclude = []
    for ex in exclude:
        try:
            avgDurs.remove(ex)
        except ValueError:
            pass

    for avgDur in avgDurs:
        # skip unknown durations
        try:
            avgDurDt = deltastr_to_relativedelta(avgDur)
        except ValueError:
            continue

        avgDurPath = parentDir / avgDur

        earliestAvgEnd = subfolder_format(avgDur, SFTend - avgDurDt)
        latestAvgEnd = subfolder_format(avgDur, SFTstart)

        epochs = np.sort([x.name for x in avgDurPath.glob("*")])

        startInd = np.searchsorted(epochs, earliestAvgEnd)
        endInd = np.searchsorted(epochs, latestAvgEnd)+1
        checkfolders = epochs[startInd:endInd]
        for checkfolder in checkfolders:
            pattern = (avgDurPath /
                       checkfolder /
                       chformat /
                       "sfts" /
                       sftname)
            if pattern.exists():
                return str(pattern)

    # If we haven't found anything then return an empty string
    return ''


def better_parse_filepath(fpath):
    """ An imporved parse filepath method - Untested """
    mdata = {}
    fpath = Path(fpath).expanduser().absolute()
    mdata['username'] = fpath.home().name
    mdata['public-html-folder'] = fpath.home() / "public_html"
    # search backwards in the filepath to find the SFT duration folder
    pattern = re.compile(r"\d+s")
    sftfolder_idx = -1
    for i in range(len(fpath.parts) - 1, -1, -1):
        if pattern.fullmatch(fpath.parts[i]):
            mdata['Tsft-folder'] = Path(*fpath.parts[:i+1])
            sftfolder_idx = i
            break
    mdata['Tsft-label'] = mdata['Tsft-folder'].name
    mdata['Tsft'] = int(mdata['Tsft-label'].strip("s"))
    mdata['parentPath'] = mdata['Tsft-folder'].parent
    for idx, part in enumerate(fpath.parts[sftfolder_idx+1:]):
        if idx == 0:
            mdata['segtype'] = part.replace("_", ":", 1)
            mdata['segtype-folder'] = mdata['Tsft-folder'] / part
        elif idx == 1:
            mdata['duration-label'] = part
            mdata['duration'] = deltastr_to_relativedelta(part)
            mdata['duration-folder'] = mdata['segtype-folder'] / part
        elif idx == 2:
            mdata['epoch-label'] = part
            mdata['epoch'] = datestr_to_datetime(part)
            mdata['epoch-folder'] = mdata['duration-folder'] / part
            mdata['html-folder'] = (mdata['segtype-folder'] /
                                    "summary" /
                                    mdata['duration-label'] /
                                    part)
            stdsuperdagpath = mdata['epoch-folder'] / 'SUPERDAG.dag'
            if stdsuperdagpath.exists():
                mdata['superdag-path'] = stdsuperdagpath
                mdata['superdagout-path'] = (mdata['epoch-folder'] /
                                             'SUPERDAG.dag.dagman.out')
                mdata['superdag-exists'] = mdata['superdag-path'].exists()
                mdata['superdagout-exists'] = (
                    mdata['superdagout-path'].exists()
                )
        elif idx == 3:
            mdata['channel-label'] = part
            mdata['channel'] = mdata['channel-label'].replace("_", ":", 1)
            mdata['ifo'] = mdata['channel'].split(":")[0]
            mdata['channel-path'] = mdata['epoch-folder'] / fpath
            mdata['sfts-path'] = mdata['channel-path'] / "sfts"
            assert mdata['channel-path'].exists()
            assert mdata['sfts-path'].exists()
            mdata['num-sfts-per-channel'] = len(sorted(
                mdata['sfts-path'].glob('*.sft')))
            if 'superdag-path' not in mdata:
                oldsuperdagpath = mdata['channel-path'] / 'SUPERDAG.dag'
                if oldsuperdagpath.exists():
                    mdata['superdag-path'] = oldsuperdagpath
                    mdata['superdagout-path'] = (mdata['channel-path'] /
                                                 'SUPERDAG.dag.dagman.out')
                    mdata['superdag-exists'] = mdata['superdag-path'].exists()
                    mdata['superdagout-exists'] = (
                        mdata['superdagout-path'].exists()
                    )
            for npztype in ['timeaverage', 'speclong', 'spectrogram',
                            'coherence']:
                matches = mdata['channel-path'].glob(
                    f"fullspect_*_{npztype}.npz")
                if len(matches) == 1:
                    mdata[f"{npztype}-npz-path"] = matches[0]
                elif len(matches) == 0:
                    pass
                else:
                    raise Exception(f"Expected 1 file to match pattern "
                                    f"{pattern}, found {len(matches)}")
            autoline_path = mdata['channel-path'] / 'autolines_complete.txt'
            if autoline_path.exists():
                mdata['autolines-complete-path'] = autoline_path
            autoline_annot_path = (mdata['channel-path'] /
                                   'autolines_annotated_only.txt')
            if autoline_path.exists():
                mdata['autolines-annotated-path'] = autoline_annot_path

    # If new format of the file structure (SUPERDAG in epoch folder)
    if mdata['superdag-exists']:
        # Read the superdag file
        with open(mdata['superdag-path'], 'r') as dagfile:
            lines = dagfile.readlines()
        makesftfiles = [line.split()[-1] for line in lines if 'SPLICE' in line]
        if stdsuperdagpath.exists():
            mdata['multi-channel-sftdag-paths'] = [
                Path(f) for f in makesftfiles
            ]
            mdata['multi-channel-num-sfts-expected'] = 0
            mdata['multi-channel-num-sfts'] = 0
            mdata['multi-channel-sftdag-exists'] = [
                Path(f).exists() for f in makesftfiles]
            # Handle the fact that the monthly folders were renamed
            # O4 only
            if (all(~x for x in mdata['multi-channel-sftdag-exists']) and
                    mdata['duration-label'] == "month"):
                for idx, makesftfile in enumerate(makesftfiles):
                    if not mdata['multi-channel-sftdag-exists'][idx]:
                        edited_file = makesftfile.replace(
                            f"month/{mdata['epoch-label']}01",
                            f"month/{mdata['epoch-label']}")
                        if Path(edited_file).exists():
                            mdata['multi-channel-sftdag-paths'][idx] = Path(
                                edited_file)
                            mdata['multi-channel-sftdag-exists'][idx] = True
            mdata['multi-channel-list'] = []
            for idx, e in enumerate(mdata['multi-channel-sftdag-exists']):
                if e:
                    with (open(mdata['multi-channel-sftdag-paths'][idx], 'r')
                          as makesftdag):
                        lines = makesftdag.readlines()
                    sftopts = [
                        line.split('argList="')[-1].split('"')[0]
                        for line in lines if 'VARS MakeSFT' in line]
                    chans = sftopts[0].split(' -N ')[-1].split(
                        ' -F ')[0].replace(':', '_').split(',')
                    mdata['multi-channel-num-sfts-expected'] += (
                        len(chans) * len(sftopts))
                    for chan in chans:
                        if chan not in mdata['multi-channel-list']:
                            mdata['multi-channel-list'].append(chan)
            if len(mdata['multi-channel-list']) != 0:
                for chan in mdata['multi-channel-list']:
                    sftspath = mdata['epoch-folder'] / chan / 'sfts'
                    mdata['multi-channel-num-sfts'] += (
                        len(sorted(sftspath.glob('*.sft'))))
                mdata['num-sfts-expected-per-channel'] = int(np.round(
                    mdata['multi-channel-num-sfts-expected'] /
                    len(mdata['multi-channel-list'])))
        elif not stdsuperdagpath.exists() and oldsuperdagpath.exists():
            mdata['sftdag-path'] = mdata['channel-path'] / makesftfiles[0]
            mdata['sftdag-exists'] = mdata['sftdag-path'].exists()
            with open(mdata['sftdag-path'], 'r') as makesftdag:
                lines = makesftdag.readlines()
            sftopts = [line.split('argList="')[-1].split('"tagstring')[0]
                       for line in lines if 'VARS MakeSFT' in line]
            mdata['num-sfts-expected-per-channel'] = len(sftopts)
        mdata['fmin'] = float(
            re.search('-F (\\d*\\.?\\d*)', sftopts[0]).group(1))
        mdata['fmax'] = mdata['fmin'] + float(
            re.search('-B (\\d*\\.?\\d*)', sftopts[0]).group(1))
        mdata['sft-overlap'] = float(
            re.search('-P (\\d?\\.?\\d*)', sftopts[0]).group(1)) or 0
        mdata['fmin-label'] = f"{mdata['fmin']:.{numdecs(1 / mdata['Tsft'])}f}"
        mdata['fmax-label'] = f"{mdata['fmax']:.{numdecs(1 / mdata['Tsft'])}f}"
        mdata['gpsstart'] = int(re.search('-s (\\d+)', sftopts[0]).group(1))
        mdata['gpsend'] = int(re.search('-e (\\d+)', sftopts[-1]).group(1))
        with open(mdata['superdag-path'], 'r') as dagfile:
            lines = dagfile.readlines()
        if 'channel-label' in mdata:
            cohlines = [line for line in lines if "ChASFTs" in line and
                        mdata['channel-label'] in
                        line.split('--ChBSFTs=')[1].split()[0]]
            postproclines = [line for line in lines
                             if "VARS PostProcess" in line and
                             mdata['channel-label'] in line]
            if len(cohlines) == 0:
                mdata['coherence-ref-channel'] = None
            elif len(cohlines) != 0:
                cohline = cohlines[0]
                refchannel = cohline.split(
                    "--ChASFTs=")[1].split(" ")[0].split("/")[-3]
                if refchannel[2] != "_":
                    raise Exception(f"\"{refchannel}\" does not appear to be a"
                                    " channel")
                refchannel = refchannel.replace("_", ":", 1)
                mdata['coherence-ref-channel'] = refchannel
            if len(postproclines) == 1:
                postprocline = postproclines[0]
                if '--static-plot-sub-band' in postprocline:
                    split_str = '--static-plot-sub-band '
                else:
                    split_str = '--plot-sub-band '
                mdata['plot-subband'] = int(
                    postprocline.split(split_str)[1].replace(
                        "\"", " ").split()[0])
            else:
                raise Exception(f"SUPERDAG.dag contains {len(postproclines)} "
                                f"lines  containing 'VARS PostProcess'; "
                                f"1 expected")

    return mdata


def parse_filepath(fpath):
    """
    Extract metadata from a given file path.
    example: "parentDir/1800s/H1_DMT-ANALYSIS_READY/4hours/20200206-000000/H1_GDS-CALIB_STRAIN"  # noqa

    As much metadata as possible will be returned. If, for example, you supply
    a truncated path like: "parentDir/1800s/H1_DMT-ANALYSIS_READY/4hours"
    There will simply be less information in the output dictionary.
    /home/ansel.neunzert/public_html/testing_data_v2/1800s/H1_DMT-ANALYSIS_READY/day/20200201/H1_PEM-CS_MAG_EBAY_LSCRACK_Z_DQ  # noqa

    A list of all the dictionary keys is given below -- it is lengthy.
    The data type and an example are also given.

    NOTE: This list is somewhat outdated because the file structure changed to improve the workflow.
    Now, SUPERDAG.dag can exist in the epoch-folder and makesfts.dag will exist in epoch-folder/frametype folder.
    This script is trying to be both backwards compatible with the old structure and also works with the new structure

    username (str)
        ex.: pulsar
    public-html-folder (str)
        ex.: /home/pulsar/public_html
    parentPath (str)
        ex.: /home/pulsar/public_html/fscan
    Tsft-label (str)
        ex.: 1800s
    Tsft (int)
        ex.: 1800
    Tsft-folder (str)
        ex.: /home/pulsar/public_html/fscan/1800s
    segtype (str)
        ex.: H1:DMT-GRD_ISC_LOCK_NOMINAL
    segtype-folder (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL
    duration-label (str)
        ex.: day
    duration (relativedelta)
        ex.: relativedelta(days=+1)
    duration-folder (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day  # noqa
    epoch-label (str)
        ex.: 20230107
    epoch (datetime)
        ex.: 2023-01-07 00:00:00
    epoch-folder (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107  # noqa
    html-folder (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/summary/day/20230107  # noqa
    channel-label (str)
        ex.: H1_PEM-EX_ADC_0_19_OUT_DQ
    channel (str)
        ex.: H1:PEM-EX_ADC_0_19_OUT_DQ
    ifo (str)
        ex.: H1
    channel-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ  # noqa
    sfts-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/sfts  # noqa
    num-sfts-per-channel (int)
        ex.: 88
    superdag-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/SUPERDAG.dag  # noqa
    sftdag-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/tmpSFTDAGtmp.dag  # noqa
    superdagout-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/SUPERDAG.dag.dagman.out  # noqa
    superdag-exists (bool)
        ex.: True
    superdagout-exists (bool)
        ex.: True
    sftdag-exists (bool)
        ex.: True
    coherence-ref-channel (str)
        ex.: H1:GDS-CALIB_STRAIN
    gpsstart (int)
        ex.: 1357085055
    gpsend (int)
        ex.: 1357171177
    fmin (float)
        ex.: 10.0
    fmin-label (str)
        ex.: 10.0000
    fmax (float)
        ex.: 310.0
    fmax-label (str)
        ex.: 310.0000
    plot-subband (int)
        ex.: 100
    sft-overlap (float)
        ex.: 0.5
    timeaverage-npz-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/fullspect_10.0000_310.0000_1357085055_1357171177_timeaverage.npz  # noqa
    speclong-npz-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/fullspect_10.0000_310.0000_1357085055_1357171177_speclong.npz  # noqa
    spectrogram-npz-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/fullspect_10.0000_310.0000_1357085055_1357171177_spectrogram.npz  # noqa
    coherence-npz-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_PEM-EX_ADC_0_19_OUT_DQ/fullspect_10.0000_310.0000_1357085055_1357171177_coherence.npz  # noqa
    autolines-complete-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_GDS-CALIB_STRAIN/autolines_complete.txt  # noqa
    autolines-annotated-path (str)
        ex.: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/day/20230107/H1_GDS-CALIB_STRAIN/autolines_annotated_only.txt  # noqa

    Parameters
    ----------
    fpath : Path, str
        Path to a subdirectory of the fscan outputs

    Returns
    -------
    mdata : dict
    """

    mdata = {}
    # make sure we have expanded all ~ and . in the file path name
    fpath = Path(fpath).absolute()

    # split it into substrings
    substrs = fpath.parts

    # Get some basic information about the user and whether this is in a
    # public_html directory
    mdata['username'] = substrs[2]
    if substrs[3] == "public_html":
        mdata['public-html-folder'] = str(
            Path(substrs[0]).joinpath(*substrs[1:4]))
    # Next, we go backward through the file path levels until we reach
    # something that looks like Tsft, and save the appropriate index
    # (It is important to go backward because the autogenerated path should
    # never have something in it like "12345s" which is not a Tsft. However,
    # the parent path might)

    for iback, substr in enumerate(substrs[::-1]):
        if len(substr) == 0:
            return mdata
        elif substr[-1] == "s" and substr[:-1].isnumeric():
            starti = len(substrs)-iback-1
            break

    # now we can select out the auto-generated part of the path
    autopath = substrs[starti:]

    # and we can start building the metadata dict, using as much info
    # as there is available
    mdata['parentPath'] = str(Path(substrs[0]).joinpath(*substrs[:starti]))
    mdata['Tsft-label'] = autopath[0]
    mdata['Tsft'] = int(autopath[0].strip("s"))
    mdata['Tsft-folder'] = str(Path(mdata['parentPath']) / autopath[0])
    ndecs = numdecs(1 / mdata['Tsft'])
    if len(autopath) > 1:
        mdata['segtype'] = autopath[1].replace("_", ":", 1)
        mdata['segtype-folder'] = str(Path(mdata['Tsft-folder']) / autopath[1])
    if len(autopath) > 2:
        mdata['duration-label'] = autopath[2]
        mdata['duration'] = deltastr_to_relativedelta(autopath[2])
        mdata['duration-folder'] = str(Path(mdata['segtype-folder']) /
                                       autopath[2])
    if len(autopath) > 3:
        mdata['epoch-label'] = autopath[3]
        mdata['epoch'] = datestr_to_datetime(autopath[3])
        mdata['epoch-folder'] = str(Path(mdata['duration-folder']) /
                                    autopath[3])
        mdata['html-folder'] = str(Path(mdata['segtype-folder']) /
                                   'summary' /
                                   mdata['duration-label'] /
                                   mdata['epoch-label'])
        mdata['superdag-path'] = str(Path(mdata['epoch-folder']) /
                                     'SUPERDAG.dag')
        mdata['superdagout-path'] = str(Path(mdata['epoch-folder']) /
                                        'SUPERDAG.dag.dagman.out')
        mdata['superdag-exists'] = Path(mdata['superdag-path']).is_file()
        mdata['superdagout-exists'] = Path(mdata['superdagout-path']).is_file()

        # If new format of the file structure (SUPERDAG in epoch folder)
        if mdata['superdag-exists']:
            # Read the superdag file
            with open(mdata['superdag-path'], 'r') as dagfile:
                lines = dagfile.readlines()
            makesftfiles = [line.split()[-1]
                            for line in lines if 'SPLICE' in line]
            mdata['multi-channel-sftdag-paths'] = [f for f in makesftfiles]
            mdata['multi-channel-num-sfts-expected'] = 0
            mdata['multi-channel-num-sfts'] = 0
            mdata['multi-channel-sftdag-exists'] = [
                Path(f).exists() for f in makesftfiles]

            # Handle the fact that the monthly folders were renamed
            # O4 only
            if (all(~x for x in mdata['multi-channel-sftdag-exists']) and
                    mdata['duration-label'] == "month"):
                for idx, makesftfile in enumerate(makesftfiles):
                    if not mdata['multi-channel-sftdag-exists'][idx]:
                        edited_file = makesftfile.replace(
                            f"month/{mdata['epoch-label']}01",
                            f"month/{mdata['epoch-label']}")
                        if Path(edited_file).exists():
                            mdata['multi-channel-sftdag-paths'][
                                idx] = edited_file
                            mdata['multi-channel-sftdag-exists'][idx] = True
            mdata['multi-channel-list'] = []
            for idx, e in enumerate(mdata['multi-channel-sftdag-exists']):
                if e:
                    with (open(mdata['multi-channel-sftdag-paths'][idx], 'r')
                          as makesftdag):
                        lines = makesftdag.readlines()
                    sftopts = [
                        line.split('argList="')[-1].split('"')[0]
                        for line in lines if 'VARS MakeSFT' in line]
                    chans = sftopts[0].split(' -N ')[-1].split(
                        ' -F ')[0].replace(':', '_').split(',')
                    mdata['multi-channel-num-sfts-expected'] += (
                        len(chans) * len(sftopts))
                    for chan in chans:
                        if chan not in mdata['multi-channel-list']:
                            mdata['multi-channel-list'].append(chan)
            if len(mdata['multi-channel-list']) != 0:
                for chan in mdata['multi-channel-list']:
                    mdata['multi-channel-num-sfts'] += (
                        len(sorted((Path(mdata['epoch-folder']) /
                                    chan /
                                    'sfts').glob('*.sft'))))
                mdata['num-sfts-expected-per-channel'] = int(np.round(
                    mdata['multi-channel-num-sfts-expected'] /
                    len(mdata['multi-channel-list'])))
                mdata['fmin'] = float(
                    re.search('-F (\\d*\\.?\\d*)', sftopts[0]).group(1))
                mdata['fmax'] = mdata['fmin'] + float(
                    re.search('-B (\\d*\\.?\\d*)', sftopts[0]).group(1))
                mdata['sft-overlap'] = float(
                    re.search('-P (\\d?\\.?\\d*)', sftopts[0]).group(1)) or 0
                mdata['fmin-label'] = f"{mdata['fmin']:.{ndecs}f}"
                mdata['fmax-label'] = f"{mdata['fmax']:.{ndecs}f}"
                mdata['gpsstart'] = int(
                    re.search('-s (\\d+)', sftopts[0]).group(1))
                mdata['gpsend'] = int(
                    re.search('-e (\\d+)', sftopts[-1]).group(1))

    if len(autopath) > 4:
        mdata['channel-label'] = autopath[4]
        mdata['channel'] = mdata['channel-label'].replace("_", ":", 1)
        mdata['ifo'] = mdata['channel'].split(":")[0]
        mdata['channel-path'] = str(Path(mdata['epoch-folder']) /
                                    autopath[4])
        assert Path(mdata['channel-path']).is_dir()
        if superdag_exists := (Path(mdata['channel-path']) /
                               'SUPERDAG.dag').is_file():
            mdata['superdag-path'] = str(Path(mdata['channel-path']) /
                                         'SUPERDAG.dag')
            mdata['superdagout-path'] = str(Path(mdata['channel-path']) /
                                            'SUPERDAG.dag.dagman.out')
            mdata['superdag-exists'] = superdag_exists
            mdata['superdagout-exists'] = (
                Path(mdata['superdagout-path']).is_file()
            )
            # Read the superdag file
            with open(mdata['superdag-path'], 'r') as dagfile:
                lines = dagfile.readlines()
            makesftfile = [line.split()[-1]
                           for line in lines if 'SPLICE' in line][0]
            mdata['sftdag-path'] = str(Path(mdata['channel-path']) /
                                       makesftfile)
            mdata['sftdag-exists'] = Path(mdata['sftdag-path']).exists()

            if mdata['sftdag-exists']:
                with open(mdata['sftdag-path'], 'r') as makesftdag:
                    lines = makesftdag.readlines()
                sftopts = [line.split('argList="')[-1].split('"tagstring')[0]
                           for line in lines if 'VARS MakeSFT' in line]
                mdata['num-sfts-expected-per-channel'] = len(sftopts)
                mdata['fmin'] = float(
                    re.search('-F (\\d*\\.?\\d*)', sftopts[0]).group(1))
                mdata['fmax'] = mdata['fmin'] + float(
                    re.search('-B (\\d*\\.?\\d*)', sftopts[0]).group(1))
                mdata['sft-overlap'] = float(
                    re.search('-P (\\d?\\.?\\d*)', sftopts[0]).group(1)) or 0
                mdata['fmin-label'] = f"{mdata['fmin']:.{ndecs}f}"
                mdata['fmax-label'] = f"{mdata['fmax']:.{ndecs}f}"
                mdata['gpsstart'] = int(
                    re.search('-s (\\d+)', sftopts[0]).group(1))
                mdata['gpsend'] = int(
                    re.search('-e (\\d+)', sftopts[-1]).group(1))

        if mdata['superdag-exists']:
            with open(mdata['superdag-path'], 'r') as dagfile:
                lines = dagfile.readlines()

            mdata['sfts-path'] = str(Path(mdata['channel-path']) / "sfts")
            mdata['num-sfts-per-channel'] = len(sorted(
                Path(mdata['sfts-path']).glob('*.sft')))

            cohlines = [line for line in lines if "ChASFTs" in line and
                        f"/{mdata['channel-label']}/" in
                        line.split('--ChBSFTs=')[1].split()[0]]
            postproclines = [line for line in lines
                             if "VARS PostProcess" in line and
                             f"/{mdata['channel-label']} " in line]
        # If coherence is calculated, extract the ref channel
        # if we didn't calculate coherence, there is noref channel
            if len(cohlines) == 0:
                mdata['coherence-ref-channel'] = None
            elif len(cohlines) != 0:
                cohline = cohlines[0]
                refchannel = cohline.split(
                    "--ChASFTs=")[1].split(" ")[0].split("/")[-3]
                if refchannel[2] != "_":
                    raise Exception(f"\"{refchannel}\" does not appear to be a"
                                    " channel")
                refchannel = refchannel.replace("_", ":", 1)
                mdata['coherence-ref-channel'] = refchannel
            if len(postproclines) == 1:
                postprocline = postproclines[0]
                if '--static-plot-sub-band' in postprocline:
                    split_str = '--static-plot-sub-band '
                else:
                    split_str = '--plot-sub-band '
                mdata['plot-subband'] = int(
                    postprocline.split(split_str)[1].replace(
                        "\"", " ").split()[0])
            else:
                raise Exception(f"SUPERDAG.dag contains {len(postproclines)} "
                                f"lines  containing 'VARS PostProcess'; "
                                f"1 expected")

    if 'channel-path' in mdata:
        for npztype in ['timeaverage', 'speclong', 'spectrogram', 'coherence']:
            matches = sorted(Path(mdata['channel-path']).glob(
                f"fullspect_*_{npztype}.npz"))
            if len(matches) == 1:
                mdata[f"{npztype}-npz-path"] = str(matches[0])
            elif len(matches) == 0:
                pass
            else:
                raise Exception(f"Expected 1 file to match pattern "
                                f"fullspec_*_{npztype}.npz, found "
                                f"{len(matches)}")
        autoline_path = Path(mdata['channel-path']) / "autolines_complete.txt"
        if autoline_path.is_file():
            mdata['autolines-complete-path'] = str(autoline_path)
        autoline_annot_path = (Path(mdata['channel-path']) /
                               "autolines_annotated_only.txt")
        if autoline_annot_path.is_file():
            mdata['autolines-annotated-path'] = str(autoline_annot_path)

    return mdata


def add_dtlargs(parser):
    """
    This appends all of the arguments that dateTimeLogic (specifically
    args_to_intervals()) needs to generate a range of epochs. May be used by
    external scripts that call args_to_intervals() or other dateTimeLogic
    functions to avoid rewriting the same arguments.

    Parameters
    ----------
    parser : argparse parser

    Returns
    -------
    parser : argparse parser
        with appropriate arguments appended.
    """

    parser.register('type', 'bool', str_to_bool)
    parser.add_argument("--analysisStart", type=str, default=None,
                        help="Start of entire analysis. Specify as YYYYMMDD, "
                             "YYYY-MM-DD, YYYY-MM-DD-HH:mm:SS or some other "
                             "formats Ansel should document.")
    parser.add_argument("--analysisEnd", type=str, default=None,
                        help="End of entire analysis. Same formats as "
                             "analysisStart.")
    parser.add_argument("--analysisDuration", type=str, default=None,
                        help="Duration of entire analysis. Accepts formats "
                             "like '1day','1week','1month','36h', "
                             "'1w3days2h1minute', etc.")
    parser.add_argument("--averageDuration", type=str, required=True,
                        help="Duration of each interval for averaging. Same "
                             "format as analysisDuration.")
    parser.add_argument("--snapToLast", type=str, default='',
                        help="Currently accepts 'midnight','Wednesday', "
                             "'month', and any combination e.g. "
                             "'midnightWednesday'. Doesn't care about "
                             "capitalization.")
    parser.add_argument("--greedy", type='bool', default=False,
                        help="If there aren't a round number of "
                             "averageDurations per analysisDuration, compute "
                             "one extra averageDuration interval.")
    return parser


def dtl_args_to_startenddur(**kwargs):
    """
    Convert the date time arguments into start, end, average duration values

    Parameters
    ----------
    kwargs
        Options for keyword arguments are: analysisStart, analysisEnd,
        analysisDuration, averageDuration, snapToLast, and greedy. At minimum,
        exactly two of analysisStart, analysisEnd, analysisDuration must be
        specified.

    Returns
    -------
    analysis_start : datetime.datetime
        Start of entire analysis
    analysis_end : datetime.datetime
        End of entire analysis
    average_dur : dateutils.relativedelta.relativedelta
        Duration of each interval for averaging
    """

    analysis_start = kwargs.get('analysisStart', None)
    analysis_end = kwargs.get('analysisEnd', None)
    analysis_dur = kwargs.get('analysisDuration', None)
    average_dur = kwargs.get('averageDuration')
    snap = kwargs.get('snapToLast', '')
    greedy = kwargs.get('greedy', False)
    if not isinstance(greedy, bool):
        greedy = str_to_bool(greedy)

    # make sure we have exactly 2 pieces of info for the over all start and end
    # time
    provided_args = sum(arg is not None for arg in [analysis_start,
                                                    analysis_end,
                                                    analysis_dur])
    if provided_args != 2:
        raise ValueError("Must specify exactly 2 of analysisStart, "
                         "analysisEnd, analysisDuration")

    average_dur = deltastr_to_relativedelta(average_dur)

    # turn the start and end arguments into datetimes
    # turn the analysis duration into relativedelta
    if analysis_start:
        analysis_start = datestr_to_datetime(analysis_start)
    if analysis_end:
        analysis_end = datestr_to_datetime(analysis_end)
    if analysis_dur:
        analysis_dur = deltastr_to_relativedelta(analysis_dur)

    # If we did get analysisDuration, use it to compute start or end
    # After this, we should be done with analysisDuration
    if analysis_dur:
        if analysis_start:
            analysis_end = analysis_start + analysis_dur
        elif analysis_end:
            analysis_start = analysis_end - analysis_dur
    if analysis_end < analysis_start + average_dur:
        raise ValueError(f"{analysis_end} is prior to "
                         f"{analysis_start + average_dur}")

    analysis_start = snap_to(analysis_start, snap.lower())

    if snap and analysis_dur:
        analysis_end = analysis_start + analysis_dur

    if greedy:
        quitpoint = analysis_end
    else:
        quitpoint = analysis_end - average_dur

    t = analysis_start
    while t <= quitpoint:
        if t == quitpoint and greedy:
            break
        t += average_dur

    analysis_end = t

    return analysis_start, analysis_end, average_dur


def available_epochs(segtype_path, **kwargs):
    """
    Find available epochs from other epochs in the segtype_path

    Parameters
    ----------
    segtype_path : Path, str
        Path to the segment type
    kwargs : keyword arguments
        Parameters are passed to dtutils.dtl_args_to_startenddur.
        Options for keyword arguments are: analysisStart, analysisEnd,
        analysisDuration, averageDuration, snapToLast, and greedy. At minimum,
        exactly two of analysisStart, analysisEnd, analysisDuration must be
        specified. Also, only_channels is an optional keyword argument that is
        a list of (possibly glob-type) strings for only those channels of
        interest should be kept as an available epoch

    Returns
    -------
    epochs : list
        List of available epoch paths
    """
    # convert the range of times into a start, end, and averaging duration
    start, end, average_dur = dtl_args_to_startenddur(**kwargs)

    # the averaging tag is the folder format one level into the segment folder
    avg_tag = relativedelta_to_tag(average_dur)

    for idx, ch in enumerate(only_channels := kwargs.get('only_channels', [])):
        only_channels[idx] = ch.replace(':', '_', 1)

    # find all folders between the start and end
    # TODO: is there any way to not have a list of all folders in the
    #       directory?
    # and restrict to channels in only_channels if given
    possible_epochs = Path(segtype_path, avg_tag).glob("*")
    epochs = []
    for epoch in sorted(possible_epochs):
        try:
            this_epoch = datestr_to_datetime(epoch.name)
        except ValueError:
            continue
        if start <= this_epoch < end:
            if len(only_channels) > 0:
                for ch in only_channels:
                    if len(sorted(epoch.glob(ch))) > 0:
                        epochs.append(epoch)
            else:
                epochs.append(epoch)

    return epochs


def metadata_from_folders_in_range(segtype_path, only_channels=None, **kwargs):
    """
    Parse filepath metadata for all available folders in some
    range of epochs.

    Arguments
    ---------
    segtype_path : Path, str
        Path including parent directory, Tsft, and the segment type
        ex: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/
    only_channels : list
        If you want to restrict only certain channels, supply them here.
        Wildcards (*) may be used.
    kwargs : key word arguments
        These should be supplied as on the dateTimeLogic command line.
        You will need at least averageDuration, and two of the following:
        analysisStart, analysisEnd, analysisDuration

    Returns
    -------
    mdatas : list of dicts
        Contains one metadata dict per channel subfolder that exists.
    """
    if only_channels is None:
        only_channels = []

    _, durationtags, epochtags = args_to_intervals(**kwargs)
    mdatas = []
    for epochtag in epochtags:
        epochpath = Path(segtype_path) / durationtags[0] / epochtag
        if len(only_channels) == 0:
            channelpaths = sorted(epochpath.glob("*"))
        else:
            channelpaths = []
            for ch in only_channels:
                channelpaths += sorted(epochpath.glob(ch.replace(":", "_")))
        channelpaths = [c for c in channelpaths if c.is_dir()]
        channelpaths = [c for c in channelpaths if not str(c).endswith("logs")]
        channelpaths = [c for c in channelpaths
                        if not str(c).endswith("SFT_GEN")]

        mdatas += [parse_filepath(c) for c in channelpaths]
    return mdatas


def metadata_where_fields_exist_in_range(segtype_path,
                                         fields,
                                         only_channels=None,
                                         **kwargs):
    """
    Parse filepath metadata for all available folders in some
    range of epochs, then restrict to cases where the requested metadata fields
    exist. (Good for getting all available npz files of a particular type,
    while ignoring directories that contain no data, for instance.)

    Arguments
    ---------
    segtype_path : Path, `str`
        Path including parent directory, Tsft, and the segment type
        ex: /home/pulsar/public_html/fscan/1800s/H1_DMT-GRD_ISC_LOCK_NOMINAL/
    fields : list of str
        All the metadata fields required. See documentation for
        parse_filepath()
    only_channels : list
        If you want to restrict only certain channels, supply them here.
        Wildcards (*) may be used.
    kwargs : key word arguments
        These should be supplied as on the dateTimeLogic command line.
        You will need at least averageDuration, and two of the following:
        analysisStart, analysisEnd, analysisDuration

    Returns
    -------
    mdata_keep : list of dicts
        Contains one metadata dict per channel subfolder that meets
        requirements.
    """
    if only_channels is None:
        only_channels = []

    mdata = metadata_from_folders_in_range(
        segtype_path, only_channels, **kwargs)
    mdata_keep = []
    for m in mdata:
        keep = True
        for field in fields:
            if field not in m.keys():
                keep = False
        if keep:
            mdata_keep += [m]
    return mdata_keep


def main():
    # this is for testing - these arguments
    parser = argparse.ArgumentParser()
    parser = add_dtlargs(parser)
    args = parser.parse_args()

    gps_intervals, durationtags, epochtags = args_to_intervals(**args.__dict__)

    # everything over here is for testing
    # Just as a cross-check, I'm computing the GPS times back into human-
    # readable format using the external tconvert tool, rather than doing it in
    # python

    import subprocess
    for i in range(len(gps_intervals)):
        interval = gps_intervals[i]
        epochtag = epochtags[i]
        durationtag = durationtags[i]
        print(f"{durationtag}/{epochtag}")
        subprocess.call(['lal_tconvert', str(interval[0])])
        subprocess.call(['lal_tconvert', str(interval[1])])

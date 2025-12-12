# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2025)
#
# This file is part of fscan

import argparse
import numpy as np
from pathlib import Path

from ..utils import io
from . import spectlinetools as slt
from . import linefinder as lf
from . import combfinder as cf


def line_loc_from_linesfile(linesfile, sfreqs, **kwargs):
    """
    Determine index locations for lines from a lines file

    Parameters
    ----------
    linesfile : Path
        Path to lines file
    sfreqs : 1d array (dtype: float)
        spectral bin center frequencies
    kwargs
        arguments passed to process.spectlinetools.clip_spect

    Returns
    -------
    llocs : 1d array (dtype: integer)
        indices of spectral bin centers nearest to marks
    lnames : 1d array (dtype: string)
        label for each spectral bin center
    """
    lfpath = linesfile.absolute()

    lfreqs, lnames = io.load_lines_from_linesfile(lfpath)

    lfreqs, lnames = slt.clip_spect(lfreqs, lnames,
                                    **kwargs)

    llocs = slt.match_bins(sfreqs, lfreqs)

    return llocs, lnames


def autotag(sfreq, sval, cf_neighbors=50, cf_requirelen=5,
            linelist=None, lf_far=0.001, lf_win=0.05,
            tracked_list=None, tracked_combs_list=None, tracked_tag=None,
            autofound_tag=None,
            annotated_only_outfile=None, complete_outfile=None):
    """
    This function works with a list of previously tracked lines + the results
    of the linefinder & combfinder code to generate a lines list that contains
    information from both sources in a readable, less-cluttered way.

    It saves two output text files, one of which contains the full line list
    including all auto-found line entries, and the other of which only saves
    lines with some kind of annotation (auto-generated or from tracked list)

    Parameters
    ----------
    sfreq : 1d array (dtype: float)
    sval : 1d array (dtype: float)
    cf_neighbors : int (default: 50)
    cf_requirelen : int (default: 5)
    linelist : Path (default: None)
    lf_far : float (default: 0.001)
    lf_win : float (default: 0.05)
    tracked_list : Path (default: None)
    tracked_combs_list : Path (default: None)
    tracked_tag : str (default: None)
    annotated_only_outfile : Path (default: None)
    complete_outfile : Path (default: None)
    """

    # ======================
    # Starting list of lines
    # ======================

    # If lines file was given, load lines from that.
    # Otherwise, auto-identify lines.
    if linelist:
        lloc, lname = line_loc_from_linesfile(
            linelist, sfreq, fmin=sfreq[0], fmax=sfreq[-1],
            islinefile=True)
    else:
        lloc = lf.peaks(sval, lf_far, lf_win/(sfreq[1]-sfreq[0]))
        lname = np.array([""]*len(lloc))
    lname = lname.astype(object)  # needed for variable length strings

    # ==============================================
    # Pre-process tracked lines and combs annotation
    # ==============================================

    afreq = []
    anames = []

    # Read from tracking list(s)
    if tracked_list:
        tfreq = np.array([])
        tnames = np.array([])
        for one_list in tracked_list:
            tfreq_temp, tnames_temp = io.load_lines_from_linesfile(
                one_list)
            tfreq = np.append(tfreq, tfreq_temp)
            tnames = np.append(tnames, tnames_temp)
        tfreq, tnames = slt.clip_spect(tfreq, tnames,
                                       fmin=sfreq[0],
                                       fmax=sfreq[-1],
                                       islinefile=True)
        tnames = [t.replace("NEW", "") for t in tnames]
        # Split out lines and combs from tracking list
        tracked_combs_as_strings = []
        tracked_comb_tags = []
        for i, name in enumerate(tnames):
            if " comb " in (name+" ").lower().replace(";", " "):
                spstr = name.split(";", 1)[0].split()[-1]
                offstr = name.split(";", 1)[1].split()[0]
                tracked_combs_as_strings += [(spstr, offstr)]
                if ("[" == name.strip()[0]) and ("]" in name):
                    tracked_comb_tags += [
                        name.split("[")[1].split("]")[0].strip()]
                elif tracked_tag:
                    tracked_comb_tags += [tracked_tag]
                else:
                    tracked_comb_tags += [""]
            else:
                afreq += [tfreq[i]]
                anames += [tnames[i]]

        # Recall that we have a tag saved for *each* entry in the tracked
        # lines list. However, what we want is one tag per tracked comb,
        # not one tag per *tooth* of the tracked comb.
        # This picks out the set of unique tracked combs, and also finds
        # the corresponding tag (selects the tag of the first tooth).
        unique_tracked_combs_as_strings = list(set(tracked_combs_as_strings))
        unique_tracked_comb_tags = []
        for ctag in unique_tracked_combs_as_strings:
            unique_tracked_comb_tags += [
                tracked_comb_tags[
                    tracked_combs_as_strings.index(ctag)]]
        tracked_combs = [(float(x[0]), float(x[1]))
                         for x in unique_tracked_combs_as_strings]
    # If no tracking list, skip this step
    else:
        tracked_combs = []

    # If additional tracked combs specified from command line, process those
    if tracked_combs_list:
        for combarg in tracked_combs_list:
            # Get all the frequencies and indices expected in the
            # spectral range
            combsp, comboff = io.combarg_to_combparams(combarg)
            tracked_combs += [(combsp, comboff)]

    # Process annotations
    # If a "tracked lines tag" has been specified, append [<tag>] to any
    # un-tagged entries in the tracked lines list
    aloc = slt.match_bins(sfreq, afreq)
    if tracked_tag:
        anames_old = anames[:]
        anames = []
        for aname in anames_old:
            if ("[" != aname.strip()[0]) or ("]" not in aname):
                anames += [f"[{tracked_tag}] {aname}"]
            else:
                anames += [aname]

    # Process tracked comb entries
    cf_lloc = lloc[:]
    for ic, comb in enumerate(tracked_combs):
        cfreq, cinds, cnames = slt.combparams_to_labeled_teeth(
            comb[0], comb[1], sfreq, lloc)
        ctag = unique_tracked_comb_tags[ic]
        cnames = np.array(
            [f"[{ctag}] "+cname for cname in cnames])
        # Intersect with line locations to determine which are found here
        refound = np.isin(cinds, cf_lloc)
        refoundfreq = cfreq[refound]
        refoundinds = cinds[refound]
        refoundnames = cnames[refound]
        # Filter "re-found" comb teeth for those in consecutive blocks
        # And reject all corresponding spectral indices
        consecfilter = slt.consecutive_filter_Hz(refoundfreq,
                                                 comb[0], comb[1],
                                                 cf_requirelen)
        filterinds = refoundinds[consecfilter]
        filternames = refoundnames[consecfilter]
        if len(filterinds) > 0:
            print(
                f"{len(filterinds)} entries belong to tracked comb"
                f" {comb[0]},{comb[1]}")
        # Filter the line list by the indices to keep
        keep = np.invert(np.isin(cf_lloc, filterinds))
        cf_lloc = cf_lloc[keep]
        aloc = np.append(aloc, filterinds)
        anames = np.append(anames, filternames)

    # ==========
    # Find combs
    # ==========

    foundCombs = cf.find_combs(sfreq, sval, cf_lloc,
                               neighbors=cf_neighbors,
                               requirelen=cf_requirelen)

    # ==================
    # Annotate line list
    # ==================

    # Append labels from auto-found comb list where relevant
    for comb in foundCombs:

        _, cloc, cnames = slt.combparams_to_labeled_teeth(
            comb[0], comb[1], sfreq, lloc)
        if autofound_tag:
            cnames = [f"[{autofound_tag}] "+cname for cname in cnames]
        aloc = np.append(cloc, aloc)
        anames = np.append(cnames, anames)

    # If a line has a previous annotation and was auto-identified,
    # combfinder, append the annotation to the auto-identified
    # label for the same location.
    overlap_loc = []
    overlap_name = []
    for i, l in enumerate(lloc):
        if l in aloc:
            appendLabels = anames[aloc == l].tolist()
            for appendLabel in appendLabels:
                if len(lname[i].strip()) == 0:
                    lname[i] = appendLabel
                elif appendLabel.strip() not in lname[i]:
                    overlap_loc += [l]
                    overlap_name += [appendLabel]

    lloc = np.append(lloc, overlap_loc).astype(int)
    lname = np.append(lname, overlap_name)

    # ===========
    # Saving data
    # ===========
    if annotated_only_outfile:
        with open(annotated_only_outfile, 'w') as f:
            for i in range(len(lloc)):
                if len(lname[i].strip()) > 0:
                    f.write(f"{sfreq[lloc[i]]},{lname[i]}\n")

    if complete_outfile:
        with open(complete_outfile, 'w') as f:
            for i in range(len(lloc)):
                f.write(f"{sfreq[lloc[i]]},{lname[i]}\n")


def main():
    parser = argparse.ArgumentParser()

    # Arguments for input spectrum
    data_args = parser.add_argument_group("Input data handling")
    data_args.add_argument("--npz-spectfile", type=Path, required=True,
                           help="Path to the .npz spectfile")
    data_args.add_argument("--fmin", required=True, type=float,
                           help="Minimum frequency to analyze")
    data_args.add_argument("--fmax", required=True, type=float,
                           help="Maximum frequency to analyze")
    data_args.add_argument("--freq-colname", type=str, default=None,
                           help="Name of frequencies colum in npz file")
    data_args.add_argument("--data-colname", type=str, default=None,
                           help="Name of data column in npz file")

    # Arguments for auto line identification or input custom lines file to use
    # for comb finding
    line_args = parser.add_argument_group("Line list or line finding")
    line_args.add_argument(
        "--autoline-FAR", type=float, default=0.001,
        help="(very) approximate target per-bin false alarm rate for"
             " linefinding",
    )
    line_args.add_argument("--autoline-window", type=float, default=0.05,
                           help="window for running statistics in Hz")
    line_args.add_argument("--autofound-tag", type=str, default=None,
                           help="A tag to prefix any auto-identified lines")
    line_args.add_argument(
        "--find-lines-from-list", type=Path,
        help="Path to existing line file which contains entries to use as"
             " the starting point for combfinding. Overrides the combfinder's"
             " usual first step of auto-finding peaks.",
    )

    # Arguments to use for annotation
    annotate_args = parser.add_argument_group("Annotation arguments")
    annotate_args.add_argument(
        "--tracked-list", type=Path, default=None, nargs="+",
        help="File(s) containing a list of lines to consider 'previously"
             " known', i.e. tracked",
    )
    annotate_args.add_argument(
        "--tracked-tag", type=str, default=None,
        help="A tag to prefix any entries from the tracked list",
    )

    # Arguments to parameterize comb finding
    combfinding_args = parser.add_argument_group("Comb finding")
    combfinding_args.add_argument(
        "--neighbors", type=int, default=50,
        help="Number of nearest neighbors to compare with for each line",
    )
    combfinding_args.add_argument(
        "--requirelen", type=int, default=5,
        help="Minimum number of required entries in comb",
    )
    combfinding_args.add_argument(
        "--tracked-combs", nargs="+",
        help="Additional list of combs to consider 'tracked'",
    )

    # Arguments for saving output
    out_args = parser.add_argument_group("File outputs")
    out_args.add_argument("--complete-outfile", type=Path, default=None,
                          help="Output file for all auto-found lines")
    out_args.add_argument(
        "--annotated-only-outfile", type=Path, default=None,
        help="Output file for auto-found lines, only those with labels",
    )
    out_args.add_argument(
        "--comblist-outfile-entry-format", type=Path,
        help="Output file for auto-found combs in terms of each"
             " individual tooth.",
    )

    args = parser.parse_args()

    # =====================
    # spectrum file loading
    # =====================

    sfreq, sval, _ = io.load_spect_data(
        args.npz_spectfile,
        fmin=args.fmin,
        fmax=args.fmax,
        freqname=args.freq_colname,
        dataname=args.data_colname,
        islinesfile=False
    )

    autotag(sfreq, sval,
            cf_neighbors=args.neighbors,
            cf_requirelen=args.requirelen,
            linelist=args.find_lines_from_list,
            lf_far=args.autoline_FAR,
            lf_win=args.autoline_window,
            tracked_list=args.tracked_list,
            tracked_combs_list=args.tracked_combs,
            tracked_tag=args.tracked_tag,
            autofound_tag=args.autofound_tag,
            annotated_only_outfile=args.annotated_only_outfile,
            complete_outfile=args.complete_outfile)


if __name__ == "__main__":
    main()

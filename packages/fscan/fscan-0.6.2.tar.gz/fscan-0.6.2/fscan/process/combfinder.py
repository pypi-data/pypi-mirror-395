# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

import numpy as np
from tqdm import tqdm
from . import spectlinetools as slt
from .lineobjects import Line, LineList, Spectrum


def find_combs(sfreq, sval, lloc, neighbors=50, requirelen=3, maxlines=5000):
    """
    Parameters
    ----------
    sfreq : np.ndarray of floats
        Spectral frequencies
    sval : np.ndarray of floats
        Spectral values
    lloc : np.ndarray of ints
        Indices (locations) of lines/peaks in the spectrum
    neighbors : int
        Number of nearest neighbors to use for pairwise comparison
    requirelen : int
        Number of peaks to require for a comb
    maxlines : int
        Maximum number of lines to include

    Returns
    -------
    combCandidates : list
        tuples containing (spacing, offset)
    """

    if len(lloc) > maxlines:
        return []
    # Sort the lines on their heights
    # (This will help compare lines with their nearest
    # neighbors in height.)
    lheight = sval[lloc]
    inds_that_sort_height = np.argsort(lheight)
    lloc_sorted = lloc[inds_that_sort_height]

    # Set up a spectrum object; all generated combs
    # will be associated with this.
    mainSpect = Spectrum(
        freq_array=sfreq,
        val_array=sval
    )

    # Set up the comb candidates list
    combCandidates = []

    # Check that we are not trying to compare more neighbors
    # than actually exist
    if neighbors > len(lloc)-1:
        print(
            f"Request to compare {neighbors} neighbors is excessive for"
            f" {len(lloc)} total lines")
        neighbors = len(lloc)-1
        print(f"Adjusting the number of nearest neighbors to {neighbors}")

    # Set up the pairwise comparisons. (This looks rather opaque.
    # The result, `coords`, is a set of tuples of integers which give
    # the indices of pairs of lines. We're basically generating the
    # indices of a square matrix that select the upper right triangle
    # except the diagonal, and except another upper triangular matrix
    # offset from the diagonal by 1+neighbors. In the end this compares
    # all unique combinations of indices i, j where i!=j and
    # abs(i-j)<=neighbors.)

    coordsA = set(zip(*np.triu_indices(len(lloc), 1)))
    coordsB = set(zip(*np.triu_indices(len(lloc), 1+neighbors)))
    coords = coordsA-coordsB

    # Warn the user about how many combinations we're about to compute.
    # And prepare to report every 10% to completion.
    print(f"About to perform {len(coords)} comparisons of line pairs.")

    # Nowe we loop through the
    for icoord, coord in enumerate(tqdm(coords)):
        i, j = coord
        llocA = lloc_sorted[i]
        llocB = lloc_sorted[j]

        # Determine which line is higher frequency
        llocMin = min(llocA, llocB)
        llocMax = max(llocA, llocB)
        binsp = llocMax - llocMin

        # Don't accept a bin spacing of 1 or 0.
        if binsp < 2:
            continue

        # Populate an initial list of locations for the
        # candidate comb, which so far just contains the
        # two original lines.
        comblocs = [llocMin, llocMax]
        # Set the current tooth to the higher frequency line.
        tooth = llocMax

        # Set up a LineList to hold comb info as we build it.
        # Append the orginal two lines.
        tempList = LineList(
            spectrum=mainSpect
        )
        for combloc in comblocs:
            tempList.append_line(
                Line(
                    spectrum=mainSpect,
                    spectral_index=combloc),
                duplicate_mode='disallow')

        # Now we're going to iterate through the available
        # spectrum looking for more members of this (possible)
        # comb.
        while tooth < len(mainSpect.freq_array):
            additionFound = False
            # Accept up to one bin off, prioritizing 0 bins off.
            for binerr in [0, 1, -1]:
                if tooth + binsp + binerr in lloc:
                    comblocs += [tooth + binsp + binerr]
                    tooth += binsp + binerr
                    additionFound = True
                    break
            # If we found another possible tooth, propose
            # a new comb which is a combination of the current
            # tempList and the new tooth. Check to see if that
            # is also a comb.
            if additionFound:
                proposeList = LineList(
                    spectrum=mainSpect)
                proposeList.members = tempList.members[:]
                proposeList.append_line(Line(
                    spectrum=mainSpect,
                    spectral_index=tooth),
                    duplicate_mode='disallow')
                proposeList.fit_comb_params()
                # If it's still a comb, great! Append the
                # new tooth to tempList and keep looping.
                if proposeList.iscomb:
                    tempList.append_line(Line(
                        spectrum=mainSpect,
                        spectral_index=tooth),
                        duplicate_mode='disallow')
                # If it's not still a comb, we failed
                # to find a tooth here. Break the loop.
                else:
                    break
            # If we didn't find another tooth, break the loop.
            else:
                break

        # After we have finished iterating across the spectrum,
        # check if we have gathered enough teeth.
        if len(tempList.members) >= requirelen:
            # if so, fit comb parameters to the recovered teeth.
            tempList.fit_comb_params()

            # Next, we're going to try to merge the new comb
            # into the existing list, in case it's not unique.
            repeatMergeSearch = True
            while repeatMergeSearch:
                merged = False
                for c in combCandidates:
                    # skip anything we previously demoted from
                    # comb status
                    if not c.iscomb:
                        continue
                    # Get the spectral indices of the two combs
                    # which we want to compare. Check if their
                    # union also describes a comb. If so, use
                    # that instead of either comb.
                    locsA = tempList.get_all_spectral_indices()
                    locsB = c.get_all_spectral_indices()
                    union = set(locsA+locsB)
                    proposeList = LineList(
                        spectrum=mainSpect)
                    for u in union:
                        proposeList.append_line(Line(
                            spectrum=mainSpect,
                            spectral_index=u),
                            duplicate_mode='disallow')
                    try:
                        proposeList.fit_comb_params()
                    except Exception:
                        pass
                    if proposeList.iscomb:
                        c.iscomb = False
                        tempList.members = proposeList.members[:]
                        merged = True
                        break

                # if this candidate got merged, start again from
                # the top with the merging.
                repeatMergeSearch = merged

            # Append the new comb to the candidates.
            combCandidates += [tempList]

    # Now filter out anything that got merged away
    combCandidates = [c for c in combCandidates if c.iscomb]

    # Now we're going to trim out overlapping combs, as best we can
    # Note that this prioritizes combs with *many teeth*. An alternate
    # method would be to prioritize combs with *tall* and/or *consistent*
    # teeth.

    # Sort combs by number of members.
    combCandidates.sort(key=lambda x: len(x.members), reverse=True)

    # Set up an empty list of lines that have been "used up" by combs
    usedLines = LineList(
        spectrum=mainSpect)

    # Loop through the comb candidates
    for c in combCandidates:
        # Find all the lines in *this* comb that have survived the "using up"
        # of lines so far.
        survivingLines = []
        for m in c.members:
            if m.spectral_index not in usedLines.get_all_spectral_indices():
                survivingLines += [m]
        survivefs = [x.freq for x in survivingLines]
        # We now have all the frequencies of the surviving lines, but we should
        # demand that at least `requirelen` are consecutive.
        c.fit_comb_params()  # Refit the comb params
        nSurvive = np.count_nonzero(slt.consecutive_filter_Hz(survivefs,
                                                              c.combsp,
                                                              c.comboff,
                                                              requirelen))
        if nSurvive > 0:
            for s in survivingLines:
                usedLines.append_line(s, move_quiet=True)
        else:
            c.iscomb = False
            c.combsp = None
            c.comboff = None

    # Again, filter out anything that got demoted.
    combCandidates = [c for c in combCandidates if c.iscomb]

    # Convert to parameters for returning
    combParams = [(c.combsp, c.comboff) for c in combCandidates]

    return combParams

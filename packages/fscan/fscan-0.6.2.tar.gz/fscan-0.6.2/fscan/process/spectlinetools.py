# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

import numpy as np


def clip_spect(freq, val, fmin=None, fmax=None, islinefile=False):
    """
    We often need to limit the frequency range of a spectrum.
    This function accepts the original frequency and correspond value
    (ASD, PSD, coherence, etc) arrays and returns truncated arrays.

    Note that this could be done with np.where(), but if we're dealing
    with a large array that's already sorted, searchsorted()
    should speed things up.

    Parameters
    ----------
    freq : 1d np.ndarray
        Initial array of frequencies (floats)
    val : 1d np.ndarray
        Initial array of corresponding values. Note: in the case of line lists,
        these are likely to be strings.
    fmin : float
        Intended minimum frequency for the output array
    fmax : float
        Intended maximum frequency for the output array
    islinefile : bool
        If true, will assume the frequencies are not already sorted

    Returns
    -------
    freq_out : 1d np.ndarray
        Truncated frequency array
    val_out : 1d np.ndarray
        Truncated values array

    Raises
    ------
    Exception
    """

    freq = np.array(freq)
    val = np.array(val)

    if fmin is None:
        fmin = freq[0]
    if fmax is None:
        fmax = freq[-1]+.1  # has to be slightly bumped up for the searchsorted

    if fmin > fmax:
        raise Exception(
            "Requested frequency minimum is greater than requested maximum.")

    # Line files often have frequencies out of order,
    # so we should sort the entries.
    if islinefile:
        sorting_inds = np.argsort(freq)
        freq = freq[sorting_inds]
        val = val[sorting_inds]

    else:  # don't bother sorting the entries if it's a spectral file
        if fmin > freq[-1] or fmax < freq[0]:
            print("All data lies outside the given frequency range.")

    hicut = np.searchsorted(freq, fmax)
    lowcut = np.searchsorted(freq, fmin)
    freq_out = freq[lowcut:hicut]
    val_out = val[lowcut:hicut]

    return freq_out, val_out


def match_bins(spect, marks):
    """
    For some set of artifact/line frequencies (marks), find
    the indices of the closest frequency bin centers in a spectrum (spect).

    Parameters
    ----------
    spect : 1d array (dtype: float)
        spectral bin center frequencies
    marks : 1d array (dtype: float)
        artifact/line frequencies

    Returns
    -------
    inds : 1d array (dtype: integer)
        indices of spectral bin centers nearest to marks

    Raises
    ------
    Exception
    """

    if len(marks) == 0:
        return np.array([])
    # for each bincenter, figure out the distance to next bincenter
    binwidths = np.diff(spect)

    # the rightmost bincenter nothing after it, so use the preceding binwidth
    binwidths = np.append(binwidths, binwidths[-1])
    # for each bin center, the right edge of the bin should be 1/2 of the
    # rightward binwidth
    edges = spect + binwidths/2.
    # the leftmost bin has no left edge so use the subsequent binwidth
    edges = np.append(spect[0]-binwidths[0]/2., edges)

    if min(marks) < edges[0]:
        edges[0] = min(marks)-.1
    if max(marks) > edges[-1]:
        edges[-1] = max(marks)+.1

    # now digitize, using the calculated bin edges
    inds = np.digitize(marks, edges)

    # subtract 1 off the results so that they correspond appropriately to the
    # original bincenters
    inds -= 1

    # raise an exception if we got any results that aren't within the spectrum
    # bounds (returning negative numbers will create unexpected results)

    if len(inds) > 0:
        if np.amin(inds) < 0 or np.amax(inds) > len(spect)-1:
            raise Exception(
                "Not all tested values are within the spectrum bounds.")

    return inds


def consecutive_filter_Hz(fs, sp, off, requirelen):
    """
    Filter a list of tooth frequencies for a comb of known spacing and offset
    and return only those which are in consecutive blocks of length
    `requirelen` or greater

    Parameters
    ----------
    fs : numpy array, dtype float
        1d array of frequency values for each tooth
    sp : float
        comb spacing
    off : float
        comb offset
    requirelen : int
        Minimum consecutive block size to retain

    Returns
    -------
    1d numpy array, dtype bool
        Whether or not each entry in x is part of a consecutive block.

    """

    if isinstance(fs, list):
        fs = np.array(fs)
    ns = np.round((fs-off)/sp)
    return consecutive_filter_int(ns, requirelen)


def consecutive_filter_int(x, requirelen):
    """
    Filter a list of integers (for example, representing comb tooth harmonics)
    and return only those which are in consecutive blocks of length
    `requirelen` or greater.

    Parameters
    ----------
    x : numpy array, dtype int
        1D array of integers
    requirelen : int
        Minimum consecutive block size to retain

    Returns
    -------
    1d numpy array, dtype bool
        Whether or not each entry in x is part of a consecutive block.
    """

    x = np.sort(x)
    sublists = np.split(x, np.where(np.diff(x) > 1)[0]+1)
    retainvals = [
        item for sublist in sublists if len(sublist) >= requirelen
        for item in sublist]

    return np.isin(x, retainvals)


def combparams_to_teeth(combsp, comboff, freq):
    """
    Parameters
    ----------
    combsp : float
        comb spacing
    comboff : float
        comb offset
    freq : 1d numpy array, dtype float
        spectral frequencies

    Returns
    -------
    combfreq : 1d numpy array, dtype float
        frequencies of the comb teeth expected in the input frequency range
    combinds : 1d numpy array, dtype int
        spectral indices of comb teeth expected in the input frequency range
    """

    # Generate expected frequencies
    combfreq = np.arange(0, freq[-1], combsp)+comboff
    combnames = np.array([""]*len(combfreq))
    # Clip to spectral bounds
    combfreq, combnames = clip_spect(
        combfreq, combnames, freq[0], freq[-1], islinefile=True)
    # Comvert to indices
    combinds = match_bins(freq, combfreq)
    return combfreq, combinds


def combparams_to_labels(combsp, comboff, freq, knownpeaks=None, maxdecs=10):
    """
    Parameters
    ----------
    combsp : float
        comb spacing
    comboff : float
        comb offset
    freq : 1d numpy array, dtype float
        spectral frequencies
    knownpeaks : 1d numpy array, dtype int
        spectral indices of all known spectral peaks
    maxdecs : int
        maximum number of decimal places to consider

    Returns
    -------
    splabel : str
        label for spacing with appropriate precision
    offlabel : str
        label for offset with appropriate precision
    combfreq : 1d numpy array, dtype float
        comb tooth frequencies
    combinds : 1d numpy array, dtype int
        locations of comb teeth in `freq` array
    """

    # Determine highest verifiable peak location comb
    combfreqs, combinds = combparams_to_teeth(combsp, comboff, freq)

    # If no knownpeaks argument was supplied, look at all possible peaks
    if knownpeaks is None:
        knownpeaks = np.arange(len(freq))
    foundinds = combinds[np.isin(combinds, knownpeaks)]

    # If there are no peaks found, return empty arrays and warn the user
    if len(foundinds) == 0:
        wstring = f"Frequencies for {combsp},{comboff} Hz comb" \
                    " do not overlap with supplied `knownpeaks` array."
        print(wstring)
        return np.array([]), np.array([]), np.array([]), np.array([])

    maxind = max(foundinds)
    maxn = np.round((freq[maxind]-comboff)/combsp)

    # Now we need to determine the appropriate OFFSET rounding
    for ndecs_off in range(0, maxdecs):
        testoff = np.round(comboff, decimals=ndecs_off)
        testf = combsp*maxn+testoff
        testind = match_bins(freq, [testf])[0]
        if testind == maxind:
            comboff = testoff
            break

    # Now we need to determine the appropriate SPACING rounding
    for ndecs_sp in range(0, maxdecs):
        testsp = np.round(combsp, decimals=ndecs_sp)
        testf = testsp*maxn+comboff
        testind = match_bins(freq, [testf])[0]
        if testind == maxind:
            combsp = testsp
            break

    return (f"{combsp:.{ndecs_sp}f}",
            f"{comboff:.{ndecs_off}f}",
            combfreqs,
            combinds)


def combparams_to_labeled_teeth(combsp, comboff, freq, knownpeaks=None,
                                maxdecs=10):
    """
    Parameters
    ----------
    combsp : float
        comb spacing
    comboff : float
        comb offset
    freq : 1d numpy array, dtype float
        spectral frequencies
    knownpeaks : 1d numpy array, dtype int
        spectral indices of all known spectral peaks
    maxdecs : int
        maximum number of decimal places to consider

    Returns
    -------
    combfreq : 1d numpy array, dtype float
        frequencies of the comb teeth expected in the input frequency range
    combinds : 1d numpy array, dtype int
        spectral indices of comb teeth expected in the input frequency range
    combnames : 1d numpy array, dtype str
        formatted labels for each comb tooth, rounded to the smallest number of
        decimal places that can accurately describe the comb
    """
    splabel, offlabel, combfreqs, combinds = combparams_to_labels(
        combsp, comboff, freq, knownpeaks, maxdecs)

    combnames = []
    for combfreq in combfreqs:
        n = int(np.round((combfreq-comboff)/combsp))
        combnames += [
            f"Tooth of the {splabel};"
            f"{offlabel} Hz comb (n={n})"]
    combnames = np.array(combnames)

    return combfreqs, combinds, combnames

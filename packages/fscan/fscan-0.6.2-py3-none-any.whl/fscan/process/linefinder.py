# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

import numpy as np
from scipy.signal import peak_prominences
from scipy.stats import norm
from scipy.interpolate import interp1d


def running(x, window):
    """
    This computes a running average, median, and standard deviation
    for a given input array.

    This will return arrays the same length as the original input.

    Since the window can't be done properly at the edges of the array,
    the values for bins floor(window/2) away from the edges are filled
    in with copies of the first/last properly calculated values.

    The result for each bin *does* take into account the original data
    in that bin, not just the surrounding data.

    Parameters
    ----------
    x : 1d np.ndarray, dtype = float
        The input array to calculate running statistics

    window : int
        Number of bins to use for the window (should be odd; will be
        readjusted if even)

    Returns
    -------
    avg : 1d np.ndarray
        Running average
    std : 1d np.ndarray
        Running standard deviation
    med : 1d np.ndarray
        Running median
    """

    # make the window an int if it's not already
    nwindow = int(window)

    # make the window an odd number of it's not
    # already
    if window % 2 == 0:
        window += 1
    # set up the 'halfwindow' value (note the floor)
    halfwindow = int(np.floor(window/2.))

    # The edges of the array are problematic; we
    # are going to calculate statistics only for
    # bins that are at least `halfwindow` away from
    # the edges. To do this, we set up a new array
    # with the truncated length `nremainder`.

    # We will also need to average together `nwindow`
    # values for each data point. So the other
    # dimension of our array is `nwindow`.
    nremainder = len(x)-2*halfwindow
    dat = np.zeros((nwindow, nremainder))

    # Now we start populating the rows of our array
    # `dat`. Each row is a sample of the original
    # array, shifting by 1 bin each time.
    # To visualize (window=3):
    # 1 2 3 4 5 ...
    # 2 3 4 5 6 ...
    # 3 4 5 6 7 ...
    # etc
    for i in range(0, nwindow):
        dat[i] = x[i:i+nremainder]

    # Transpose the matrix. Now every row corresponds
    # to the data that will be averaged together for
    # a single output data point. Note that the target
    # bin IS included in this data and will influence the
    # running statistics.
    dat = np.transpose(dat)

    # Grab the data for the first and last bins;
    # we will use this to fill in the extra `halfwindow`
    # on each side of the array.
    replineA = np.array([dat[0]])
    replineB = np.array([dat[-1]])
    repA = np.repeat(replineA, halfwindow, axis=0)
    repB = np.repeat(replineB, halfwindow, axis=0)
    dat = np.append(repA, dat, axis=0)
    dat = np.append(dat, repB, axis=0)

    # Now we just compute the statistics and return them
    avg = np.average(dat, axis=1)
    std = np.std(dat, axis=1)
    med = np.median(dat, axis=1)
    return avg, std, med


def peaks(val, far, window, normval=True, logval=True):
    """
    Identify peaks in an array of data.

    It is intended specifically to identify narrow lines in
    high-resolution spectral data.

    Parameters
    ----------
    val : 1d np.ndarray, dtype = float
        The values (not frequencies) for the spectrum.
        Could be ASD, PSD, etc.

    far : float
        An approximate (... very approximate) per-bin
        false alarm rate to target. A value around 0.001
        may be a good starter. This is not set as a default
        because the user should consider it carefully.

    window : int
        A window width *in bins* for computing the running
        statistics. As a starter value, select a number of
        bins corresponding to ~0.05 Hz in the original
        spectrum.

    normval : bool
        normalize the val array by the smallest value (as long as that value
        is not zero)

    logval : bool
        the log10 of the val array is taken when this is True and all values
        of the array are non-zero

    Returns
    -------
    peak_inds : 1d np.ndarray, dtype = int
        The indices of the original array where a peak is
        apparently located.
    """

    # Check if the array is uniform values. If so, don't
    # return any lines (trying to run this will cause it
    # to stall on the prominence computation).
    if min(val) == max(val):
        return np.array([])

    # convert to the log of the values
    # this slightly distorts the distribution, but handles
    # very high peak prominences better
    # we have to be careful if the input val array is zeros
    val0 = np.copy(val)
    if normval and (minval := min(val0)) != 0:
        val0 /= minval
    if logval and np.all(val != 0):
        val0 = np.log10(val0)

    # determine the prominences of all data points
    proms0 = peak_prominences(val0, np.arange(len(val0)))[0]

    # compute running average, standard dev, and median
    _, _, med0 = running(val0, int(np.round(window)))

    # set up a dummy x-axis (the units are entirely unimportant;
    # it is frequency-like)
    x = np.linspace(0, 100, len(val0))
    # Now create an x-axis with double the resolution.
    # we will use both of these quantities later for the "mirrored"
    # data series.
    xdouble = np.linspace(0, 100, len(val0)*2)

    # subtract off the median so that values below it are negative
    zeroedval = val0[:] - med0
    # select the indices where there are negative values
    # (below median in original data set)
    select = np.where(zeroedval < 0)[0]

    # We're going to create a symmetrical set of data
    # points above zero, just copying the points below zero
    # and flipping the sign.
    # First, we set up some empty arrays for the x- and y-axes.
    doubleside = np.zeros(len(select)*2)
    xtestdoubleside = np.zeros(len(select)*2)

    # For the y-values,
    # we're going to interleave the negative values with their
    # "mirrored" positive counterparts.
    # (This is necessary to preserve the frequency dependence of
    # the running statistics)
    doubleside[0::2] = zeroedval[select]
    doubleside[1::2] = zeroedval[select]*-1

    # For the x-axis, we will use the double-resolution dummy
    # axis as a source. We are grabbing the matching bins
    # for the selected (below zero) data points, and the
    # subsequent bins for their "mirrored" counterparts.
    xtestdoubleside[0::2] = xdouble[select*2]
    xtestdoubleside[1::2] = xdouble[select*2+1]

    # Having finished creating this modified data set which
    # excludes lines (and indeed anything above the median),
    # we re-compute the running statistics
    avg, std, med = running(doubleside, int(window))

    # Convert the requested FAR to a running threshold value
    # using the computed running statistics
    t_doublesided = norm.ppf(1-far, scale=std, loc=med)
    # Interpolate the running threshold value to account for gaps left
    # by exclusion of data above the median
    tfunc = interp1d(xtestdoubleside, t_doublesided, bounds_error=False)
    t = tfunc(x) + med0

    # Set a prominence threshold based on empirical studies of
    # the prominence distribution of Gaussian noise
    # (Future TODO: should probably revisit stats due to the log at the
    # beginning)
    tprom = tfunc(x)*1.97

    # Determine the points at which both thresholds are exceeded
    peak_inds = np.where((val0 >= t) & (proms0 >= tprom))[0]

    # Return the appropriate indices
    return peak_inds

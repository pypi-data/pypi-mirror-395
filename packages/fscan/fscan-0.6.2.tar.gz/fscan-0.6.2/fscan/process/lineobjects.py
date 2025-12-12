# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

from dataclasses import dataclass, field
from .spectlinetools import match_bins
import numpy as np
from scipy.optimize import curve_fit

# ------------------------------------------
# Small functions for comb parameter fitting
# ------------------------------------------


def comb_form(n, sp, off):
    """
    This function returns the frequency of the nth harmonic
    of a comb with spacing `sp` and offset `off`
    (Used for fitting comb parameters)

    Parameters
    ----------
    n : int
        harmonic number
    sp : float
        spacing (Hz)
    off : float
        offset from integer multiples of spacing (Hz)

    Returns
    -------
    frequency : float
        Frequency of nth harmonic
    """
    frequency = (sp * n) + off

    return frequency


def comb_form_zero_off(n, sp):
    """
    This function returns the frequency of the nth harmonic
    of a comb with spacing `sp` and offset zero
    (Used for fitting comb parameters)

    Parameters
    ----------
    n : int
        harmonic number
    sp : float
        spacing (Hz)

    Returns
    -------
    frequency : float
        Frequency of nth harmonic
    """
    frequency = (sp * n)
    return frequency


@dataclass(kw_only=True)
class Spectrum:
    """
    Lines are optionally associated with a spectrum. Most of the
    spectral properties listed here (channel, data type, etc.)
    are not actually used, but are included here for ease of
    extensibility to tracking lines across multiple spectra.

    A Spectrum object can hold a full array of frequencies and
    values, which can in turn be accessed to find out (for
    instance) which spectral bin an associated line belongs to.
    """
    label: str = ''  # a label for the spectrum
    source_file: str = ''  # path to the source file
    # 'spect' in usual cases; could also be 'list'
    # for linelists with a given resolution
    source_type: str = ''
    freq_array: np.ndarray = field(
        default_factory=lambda: np.array([], dtype=float))
    val_array: np.ndarray = field(
        default_factory=lambda: np.array([], dtype=float))
    resolution: float = np.nan
    freq_min: float = np.nan
    freq_max: float = np.nan
    channel: str = ''
    epoch_start_gps: int = 0
    epoch_duration_sec: int = 0
    # such as ASD, PSD, coherence, persistence...
    height_datatype: str = ''

    def __post_init__(self):
        if len(self.freq_array) > 0:
            if self.resolution is not np.nan:
                raise Exception(
                    "Please do NOT supply both a frequency array and a"
                    " frequency resolution, as these may conflict.")
            if self.freq_min is not np.nan:
                raise Exception(
                    "Please do NOT supply both a frequency array and a"
                    " frequency minimum, as these may conflict.")
            if self.freq_max is not np.nan:
                raise Exception(
                    "Please do NOT supply both a frequency array and a"
                    " frequency maximum, as these may conflict.")
            self.freq_min = self.freq_array[0]
            self.freq_max = self.freq_array[-1]
            self.resolution = ((self.freq_max - self.freq_min) /
                               (len(self.freq_array) - 1))


@dataclass(kw_only=True)
class LineList:
    """
    A LineList object is a collection of Lines associated with a particular
    artifact
    """
    label: str = ''
    members: list = field(default_factory=list)
    spectrum: Spectrum = None
    iscomb: bool = False
    combsp: float = np.nan
    comboff: float = np.nan

    def append_line(self, line, duplicate_mode='allow', move_quiet=False):
        """
        Append a lin to the LineList

        Parameters
        ----------
        line : Line
            Line object to add to this LineList
        duplicate_mode : str
            Specify duplication mode. Options are:
            - 'allow'
            - 'alert'
            - 'skip'
            - 'disallow'
        move_quiet : bool
            If True, remove from previous parent silently, otherwise notify
            (default: False)

        Raises
        ------
        Exception
        ValueError
        """

        if not isinstance(line, Line):
            raise Exception("Can only append a Line to a LineList")

        if duplicate_mode == "allow":
            pass
        elif duplicate_mode in ["alert", "skip", "disallow"]:
            for m in self.members:
                if is_equivalent(m, line):
                    if duplicate_mode == "alert":
                        print(
                            f"Warning: added line with frequency {line.freq}"
                            f" is equivalent to line with frequency {m.freq}"
                            f" in LineList '{self.label}'")
                    elif duplicate_mode == "skip":
                        return
                    else:
                        raise Exception(
                            f"Added line with frequency {line.freq} is"
                            f" equivalent to line with frequency {m.freq} in"
                            f" LineList '{self.label} and cannot be added"
                            f" under duplicate mode 'disallow'.")
        else:
            raise ValueError(
                "Invalid duplication mode (specify: allow, alert, skip, or "
                "disallow)"
            )

        # If the line already has a parent, we are effectively moving it.
        if line.parent:
            if not move_quiet:
                print(
                    f"Line can only be a member of one line list. It will be"
                    f" removed from LineList {line.parent.label} so that it"
                    f" can be appended to LineList {self.label}")
            line.parent.members.remove(line)
        # Set the line properties appropriately
        self.members += [line]
        line.parent = self
        # If this LineList is associated with a spectrum,
        # propose associating the line with the same spectrum
        if self.spectrum is not None:
            # If the line already has a spectrum and it's not the
            # same spectrum, raise an exception
            if line.spectrum is not None:
                if line.spectrum != self.spectrum:
                    raise Exception(
                        "Cannot append Line to LineList; "
                        "they have different source spectra.")
            # If the line has no spectrum of its own,
            # associate it with the LineList's spectrum
            line.spectrum = self.spectrum
            line.adjust_to_bin()
        # Sort the lines by frequency
        self.sort_lines()

    def sort_lines(self):
        """ sort the lines in the LineList in place """
        self.members.sort(key=lambda x: x.freq)

    def print_lines(self):
        """ Print the lines in the LineList """
        for m in self.members:
            print(f"{m.freq},{m.label}")

    def get_frequency_range(self):
        """ Return the min and max frequencies of lines in the LineList

        Returns
        -------
        min_freq : float
        max_freq : float

        Notes
        -----
        This function sorts the lines in the LineList in place by calling
        self.sort_lines().
        """
        self.sort_lines()
        min_freq = self.members[0].freq
        max_freq = self.members[-1].freq
        return min_freq, max_freq

    def get_all_frequencies(self):
        """ Return a list of frequencies of lines in the LineList """
        return [m.freq for m in self.members]

    def get_all_spectral_indices(self):
        """ Return a list of spectral indices of lines in the LineList """
        return [m.spectral_index for m in self.members]

    def fit_comb_params(self):
        """
        This function attempts to fit a frequency and offset to current
        members of the LineList, and sets self.iscomb=True if successful
        as well as updating self.combsp and self.comboff.

        Zero offset is tried first, so that it is prioritized over nonzero
        offset.

        In order to be a successful fit, the recovered comb parameters must
        accurately predict the frequency bins of *every* line in the current
        set of LineList members.
        """
        # grab the frequency information of the current set of lines
        freqs = np.array(self.get_all_frequencies())
        fmin, fmax = self.get_frequency_range()
        frange = fmax-fmin

        # get an extremely rough spacing estimate
        # (only for harmonic calculation)
        approx_sp = min(np.diff(freqs))

        # Calculate harmonic numbers for given peaks.
        # If we allow offset, then we should choose
        # the floor of the frequency/spacing. (Remainder
        # can be described by an offset.)

        # If we hypothesize zero offset, then we should round (closest
        # integer gives best chance of finding a real comb).
        ns_zero_off = np.round(freqs/approx_sp)
        # If we hypothesize non-zero offset, we should take the floor
        # instead (any deviation from an integer multiple of the spacing
        # can be explained as a positive offset that way)
        ns_with_off = np.floor(freqs/approx_sp)
        nss = [ns_zero_off, ns_with_off]

        # First, attempt a curve fit assuming zero offset.
        # If that doesn't fit, attempt a curve fit with nonzero offset.
        bounds_zero_off = (
            [0, 0],
            [frange, 0])
        bounds_with_off = (
            [0, 0],
            [frange, frange])
        boundss = [bounds_zero_off, bounds_with_off]

        # First try fitting to a comb with zero offset. If that fails,
        # try fitting to a comb with nonzero offset.
        isComb = False
        for iform, form in enumerate(zip(nss, boundss)):
            ns, bounds = form
            try:
                params, _ = curve_fit(comb_form,
                                      ns,
                                      freqs,
                                      bounds=bounds,
                                      method='dogbox')
            except Exception:
                continue
            sp, off = params

            # Check whether the proposed spacing & offset fully describe
            # the given set of lines
            predictedFreqs = ns*sp + off
            predictedLocs = match_bins(
                self.spectrum.freq_array,
                predictedFreqs)

            if np.all(predictedLocs == self.get_all_spectral_indices()):
                isComb = True
                break

        if isComb:
            self.iscomb = True
            self.combsp = sp
            self.comboff = off
        else:
            self.iscomb = False
            self.combsp = np.nan
            self.comboff = np.nan


@dataclass(kw_only=True)
class Line:
    """
    The most important property of a line is its frequency;
    it makes no sense to define a line without that.

    The second most important property of a line is the spectrum
    in which it occurs (if specified). An alternate way to specify
    the line frequency is by supplying a spectrum and spectral index.

    Lines may be members of LineLists. At present, each line can
    only have one such parent.

    Lines can also store additional information, like a label, a
    prominence, or a height (the latter currently unused, but included
    for future extensibility).
    """
    freq: float = np.nan
    label: str = ''
    spectral_index: int = -1
    prominence: float = np.nan
    height: float = np.nan
    spectrum: Spectrum = None
    parent: LineList = None

    def __post_init__(self):
        # if we weren't given a spectrum, but the parent LineList has one,
        # update the Line spectrum property accordingly.
        if not self.spectrum and self.parent:
            if self.parent.spectrum:
                self.spectrum = self.parent.spectrum

        # If we got a frequency and a spectral index, complain since these
        # things could be incompatible; one should be calculated from the other
        if self.freq is not np.nan:
            if self.spectral_index >= 0:
                raise Exception(
                    "Please do NOT supply both a frequency and a spectral "
                    "index, as these may conflict.")
        # adjust_to_bin handles the cases where there is a spectral index and
        # a spectrum, or where there is a frequency and we need to get the
        # nearest spectral index
        self.adjust_to_bin()

        # If we still don't have a frequency, raise an exception
        if self.freq is np.nan:
            raise Exception(
                "Line must have a frequency, or enough information "
                "to calculate one")

    def adjust_to_bin(self):
        """ If there is a spectrum associated with the line, we may wish
        to adjust the frequency of the line to that of the nearest spectral
        bin center.

        Raises
        ------
        Exception
        """
        if self.spectrum is None:
            raise Exception(
                "Cannot adjust to bin; no spectrum associated with this line.")

        if self.spectral_index >= 0:
            pass
        else:
            self.spectral_index = match_bins(
                self.spectrum.freq_array,
                [self.freq])[0]
        self.freq = self.spectrum.freq_array[self.spectral_index]


def is_equivalent(A, B, tol=None):
    """
    Accepts two line objects, which may or may not
    be associated with the same spectrum.
    Determines whether they are equivalent.

    Parameters
    ----------
    A : Line
        First line to compare
    B : Line
        Second line to compare
    tol : float
        Absolute frequency tolerance, if an explicit value needs
        to be used. Otherwise, will use spectral information.

    Returns
    -------
    bool
        Whether or not the lines are equivalent for
        the given tolerance and/or spectral info.

    Raises
    ------
    Exception
    """

    # === Direct comparisons with tolerance

    # if an explicit tolerance was given, use that
    if tol:
        return np.isclose(A.freq, B.freq, atol=tol)

    # === Impossible to compare lines (not enough spectral info)

    # if A and B are unassociated with any spectrum
    # and no tolerance was supplied
    elif (not A.spectrum) or (not B.spectrum):
        raise Exception(
            "These lines cannot be compared. They lack spectrum information"
            " and no tolerance was supplied.")

    # if A and B are associated with spectra, but the resolution is unknown
    elif (not A.spectrum.resolution) or (not B.spectrum.resolution):
        raise Exception(
            "These lines cannot be compared. Their spectra lack resolution"
            " information.")

    # === Spectral info available, ordered best case to worst case

    # if A and B are in the same line list and they both have
    # spectral indices (from any source)
    elif A.spectrum == B.spectrum and A.spectral_index and B.spectral_index:
        return (A.spectral_index == B.spectral_index)

    # if A and B both have spectra with associated frequency arrays
    elif (A.spectrum == B.spectrum) and (A.spectrum.freq_array is not None):
        # Select the lower-resolution spectrum to use for comparison.
        refspect = [A.spectrum, B.spectrum].sort(key=lambda x: x.resolution)[1]
        # compare the indices in the lower-resolution spectrum
        compare_inds = []
        for line in [A, B]:
            if line.spectrum is refspect:
                compare_inds += [line.spectral_index]
            else:
                compare_inds += [match_bins(
                    refspect,
                    [line.freq])[0]]
        return (compare_inds[0] == compare_inds[1])

    # As a last resort, if A and B both have spectra with associated
    # resolution info, work with that info. "Worst" resolution here means
    # largest spectrum.resolution value, widest spacing of bins.
    else:
        worstres = max(A.spectrum.resolution, B.spectrum.resolution)
        return np.isclose(A.freq, B.freq, atol=worstres)

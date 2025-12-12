# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#               Ansel Neunzert (2023)
#
# This file is part of fscan

import numpy as np
from pathlib import Path
import re
import yaml

from ..process.spectlinetools import clip_spect
from .utils import numdecs


def read_channel_config(chan_opts):
    """
    Helper method in case we needed access to loading the channel yml
    information

    Parameters
    ----------
    chan_opts : Path, str
        Path to the channel yml file

    Returns
    -------
    ch_info : dict
        Channel info
    """
    with open(chan_opts) as f:
        ch_info = yaml.safe_load(f)

    return ch_info


def read_fscan_ascii_data(fname, dtype=None):
    """
    Read ASCII data

    Parameters
    ----------
    fname : Path, str
        Path to the ASCII data file
    dtype : str, optional
        Data type of the file, if known. If `dtype=None`, then this function
        will attempt to infer the data type automatically.

    Returns
    -------
    data : np.array
        numpy array of the data
    header : dict
        dictionary of the metadata from the ASCII file header or path
        information

    Raises
    ------
    ValueError
        If the `dtype` parameter provided does not match expected from
        file metadata (header or filename)
    """

    assert Path(fname).suffix == ".txt"

    fname = Path(fname).expanduser().absolute()

    data = np.transpose(np.loadtxt(fname))

    # Get header information either from the header line or from the
    # parent path and file name
    header = {}
    with open(fname) as fi:
        header_line = fi.readline()
    if header_line.startswith("#"):
        header_line = header_line.split(' ')[1:]
        if '/' not in header_line[0]:
            header['channel'] = header_line[0]
        else:
            chB, chA = header_line[0].split('/')
            header['channelA'] = chA
            header['channelB'] = chB
            if not dtype:
                dtype = 'coherence'
            elif dtype != 'coherence':
                raise ValueError('Inconsistent dtype')
        header['segtype'] = header_line[1]
        header['epoch'] = header_line[2]
        header['duration'] = header_line[3]
        header['gpsstart'] = int(header_line[4])
        header['gpsend'] = int(header_line[5])
        header['fmin'] = float(header_line[6])
        header['fmax'] = float(header_line[7])
        header['Tsft'] = int(header_line[8])
    else:
        # pattern matching of the filepath to get parts for the header
        for part in fname.parts[::-1]:
            if (re.match(r'[A-Z]{1}\d{1}_.+', part) and
                    'channel' not in header and
                    'channelB' not in header):
                if fname.name.endswith('_coh.txt'):
                    header['channelB'] = part.replace('_', ':', 1)
                    header['channelA'] = 'Undefined - maybe h(t) channel'
                    if not dtype:
                        dtype = 'coherence'
                    elif dtype != 'coherence':
                        raise ValueError('Inconsistent dtype')
                else:
                    header['channel'] = part.replace('_', ':', 1)
            elif re.match(r'\d+-?\d*', part) and 'epoch' not in header:
                header['epoch'] = part
            elif (re.match(r'^\d*\w+\d*\w*', part) and
                  'duration' not in header):
                header['duration'] = part
            elif ((re.match(r'.\d_.+', part) or re.match(r'ALL', part)) and
                  'segtype' not in header):
                header['segtype'] = part
            elif re.match(r'\d+s', part) and 'Tsft' not in header:
                header['Tsft'] = int(part.split('s', 1)[0])
        # pattern matching in the filename
        for part in fname.name.split('_'):
            if re.match(r'\d+.\d+', part) and 'fmin' not in header:
                header['fmin'] = float(part)
            elif re.match(r'\d+.\d+', part) and 'fmax' not in header:
                header['fmax'] = float(part)
            elif re.match(r'\d+', part) and 'gpsstart' not in header:
                header['gpsstart'] = int(part)
            elif re.match(r'\d+', part) and 'gpsend' not in header:
                header['gpsend'] = int(part)

    # Apply dtype is not already known, determined from file name
    # Raise an error if dtype provided doesn't match the expected one
    if 'timeaverage' in fname.name:
        if not dtype:
            dtype = 'normpow'
        elif dtype != 'normpow':
            raise ValueError('Inconsistent dtype')
    elif 'spectrogram' in fname.name:
        if not dtype:
            dtype = 'spectrogram'
        elif dtype != 'spectrogram':
            raise ValueError('Inconsistent dtype')
    elif 'PWA' in fname.name:
        if not dtype:
            dtype = 'PWA'
        elif dtype != 'PWA':
            raise ValueError('Inconsistent dtype')
    elif 'speclong' in fname.name:  # speclong may not always be in the name
        if not dtype:
            dtype = 'speclong'
        elif dtype != 'speclong':
            raise ValueError('Inconsistent dtype')
    elif 'coh' in fname.name:  # coh may not always be in the name
        if not dtype:
            dtype = 'coherence'
        elif dtype != 'coherence':
            raise ValueError('Inconsistent dtype')

    # Raise error if dtype is not determined
    if not dtype:
        raise ValueError('Unable to determine file data type')

    header['dtype'] = dtype

    # If channel unknown, mark it as such
    if 'channel' not in header and dtype != 'coherence':
        header['channel'] = 'Unknown'

    return data, header


def get_metadata_from_fscan_npz(fname):
    """ Get the metadata from a fscan npz file.

    Parameters
    ----------
    fname : Path, str
        Path to the fscan npz file

    Returns
    -------
    metadata : dict
        Dictionary of metadata from fscan npz file.
    """

    # allow_pickle is required to load the metadata, which is a dict
    # TODO: maybe the allow_pickle can be removed
    data = np.load(fname, allow_pickle=True)

    metadata = {}
    if str(fname).endswith("_coherence.npz"):
        metadata['channelA'] = str(data['channelA'])
        metadata['channelB'] = str(data['channelB'])
    else:
        metadata['channel'] = str(data['channel'])
    metadata['segtype'] = str(data['segtype'])
    metadata['epoch'] = str(data['epoch'])
    metadata['duration'] = str(data['duration'])
    metadata['gpsstart'] = int(data['gpsstart'])
    metadata['gpsend'] = int(data['gpsend'])
    metadata['fmin'] = float(data['fmin'])
    metadata['fmax'] = float(data['fmax'])
    metadata['Tsft'] = int(data['Tsft'])
    try:
        metadata['dtype'] = str(data['dtype'])
    except KeyError:
        metadata['dtype'] = None

    return metadata


def load_spect_from_fscan_npz(fname, freqname="", dataname=""):
    """ Load spectrum from a data file. Expects Fscan-like .npz data formats.

    Parameters
    ----------
    fname : Path, str
        Path to file
    freqname : str
        name of frequency array to load from npz; if empy string or None
        assume freqname = 'f'
    dataname : str
        name of data array to load from npz; if empty string or None
        guess dataname based on the suffix string of the npz file

    Returns
    -------
    freq : 1-d numpy array (dtype: float)
        Array of frequencies
    val : 1-d numpy array (dtype: float)
        Array of values associated with the data
    meta : dict
        Dictionary of metadata

    Raises
    ------
    Exception
        If the name of the values column could not be guessed
    """

    # Make sure the file path is properly formatted
    fname = Path(fname).expanduser().absolute()

    # allow_pickle is required to load the metadata, which is a dict
    # TODO: maybe the allow_pickle can be removed
    data = np.load(fname, allow_pickle=True)

    # If no column name was specified, guess one from the Fscan standard names.
    if freqname == "" or not freqname:
        freqname = 'f'
        print(f"Attempting to load frequencies from array '{freqname}'")
    if dataname == "" or not dataname:
        if str(fname).endswith("_timeaverage.npz"):
            dataname = 'normpow'
        elif str(fname).endswith("_speclong.npz"):
            dataname = 'amppsdwt'
        elif str(fname).endswith("_coherence.npz"):
            dataname = 'coh'
        else:
            raise Exception(
                "Could not guess name of the values column in the npz file")
        print("Attempting to load values from array '{}'".format(dataname))

    # load the data
    freq = data[freqname]
    val = data[dataname]

    try:
        metadata = get_metadata_from_fscan_npz(fname)
    except KeyError:
        metadata = None

    return freq, val, metadata


def load_spect_data(spectfile, **kwargs):
    """
    Load spectral data from Fscan-like .npz file or ASCII data

    Parameters
    ----------
    spectfile : Path, str
        Path to Fscan ASCII or .npz file
    kwargs : dict
        keyword arguments passed to load_spect_from_fscan_npz or
        read_fscan_ascii_data

    Returns
    -------
    sfreq : np.array
        Frequency data
    sval : np.array
        Data values
    metadata : dict
        Fscan metadata

    Raises
    ------
    ValueError
        If dataname is unsupported or the file type is unsupported
    """

    dataname = kwargs.pop("dataname", "")
    freqname = kwargs.pop("freqname", "")

    if (suff := Path(spectfile).suffix) == ".npz":
        sfreq, sval, metadata = load_spect_from_fscan_npz(
            spectfile, dataname=dataname, freqname=freqname
        )
    elif suff == ".txt":
        dtype = kwargs.pop("dtype", None)
        data, metadata = read_fscan_ascii_data(spectfile, dtype=dtype)
        if metadata['dtype'] == 'normpow':
            sfreq, sval = data
        elif metadata['dtype'] == 'speclong':
            sfreq, psd, amppsd, psdwt, amppsdwt, persist = data
            if dataname in ["", "amppsdwt"] or not dataname:
                sval = amppsdwt
            elif dataname == 'psd':
                sval = psd
            elif dataname == 'amppsd':
                sval = amppsd
            elif dataname == 'psdwt':
                sval = psdwt
            elif dataname == 'persist':
                sval = persist
            else:
                raise ValueError('Unsupported dataname')
        elif metadata['dtype'] == 'coherence':
            sfreq, sval = data
    else:
        raise ValueError('Unsupported file type')

    sfreq, sval = clip_spect(sfreq, sval, **kwargs)

    return sfreq, sval, metadata


def load_spectrogram_data(fname, **kwargs):
    """
    Load spectrogram from a data file

    Expects ASCII txt file or Fscan-like .npz data format

    Parameters
    ----------
    fname : Path, str
        Path to file
    kwargs : dict
        keyword arguments passed to read_fscan_ascii_data

    Returns
    -------
    times : 1-d numpy array (dtype: int)
    freq : 1-d numpy array (dtype: float)
        Array of frequencies
    val : 1-d numpy array (dtype: float)
        Array of values associated with the data
    metadata : dictionary
        Dictionary of metadata

    Raises
    ------
    ValueError
        If file type is unsupported; or data type is not determined or
        inconsistent
    """

    # Make sure the file path is properly formatted
    fname = Path(fname).expanduser().absolute()

    if (suff := fname.suffix) == ".npz":
        data = np.load(fname, allow_pickle=True)
    elif suff == ".txt":
        dtype = kwargs.pop("dtype", None)
        asciidata, metadata = read_fscan_ascii_data(fname, dtype=dtype)
        if not metadata['dtype'] == 'spectrogram':
            raise ValueError
        data = {
            'gpstimes': asciidata[0, 1:],
            'f': asciidata[1:, 0],
            'vals': asciidata[1:, 1:],
        }
    else:
        raise ValueError('Unsupported file type')

    try:
        metadata = get_metadata_from_fscan_npz(fname)
    except KeyError:
        metadata = None

    return data['gpstimes'], data['f'], data['vals'], metadata


def load_lines_from_linesfile(fname):
    """
    Load line data from a linesfile. Expects csv data with two entries per row,
    the first being a frequency (float) and the second being a label (which
    cannot include commas)

    Example:

    10.000,First line label
    10.003,Second line label
    ...

    If an .npz file is supplied instead, assume it contains frequencies and
    that there are no labels.

    Parameters
    ----------
    fname : Path, str
        Path to file

    Returns
    -------
    lfreq : 1-d numpy array (dtype: float)
        Array of frequencies
    names : 1-d numpy array (dtype: str)
        strings of names associated with given lines.
    """

    # Make sure the file path is properly formatted
    fname = Path(fname).expanduser().absolute()

    if fname.suffix == ".npz":
        lfreq = np.load(fname)
        names = np.array([""]*len(lfreq))
    else:
        # Load the data
        linesdata = np.genfromtxt(fname, delimiter=",", dtype=str)
        if len(linesdata) == 0:
            print("Linesfile does not contain any data.")
            return [], []
        lfreq = linesdata[:, 0].astype(float)
        names = linesdata[:, 1]

    return lfreq, names


def combarg_to_combparams(combarg, delimiter=","):
    """
    Very small utility for parsing arguments from the command line to
    comb parameters.

    Parameters
    ----------
    combarg : str
        Format: "<spacing>,<offset>" (or other delimiter if specified)
    delimiter : str
        string expected to separate the spacing and offset

    Returns
    -------
    combsp : float
        comb spacing
    comboff : float
        comb offset

    Raises
    ------
    Exception
        Incorrect format of comb arguments
    """

    if delimiter not in combarg:
        raise Exception(
            f"'{combarg}' is not in correct format to specify a comb.")

    # Grab spacing and offset
    combsp, comboff = combarg.split(delimiter)
    combsp = float(combsp)
    comboff = float(comboff)

    return combsp, comboff


def convert_fscan_txt_to_npz(parentPathInput, spects, **kwargs):
    """
    Convert Fscan txt files to npz files

    Parameters
    ----------
    parentPathInput : Path, str
        Full path to files
    spects : str
        glob-style string for txt files to convert to npz
    kwargs : dict
        keyword arguments to pass to read_fscan_ascii_data

    Returns
    -------
    error_num : int
        Return 0 if successful, 1 if data is all zeros or nans

    Raises
    ------
    NameError
        If no files are found with the specified pattern
    """

    files = sorted(Path(parentPathInput).glob(spects))

    if len(files) == 0:
        raise NameError(f"No files found with pattern {spects}")

    error_num = 0

    for f in files:
        dtype = kwargs.pop("dtype", None)
        data, header = read_fscan_ascii_data(f, dtype=dtype)

        temp_s = str(f).replace("_H1_", "_").replace(
            "_L1_", "_").strip(".txt")
        temp_s = Path(temp_s).name
        n = temp_s.split("_")
        n[0] = "fullspect"
        n[1] = f"{header['fmin']:.{numdecs(1 / header['Tsft'])}f}"
        n[2] = f"{header['fmax']:.{numdecs(1 / header['Tsft'])}f}"

        if temp_s.endswith("_PWA"):
            out = parentPathInput / "_".join(n).replace(
                "_PWA", "_speclongPWA.npz")
            freq, pwa_tavgwt, pwa_sumwt = data
            if np.all(np.isnan(pwa_tavgwt)):
                error_num = 1
            else:
                np.savez_compressed(out,
                                    channel=header['channel'],
                                    segtype=header['segtype'],
                                    epoch=header['epoch'],
                                    duration=header['duration'],
                                    gpsstart=header['gpsstart'],
                                    gpsend=header['gpsend'],
                                    fmin=header['fmin'],
                                    fmax=header['fmax'],
                                    Tsft=header['Tsft'],
                                    f=freq,
                                    pwa_tavgwt=pwa_tavgwt,
                                    pwa_sumwt=pwa_sumwt,
                                    dtype=dtype,
                                    )
            del freq, pwa_tavgwt, pwa_sumwt
        elif 'spectrogram' in temp_s:
            out = parentPathInput / ".".join(["_".join(n), "npz"])
            gpstimes = data[0, 1:]
            vals = data[1:, 1:]
            freq = data[1:, 0]
            if np.all(vals == 0):
                error_num = 1
            else:
                np.savez_compressed(out,
                                    channel=header['channel'],
                                    segtype=header['segtype'],
                                    epoch=header['epoch'],
                                    duration=header['duration'],
                                    gpsstart=header['gpsstart'],
                                    gpsend=header['gpsend'],
                                    fmin=header['fmin'],
                                    fmax=header['fmax'],
                                    Tsft=header['Tsft'],
                                    f=freq,
                                    vals=vals,
                                    gpstimes=gpstimes,
                                    dtype=dtype,
                                    )
            del gpstimes, vals, freq
        elif 'timeaverage' in temp_s:
            out = parentPathInput / ".".join(["_".join(n), "npz"])
            freq, normpow = data
            if np.all(normpow == 0):
                error_num = 1
            else:
                np.savez_compressed(out,
                                    channel=header['channel'],
                                    segtype=header['segtype'],
                                    epoch=header['epoch'],
                                    duration=header['duration'],
                                    gpsstart=header['gpsstart'],
                                    gpsend=header['gpsend'],
                                    fmin=header['fmin'],
                                    fmax=header['fmax'],
                                    Tsft=header['Tsft'],
                                    f=freq,
                                    normpow=normpow,
                                    dtype=dtype,
                                    )
            del freq, normpow
        elif 'coh' in temp_s:
            out = parentPathInput / "_".join(n).replace(
                "_coh", "_coherence.npz")
            freq, coh = data
            if np.all(np.isnan(coh)):
                error_num = 1
            else:
                np.savez_compressed(out,
                                    channelA=header['channelA'],
                                    channelB=header['channelB'],
                                    segtype=header['segtype'],
                                    epoch=header['epoch'],
                                    duration=header['duration'],
                                    gpsstart=header['gpsstart'],
                                    gpsend=header['gpsend'],
                                    fmin=header['fmin'],
                                    fmax=header['fmax'],
                                    Tsft=header['Tsft'],
                                    f=freq,
                                    coh=coh,
                                    dtype=dtype,
                                    )
            del freq, coh
        elif 'speclong' in temp_s:
            out = parentPathInput / "".join(["_".join(n), "_speclong.npz"])
            freq, psd, amppsd, psdwt, amppsdwt, persist = data
            if np.all(psd == 0):
                error_num = 1
            else:
                np.savez_compressed(out,
                                    channel=header['channel'],
                                    segtype=header['segtype'],
                                    epoch=header['epoch'],
                                    duration=header['duration'],
                                    gpsstart=header['gpsstart'],
                                    gpsend=header['gpsend'],
                                    fmin=header['fmin'],
                                    fmax=header['fmax'],
                                    Tsft=header['Tsft'],
                                    f=freq,
                                    psd=psd,
                                    amppsd=amppsd,
                                    psdwt=psdwt,
                                    amppsdwt=amppsdwt,
                                    persist=persist,
                                    dtype=dtype,
                                    )
            del freq, psd, amppsd, psdwt, amppsdwt, persist
        else:
            raise ValueError('Unable to determine data format type')

    return error_num


def delete_ascii(parentPathInput, spects):
    """
    Delete Fscan txt files

    Parameters
    ----------
    parentPathInput : Path, str
        Full path to files
    spects : str
        glob-style string for txt files to delete

    Raises
    ------
    FileNotFoundError
        If no files are found with the specified pattern
    """
    files = sorted(Path(parentPathInput).glob(spects))

    if len(files) == 0:
        raise FileNotFoundError(f"No files found with pattern {spects}")

    for f in files:
        assert f.suffix == '.txt'

        f.unlink()


def save_compiled_linecount_history(data_dict, outfile):
    """
    Save compiled line count history file

    Parameters
    ----------
    data_dict : dict
    outfile : Path, str
    """
    np.savez_compressed(outfile, **data_dict)


def load_compiled_linecount_history(infile):
    """
    Load compiled line count history file

    Parameters
    ----------
    infile : Path, str

    Returns
    -------
    data_dict : dict
    """
    data_dict = np.load(infile, allow_pickle=True)

    return data_dict

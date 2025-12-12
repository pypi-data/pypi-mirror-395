# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Taylor Starkman (2024)
#               Ansel Neunzert (2024)
#               Evan Goetz (2025)
#
# This file is part of fscan

import argparse
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
from pathlib import Path
import re

from ..process.history import compile_linecount_history
from ..utils import dtutils as dtl

mpl.use("Agg")


def linecount_plots(segtypePath, channel, outfile_heatmap, outfile_countplot,
                    f_bins=None, numSFTsCutoff=6, dataPtsInHistory=30,
                    autolinesType='complete', **kwargs):
    """
    This function generates two plots: a heatmap plot of the line density per
    Hz per root (number of SFTs), and a simple count of the lines over time.
    It pulls from the Fscan auto-generated lines files.

    Parameters
    ----------
    segtypePath : Path
    channel : str
    outfile_heatmap : Path
    outfile_countplot : Path
    f_bins : list of str
        strings like 0-100Hz, etc.
    numSFTsCutoff : int (default=6)
    dataPtsInHistory : int (default=30)
    autolinesType : str (default='complete')
    **kwargs
        Values to pass to fscan.process.history.compile_linecount_history()
    """

    # A default set of bands
    if f_bins is None:
        f_bins = [
            '0-200Hz', '200-400Hz', '(Violin Mode) 400-600Hz',
            '600-900Hz', '(Violin Mode) 900-1100Hz',
            '1100-1400Hz', '(Violin Mode) 1400-1600Hz',
            '1600-1800Hz', '1800-2000Hz',
        ]

    data_dict = compile_linecount_history(segtypePath, channel, autolinesType,
                                          **kwargs)

    # Get the minimum and maximum frequency for each entry in f_bins
    # This is a list of tuples (fmin, fmax) for each band
    bands = []
    for band in f_bins:
        match = re.search(r'(\d+)-(\d+)Hz', band)
        if match:
            bands.append((float(match.group(1)), float(match.group(2))))
    # determine the frequency bandwidth of each entry in f_bins
    bin_widths = np.array([band[1]-band[0] for band in bands])

    # Define array to be filled with the number of lines per square root num
    # sfts per frequency bin values
    heatmap_values = np.zeros((len(f_bins), len(data_dict['dates'])))
    count_values = np.zeros(len(data_dict['dates']))
    sufficient = np.full(len(data_dict['dates']), False)

    for dateidx, date in enumerate(data_dict['dates']):
        if (n_sfts := data_dict[f'numsfts_{date}'][0]) > numSFTsCutoff:
            sufficient[dateidx] = True
            lines = data_dict[f'lines_{date}']
            num_lines_per_freq_band = np.array(
                [len(lines[(lines >= band[0]) & (lines < band[1])])
                 for band in bands])
            heatmap_values[:, dateidx] = np.array(
                num_lines_per_freq_band / np.sqrt(n_sfts) / bin_widths)
            count_values[dateidx] = len(lines)
        else:
            print(f'WARNING: insufficient data (lines file or SFTs for {date}')
            continue

    # Create "history" arrays that don't include the most recent epoch
    # (to establish threshold values)
    sufficient_history = sufficient[:-1]
    count_history = count_values[:-1][sufficient_history]
    count_history = count_history[-1*dataPtsInHistory:]
    # Avoiding numpy warnings, just be clear that we need at least 2
    # values to determine mean and std deviation
    if len(count_history) > 1:
        count_mean = np.mean(count_history)
        count_std = np.std(count_history)
    else:
        count_mean = np.nan
        count_std = np.nan

    # Define array to create an alert tag on a frequency bin if value is above
    # threshold
    alerts = np.zeros(len(heatmap_values[:, -1])).astype(str)

    # Loop through all frequency bins and determine if the most recent date is
    # above the threshold defined as mean + 2 * standard deviation
    for i in range(len(alerts)):
        heatmap_history = heatmap_values[i, :-1][sufficient_history]
        heatmap_history = heatmap_history[-1*dataPtsInHistory:]
        # Avoiding numpy warnings, just be clear that we need at least 2
        # values to determine mean and std deviation
        if len(heatmap_history) > 1:
            mean = np.mean(heatmap_history)
            std = np.std(heatmap_history)
        else:
            mean = np.nan
            std = np.nan
        thresh = mean + std * 2

        if heatmap_values[i, -1] >= thresh:
            alerts[i] = 'ALERT'

    # Define location of frequency bin ticks and use tick locations to produce
    # an array containing only the values necessary to place ticks on bins
    # where the value is above the threshold
    y_tick_locations = np.arange(0, len(f_bins), 1)

    if sufficient[-1]:
        alert_loc = y_tick_locations[alerts != '0.0']
        alerts = alerts[alerts != '0.0']
    else:
        alerts = np.array(['INSUFFICIENT DATA'])
        if len(f_bins) % 2 == 1:
            alert_loc = np.array([np.ceil(len(f_bins)/2)])
        else:
            alert_loc = np.array([len(f_bins)/2])
    y_tick_locations = np.arange(0, len(f_bins), 1)

    # Create datetime objects with the start and end dates
    startDate = dtl.datestr_to_datetime(data_dict['dates'][0])
    endDate = dtl.datestr_to_datetime(data_dict['dates'][-1])

    # Calculate the length of the analysis in seconds, then determine how often
    # to include date labels on the x-axis to avoid overcrowding and create the
    # necessary 'days' object to input into matplotlib later
    sduration = (endDate - startDate).total_seconds()
    if sduration <= 3.5*7*24*60*60:  # 3.5 weeks
        days = mdates.DayLocator(interval=1)
    elif sduration <= 16*7*24*60*60:  # 16 weeks
        days = mdates.DayLocator(interval=7)
    else:  # anything longer than 16 weeks
        days = mdates.DayLocator(interval=30)

    # Determine if a cutoff is necessary due to saturation. If a day in the
    # analysis is saturated, then the max value displayed on the colorbar
    # will be 3 * median of all values.
    # If no days are saturated, then the max value for the colorbar will
    # be the max value present in the heatmap
    total_mean = np.mean(heatmap_values)
    median = np.median(heatmap_values)

    # Handle case where there's no data at all above zero in the heatmap
    if np.all(heatmap_values <= 0):
        cutofflow = 1
        cutoffhigh = 2

    # Handle normal cases where there's data
    else:
        cutofflow = np.min(heatmap_values[heatmap_values > 0])
        if np.absolute(total_mean - median) > 10:
            cutoffhigh = 3 * median
        else:
            cutoffhigh = np.max(heatmap_values)

    # Convert date strings from entire analysis duration to datetime objects
    # for effective plotting
    dates_as_datetime = np.array(
        [dtl.datestr_to_datetime(x) for x in data_dict['dates']])

    plt.clf()
    cmap = plt.cm.viridis.copy()
    norm = mpl.colors.Normalize(vmin=cutofflow, vmax=cutoffhigh)

    # Create figure to make heatmap within
    fig, ax1 = plt.subplots()
    fig.subplots_adjust(wspace=1)

    # Set up axes and labels for the heatmap
    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    ax1.xaxis.set_tick_params(rotation=-90, size=8)
    ax1.set_xlabel("Date")
    ax1.set_yticks(y_tick_locations,
                   labels=f_bins,
                   fontsize=8)
    ax1.set_title("Line density per Hz per sqrt(# of SFTs)")

    # Define the heatmap
    im1 = ax1.pcolormesh(dates_as_datetime, f_bins, heatmap_values,
                         norm=norm,
                         cmap=cmap)
    # Tell matplotlib that if the value is below the minimum heatmap value, it
    # should be gray (this grays out any days where data is not present)
    im1.cmap.set_under('#C0C0C0')

    # If any days are saturated, colorbar will have an upward pointing arrow
    # If no days are saturated, there will be no arrow on the colorbar
    if cutoffhigh == np.max(heatmap_values):
        cbar_extend = 'min'
    else:
        cbar_extend = 'both'
    cbar = fig.colorbar(im1,
                        ax=ax1,
                        extend=cbar_extend,
                        location='bottom',
                        pad=0.3,
                        )

    num_ticks = 8  # number of ticks on colorbar

    # Define the values to be shown on the colorbar, create the arrays
    # needed to label the colorbar, and set the tick locations/labels
    numerical_cbar_labels = np.linspace(cutofflow, cutoffhigh, num_ticks - 1)
    numerical_cbar_labels = np.trunc(numerical_cbar_labels * 100)/100
    cbar_labels = np.concatenate((['Insufficient\ndata'],
                                  numerical_cbar_labels))
    cbar.ax.set_xticks(ticks=np.linspace(cutofflow, cutoffhigh, num_ticks),
                       labels=cbar_labels,
                       )
    cbar.ax.set_ylabel(r"$\frac{N_{\mathrm{lines}}}"
                       r"{\sqrt{N_{\mathrm{SFTs}}} \cdot \mathrm{Hz}}$",
                       rotation=0,
                       size=15,
                       )
    cbar.ax.yaxis.set_label_position("left")
    cbar.ax.yaxis.set_label_coords(-0.2, -0.1)

    # Define second axis to display alert labels
    ax2 = ax1.twinx()

    # Set up second axis and plot alerts
    if sufficient[-1]:
        color = 'red'
        size = 8
        offset = 0.4
    else:
        color = 'orange'
        size = 12
        offset = 0.8

    ax2.set_yticks(alert_loc + offset, labels=alerts, color=color, size=size)
    ax2.tick_params(right=False,
                    rotation=-90,
                    pad=0.01
                    )
    ax2.pcolormesh(dates_as_datetime, f_bins, heatmap_values,
                   norm=norm,
                   cmap=cmap)

    # Save the heatmap figure and make it look nice
    plt.tight_layout()
    plt.savefig(outfile_heatmap,
                dpi=250)

    # =========================
    # Line count over time plot
    # =========================

    # Set up a new figure to plot the total line count over time
    plt.figure()

    # Plot the total line counts for dates where sufficient data exists
    plt.scatter(dates_as_datetime[sufficient], count_values[sufficient],
                color="deepskyblue",
                )

    # Either mark the latest epoch's data point, or make a note on
    # the title indicating why no data point is marked
    if sufficient[-1]:
        plt.scatter(dates_as_datetime[-1], count_values[-1],
                    color="deepskyblue",
                    linewidth=2,
                    edgecolor='black',
                    label="This epoch",
                    zorder=2,
                    )
        plt.title("Line count over time")
    else:
        plt.title("Line count over time\n (insufficient data for this epoch)")

    # Determine which data points count as part of the history
    # and make a vertical line to mark that span
    dates_history = dates_as_datetime[:-1][
        sufficient_history][-1*dataPtsInHistory:]
    half_epoch = (endDate-startDate)/len(data_dict['dates'])/2.
    if len(dates_history) > 0:
        plt.axvspan(dates_history[0]-half_epoch, endDate+half_epoch,
                    color='orange', alpha=0.3,
                    label="Data used in\nthreshold calculation",
                    zorder=0)

    # Set up the horizontal lines to plot, as well as colors and line styles
    hvals = [
            count_mean+2*count_std,
            count_mean+count_std,
            count_mean,
            count_mean-count_std]
    hlabs = [
            "alert threshold\n(mean + 2*stddev)",
            "mean + stddev", "mean", "mean - stddev"]
    cols = ['red', 'orange', 'lightblue', 'lightgreen']
    lws = [3, 1, 1, 1]
    lss = ['solid', 'dotted', 'dotted', 'dotted']

    # Plot the horizontal lines
    for hval, hlab, col, lw, ls in zip(hvals, hlabs, cols, lws, lss):
        plt.axhline(hval, label=hlab,
                    zorder=1,
                    color=col,
                    linewidth=lw,
                    linestyle=ls)

    # Make a legend and plot title
    plt.legend(loc='lower left', bbox_to_anchor=(0, 0))
    plt.grid(visible=False)

    # Force the plot to display the full requested time period
    plt.xlim(startDate, endDate+half_epoch)

    # Format the date axis
    ax_tot = plt.gca()
    ax_tot.xaxis.set_major_locator(days)
    ax_tot.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    ax_tot.xaxis.set_tick_params(rotation=-90, size=8)
    ax_tot.set_xlabel("Date")
    ax_tot.set_ylabel("Number of lines counted")

    # Save the figure
    plt.tight_layout()
    plt.savefig(outfile_countplot,
                dpi=250)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--segtypePath", type=Path, required=True,
                        help='Path to data used to create heatmap')
    parser.add_argument("--channel", type=str, required=True,
                        help="Channel of data to create heatmap of, e.g., "
                             "H1:GDS-CALIB_STRAIN_CLEAN")
    parser.add_argument("--outfile-heatmap", type=Path, required=True,
                        help="Path to heatmap output image (.png)")
    parser.add_argument("--outfile-countplot", type=Path, required=True,
                        help="Path to line count vs time output image (.png)")
    parser.add_argument("--fBins", type=str, nargs='*',
                        default=None,
                        help="Frequency bands for dividing up the full "
                             "band to count line artifacts '<fmin>-<fmax>Hz' "
                             "in ascending order")
    parser.add_argument("--numSFTsCutoff", type=int, default=6,
                        help="Number of SFTs required for a day to be "
                             "considered to have sufficient data for analysis")
    parser.add_argument("--dataPtsInHistory", type=int, default=30,
                        help="Epochs to count as part of in recent history")
    parser.add_argument("--autolinesType", type=str, default="complete",
                        choices=['complete', 'annotated'],
                        help="Choose 'complete' for all lines found by line "
                             "count. Choose 'annotated' to only plot lines "
                             "identified as belonging to combs")
    parser = dtl.add_dtlargs(parser)
    args = parser.parse_args()

    if args.fBins is None:
        args.fBins = [
            '0-200Hz', '200-400Hz', '(Violin Mode) 400-600Hz',
            '600-900Hz', '(Violin Mode) 900-1100Hz',
            '1100-1400Hz', '(Violin Mode) 1400-1600Hz',
            '1600-1800Hz', '1800-2000Hz',
        ]

    linecount_plots(args.segtypePath,
                    args.channel,
                    args.outfile_heatmap,
                    args.outfile_countplot,
                    f_bins=args.fBins,
                    numSFTsCutoff=args.numSFTsCutoff,
                    dataPtsInHistory=args.dataPtsInHistory,
                    autolinesType=args.autolinesType,
                    analysisStart=args.analysisStart,
                    analysisEnd=args.analysisEnd,
                    analysisDuration=args.analysisDuration,
                    averageDuration=args.averageDuration,
                    snapToLast=args.snapToLast,
                    greedy=args.greedy,
                    )


if __name__ == "__main__":
    main()

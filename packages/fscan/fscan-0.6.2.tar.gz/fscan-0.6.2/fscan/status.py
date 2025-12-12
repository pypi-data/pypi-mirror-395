# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Sudhagar Suyamprakasam (2023)
#               Ansel Neunzert (2023)
#               Evan Goetz (2023)
#
# This file is part of fscan

import argparse
import os
from glob import glob
import json
import numpy as np
from .utils import dtutils as dtl
from .plot.static import expected_pngs
from argparse import RawTextHelpFormatter
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.dates as mdates
from .utils.utils import (str_to_bool, sft_vals_from_makesft_dag_vars,
                          sft_name_from_vars)
mpl.use("Agg")


def dag_status_check(path):
    """
    Parameters
    ---------
    path : str
        file path that terminates in a channel name (old style)
        or epoch (new style)

    Returns
    -------
    status : str
        one of "Success", "Failure", "Running",
        "Unsubmitted" or "Nonexistent", indicating
        the status of SUPERDAG processing in the
        given folder.
    """

    # parse the filepath
    mdata = dtl.parse_filepath(path)
    # if the super dag exists
    if mdata['superdag-exists']:
        # if the superdag outfile exists...
        if mdata['superdagout-exists']:
            with open(mdata['superdagout-path'], 'r') as f:
                lines = f.readlines()
            # if the dag exited...
            if "EXITING WITH STATUS" in lines[-1]:
                # if the dag exited successfully...
                if lines[-1].strip().endswith("0"):
                    return "Success"
                else:  # if the dag exited, but not successfully
                    return "Failure"
            else:  # if the dag did not exit
                return "Running"
        else:  # if the superdag outfile doesn't exist
            return "Unsubmitted"
    else:  # if superdag doesn't exist
        return "Nonexistent"


def diagnose_dag(path, detailSuccessful=False):
    """
    Parameters
    ---------
    path : str
        file path that terminates in an epoch (new scheme) or channel name
        (old scheme)
    detailSuccessful : bool
        if true, will also print out a detailed report
        on finished / running jobs for successful dags

    Returns
    ------
    dagStat : str
        "Success", "Failure", etc
        see dag_status_check() for details
    out : str
        a multi-line string containing information
        about the dag's completion status. If detailed
        information about different job types is
        returned, this will be formatted like a table.
    sftsToGenerate : int
        count of MakeSFT jobs which are not commented
        out in the dag
    sftsToLink : int
        count of MakeSFT jobs which are commented out
        in the dag (because they were found elsewhere
        and should be linked for reuse)
    sftsFound : int
        actual number of SFTs in the `sfts/` subfolder
    sftLinksFound : int
        actual number of symlinks found in the
        `sfts` subfolder
    """

    # First, we'll grab the basic status of the dag
    dagStat = dag_status_check(path)

    out = ""
    out += f"\n\n{path}"
    out += f"\nDAG status is: {dagStat}"

    # If we don't have the appropriate output files,
    # Don't bother to get detailed info
    # Return meaningless negative values for SFT
    # counts.
    if dagStat == "Nonexistent":
        return dagStat, out, -1, -1, -1, -1

    # If the dag failed or is running, we might
    # want to know how far through the workflow it
    # managed to get. So we'll set the printDetails
    # option to True
    if (dagStat in ['Failure', 'Running'] or
            (dagStat == "Success" and detailSuccessful)):
        printDetails = True
    else:
        printDetails = False

    # let's re-parse the file path and grab
    # all the metadata
    mdata = dtl.parse_filepath(path)

    # then we load all the lines of the dag
    # and its output file (if it exists)
    with open(mdata['superdag-path'], 'r') as f:
        dag = f.readlines()
    if mdata['superdagout-exists']:
        with open(mdata['superdagout-path'], 'r') as f:
            dagout = f.readlines()
    # note: if the superdagout does not exist, we will still
    # iterate through the dag, but all jobs will be assigned
    # 'notSubmitted' status

    # if there's another dag spliced in to SUPERDAG
    # (and there often will be)
    # we should get that content and append
    # it to the dag content
    splicedag = []
    for line in dag:
        if 'SPLICE' in line:
            tag = line.split()[1]
            if line.split()[-1] == 'tmpSFTDAGtmp.dag':
                with open(os.path.join(path, 'tmpSFTDAGtmp.dag'), 'r') as f:
                    sftdaglines = f.readlines()
            else:
                with open(line.split()[-1], 'r') as f:
                    sftdaglines = f.readlines()
            for sftdagline in sftdaglines:
                splicedag.append(f'{sftdagline.strip()} SPLICETAG={tag}\n')
    dag = splicedag + dag

    # Next, let's get a list of all the jobs
    # in the dag file
    # (We'll also list any jobs that were commented
    # out by the SFT reuse code)
    jobs = []
    comment_jobs = []
    for line in dag:
        line.strip()
        if line.startswith("JOB") or line.startswith("# JOB"):
            if 'SPLICETAG' in line:
                tag = f"{line.split('=')[-1].strip()}+"
            else:
                tag = ""
            if line.startswith("JOB"):
                jobs += [f"{tag}{line.split()[1]}"]
            else:
                comment_jobs += [f"{tag}{line.split()[2]}"]

    # Next, let's determine the most recent status of
    # each job. We'll iterate backward through the dag
    # output.
    statuses = []
    for job in jobs:
        status = "notSubmitted"
        if mdata['superdagout-exists']:
            for line in dagout[::-1]:
                if (f" {job} " in line):
                    if "Submitting HTCondor Node " in line:
                        status = "submitted"
                    if " failed " in line:
                        status = "failed"
                        break
                    if "completed successfully" in line:
                        status = "succeeded"
                        break
        statuses += [status]

    # Append the information for any commented-out jobs
    # Their status is just "commented" because they are
    # not actually run in the dag workflow
    for comment_job in comment_jobs:
        jobs += [comment_job.strip("# ")]
        statuses += ["commented"]

    # Things will get verbose if we print info for *all* the
    # jobs of a given type, so let's group them up and print
    # just one line of info for each type.

    # Keep everything before the last underscore as a job type.
    # For example "SomeType_ofjob_12" becomes "SomeType_ofjob"
    all_jtypes = ['_'.join(j.split('_')[:-1]) if '_' in j else j for j in jobs]
    # Keep just the unique job types
    jtypes = list(set(all_jtypes))
    # order them by their appearance in the dag
    jtypes.sort(key=lambda x: all_jtypes.index(x))

    # For each of our job types, we want to count the total number
    # of individual jobs at different statuses.
    # Set up a dictionary to hold this info.
    sdict = {
        'succeeded': [],
        'failed': [],
        'submitted': [],
        'unsubmitted': [],
        'total': [],
    }

    # convert stuff to np arrays for easier indexing
    jobs = np.array(jobs)
    all_jtypes = np.array(all_jtypes)
    statuses = np.array(statuses)

    # Iterate over job types, and count up how many are
    # in each state
    for jtype in jtypes:
        sdict['total'] += [len(np.where(all_jtypes == jtype)[0])]
        sdict['submitted'] += [len(np.where(
            (all_jtypes == jtype) &
            (statuses == 'submitted')
            )[0])]
        sdict['unsubmitted'] += [len(np.where(
            (all_jtypes == jtype) &
            (statuses == 'notSubmitted')
            )[0])]
        sdict['succeeded'] += [len(np.where(
            (all_jtypes == jtype) &
            (statuses == 'succeeded')
            )[0])]
        sdict['failed'] += [len(np.where(
            (all_jtypes == jtype) &
            (statuses == 'failed')
            )[0])]

    # (Most of this block is just for pretty printed output)
    # define a visual spacer for the table
    spacer = " | "
    # determine table column width
    nchars = max([len(jtype) for jtype in jtypes])
    nchars = max(nchars, max([len(k) for k in sdict.keys()]))
    nchars += 1

    # If we're including detailed info...
    if printDetails:
        # print a header line
        pline = []
        for k in sdict.keys():
            pline += [f"{k:<{nchars}s}"]
        out += f"\n{'':<{nchars+len(spacer)}s}"+spacer.join(pline)

        # iterate over job types
        for i, jtype in enumerate(jtypes):
            # print the results line for that job type
            pline = [f"{jtype:<{nchars}s}"]
            for k in sdict.keys():
                pline += [f"{sdict[k][i]:<{nchars}d}"]
            out += f"\n{spacer.join(pline)}"

    # Great, we're done with the job status table now

    # Next, let's tally SFTs
    sftsToGenerate = 0
    sftsToLink = 0
    sftsFound = 0
    sftLinksFound = 0
    pngs_expected = 0
    pngs_found = 0
    for line in dag:
        if 'VARS MakeSFTs' in line:
            pars = sft_vals_from_makesft_dag_vars(line)

            if line.startswith('#'):
                sftsToLink += len(pars[7])
            else:
                sftsToGenerate += len(pars[7])

            for idx, sftpath in enumerate(pars[7]):
                sftname = sft_name_from_vars(
                    pars[0], pars[1], pars[2], pars[3], pars[4], pars[5],
                    pars[6][idx])
                sft = os.path.join(sftpath, sftname)
                if os.path.islink(sft):
                    sftLinksFound += 1
                elif os.path.exists(sft):
                    sftsFound += 1

        elif 'VARS PostProcess' in line:
            ch_path = line.split('--parentPathInput ')[-1].split()[0]
            mdata = dtl.parse_filepath(ch_path)
            ptypes_base = ['timeaverage', 'spectrogram', 'persist']
            if ('coherence-ref-channel' in mdata and
                    mdata["coherence-ref-channel"] is not None):
                ptypes = ptypes_base + ['coherence']
            else:
                ptypes = ptypes_base

            for ptype in ptypes:
                # we call `expected_pngs` from makePlots here
                # to get a "checklist" of, well, expected pngs
                pngfnames, _, _ = expected_pngs(
                    ch_path, mdata['fmin'], mdata['fmax'],
                    mdata['plot-subband'],
                    mdata['gpsstart'], mdata['gpsend'],
                    mdata['Tsft'], ptype)
                pngs_expected += len(pngfnames)
                for pngfname in pngfnames:
                    if os.path.isfile(pngfname):
                        pngs_found += 1

    # If requested, we'll be printing a detailed report to
    # to the user. (We need to calculate the SFT stats above
    # because they will be returned regardless of the
    # printDetails option. They are used elsewhere.)
    if printDetails:
        out += "\n\nSFT report:"
        out += f"\nGenerated {sftsFound} of {sftsToGenerate} expected SFTs."
        out += f"\nLinked {sftLinksFound} of {sftsToLink} expected SFTs."
        out += (f"\n({sftLinksFound+sftsFound} of {sftsToGenerate+sftsToLink} "
                "SFTs accounted for.)")

        out += "\n\nPlotting report:"
        out += (f"\nGenerated {pngs_found} of {pngs_expected} expected")

    # Return key results
    return dagStat, out, sftsToGenerate, sftsToLink, sftsFound, sftLinksFound


def nagios_report(epoch_path, outputfilename):
    """ Write a nagios-readable JSON file for the dag status """

    status = dag_status_check(epoch_path)

    epoch = os.path.basename(epoch_path)
    segtype_duration_path = os.path.dirname(epoch_path)

    if status == 'Success':
        message = f'Fscan completed successfully for {epoch}'
        exitcode = 0
    elif status == 'Running':
        message = f"Fscan is still running for {epoch}"
        exitcode = 0
    elif status == 'Failure':
        message = f"Fscan failed for {epoch}"
        exitcode = 1
    else:
        message = ('Fscan either has not submitted the workflow or '
                   f'no dag file exists for {epoch}')
        exitcode = 2

    timeout = 43200  # 12 h
    timeoutmessage = ('Fscan nagios check has not run to completion in '
                      f'{timeout} s')

    nagios_message = {
        'created_gps': dtl.datetime_to_gps(dtl.datestr_to_datetime('now')),
        'status_intervals': [
            {'start_sec': 0,
             'txt_status': message,
             'num_status': exitcode},
            {'start_sec': timeout,
             'txt_status': timeoutmessage,
             'num_status': 2}]}

    outfolder = os.path.join(segtype_duration_path, "dag_status_reports")
    os.makedirs(outfolder, exist_ok=True)

    with open(os.path.join(outfolder, outputfilename), 'w') as f:
        json.dump(nagios_message, f, indent=4)


def summarize_span(args):
    """
    This function iterates over a series of epochs as specified
    by the user arguments. Within each epoch it looks for
    sub-folders to compile a list of channels.

    If args.save_output is True, the following information will
    be generated within a `dag_status_reports` folder just under
    the averaging duration level in the file tree
    (example: `day/dag_status_reports`):

    (1) A summary plot showing a color-coded matrix of epochs
        and channels with the dag status for each epoch+channel

    (2) For each channel, a plot showing the availability of
        SFTs and how that availability compares to the expected
        number of SFTs.

    (3) A text file with the results of `diagnose_dag()` for each
        channel+epoch.

    If args.save_output is false, no plots are generated and the
    text is printed rather than being saved.

    Parameters
    ----------
    args : namespace
        generated by argparse; see parser below for details
    """

    # first, we use the supplied arguments to generate a list of
    # epochs for analysis
    _, durationtags, epochtags = dtl.args_to_intervals(
        analysisStart=args.analysis_start,
        analysisEnd=args.analysis_end,
        analysisDuration=args.analysis_duration,
        averageDuration=args.average_duration,
        snapToLast=args.snapToLast,
        greedy=args.greedy,
    )

    # Set up the output folder if it doesn't already exist
    outfolder = os.path.join(args.segtype_path,
                             durationtags[0],
                             "dag_status_reports")
    os.makedirs(outfolder, exist_ok=True)

    # Set up a string to contain the text output
    summary_diagnosis = ""
    dags = {'Success': 0,
            'Failure': 0,
            'Running': 0,
            'Unsubmitted': 0,
            'Nonexistent': 0,
            }
    dag_stats = np.zeros(len(epochtags), dtype='<U20')
    sft_stats = np.zeros((len(epochtags), 4), dtype=int)

    # Loop over epochs running diagnose_dag() for each epoch
    for idx, (dur, epoch) in enumerate(zip(durationtags, epochtags)):
        epoch_path = os.path.join(args.segtype_path, dur, epoch)
        # This first case is the new style where all channels are run from one
        # SUPERDAG. Suceess or failure depends on the whole dag succeeding or
        # failing
        if os.path.exists(os.path.join(epoch_path, 'SUPERDAG.dag')):
            dd_out = diagnose_dag(epoch_path)
            dags[dd_out[0]] += 1
            dag_stats[idx] = dd_out[0]
            summary_diagnosis += dd_out[1]
            sft_stats[idx] = dd_out[2:]
        # This second case is the older style where each channel has a SUPERDAG
        # The output formatting is changed where we consider success or failure
        # not on a channel-by-channel basis but on a whole epoch basis
        else:
            # List of channels excluding any segments list
            channel_paths = [
                ch for ch in glob(os.path.join(epoch_path, '*'))
                if '.txt' not in ch]
            any_dag_failed = False
            dags_succeeded = 0
            any_dag_running = False
            any_unsubmitted = False
            any_nonexistent = False
            for ch_idx, ch_path in enumerate(channel_paths):
                dd_out = diagnose_dag(ch_path)
                if dd_out[0] == 'Failure':
                    any_dag_failed = True
                elif dd_out[0] == 'Success':
                    dags_succeeded += 1
                elif dd_out[0] == 'Running':
                    any_dag_running = True
                elif dd_out[0] == 'Unsubmitted':
                    any_unsubmitted = True
                elif dd_out[0] == 'Nonexistent':
                    any_nonexistent = True
                summary_diagnosis += dd_out[1]
                for n in range(len(dd_out[2:])):
                    sft_stats[idx, n] += dd_out[2 + n]

            if any_dag_failed:
                dags['Failure'] += 1
                dag_stats[idx] = 'Failure'
            elif dags_succeeded == len(channel_paths):
                dags['Success'] += 1
                dag_stats[idx] = 'Success'
            elif any_dag_running:
                dags['Running'] += 1
                dag_stats[idx] = 'Running'
            elif any_unsubmitted:
                dags['Unsubmitted'] += 1
                dag_stats[idx] = 'Unsubmitted'
            elif any_nonexistent:
                dags['Nonexistent'] += 1
                dag_stats[idx] = 'Nonexistent'
            else:
                raise Exception

    # If we are making plots, etc...
    if args.save_output:

        # convert epochs to an array, and make
        # a second array of epochs as datetime objects
        # (for later use)
        epochs = np.array(epochtags)
        epochs_dt = np.array(
            [dtl.datestr_to_datetime(e)
                for e in epochtags]
                )

        # --------------------
        # SFT history plotting
        # --------------------

        sftpltoutpath = os.path.join(outfolder, "sft_history.png")
        plt.clf()
        plt.gcf().set_size_inches(10, 10)

        # Determine which epochs for this channel have
        # existing dags / defined status, and which don't
        dagdef = np.where(sft_stats[:, 0] >= 0)[0]

        # Extract SFT stats for the epochs with existing dags
        toGen, toLink, didGen, didLink = np.transpose(
            sft_stats[:, :][dagdef])

        # Make bar plots for each epoch - existing dags only
        # (note that the first layer of the bar plot is saved in a variable
        # `bars`; this will later be used to keep track of the horizontal
        # bar positions and widths)
        bars = plt.bar(epochs_dt[dagdef],
                       didGen,
                       label="SFTs generated",
                       color='orange')
        plt.bar(epochs_dt[dagdef],
                (toGen - didGen),
                color='bisque',
                label="SFT generation shortfall",
                bottom=didGen)
        plt.bar(epochs_dt[dagdef],
                didLink,
                color='dodgerblue',
                label="SFTs linked",
                bottom=toGen)
        plt.bar(epochs_dt[dagdef],
                (toLink - didLink),
                color='lightskyblue',
                label="SFT linkage shortfall",
                bottom=(toGen + didLink))

        # Let's calculate the total number of SFTs
        # that could be generated in this time span.
        # First we'll need the file path so that the
        # correct metadata can be calculated.
        fpath = os.path.join(args.segtype_path,
                             durationtags[0],
                             epochs[dagdef][0])
        if os.path.exists(os.path.join(fpath, 'SUPERDAG.dag')):
            mdata = dtl.parse_filepath(fpath)
        else:
            mdata = dtl.parse_filepath(channel_paths[0])

        # Next, we actually calculate "n", the total number
        # of SFTs that would fit in this time span.
        sftstep = mdata['Tsft'] * (1.0 - mdata['sft-overlap'])
        totsec = mdata['gpsend'] - mdata['gpsstart']
        n = int(np.floor((totsec - mdata['Tsft']) / sftstep)) + 1
        n *= (len(mdata['multi-channel-list']) if 'multi-channel-list' in mdata
              else len(channel_paths))

        # Add a dotted line to indicate the maximum
        plt.axhline(n, color='black',
                    linestyle='dotted',
                    label='Maximum possible SFTs')

        # Finaly, it's time to clean up the plot a bit
        # Add titles and neatly format the horizontal date axis
        ax = plt.gca()
        plt.title("SFT availability")
        plt.xlabel("Date")
        plt.ylabel("Number of SFTs")
        days = mdates.DayLocator(interval=1)
        ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_ylim(0, n*1.05)  # Set the y limit just above the max number

        # The following section adds little "caps" to the bar chart
        # indicating the expected number of generated and total SFTs.
        # There's not really new info here, it's just for readability.

        # Grab the existing bar data. For each bar, generate a 2x2 numpy
        # array holding the start and end points for the line which will
        # "cap" it. Keep these arrays in a list called genCapData.
        # (That is, data for the 'generated SFTs' bar caps)
        p = bars.patches
        genCapData = []

        for i in range(len(p)):
            linedata = np.zeros((2, 2))
            linedata[0, 0] = p[i].xy[0]  # left x coord
            linedata[1, 0] = p[i].xy[0] + p[i].get_width()  # right x
            linedata[0, 1] = toGen[i]  # left y
            linedata[1, 1] = toGen[i]  # right y
            genCapData += [linedata]

        # The 'total SFTs' bar caps will be identical in horizontal
        # position, just shifted upwards
        totCapData = [np.copy(x) for x in genCapData]
        for i in range(len(totCapData)):
            totCapData[i][0, 1] += toLink[i]
            totCapData[i][1, 1] += toLink[i]

        # Now we turn our curated "bar cap" data into actual line
        # collections and plot them
        ax.add_collection(
            LineCollection(
                totCapData,
                color='darkblue',
                linewidth=2,
                zorder=3,
                label="Expected total SFTs"))

        ax.add_collection(
            LineCollection(
                genCapData,
                color='deeppink',
                linewidth=2,
                zorder=2,
                label="Expected generated SFTs"))

        # Finally, we clean up the x-axis ticks, create
        # the legend, and save.
        plt.xticks(rotation=90, fontsize=8)
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.savefig(sftpltoutpath,
                    bbox_inches='tight')
        print(f"Output written to {sftpltoutpath}")

        # --------------------
        # Text file generation
        # --------------------

        # Create the output path
        textoutpath = os.path.join(
                    outfolder,
                    "status_summary.txt")

        # Write out the arguments that were used to run this analysis
        with open(textoutpath, 'w') as f:
            f.write("Arguments supplied to analysis summary:")
            f.write(' '.join(f'{k} {v}' for k, v in vars(args).items()))
            f.write("\n\n")
            for idx, (dur, epoch) in enumerate(zip(durationtags, epochtags)):
                f.write(f"{epoch}: {dag_stats[idx]}\n")
            # Write the actual information about the dag status for all
            # the queried epochs (this was generated much earlier)
            f.write(summary_diagnosis)
        # Tell the user where we put the info
        print(f"Output written to {textoutpath}")

    # If we're not saving output, just print instead
    else:
        for idx, (dur, epoch) in enumerate(zip(durationtags, epochtags)):
            print(f"{epoch}: {dag_stats[idx]}")
        print("")
        print(summary_diagnosis)


def main():

    # ----------------
    # Input arguments
    # ----------------

    # set up parser
    parser = argparse.ArgumentParser(
        description="""Please run

        $python3 AnalysisSummary.py dagstat --help

        or

        $python3 AnalysisSummary.py summarize --help

        to see all help options for the different modes.""",
        formatter_class=RawTextHelpFormatter)

    # Define three subparser for the different  modes
    sp = parser.add_subparsers(dest='command')

    g0 = sp.add_parser("dagstat", description="""
                            Query the status
                            of a particular dag
                            """)

    g1 = sp.add_parser("summarize",
                       description="Arguments for batch analysis")

    g2 = sp.add_parser("monitor",
                       description="Monitor a dag for nagios")

    # Add common argument (input directory) for dagstat
    g0.add_argument("--dag-dir", type=str, default=None,
                    required=True,
                    help="Path to directory containing SUPERDAG.dag")

    # Add arguments specific to the batch/summarize mode
    g1.register('type', 'bool', str_to_bool)
    g1.add_argument("--segtype-path",
                    required=True,
                    help="Path to a directory where the last level specifies "
                         "segment type")
    g1.add_argument("--save-output",
                    default=False,
                    type='bool',
                    help="Default false. If true, will save output text files "
                         "and images instead of printing info.")

    # For the batch mode, also add all dateTimeLogic arguments
    g1 = dtl.add_dtlargs(g1)

    g2.add_argument("--dag-dir", type=str, default=None,
                    required=True,
                    help="Path to directory containing SUPERDAG.dag")
    g2.add_argument("--nagios-output",
                    type=os.path.normpath,
                    default='nagios.json',
                    help='Path for nagios json output')

    # parse arguments
    args = parser.parse_args()

    # Now for the main flow of the script...
    # This reports detailed info on the status of a single SUPERDAG
    if args.command == "dagstat":
        _, diagnosis, _, _, _, _ = diagnose_dag(
            args.dag_dir, detailSuccessful=True)
        print(diagnosis)

    # This summarizes a span of times and channels according to the
    # user arguments, generating plots and/or text output
    elif args.command == "summarize":
        summarize_span(args)

    elif args.command == 'monitor':
        nagios_report(args.dag_dir, args.nagios_output)


if __name__ == "__main__":
    main()

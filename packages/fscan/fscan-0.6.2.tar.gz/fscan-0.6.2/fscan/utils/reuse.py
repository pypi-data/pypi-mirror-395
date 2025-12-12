# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2023, 2025)
#
# This file is part of fscan

import os
from pathlib import Path
import re
from .dtutils import find_specific_SFT
from .utils import (sft_vals_from_makesft_dag_vars,
                    sft_name_from_vars)


def use_existing_sfts(epseg_info, channels):
    """
    Find existing SFT files for given channels and comment out jobs in
    DAG files as needed.

    This function creates symbolic links to SFTs found elsewhere.

    Note: this function has been updated to work with the latest
    lalpulsar_MakeSFTDAG.py output DAG where datafind happens at runtime
    and then the DAG only creates SFTs and moves them to the requested
    locations. To use with older versions of lalpulsar_MakeSFTDAG.py output,
    an older version of this function must be used

    Parameters
    ----------
    epseg_info : dict
    channels : list
    """

    for idx, (frametype, chans) in enumerate(channels.items()):
        sft_dag_file = os.path.join(
            epseg_info['epoch_path'], f'{frametype}_SFT_GEN', "makesfts.dag")

        # If the dag file doesn't exist, then skip
        if not os.path.exists(sft_dag_file):
            continue

        replacejobs = {}  # dict of dicts
        channel_path_resolve = {}  # channel: path to channel
        # open the SFT dag and read the contents
        with open(sft_dag_file, 'r') as sftdag:
            lines = sftdag.readlines()
        # Here we loop over the lines in the DAG file which is equivalent to
        # looping over SFT start times
        for line in lines:
            if "VARS MakeSFTs" in line:
                # Extract the start and end times and Tsft for each SFT from
                # the dag file (note that SFTGPSstart is the start of a
                # *specific* SFT, but epseg_info['SFTGPSstart'] is the start of
                # the *first* SFT in the epoch. Confusing notation, sorry.)
                pars = sft_vals_from_makesft_dag_vars(line)

                # Loop over the channels and mark whether the SFT was found or
                # not with the found filepath
                found_sft_files = {}
                for ch_tup in chans:
                    # create filename
                    sftname = sft_name_from_vars(
                        pars[0], pars[1], pars[2], pars[3], pars[4], pars[5],
                        ch_tup[1])
                    # find the matching SFT path if one exists
                    found_sft_path = find_specific_SFT(
                        sftname, epseg_info['segtype_path'], ch_tup[1],
                        exclude=[epseg_info['duration_tag']],
                        mode=None
                    )  # we might want to change the mode later
                    # If there was no path found, insert into the dict False
                    # otherwise a path was found so mark as True
                    if found_sft_path == '':
                        found_sft_files[ch_tup[1]] = None
                    else:
                        found_sft_files[ch_tup[1]] = found_sft_path
                # After looping through all of the channels, if all of the
                # dict entries were True, then give an "all-exist" key as True
                # and an empty list of the unfinished-channels. If not all of
                # the SFTs were found, then make a list of the keys whose
                # values are False, and set "all-exist" to False.
                if all(found_sft_files.values()):
                    found_sft_files['all-exist'] = True
                else:
                    found_sft_files['all-exist'] = False
                # record the job number of the line; we will comment it out
                jobnum = line.split(" MakeSFTs_")[1].split(" ")[0]
                # For the replacejobs dict, insert an entry for the job name
                # with the found_sft_files dict
                replacejobs[f"MakeSFTs_{jobnum}"] = found_sft_files

            elif "VARS MoveSFTs" in line:
                # For the MoveSFTs job arguments, we need to map the channels
                # to output paths so we make a dict to do this
                matching = re.search(r'channels="([^"]+)"', line)
                moving_channels = matching.group(1).split() if matching else []
                matching = re.search(r'destdirectory="([^"]+)"', line)
                moving_destdirs = matching.group(1).split() if matching else []
                for ch, path in zip(moving_channels, moving_destdirs):
                    channel_path_resolve[ch] = path

        if len(channel_path_resolve) == 0:
            raise RuntimeError(f"No MoveSFTs job found in {sft_dag_file}")

        # A boolean value if all SFTs for all channels were found
        found_all_sfts = all(
            all(found.values()) for found in replacejobs.values()
        )

        # make the symlinks
        for jobname, jobinfo in replacejobs.items():
            if jobinfo['all-exist']:
                for ch, sftpath in jobinfo.items():
                    if ch != "all-exist" and sftpath is not None:
                        sftpath = Path(sftpath)
                        symlinkpath = (Path(channel_path_resolve[ch]) /
                                       sftpath.name)
                        if (not symlinkpath.exists() and
                                not symlinkpath.is_symlink()):
                            os.symlink(sftpath, symlinkpath)

        # we are going to overwrite the SFT dag content; initialize it
        newsftdag_content = ""
        # this variable will track whether there are any SFT jobs that will
        # need to remain in the dag (SFTs that don't already exist elsewhere)
        remaining_sftjobs = False
        # Iterate through the SFT dag again, commenting out all parts of
        # the jobs we don't need (SFT creation).
        # Remove parents from MoveSFTs.
        for line in lines:
            if " MakeSFTs_" in line and "MoveSFTs" not in line:
                jobnum = line.split(" MakeSFTs_")[1].split(" ")[0]
                if replacejobs[f"MakeSFTs_{jobnum}"]["all-exist"]:
                    newsftdag_content += f"# {line}"
                else:
                    newsftdag_content += line
                    if not remaining_sftjobs:
                        remaining_sftjobs = True
            elif "MoveSFTs" in line and found_all_sfts:
                newsftdag_content += f"# {line}"
            elif "MoveSFTs" in line and not found_all_sfts:
                if "JOB" in line or "RETRY" in line or "VARS" in line:
                    newsftdag_content += line
                elif "PARENT" in line and "CHILD" in line:
                    parents = ' '.join(
                        [jobname for jobname, jobinfo in replacejobs.items()
                         if not jobinfo['all-exist']
                         ]
                    )
                    newsftdag_content += f"PARENT {parents} CHILD MoveSFTs\n"

        # Write the new content
        with open(sft_dag_file, 'w') as sftdag:
            sftdag.write(newsftdag_content)

        # If nothing remains uncommented in the SFT dag file, we will need to
        # comment out the "spliceSFTDAG" lines from the SUPERDAG.
        # Note that this does not only appear on the first line, but also in a
        # parent/child relationship later.
        if not remaining_sftjobs:
            print("All SFTS were found in other directories")
            superdagfile = os.path.join(
                epseg_info['epoch_path'], "SUPERDAG.dag")
            newsuperdag_content = ""
            with open(superdagfile, 'r') as superdag:
                superlines = superdag.readlines()
            for line in superlines:
                if f"{frametype}_SFTs" not in line:
                    newsuperdag_content += line
                else:
                    newsuperdag_content += f"# {line}"
            with open(superdagfile, 'w') as superdag:
                superdag.write(newsuperdag_content)

    return

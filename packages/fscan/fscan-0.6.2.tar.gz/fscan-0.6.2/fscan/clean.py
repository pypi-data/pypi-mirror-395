# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#               Sudhagar Suyamprakasam (2023)
#
# This file is part of fscan

import argparse
import os
from gwpy.time import tconvert, from_gps
from datetime import timedelta


def clean_dir(args):
    """
    Remove file and symboliclink from the specific directory.

    Parameters:
    -----------
    args : argument list
    """

    # Make the log directory if log path and file given
    if args.log is not None:
        # fancy way to use '.' if dirname() returns ''
        log_dir = os.path.dirname(args.log) or '.'
        os.makedirs(log_dir, exist_ok=True)

    # Get today's date
    current_date = from_gps(tconvert('today'))
    current_date_str = current_date.strftime('%Y%m%d')

    # Date to check
    check_date = current_date - timedelta(days=args.ndays)
    check_date_str = check_date.strftime('%Y%m%d')

    # Open a log file if requested
    if args.log is not None:
        logfile = '.'.join([args.log, current_date_str])
        f = open(logfile, 'w')

    saveroot = ''

    # Walk through the directories in the base directory
    for root, dirlist, files in os.walk(
            os.path.join(args.path, check_date_str)):

        # save any SFT files in this or any subdirectory
        if '.keepsfts' in files:
            saveroot = root

        if saveroot != '' and saveroot not in root:
            saveroot = ''

        # Proceed to this next code block only if .keepsfts was not in this
        # directory or parent directories.
        # Only worry about the sfts, cache, and log directories
        if 'sfts' in root and saveroot == '':
            # loop over files in the sfts directory
            for sftfile in files:
                # make sure we're matching the extension pattern
                if sftfile.endswith(args.extension) is True:
                    get_file = os.path.join(root, sftfile)

                    # see if the link or file conditions are satisfied
                    if os.path.islink(get_file) is True:
                        if args.dry_run is True:
                            print(f'Link for deletion: {get_file}')
                        else:
                            os.remove(get_file)
                        if args.log is not None:
                            f.write(f'Link for deletion: {get_file}\n')
                    elif os.path.isfile(get_file) is True:
                        if args.dry_run is True:
                            print(f'File for deletion: {get_file}')
                        else:
                            os.remove(get_file)
                        if args.log is not None:
                            f.write(f'File for deletion: {get_file}\n')

        elif 'cache' in root or 'logs' in root:
            for auxfile in files:
                get_file = os.path.join(root, auxfile)
                if args.dry_run is True:
                    print(f'File for deletion: {get_file}')
                else:
                    os.remove(get_file)
                if args.log is not None:
                    f.write(f'File for deletion {get_file}\n')

    if args.log is not None:
        f.close()


def main():
    # Input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True,
                        help="Directory path to date directories of data")
    parser.add_argument("--ndays", type=int, default=60,
                        help="Files older than current days. Default 60 days")
    parser.add_argument("--extension", type=str, default='sft',
                        help="Search file extension")
    parser.add_argument('--dry-run', type=bool, default=False,
                        help='Print out the files to be removed, but do not '
                             'remove them')
    parser.add_argument("--log", type=str, default=None,
                        help="Optionally save information to a log file")

    args = parser.parse_args()

    clean_dir(args)


if __name__ == "__main__":
    main()

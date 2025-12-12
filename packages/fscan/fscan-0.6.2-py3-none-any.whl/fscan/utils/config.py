# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

import argparse
import shlex

from .utils import str_to_bool


class CustomConfParser(argparse.ArgumentParser):
    """
    This modifies the ArgumentParser class to allow empty lines,
    comment lines, and argument-value pairs on the same line.
    Basically allows config files to be more human-readable.
    """

    def __init__(self, **kwargs):
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.fromfile_prefix_chars = '@'
        self.register('type', 'bool', str_to_bool)

    # customizes a method inherited from ArgumentParser
    def convert_arg_line_to_args(self, arg_line):

        # ignore empty lines and those containing only spaces
        if len(arg_line.strip()) == 0:
            return []

        # ignore comment lines
        elif arg_line.strip()[0] == "#":
            return []

        # preserve quoted substrings when splitting the line
        else:
            return shlex.split(arg_line)


class MultiConfParser(argparse.ArgumentParser):
    """
    This creates a special kind of argument parser which first handles a
    single argument (--config) to determine if there are any configuration
    files supplied. Then, it iterates through all supplied configuration files
    and parses each one individually using the specified subsequent parser.

    When help is printed, it prints the help for both parsers.
    """

    def __init__(self, subsequentParser):
        argparse.ArgumentParser.__init__(self)
        self.subsequentParser = subsequentParser
        self.add_argument('--config', nargs='+', default=None)
        self.register('type', 'bool', str_to_bool)

    def print_help(self):
        print("Configuration files are accepted in the following manner:")
        argparse.ArgumentParser.print_help(self)
        print("\nThe following arguments are accepted from the command line "
              "or a configuration file. Command line overrides config file.")
        self.subsequentParser.print_help()

    def parse_args(self):
        confArgs, otherArgs = argparse.ArgumentParser.parse_known_args(self)
        if confArgs.config is None:
            args = self.subsequentParser.parse_args(otherArgs)
            return [args]
        else:
            multiConfArgs = []
            for confFile in confArgs.config:
                argList = ["@"+confFile] + otherArgs
                args = self.subsequentParser.parse_args(argList)
                multiConfArgs += [args]
            return multiConfArgs

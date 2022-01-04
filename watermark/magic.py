# -*- coding: utf-8 -*-
"""
IPython magic function to print date/time stamps and
various system information.
Author: Sebastian Raschka <sebastianraschka.com>
License: BSD 3 clause
"""

from IPython.core.magic import Magics
from IPython.core.magic import magics_class
from IPython.core.magic import line_magic
from IPython.core.magic_arguments import argument
from IPython.core.magic_arguments import magic_arguments
from IPython.core.magic_arguments import parse_argstring

from watermark import watermark


class PackageNotFoundError(Exception):
    pass


@magics_class
class WaterMark(Magics):
    """
    IPython magic function to print date/time stamps
    and various system information.
    """
    @magic_arguments()
    @argument('-a', '--author', type=str,
              help='prints author name')
    @argument('-gu', '--github_username', type=str,
              help='prints author github username')
    @argument('-e', '--email', type=str,
              help='prints author email')
    @argument('-ws', '--website', type=str,
              help='prints author or project website')
    @argument('-d', '--date', action='store_true',
              help='prints current date as YYYY-mm-dd')
    @argument('-n', '--datename', action='store_true',
              help='prints date with abbrv. day and month names')
    @argument('-t', '--time', action='store_true',
              help='prints current time as HH-MM-SS')
    @argument('-i', '--iso8601', action='store_true',
              help='prints the combined date and time including the time zone'
                   ' in the ISO 8601 standard with UTC offset')
    @argument('-z', '--timezone', action='store_true',
              help='appends the local time zone')
    @argument('-u', '--updated', action='store_true',
              help='appends a string "Last updated: "')
    @argument('-c', '--custom_time', type=str,
              help='prints a valid strftime() string')
    @argument('-v', '--python', action='store_true',
              help='prints Python and IPython version')
    @argument('-p', '--packages', type=str,
              help='prints versions of specified Python modules and packages')
    @argument('-co', '--conda', action='store_true',
              help='prints name of current conda environment')
    @argument('-h', '--hostname', action='store_true',
              help='prints the host name')
    @argument('-m', '--machine', action='store_true',
              help='prints system and machine info')
    @argument('-g', '--githash', action='store_true',
              help='prints current Git commit hash')
    @argument('-r', '--gitrepo', action='store_true',
              help='prints current Git remote address')
    @argument('-b', '--gitbranch', action='store_true',
              help='prints current Git branch')
    @argument('-w', '--watermark', action='store_true',
              help='prints the current version of watermark')
    @argument('-iv', '--iversions', action='store_true',
              help='prints the name/version of all imported modules')
    @line_magic
    def watermark(self, line):
        """
        IPython magic function to print date/time stamps
        and various system information.
        """
        args = vars(parse_argstring(self.watermark, line))

        # renaming not to pollute the namespace
        # while preserving backward compatibility
        args['current_date'] = args.pop('date')
        args['current_time'] = args.pop('time')
        args['watermark_self'] = self

        formatted_text = watermark.watermark(**args)
        print(formatted_text)


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)

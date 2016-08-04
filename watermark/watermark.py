"""
IPython magic function to print date/time stamps and
various system information.

Author: Sebastian Raschka <sebastianraschka.com>
License: BSD 3 clause

Installation:

  pip install -e git+https://github.com/rasbt/watermark#egg=watermark

Usage:

  %load_ext watermark

  %watermark

optional arguments:

  -a AUTHOR, --author AUTHOR
                        prints author name
  -d, --date            prints current date as MM/DD/YYYY
  -e, --eurodate        prints current date as DD/MM/YYYY
  -n, --datename        prints date with abbrv. day and month names
  -t, --time            prints current time
  -z, --timezone        appends the local time zone
  -u, --updated         appends a string "Last updated: "
  -c CUSTOM_TIME, --custom_time CUSTOM_TIME
                        prints a valid strftime() string
  -v, --python          prints Python and IPython version
  -p PACKAGES, --packages PACKAGES
                        prints versions of specified Python modules and
                        packages
  -h, --hostname        prints the host name
  -m, --machine         prints system and machine info
  -g, --githash         prints current Git commit hash
  -w, --watermark       prints the current version of watermark

Examples:

    %watermark -d -t
"""

import platform
import subprocess
from time import strftime
from socket import gethostname
from multiprocessing import cpu_count
from __init__ import __version__

import pip
import IPython
from IPython.core.magic import Magics
from IPython.core.magic import magics_class
from IPython.core.magic import line_magic
from IPython.core.magic_arguments import argument
from IPython.core.magic_arguments import magic_arguments
from IPython.core.magic_arguments import parse_argstring


@magics_class
class WaterMark(Magics):
    """
    IPython magic function to print date/time stamps
    and various system information.

    """
    @magic_arguments()
    @argument('-a', '--author', type=str,
              help='prints author name')
    @argument('-d', '--date', action='store_true',
              help='prints current date as YYYY-MM-DD')
    @argument('-n', '--datename', action='store_true',
              help='prints date with abbrv. day and month names')
    @argument('-t', '--time', action='store_true',
              help='prints current time as HH-MM-DD')
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
    @argument('-h', '--hostname', action='store_true',
              help='prints the host name')
    @argument('-m', '--machine', action='store_true',
              help='prints system and machine info')
    @argument('-g', '--githash', action='store_true',
              help='prints current Git commit hash')
    @argument('-w', '--watermark', action='store_true',
              help='prints the current version of watermark')
    @line_magic
    def watermark(self, line):
        """
        IPython magic function to print date/time stamps
        and various system information.

        watermark version 1.2.3

        """
        self.out = ''
        args = parse_argstring(self.watermark, line)

        if not any(vars(args).values()):
            self.out += strftime('%Y-%m-%dT%H:%M:%S')
            self._get_pyversions()
            self._get_sysinfo()

        else:
            if args.author:
                self.out += '% s ' % args.author.strip('\'"')
            if args.updated and args.author:
                self.out += '\n'
            if args.updated:
                self.out += 'last updated: '
            if args.custom_time:
                self.out += '%s ' % strftime(args.custom_time)
            if args.date:
                self.out += '%s ' % strftime('%Y-%m-%d')
            elif args.datename:
                self.out += '%s ' % strftime('%a %b %d %Y')
            if args.time:
                self.out += '%s ' % strftime('%H:%M:%S')
            if args.timezone:
                self.out += strftime('%Z')
            if args.python:
                self._get_pyversions()
            if args.packages:
                self._get_packages(args.packages)
            if args.machine:
                self._get_sysinfo()
            if args.hostname:
                space = ''
                if args.machine:
                    space = '  '
                self.out += '\nhost name%s: %s' % (space, gethostname())
            if args.githash:
                self._get_commit_hash(bool(args.machine))
            if args.watermark:
                if self.out:
                    self.out += '\n'
                self.out += 'watermark v. %s' % __version__
        print(self.out)

    def _get_packages(self, pkgs):
        if self.out:
            self.out += '\n'
        packages = pkgs.split(',')
        installed_dists = {i.key: i.version for i in pip.get_installed_distributions()}
        for p in packages:
            self.out += '\n%s %s' % (p, installed_dists[p])

    def _get_pyversions(self):
        if self.out:
            self.out += '\n\n'
        self.out += '%s %s\nIPython %s' % (
            platform.python_implementation(),
            platform.python_version(),
            IPython.__version__)

    def _get_sysinfo(self):
        if self.out:
            self.out += '\n\n'
        self.out += ('compiler   : %s\nsystem     : %s\n'
                     'release    : %s\nmachine    : %s\n'
                     'processor  : %s\nCPU cores  : %s\ninterpreter: %s') % (
            platform.python_compiler(),
            platform.system(),
            platform.release(),
            platform.machine(),
            platform.processor(),
            cpu_count(),
            platform.architecture()[0])

    def _get_commit_hash(self, machine):
        process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                                   shell=False,
                                   stdout=subprocess.PIPE)
        git_head_hash = process.communicate()[0].strip()
        space = ''
        if machine:
            space = '   '
        self.out += '\nGit hash%s: %s' % (space, git_head_hash.decode("utf-8"))


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)

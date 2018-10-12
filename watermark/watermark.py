"""
IPython magic function to print date/time stamps and
various system information.

Author: Sebastian Raschka <sebastianraschka.com>
License: BSD 3 clause
"""

from . import __version__
import platform
import subprocess
from time import strftime
from time import time
import datetime
from socket import gethostname
from multiprocessing import cpu_count
import warnings
import types

import IPython
from IPython.core.magic import Magics
from IPython.core.magic import magics_class
from IPython.core.magic import line_magic
from IPython.core.magic_arguments import argument
from IPython.core.magic_arguments import magic_arguments
from IPython.core.magic_arguments import parse_argstring


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
        self.out = ''
        args = parse_argstring(self.watermark, line)

        if not any(vars(args).values()) or args.iso8601:
            try:
                dt = datetime.datetime.fromtimestamp(int(time()),
                                                     datetime.timezone.utc)
                iso_dt = dt.astimezone().isoformat()
            except AttributeError:  # timezone only supported by Py >=3.2:
                iso_dt = strftime('%Y-%m-%dT%H:%M:%S')

        if not any(vars(args).values()):
            self.out += iso_dt
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
            if args.iso8601:
                self.out += iso_dt
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
            if args.gitrepo:
                self._get_git_remote_origin(bool(args.machine))
            if args.gitbranch:
                self._get_git_branch(bool(args.machine))
            if args.iversions:
                self._print_all_import_versions(self.shell.user_ns)
            if args.watermark:
                if self.out:
                    self.out += '\n'
                self.out += 'watermark %s' % __version__
        print(self.out.strip())

    def _get_packages(self, pkgs):
        if self.out:
            self.out += '\n'
        packages = pkgs.split(',')

        for p in packages:
            if p == 'scikit-learn':
                p = 'sklearn'
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn("Importing scikit-learn as `scikit-learn` has"
                              " been depracated and will not be supported"
                              " anymore in v1.7.0. Please use the package"
                              " name `sklearn` instead.",
                              DeprecationWarning)
            try:
                imported = __import__(p)
            except ImportError:
                ver = 'not installed'
            else:
                try:
                    ver = imported.__version__
                except AttributeError:
                    try:
                        ver = imported.version
                    except AttributeError:
                        try:
                            ver = imported.version_info
                        except AttributeError:
                            ver = 'unknown'

            self.out += '\n%s %s' % (p, ver)

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
        self.out += '\nGit hash%s: %s' % (space,
                                          git_head_hash.decode("utf-8"))

    def _get_git_remote_origin(self, machine):
        process = subprocess.Popen(['git', 'config', '--get',
                                    'remote.origin.url'],
                                   shell=False,
                                   stdout=subprocess.PIPE)
        git_remote_origin = process.communicate()[0].strip()
        space = ''
        if machine:
            space = '   '
        self.out += '\nGit repo%s: %s' % (space,
                                          git_remote_origin.decode("utf-8"))

    def _get_git_branch(self, machine):
        process = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref',
                                    'HEAD'],
                                   shell=False,
                                   stdout=subprocess.PIPE)
        git_branch = process.communicate()[0].strip()
        space = ''
        if machine:
            space = ' '
        self.out += '\nGit branch%s: %s' % (space,
                                            git_branch.decode("utf-8"))

    @staticmethod
    def _print_all_import_versions(vars):
        for val in list(vars.values()):
            if isinstance(val, types.ModuleType):
                try:
                    print('{:<10}  {}'.format(val.__name__, val.__version__))
                except AttributeError:
                    continue

    @staticmethod
    def _print_all_import_versions(vars):
        for val in list(vars.values()):
            if isinstance(val, types.ModuleType):
                try:
                    print('{:<10}  {}'.format(val.__name__, val.__version__))
                except AttributeError:
                    continue


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)

"""
Sebastian Raschka 2014

watermark.py
version 1.2.2


IPython magic function to print date/time stamps and various system information.

Installation:

  %install_ext https://raw.githubusercontent.com/rasbt/python_reference/master/ipython_magic/watermark.py

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
  -o, --output          [output, metadata, both]
                        where to store watermark data
                        default: output

Examples:

    %watermark -d -t

"""
import platform
import subprocess
from datetime import datetime
from socket import gethostname
from pkg_resources import get_distribution
from multiprocessing import cpu_count
import json

import IPython
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, Javascript


__version__ = '1.2.2'


class ISODateEncoder(json.JSONEncoder):
    # JSON encoder that serializes datetimes to ISO 8601 strings
    def default(self, obj, *args, **kwargs):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj, *args, **kwargs)


@magics_class
class WaterMark(Magics):
    """
    IPython magic function to print date/time stamps
    and various system information.
    """
    @line_magic
    @magic_arguments()
    @argument('-a', '--author', type=str,
              help='prints author name')
    @argument('-d', '--date', action='store_true',
              help='prints current date as MM/DD/YYYY')
    @argument('-e', '--eurodate', action='store_true',
              help='prints current date as DD/MM/YYYY')
    @argument('-n', '--datename', action='store_true',
              help='prints date with abbrv. day and month names')
    @argument('-t', '--time', action='store_true',
              help='prints current time')
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
    @argument('--output', action='store',
              choices=['output', 'metadata', 'both'],
              default='output',
              help='where to store the watermark (meta)data')
    def watermark(self, line):
        """
        IPython magic function to print date/time stamps
        and various system information.

        watermark version 1.2.2

        """
        self.args = args = parse_argstring(self.watermark, line)

        out = list(self._get_marks(args))

        if args.output in ['both', 'output']:
            max_len = max([len(m[0]) for m in out])
            tmpl = '{:%d} : {}' % max_len
            for key, value in out:
                if isinstance(value, datetime):
                    value = value.strftime(self._date_format)
                print(tmpl.format(key, value))

        if args.output in ['both', 'metadata']:
            display(Javascript('IPython.notebook.metadata.watermark = {};'
                    .format(json.dumps(dict(out), cls=ISODateEncoder))))

    @property
    def _date_format(self):
        fmt = ''
        args = self.args

        if args.date:
            fmt += '%m/%d/%Y'
        elif args.eurodate:
            fmt += '%d/%m/%Y'
        elif args.datename:
            fmt += '%a %b %d %Y'

        if args.custom_time:
            fmt += ' ' + args.custom_time
        elif args.time:
            fmt += ' %H:%M:%S'

        if (args.custom_time or args.time) and args.timezone:
            fmt += '%Z'

        # if nothing else specified, apply default
        return fmt or '%m/%d/%Y %H:%M:%S'

    def _get_marks(self, args):
        if not any([
            value for key, value in vars(args).items()
            if key not in ['output']
        ]):
            for mark in self._get_updated():
                yield mark
            for mark in self._get_pyversions():
                yield mark
            for mark in self._get_sysinfo():
                yield mark

        else:
            if args.author:
                yield ['Authored by', args.author.strip('\'"')]

            if args.updated:
                for mark in self._get_updated():
                    yield mark

            if args.python:
                for mark in self._get_pyversions():
                    yield mark

            if args.packages:
                for mark in self._get_packages(args.packages):
                    yield mark

            if args.watermark:
                yield ['watermark', __version__]

            if args.machine:
                for mark in self._get_sysinfo():
                    yield mark

            if args.hostname:
                yield ['host name', gethostname()]

            if args.githash:
                for mark in self._get_commit_hash(bool(args.machine)):
                    yield mark

    def _get_updated(self):
        yield ['Last updated', datetime.now()]

    def _get_packages(self, pkgs):
        for p in pkgs.split(','):
            yield [p, get_distribution(p).version]

    def _get_pyversions(self):
        yield [platform.python_implementation(), platform.python_version()]
        yield ['IPython', IPython.__version__]

    def _get_sysinfo(self):
        yield ['compiler', platform.python_compiler()]
        yield ['system', platform.system()]
        yield ['release', platform.release()]
        yield ['machine', platform.machine()]
        yield ['processor', platform.processor()]
        yield ['CPU cores', cpu_count()]
        yield ['interpreter', platform.architecture()[0]]

    def _get_commit_hash(self, machine):
        process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                                   shell=False, stdout=subprocess.PIPE)
        git_head_hash = process.communicate()[0].strip()
        yield ['git hash', git_head_hash.decode('utf-8')]


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)

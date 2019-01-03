# -*- coding: utf-8 -*-
"""
Function to print date/time stamps and
various system information.

Authors: Sebastian Raschka <sebastianraschka.com>, Tymoteusz Wołodźko
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
import inspect
import sys


def watermark(author=None, current_date=False, datename=False, current_time=False,
              iso8601=False, timezone=False, updated=False, custom_time=None,
              python=False, packages=None, hostname=False, machine=False,
              githash=False, gitrepo=False, gitbranch=False, watermark=False,
              iversions=False):

    '''Function to print date/time stamps and various system information.

    Parameters:
    ===========

    author:
        prints author name
    date :
        prints current date as YYYY-mm-dd
    datename :
        prints date with abbrv. day and month names
    current_time :
        prints current time as HH-MM-SS
    iso8601 :
        prints the combined date and time including the time zone
        in the ISO 8601 standard with UTC offset
    timezone : 
        appends the local time zone
    updated :
        appends a string "Last updated: "
    custom_time :
        prints a valid strftime() string
    python :
        prints Python and IPython version (if running from Jupyter)
    packages :
        prints versions of specified Python modules and packages
    hostname :
        prints the host name
    machine :
        prints system and machine info
    githash :
        prints current Git commit hash
    gitrepo :
        prints current Git remote address
    gitbranch :
        prints current Git branch
    watermark :
        prints the current version of watermark
    iversions :
        prints the name/version of all imported modules
    '''

    args = locals()
    out = ''

    if not any(args.values()) or iso8601:
        try:
            dt = datetime.datetime.fromtimestamp(int(time()),
                                                    datetime.timezone.utc)
            iso_dt = dt.astimezone().isoformat()
        except AttributeError:  # timezone only supported by Py >=3.2:
            iso_dt = strftime('%Y-%m-%dT%H:%M:%S')

    if not any(args.values()):
        out += iso_dt
        out += get_pyversions()
        out += get_sysinfo()
        
    else:
        if author:
            out += '% s ' % author.strip('\'"')
        if updated and author:
            out += '\n'
        if updated:
            out += 'last updated: '
        if custom_time:
            out += '%s ' % strftime(custom_time)
        if current_date:
            out += '%s ' % strftime('%Y-%m-%d')
        elif datename:
            out += '%s ' % strftime('%a %b %d %Y')
        if current_time:
            out += '%s ' % strftime('%H:%M:%S')
        if timezone:
            out += strftime('%Z')
        if iso8601:
            out += iso_dt
        if python:
            out += get_pyversions()
        if packages:
            out += get_packages(packages)
        if machine:
            out += get_sysinfo()
        if hostname:
            space = ''
            if machine:
                space = '  '
            out += '\nhost name%s: %s' % (space, gethostname())
        if githash:
            out += get_commit_hash(bool(machine))
        if gitrepo:
            out += get_git_remote_origin(bool(machine))
        if gitbranch:
            out += get_git_branch(bool(machine))
        if iversions:
            out += get_imported_packages() # change here
        if watermark:
            out += '\nwatermark      %s' % __version__
    print(out.strip())


def using_jupyter():
    try:
        get_ipython()
        return True
    except NameError:
        return False


def get_packages(pkgs):
    if not isinstance(pkgs, list):
        packages = pkgs.split(',')
    out = '\n'

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

        out += '\n%s %s' % (p, ver)
    
    return out


def get_pyversions():
    out = '\n%s %s' % (
        platform.python_implementation(),
        platform.python_version())
    if using_jupyter():
        import IPython
        out += '\nIPython %s' % IPython.__version__
    return out


def get_sysinfo():
    return ('\ncompiler   : %s\nsystem     : %s\n'
            'release    : %s\nmachine    : %s\n'
            'processor  : %s\nCPU cores  : %s\ninterpreter: %s') % (
        platform.python_compiler(),
        platform.system(),
        platform.release(),
        platform.machine(),
        platform.processor(),
        cpu_count(),
        platform.architecture()[0])


def get_commit_hash(machine):
    process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                                shell=False,
                                stdout=subprocess.PIPE)
    git_head_hash = process.communicate()[0].strip()
    space = ''
    if machine:
        space = '   '
    return '\nGit hash%s: %s' % (space, git_head_hash.decode("utf-8"))


def get_git_remote_origin(machine):
    process = subprocess.Popen(['git', 'config', '--get',
                                'remote.origin.url'],
                                shell=False,
                                stdout=subprocess.PIPE)
    git_remote_origin = process.communicate()[0].strip()
    space = ''
    if machine:
        space = '   '
    return '\nGit repo%s: %s' % (space, git_remote_origin.decode("utf-8"))


def get_git_branch(machine):
    process = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref',
                                'HEAD'],
                                shell=False,
                                stdout=subprocess.PIPE)
    git_branch = process.communicate()[0].strip()
    space = ''
    if machine:
        space = ' '
    return '\nGit branch%s: %s' % (space, git_branch.decode("utf-8"))


def get_imported_packages():
    packages = set()
    for val in sys.modules:
        name = val.split('.')[0]
        pkg = sys.modules[name]
        if pkg.__name__ not in sys.builtin_module_names \
           and not pkg.__name__.startswith('_') :
            try:
                packages.add((pkg.__name__, pkg.__version__))
            except AttributeError:
                continue
    out = ''
    for pkg in packages:
        out += '\n%-15s%s' % pkg
    return out
# -*- coding: utf-8 -*-
"""
Function to print date/time stamps and
various system information.

Authors: Sebastian Raschka <sebastianraschka.com>, Tymoteusz Wołodźko
License: BSD 3 clause
"""

from __future__ import absolute_import

import datetime
import importlib
import os
import platform
import subprocess
import time
import types
from multiprocessing import cpu_count
from socket import gethostname

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata

import IPython

from .version import __version__


def watermark(author=None, email=None, github_username=None,
              website=None, current_date=False, datename=False,
              current_time=False, iso8601=False, timezone=False,
              updated=False, custom_time=None, python=False,
              packages=None, conda=False, hostname=False, machine=False,
              githash=False, gitrepo=False, gitbranch=False,
              watermark=False, iversions=False, watermark_self=None,
              globals_=None):

    '''Function to print date/time stamps and various system information.

    Parameters:
    ===========

    author :
        prints author name

    github_username :
        prints author github username

    email :
        prints author email

    website :
        prints author or project website

    current_date :
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

    conda :
        prints name of current conda environment

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

    watermark_self :
        instance of the watermark magics class, which is required
        for iversions.

    '''
    output = []
    args = locals()
    watermark_self = args['watermark_self']
    del args['watermark_self']

    if not any(args.values()) or args['iso8601']:
        iso_dt = _get_datetime()

    if not any(args.values()):
        args['updated'] = True
        output.append({"Last updated": iso_dt})
        output.append(_get_pyversions())
        output.append(_get_sysinfo())
    else:
        if args['author']:
            output.append({"Author": args['author'].strip("'\"")})
        if args['github_username']:
            output.append({"Github username": \
                               args['github_username'].strip("'\"")})
        if args['email']:
            output.append({"Email": args['email'].strip("'\"")})
        if args['website']:
            output.append({"Website": args['website'].strip("'\"")})
        if args['updated']:
            value = ""
            if args['custom_time']:
                value = time.strftime(args['custom_time'])
            elif args['iso8601']:
                value = iso_dt
            else:
                values = []
                if args['current_date']:
                    values.append(time.strftime("%Y-%m-%d"))
                elif args['datename']:
                    values.append(time.strftime("%a %b %d %Y"))
                if args['current_time']:
                    time_str = time.strftime("%H:%M:%S")
                    if args['timezone']:
                        time_str += time.strftime("%Z")
                    values.append(time_str)
                value = " ".join(values)
            output.append({"Last updated": value})
        if args['python']:
            output.append(_get_pyversions())
        if args['packages']:
            output.append(_get_packages(args['packages']))
        if args['conda']:
            output.append(_get_conda_env())
        if args['machine']:
            output.append(_get_sysinfo())
        if args['hostname']:
            output.append({"Hostname": gethostname()})
        if args['githash']:
            output.append(_get_commit_hash(bool(args['machine'])))
        if args['gitrepo']:
            output.append(_get_git_remote_origin(bool(args['machine'])))
        if args['gitbranch']:
            output.append(_get_git_branch(bool(args['machine'])))
        if args['iversions']:
            if watermark_self:
                ns = watermark_self.shell.user_ns
            elif globals_:
                ns = globals_
            else:
                raise RuntimeError(
                    "Either `watermark_self` or `globals_` must be provided "
                    "to show imported package versions."
                )
            output.append(_get_all_import_versions(ns))
        if args['watermark']:
            output.append({"Watermark": __version__})

    return _generate_formatted_text(output)


def _generate_formatted_text(list_of_dicts):
    result = []
    for section in list_of_dicts:
        if section:
            text = ""
            longest = max(len(key) for key in section)
            for key, value in section.items():
                text += f"{key.ljust(longest)}: {value}\n"
            result.append(text)
    return "\n".join(result)


def _get_datetime(pattern="%Y-%m-%dT%H:%M:%S"):
    try:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        iso_dt = dt.astimezone().isoformat()
    except AttributeError:  # timezone only supported by Py >=3.2:
        iso_dt = time.strftime(pattern)
    return iso_dt


def _get_packages(pkgs):
    packages = pkgs.split(",")
    return {package: _get_package_version(package)
            for package in packages}


def _get_package_version(pkg_name):
    """Return the version of a given package"""
    if pkg_name == "scikit-learn":
        pkg_name = "sklearn"
    try:
        imported = importlib.import_module(pkg_name)
    except ImportError:
        version = "not installed"
    else:
        try:
            version = importlib_metadata.version(pkg_name)
        except importlib_metadata.PackageNotFoundError:
            try:
                version = imported.__version__
            except AttributeError:
                try:
                    version = imported.version
                except AttributeError:
                    try:
                        version = imported.version_info
                    except AttributeError:
                        version = "unknown"
    return version


def _get_pyversions():
    return {
        "Python implementation": platform.python_implementation(),
        "Python version": platform.python_version(),
        "IPython version": IPython.__version__,
    }


def _get_sysinfo():
    return {
        "Compiler": platform.python_compiler(),
        "OS": platform.system(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU cores": cpu_count(),
        "Architecture": platform.architecture()[0],
    }


def _get_commit_hash(machine):
    process = subprocess.Popen(
        ["git", "rev-parse", "HEAD"], shell=False, stdout=subprocess.PIPE
    )
    git_head_hash = process.communicate()[0].strip()
    return {"Git hash": git_head_hash.decode("utf-8")}


def _get_git_remote_origin(machine):
    process = subprocess.Popen(
        ["git", "config", "--get", "remote.origin.url"],
        shell=False,
        stdout=subprocess.PIPE,
    )
    git_remote_origin = process.communicate()[0].strip()
    return {"Git repo": git_remote_origin.decode("utf-8")}


def _get_git_branch(machine):
    process = subprocess.Popen(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        shell=False,
        stdout=subprocess.PIPE,
    )
    git_branch = process.communicate()[0].strip()
    return {"Git branch": git_branch.decode("utf-8")}


def _get_all_import_versions(vars):
    to_print = {}
    imported_pkgs = {
        val.__name__.split(".")[0]
        for val in list(vars.values())
        if isinstance(val, types.ModuleType)
    }
    imported_pkgs.discard("builtins")
    for pkg_name in imported_pkgs:
        pkg_version = _get_package_version(pkg_name)
        if pkg_version not in ("not installed", "unknown"):
            to_print[pkg_name] = pkg_version
    return to_print


def _get_conda_env():
    name = os.getenv('CONDA_DEFAULT_ENV', 'n/a')
    return {"conda environment": name}

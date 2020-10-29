"""
IPython magic function to print date/time stamps and
various system information.

Author: Sebastian Raschka <sebastianraschka.com>
License: BSD 3 clause
"""

import datetime
import platform
import subprocess
import time
import types
from multiprocessing import cpu_count
from socket import gethostname

import IPython
import pkg_resources
from IPython.core.magic import Magics, line_magic, magics_class
from IPython.core.magic_arguments import argument, \
     magic_arguments, parse_argstring
from pkg_resources import DistributionNotFound

from . import __version__


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
        output = []
        args = parse_argstring(self.watermark, line)

        if not any(vars(args).values()) or args.iso8601:
            iso_dt = self._get_datetime()

        if not any(vars(args).values()):
            output.append({"Datetime": iso_dt})
            output.append(self._get_pyversions())
            output.append(self._get_sysinfo())
        else:
            if args.author:
                output.append({"Author": args.author.strip("'\"")})
            if args.updated:
                value = ""
                if args.custom_time:
                    value = time.strftime(args.custom_time)
                if args.date:
                    value = time.strftime("%Y-%m-%d")
                elif args.datename:
                    value = time.strftime("%a %b %d %Y")
                if args.time:
                    value = time.strftime("%H:%M:%S")
                if args.timezone:
                    value = time.strftime("%Z")
                if args.iso8601:
                    value = iso_dt
                output.append({"Last updated": value})
            if args.python:
                output.append(self._get_pyversions())
            if args.packages:
                output.append(self._get_packages(args.packages))
            if args.machine:
                output.append(self._get_sysinfo())
            if args.hostname:
                output.append({"Hostname": gethostname()})
            if args.githash:
                output.append(self._get_commit_hash(bool(args.machine)))
            if args.gitrepo:
                output.append(self._get_git_remote_origin(bool(args.machine)))
            if args.gitbranch:
                output.append(self._get_git_branch(bool(args.machine)))
            if args.iversions:
                output.append(self._print_all_import_versions(
                    self.shell.user_ns))
            if args.watermark:
                output.append({"Watermark": __version__})
        print(self._generate_formatted_text(output))

    def _generate_formatted_text(self, list_of_dicts):
        result = []
        for section in list_of_dicts:
            if section:
                text = ""
                longest = max(len(key) for key in section)
                for key, value in section.items():
                    text += f"{key.ljust(longest)}: {value}\n"
                result.append(text)
        return "\n".join(result)

    def _get_datetime(self, pattern="%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.datetime.now(tz=datetime.timezone.utc)
            iso_dt = dt.astimezone().isoformat()
        except AttributeError:  # timezone only supported by Py >=3.2:
            iso_dt = time.strftime(pattern)
        return iso_dt

    def _get_packages(self, pkgs):
        packages = pkgs.split(",")
        return {package: self._get_package_version(package)
                for package in packages}

    def _get_package_version(self, pkg_name):
        """Return the version of a given package
        """
        if pkg_name == "scikit-learn":
            pkg_name = "sklearn"
        try:
            imported = __import__(pkg_name)
        except ImportError:
            version = "not installed"
        else:
            try:
                version = pkg_resources.get_distribution(pkg_name).version
            except DistributionNotFound:
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

    def _get_pyversions(self):
        return {
            "Python implementation": platform.python_implementation(),
            "Python version": platform.python_version(),
            "IPython version": IPython.__version__,
        }

    def _get_sysinfo(self):
        return {
            "Compiler": platform.python_compiler(),
            "OS": platform.system(),
            "Release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU cores": cpu_count(),
            "Architecture": platform.architecture()[0],
        }

    def _get_commit_hash(self, machine):
        process = subprocess.Popen(
            ["git", "rev-parse", "HEAD"], shell=False, stdout=subprocess.PIPE
        )
        git_head_hash = process.communicate()[0].strip()
        return {"Git hash": git_head_hash.decode("utf-8")}

    def _get_git_remote_origin(self, machine):
        process = subprocess.Popen(
            ["git", "config", "--get", "remote.origin.url"],
            shell=False,
            stdout=subprocess.PIPE,
        )
        git_remote_origin = process.communicate()[0].strip()
        return {"Git repo": git_remote_origin.decode("utf-8")}

    def _get_git_branch(self, machine):
        process = subprocess.Popen(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            shell=False,
            stdout=subprocess.PIPE,
        )
        git_branch = process.communicate()[0].strip()
        return {"Git branch": git_branch.decode("utf-8")}

    @staticmethod
    def _print_all_import_versions(vars):
        to_print = {}
        for val in list(vars.values()):
            if isinstance(val, types.ModuleType):
                if val.__name__ != "builtins":
                    try:
                        for v in ["VERSION", "__version__"]:
                            if hasattr(val, v):
                                to_print[val.__name__] = getattr(val, v)
                                break
                    except AttributeError:
                        try:
                            imported = __import__(val.__name__.split(".")[0])
                            to_print[imported.__name__] = imported.__version__
                        except AttributeError:
                            continue
        return to_print


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)

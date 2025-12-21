# -*- coding: utf-8 -*-
"""
Function to print date/time stamps and
various system information.

Authors: Sebastian Raschka <sebastianraschka.com>, Tymoteusz Wołodźko
License: BSD 3 clause
"""

from __future__ import absolute_import

import datetime
import inspect
import os
import platform
import subprocess
import time
import types
from multiprocessing import cpu_count
from socket import gethostname


try:
    from py3nvml import py3nvml
except ImportError:
    py3nvml = None

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata

import IPython

from .version import __version__


def watermark(
        author=None,
        email=None,
        github_username=None,
        website=None,
        current_date=False,
        datename=False,
        current_time=False,
        iso8601=False,
        timezone=False,
        updated=False,
        custom_time=None,
        python=False,
        packages=None,
        conda=False,
        hostname=False,
        machine=False,
        githash=False,
        gitrepo=False,
        gitbranch=False,
        watermark=False,
        iversions=False,
        gpu=False,
        jupyter_env=False,
        python_installation=False,
        check_latest=False,
        watermark_self=None,
        globals_=None
):

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

    gpu :
        prints GPU information (currently limited to NVIDIA GPUs), if available

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
                if args['current_date'] or args['datename']:
                    if args['datename']:
                        values.append(time.strftime("%a, %d %b %Y"))
                    else:
                        values.append(time.strftime("%Y-%m-%d"))
                if args['current_time']:
                    time_str = time.strftime("%H:%M:%S")
                    if args['timezone']:
                        time_str += " " + time.strftime("%Z")
                    values.append(time_str)
                value = " ".join(values)
            output.append({"Last updated": value})
        elif args['current_date'] or args['current_time']:
            if args['current_date'] and args['current_time']:
                date_str = time.strftime("%Y-%m-%d")
                time_str = time.strftime("%H:%M:%S")
                output.append({"Date/Time": f"{date_str} {time_str}"})
            elif args['current_date']:
                output.append({"Date": time.strftime("%Y-%m-%d")})
            elif args['current_time']:
                output.append({"Time": time.strftime("%H:%M:%S")})
        if args['python']:
            output.append(_get_pyversions())
        if args['packages']:
            check_latest = args.get('check_latest', False)
            output.append(_get_packages(args['packages'], check_latest))
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
        if args['gpu']:
            output.append(_get_gpu_info())
        if args['python_installation']:
            output.append({"Python installation": _get_python_installation()})
        if args['jupyter_env']:
            output.append({"Jupyter enviroment": _get_jupyter_env()})
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


def _get_packages(pkgs, check_latest=False):
    packages = pkgs.split(",")
    return {package: _get_package_version(package, check_latest)
            for package in packages}


def _get_package_version(pkg_name, check_latest=False):
    """Internal helper to get the version of a package."""
    current_version = 'unknown'
    try:
        current_version = importlib_metadata.version(pkg_name)
    except (importlib_metadata.PackageNotFoundError, KeyError):
        try:
            import importlib
            temp_mod = importlib.import_module(pkg_name)
            current_version = getattr(temp_mod, '__version__', 'unknown')
        except Exception:
            current_version = 'unknown'

    if check_latest and current_version != 'unknown':
        latest_version = _get_latest_version(pkg_name)
        if latest_version and latest_version != current_version:
            return f"{current_version} (version {latest_version} is available)"

    return current_version


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

    imported_modules = {
        val
        for val in list(vars.values())
        if isinstance(val, types.ModuleType)
    }

    imported_modules.update(
        {
            inspect.getmodule(val) for val in list(vars.values())
            if inspect.isclass(val) or inspect.isfunction(val)
        }
    )

    imported_pkgs = {module.__name__.split(".")[0] for module in imported_modules}

    imported_pkgs.discard("builtins")
    for pkg_name in sorted(imported_pkgs):
        pkg_version = _get_package_version(pkg_name)
        if pkg_version not in ("not installed", "unknown"):
            to_print[pkg_name] = pkg_version
    return to_print


def _get_conda_env():
    name = os.getenv('CONDA_DEFAULT_ENV', 'n/a')
    return {"conda environment": name}


def _get_gpu_info():
    if py3nvml is None:
        return {"GPU Info": 'Install the gpu extra '
                '(pip install "watermark[gpu]") '
                'to display GPU information for NVIDIA chipsets'}
    try:
        gpu_info = [""]
        py3nvml.nvmlInit()
        num_gpus = py3nvml.nvmlDeviceGetCount()
        for i in range(num_gpus):
            handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
            gpu_name = py3nvml.nvmlDeviceGetName(handle)
            gpu_info.append(f"GPU {i}: {gpu_name}")
        py3nvml.nvmlShutdown()
        return {"GPU Info": "\n  ".join(gpu_info)}

    except py3nvml.NVMLError_LibraryNotFound:
        return {"GPU Info": "NVIDIA drivers do not appear "
                "to be installed on this machine."}
    except:
        return {"GPU Info": "GPU information is not "
                "available for this machine."}


def _get_jupyter_env():
    """Internal helper to detect the current Jupyter environment."""
    import os
    import importlib.util

    if 'COLAB_RELEASE_TAG' in os.environ:
        return "Google Colab"

    if 'VSCODE_PID' in os.environ or 'VSCODE_CWD' in os.environ:
        return "VS Code (Notebook)"

    if 'KAGGLE_KERNEL_RUN_TYPE' in os.environ:
        return "Kaggle Notebook"

    def _is_jupyterlab():
        lab_env_vars = (
            'JUPYTERLAB_DIR',
            'JUPYTERLAB_SETTINGS_DIR',
            'JUPYTERLAB_WORKSPACES_DIR',
            'JUPYTERLAB_APP_DIR',
        )
        if any(os.environ.get(var) for var in lab_env_vars):
            return True

        parent_app = os.environ.get('JPY_PARENT_APP', '')
        parent_lower = parent_app.lower()
        if 'jupyterlab' in parent_lower or 'jupyter-lab' in parent_lower:
            return True
        if parent_app and any(token in parent_lower for token in ('notebook', 'nbclassic')):
            return False

        return importlib.util.find_spec('jupyterlab') is not None

    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            if _is_jupyterlab():
                return "JupyterLab"
            return "Jupyter Notebook (Classic)"
        elif shell == 'TerminalInteractiveShell':
            return "IPython Terminal"
    except NameError:
        return "Standard Python Interpreter"

    return "Unknown / Classic Jupyter"


def _get_python_installation():
    """Internal helper to detect how Python was installed (Issue #89)."""
    import sys
    import os

    exe_path = sys.executable.lower()

    if 'conda' in exe_path or 'anaconda' in exe_path or 'miniconda' in exe_path:
        return "Conda"

    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return "Virtual Environment (venv/virtualenv)"

    if '.pyenv' in exe_path:
        return "pyenv"

    if 'windowsapps' in exe_path or 'microsoft\\windowsapps' in exe_path:
        return "Windows Store"

    if 'homebrew' in exe_path or '/usr/local/cellar/' in exe_path:
        return "Homebrew"

    if os.path.exists('/.dockerenv'):
        return "Docker container"

    return "System/Official"


def _get_latest_version(package_name):
    """Fetch the latest version of a package from PyPI."""
    import urllib.request
    import json
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data['info']['version']
    except Exception:
        return None

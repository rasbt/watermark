[![Build Status](https://travis-ci.org/rasbt/watermark.svg?branch=master)](https://travis-ci.org/rasbt/watermark)
[![PyPI version](https://badge.fury.io/py/watermark.svg)](http://badge.fury.io/py/watermark)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
![License](https://img.shields.io/badge/license-BSD-blue.svg)

watermark
=========

An IPython magic extension for printing date and time stamps, version numbers, and hardware information.
<br>


#### Sections

- [Examples](#examples)
- [Installation and updating](#installation-and-updating)
- [Usage](#usage)
- [Changelog](#changelog)

<br>

## Examples

[[top](#sections)]

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex1.png)

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex2.png)

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex3.png)

More examples can be found in this [IPython notebook](http://nbviewer.ipython.org/github/rasbt/watermark/blob/master/docs/watermark.ipynb).

<br>

## Installation and updating

[[top](#sections)]

The `watermark` line magic can be installed by executing

    pip install watermark

or

    pip install -e git+https://github.com/rasbt/watermark#egg=watermark

<br>

Note:

To remove an old `watermark` installation (installed via the deprecated `%install_ext` magic extension), simply delete it from the ``.ipython/extensions/`` directory, which is typically located in a user's home directory.

## Usage

[[top](#sections)]

After successful installation, the `watermark` magic extension can be loaded via:

	%load_ext watermark

<br>

To get an overview of all available commands, type:

	%watermark?

<br>



	%watermark [-a AUTHOR] [-d] [-n] [-t] [-z] [-u] [-c CUSTOM_TIME] [-v]
	                 [-p PACKAGES] [-h] [-m] [-g]


	IPython magic function to print date/time stamps
	and various system information.

		watermark version 1.2.3

		optional arguments:
		  -a AUTHOR, --author AUTHOR
		                        prints author name
		  -d, --date            prints current date as YYYY-MM-DD
		  -n, --datename        prints date with abbrv. day and month names
		  -t, --time            prints current time as HH-MM-DD
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


<br>

## Changelog

[[top](#sections)]

#### v. 1.3.2 (August 3, 2016)

- Fixes an issue where the wrong package info was obtained when using the system level jupyter within a virtualenv environment.

#### v. 1.3.1 (June 6, 2016)

- Fixing an issue that caused problems importing watermark using Python 2.x

#### v. 1.3.0 (May 21, 2016)

- Removed the deprecated the %install_ext magic so that watermark can now be installed as a regular python package via `pip` (via [Peter Bull](https://github.com/pjbull))

#### v. 1.2.3 (Jan 29, 2016)
- Changed date format to the unambiguous ISO-8601 format
- Ditched the deprecated %install_ext function and made watermark a proper Python package
- Released the new version under a more permissive newBSD [license](./LICENSE)

#### v. 1.2.2 (Jun 17, 2015)
- Changed the default date-format of `-d`, `--date` to MM/DD/YYYY, the format DD/MM/YYYY can be used via the shortcut `-e`, `--eurodate`.

#### v. 1.2.1 (Mar 3, 2015)
- Small bugfix to allow custom time string formatting.

#### v. 1.2.0 (Oct 01, 2014)
- `--watermark` command added to print the current version of watermark.
- Print author name on a separate line
- Fixed bug that day takes the same value as the minute if the `-n` flag is used.

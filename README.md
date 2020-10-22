[![Build Status](https://travis-ci.org/rasbt/watermark.svg?branch=master)](https://travis-ci.org/rasbt/watermark)
[![PyPI version](https://badge.fury.io/py/watermark.svg)](http://badge.fury.io/py/watermark)
![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)
![License](https://img.shields.io/badge/license-BSD-blue.svg)

watermark
=========

An IPython magic extension for printing date and time stamps, version numbers, and hardware information.
<br>

#### Sections

- [Examples](#examples)
- [Installation and updating](#installation-and-updating)
- [Usage](#usage)
- [Development guidelines](#development-guidelines)
- [Changelog](#changelog)

<br>

## Examples

[[top](#sections)]

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex1.png)

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex2.png)

![](https://github.com/rasbt/watermark/blob/master/docs/images/ex3.png)

More examples can be found in this [Jupyter notebook](https://github.com/rasbt/watermark/blob/master/docs/watermark.ipynb).

<br>

## Installation and updating

[[top](#sections)]

The watermark line magic can be installed by executing

```bash
pip install watermark
```

Alternatively, you can install the latest development version directly from GitHub via

```bash
pip install -e git+https://github.com/rasbt/watermark#egg=watermark
```

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


```
%watermark [-a AUTHOR] [-d] [-n] [-t] [-i] [-z] [-u] [-c CUSTOM_TIME]
               [-v] [-p PACKAGES] [-h] [-m] [-g] [-w]

IPython magic function to print date/time stamps
and various system information.

optional arguments:
-a AUTHOR, --author AUTHOR
                       prints author name
-d,  --date            prints current date as YYYY-mm-dd
-n,  --datename        prints date with abbrv. day and month names
-t,  --time            prints current time as HH-MM-SS
-i,  --iso8601         prints the combined date and time including the time
                       zone in the ISO 8601 standard with UTC offset
-z,  --timezone        appends the local time zone
-u,  --updated         appends a string "Last updated: "
-c CUSTOM_TIME, --custom_time CUSTOM_TIME
                       prints a valid strftime() string
-v,  --python          prints Python and IPython version
-p PACKAGES, --packages PACKAGES
                       prints versions of specified Python modules and
                       packages
-h,  --hostname        prints the host name
-m,  --machine         prints system and machine info
-g,  --githash         prints current Git commit hash
-r,  --gitrepo         prints current Git remote address
-b,  --gitbranch       prints the current Git branch (new in v1.6)
-iv, --iversion        print name and version of all imported packages
-w,  --watermark       prints the current version of watermark
```

<br>

## Development guidelines

[[top](#sections)]

In line with [NEP 29][nep-29], this project supports:

- All minor versions of Python released 42 months prior to the project, and at minimum the two latest minor versions.

[nep-29]: https://numpy.org/neps/nep-0029-deprecation_policy.html

<br>

## Changelog

[[top](#sections)]

#### v. 2.1.0 (November 2020)

_in progress_

(Via contribution by [James Myatt](https://github.com/jamesmyatt))

- Adopt [NEP 29][nep-29] and require Python version 3.7 or newer
- Add Python 3.8 and 3.9 to Travis CI builds.

#### v. 2.0.2 (November 19, 2019)

- Support `VERSION` attributes, in addition to `__version__` attributes.

#### v. 2.0.1 (October 04, 2019)

- Fix `'sklearn'` vs. `'scikit-learn'` import compatibility.

#### v. 2.0.0 (October 04, 2019)

- Now uses `pkg_resources` as the default method for getting version numbers.
- Fixes a whitespace bug when printing the timezone.

#### v. 1.8.2 (July 28, 2019)

- When no Python library was imported and the `--iversion` is used, print an empty string instead of raising an error.

#### v. 1.8.1 (January 26, 2019)

- Fixes string alignment issues when the `-iv`/`--iversion` flag is used.

#### v. 1.8.0 (January 02, 2019)

- The `-iv`/`--iversion` flag now also shows package versions that were imported as `from X import Y`
and `import X.Y as Y`. For example,

```python
import scipy as sp
from sklearn import metrics
import numpy.linalg as linalg
```

```
%watermark --iversions
```

will return

```
scipy     1.1.0
sklearn   0.20.1
numpy     1.15.4
```

#### v. 1.7.0 (October 13, 2018)

(Via contribution by [James Myatt](https://github.com/jamesmyatt))

- Shows "not installed" for version of packages/modules that cannot be imported.
- Shows "unknown" for version of packages/modules when version attribute cannot be found.
- Add Python 3.6 and 3.7 to Travis CI builds.
- Add classifiers to setuptools configuration.

#### v. 1.6.1 (June 10, 2018)

- Now also includes the LICENSE file in the Python Wheels distribution

#### v. 1.6.0 (Jan uary18, 2018)

- Adds a new `-b`/`--gitbranch` parameter that prints the current Git branch.

#### v. 1.5.0 (August 27, 2017)

- Adds a new `-iv`/ `--iversions` parameter that prints the package names and version numbers of all packages that were previously imported in the current Python session. (Via contribution by [Aziz Alto](https://github.com/iamaziz))

#### v. 1.4.0 (April 18, 2017)

- Adds a new `-r`/ `--gitrepo` parameter that returns the URL of Git remote name "origin". (Via contribution by [Lucy Park](https://github.com/e9t))

#### v. 1.3.4 (October 15, 2016)

- Allow fetching scikit-learn's version number via `-p scikit-learn` in addition of `-p sklearn` (the former is deprecated and will not be supported in watermark > 1.7).

#### v. 1.3.3 (September 1, 2016)

- Includes LICENSE in MANIFEST.in for packaging

#### v. 1.3.2 (August 16, 2016)

- Fixes an issue where the wrong package info was obtained when using the system level Jupyter within a virtualenv environment. (Via contribrution by [Michael Bell](https://github.com/mrbell))
- Adds a new `-i`/ `--iso8601` parameter that returns the current date-time string in ISO 8601 format with offset to UTC. For instance: `2016-08-16T18:03:42-04:00`. Current caveat: Python < 3.2 requires external libraries for for computing the timezone offset, thus, Python < 3.2 will currently only print `2016-08-16T18:03:42`
- Adds offsets to UTC to the default date-time string for Python >= 3.2

#### v. 1.3.1 (June 6, 2016)

- Fixes an issue that caused problems importing watermark using Python 2.x

#### v. 1.3.0 (May 21, 2016)

- Removed the deprecated the %install_ext magic so that watermark can now be installed as a regular python package via `pip` (Via contribution by [Peter Bull](https://github.com/pjbull))

#### v. 1.2.3 (January 29, 2016)

- Changed date format to the unambiguous ISO-8601 format
- Ditched the deprecated %install_ext function and made watermark a proper Python package
- Released the new version under a more permissive newBSD [license](./LICENSE)

#### v. 1.2.2 (June 17, 2015)

- Changed the default date-format of `-d`, `--date` to MM/DD/YYYY, the format DD/MM/YYYY can be used via the shortcut `-e`, `--eurodate`.

#### v. 1.2.1 (March 3, 2015)

- Small bugfix to allow custom time string formatting.

#### v. 1.2.0 (October 1, 2014)

- `--watermark` command added to print the current version of watermark.
- Print author name on a separate line
- Fixed bug that day takes the same value as the minute if the `-n` flag is used.

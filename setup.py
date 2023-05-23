# Sebastian Raschka 2014-2022
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

from os.path import dirname, join, realpath
from textwrap import dedent

from setuptools import find_packages, setup


PROJECT_ROOT = dirname(realpath(__file__))
REQUIREMENTS_FILE = join(PROJECT_ROOT, "requirements.txt")

with open(REQUIREMENTS_FILE) as f:
    install_reqs = f.read().splitlines()

install_reqs.append("setuptools")

# Also see settings in setup.cfg
setup(
    name="watermark",
    license="newBSD",
    description=(
        "IPython magic function to print date/time stamps and "
        "various system information."
    ),
    author="Sebastian Raschka",
    author_email="mail@sebastianraschka.com",
    url="https://github.com/rasbt/watermark",
    packages=find_packages(exclude=[]),
    install_requires=install_reqs,
    long_description=dedent(
        """\
        An IPython magic extension for printing date and time stamps, version
        numbers, and hardware information.

        Contact
        =============
        If you have any questions or comments about watermark,
        please feel free to contact me via
        email: mail@sebastianraschka.com

        This project is hosted at https://github.com/rasbt/watermark

        The documentation can be found at
        https://github.com/rasbt/watermark/blob/master/README.md"""
    ),
)

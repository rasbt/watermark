# Sebastian Raschka 2014-2015
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

from textwrap import dedent

from setuptools import find_packages, setup

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
    install_requires=[
        "ipython",
        'importlib-metadata < 3.0 ; python_version < "3.8"',
    ],
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

# Sebastian Raschka 2014-2015
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

from setuptools import setup, find_packages
import os
import watermark

VERSION = watermark.__version__

setup(
    name='watermark',
    version=VERSION,
    license='newBSD',
    description=('IPython magic function to print date/time stamps and'
                 'various system information.'),
    author='Sebastian Raschka',
    author_email='mail@sebastianraschka.com',
    url='https://github.com/rasbt/watermark',
    packages=find_packages(exclude=[]),
    install_requires=['ipython'],
    long_description="""
An IPython magic extension for printing date and time stamps, version numbers,
and hardware information.

Contact
=============
If you have any questions or comments about watermark,
please feel free to contact me via
email: mail@sebastianraschka.com

This project is hosted at https://github.com/rasbt/watermark

The documentation can be found at
https://github.com/rasbt/watermark/blob/master/README.md
"""
)

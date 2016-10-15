# Sebastian Raschka 2014-2015
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause


import sys


__version__ = '1.3.4'

if sys.version_info >= (3, 0):
    from watermark.watermark import *
else:
    from watermark import *

__all__ = ['watermark']

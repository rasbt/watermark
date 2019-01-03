# Sebastian Raschka 2014-2018
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause


import sys


__version__ = '1.8.0'

if sys.version_info >= (3, 0):
    from watermark.magick import *
    from watermark.watermark import watermark
else:
    from magick import *
    from watermark import watermark

__all__ = ['watermark', 'magick']

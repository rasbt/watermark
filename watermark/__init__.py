# Sebastian Raschka 2014-2018
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

from __future__ import absolute_import

from .version import __version__

from watermark.magic import *
from watermark.watermark import watermark

__all__ = ["watermark", "magic"]

import sys

if sys.version_info >= (3, 0):
    from watermark.watermark import *
else:
    from watermark import *

from ._version import __version__

__all__ = ['watermark']



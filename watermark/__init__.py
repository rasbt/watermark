import sys

if sys.version_info >= (3, 0):
    from watermark.watermark import *
else:
    from watermark import *


__all__ = ['watermark']

__version__ = '1.3.1'

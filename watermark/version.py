try:
    import importlib.metadata as importlib_metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata

try:
    __version__ = importlib_metadata.version("watermark")
except Exception:
    __version__ = "unknown"

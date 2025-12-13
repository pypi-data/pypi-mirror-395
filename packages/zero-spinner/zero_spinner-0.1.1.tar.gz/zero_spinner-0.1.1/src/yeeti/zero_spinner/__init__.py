# Copyright (C) 2025 Yeeti
from .main import Spinner, spinner

__all__ = ['Spinner', 'spinner']

__version__ = '0.0.0'  # Placeholder

try:
    from importlib.metadata import version

    __version__ = version(__name__)
except ImportError:
    # Fallback for direct imports during dev
    pass

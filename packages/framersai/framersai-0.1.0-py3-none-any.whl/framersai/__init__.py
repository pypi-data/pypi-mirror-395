"""
Framers AI - Namespace package for Framers AI tools.

This package re-exports promptmachine-eval for convenience.
For full functionality, use: pip install promptmachine-eval
"""

__version__ = "0.1.0"

# Re-export from main package
try:
    from promptmachine_eval import *
    from promptmachine_eval import __version__ as eval_version
except ImportError:
    pass

__all__ = ["__version__"]


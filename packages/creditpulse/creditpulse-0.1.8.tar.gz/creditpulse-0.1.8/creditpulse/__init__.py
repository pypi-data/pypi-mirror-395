"""A clean Python project template with public API.

This package provides a simple, clean interface for users to import and use.

Example:
    >>> from CreditPulse import Check
    >>> client = Check()
    >>> result_juridica = client.persona_juridica()
    >>> result_natural = client.persona_natural()
"""

# Import version
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# Package metadata
__author__ = "Santiago Velez"
__email__ = "s.velez@saman-wm.com"
__description__ = "A python library for financial analysis"

from .check import Check

__all__ = ["Check"]

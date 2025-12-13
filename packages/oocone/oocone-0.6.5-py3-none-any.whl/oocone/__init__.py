"""
oocone.

Unofficial library for interacting with an enocoo energy management system.
"""

from .auth import Auth
from .enocoo import Enocoo

__all__ = ["Auth", "Enocoo"]

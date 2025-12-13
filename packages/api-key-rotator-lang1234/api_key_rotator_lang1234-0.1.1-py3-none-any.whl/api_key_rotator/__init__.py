"""
API Key Rotator - A Python library for rotating API keys with automatic expiration handling.

This package provides a thread-safe, easy-to-use solution for managing and rotating
multiple API keys, with support for automatic expiration, TTL, and dynamic key fetching.
"""

from .rotator import KeyRotator, with_key_rotation

__version__ = "0.1.1"
__author__ = "xLang1234"
__all__ = ["KeyRotator", "with_key_rotation"]

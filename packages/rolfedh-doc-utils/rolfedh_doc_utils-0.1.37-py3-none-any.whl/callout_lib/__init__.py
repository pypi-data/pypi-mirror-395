"""
Callout Library - Shared modules for AsciiDoc callout conversion

This library provides reusable components for converting AsciiDoc callouts
to various formats including definition lists, bulleted lists, and inline comments.
"""

from .detector import CalloutDetector, CodeBlock, CalloutGroup, Callout
from .converter_deflist import DefListConverter
from .converter_bullets import BulletListConverter
from .converter_comments import CommentConverter, LongCommentWarning

__all__ = [
    'CalloutDetector',
    'CodeBlock',
    'CalloutGroup',
    'Callout',
    'DefListConverter',
    'BulletListConverter',
    'CommentConverter',
    'LongCommentWarning',
]

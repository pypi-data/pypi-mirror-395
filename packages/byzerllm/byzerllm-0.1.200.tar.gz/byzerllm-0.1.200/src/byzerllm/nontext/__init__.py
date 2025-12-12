"""
Nontext AC Module - Robust media content extraction and conversion

This module provides functionality to extract and convert non-text content
(images, audio) from tagged text into base64 format.
"""

from .parser import TagParser, ParseError
from .processors import ImageProcessor, AudioProcessor
from .extractors import MediaExtractor

__all__ = [
    "TagParser",
    "ParseError", 
    "ImageProcessor",
    "AudioProcessor",
    "MediaExtractor"
]

__version__ = "1.0.0"

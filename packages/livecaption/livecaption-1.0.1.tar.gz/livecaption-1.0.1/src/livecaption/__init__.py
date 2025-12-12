"""
LiveCaption - Real-time Audio Transcription for Video Streaming

A Firefox-integrated audio transcription system optimized for
Japanese anime and streaming content.
"""

__version__ = "1.0.1"
__author__ = "b-tok"
__license__ = "MIT"

from livecaption.config import Config, get_config, save_config

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Config",
    "get_config",
    "save_config",
]

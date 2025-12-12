"""MILES Coder - A tool for encoding surface information."""

__version__ = "0.1.0"
__author__ = "Tim Würger"
__email__ = "tim.wuerger@hereon.de"

from .converter import MILESCoder
from .models import (
    MILESConversionRequest,
    JSONConversionRequest,
    MILESConversionResponse,
    JSONConversionResponse,
)

__all__ = [
    "MILESCoder",
    "MILESConversionRequest",
    "MILESConversionResponse",
    "JSONConversionRequest",
    "JSONConversionResponse",
]

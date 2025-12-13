"""
VERDICT SDK - Python client for the VERDICT AI-powered crypto trading analyzer.

This SDK provides an easy-to-use interface for accessing VERDICT's trading analysis,
sentiment analysis, and Flare Network verification capabilities.
"""

__version__ = "0.1.0"
__author__ = "VERDICT Team"

from .client import VerdictClient
from .models import (
    AnalysisResponse,
    MarketData,
    SentimentData,
    OnChainData,
    PositionInfo,
    Recommendation
)
from .exceptions import (
    VerdictAPIError,
    VerdictAuthError,
    VerdictRateLimitError,
    VerdictValidationError
)

__all__ = [
    "VerdictClient",
    "AnalysisResponse",
    "MarketData",
    "SentimentData",
    "OnChainData",
    "PositionInfo",
    "Recommendation",
    "VerdictAPIError",
    "VerdictAuthError",
    "VerdictRateLimitError",
    "VerdictValidationError",
]

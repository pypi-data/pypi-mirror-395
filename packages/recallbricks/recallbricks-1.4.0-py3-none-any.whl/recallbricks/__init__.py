"""
RecallBricks Python SDK
The Memory Layer for AI

Usage with API key (user-level access):
    >>> from recallbricks import RecallBricks
    >>> memory = RecallBricks(api_key="rb_dev_xxx")
    >>> memory.save("Important information to remember")
    >>> memories = memory.get_all()

Usage with service token (server-to-server access):
    >>> from recallbricks import RecallBricks
    >>> memory = RecallBricks(service_token="rbk_service_xxx")
    >>> memory.save("Important information to remember")
    >>> memories = memory.get_all()
"""

from .client import RecallBricks
from .exceptions import (
    RecallBricksError,
    AuthenticationError,
    RateLimitError,
    APIError
)
from .types import (
    PredictedMemory,
    SuggestedMemory,
    LearningMetrics,
    LearningTrends,
    PatternAnalysis,
    WeightedSearchResult
)

__version__ = "1.1.1"
__all__ = [
    "RecallBricks",
    "RecallBricksError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "PredictedMemory",
    "SuggestedMemory",
    "LearningMetrics",
    "LearningTrends",
    "PatternAnalysis",
    "WeightedSearchResult"
]

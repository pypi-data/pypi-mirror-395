"""GradientCast Python SDK.

Official Python SDK for GradientCast ML Services:
- Time series forecasting (GradientCastFM)
- Anomaly detection (GradientCastPulseAD)
- Intelligent pattern anomaly detection (GradientCastDenseAD)

Quick Start:
    >>> from gradientcast import GradientCastFM
    >>>
    >>> fm = GradientCastFM(api_key="your-api-key")
    >>> result = fm.forecast(
    ...     input_data={"sales": [100, 120, 115, 130, 125, 140]},
    ...     horizon_len=7,
    ...     freq="D"
    ... )
    >>> print(result.forecast["sales"])

For more information, visit: https://github.com/GradientCast/gradientcast-sdk
"""

from ._version import __version__
from ._exceptions import (
    GradientCastError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    TimeoutError,
    APIError,
)
from .client import (
    GradientCastFM,
    GradientCastPulseAD,
    GradientCastDenseAD,
)
from .types import (
    # FM types
    ForecastResponse,
    ModelInfo,
    # AD types
    ADResponse,
    ADResult,
    ThresholdConfig,
    # DenseAD types
    DenseADResponse,
    TimelinePoint,
    MagnitudeInfo,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "GradientCastFM",
    "GradientCastPulseAD",
    "GradientCastDenseAD",
    # Exceptions
    "GradientCastError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "TimeoutError",
    "APIError",
    # FM types
    "ForecastResponse",
    "ModelInfo",
    # AD types
    "ADResponse",
    "ADResult",
    "ThresholdConfig",
    # DenseAD types
    "DenseADResponse",
    "TimelinePoint",
    "MagnitudeInfo",
]

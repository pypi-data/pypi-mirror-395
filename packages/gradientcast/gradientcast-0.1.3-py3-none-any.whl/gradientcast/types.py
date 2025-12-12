"""Response types and data classes for the GradientCast SDK."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =============================================================================
# FM (Forecasting) Response Types
# =============================================================================

@dataclass
class ModelInfo:
    """Metadata about the forecast model execution.

    Attributes:
        context_length: Length of the input time series used for context.
        requested_horizon_length: Number of future points requested.
        frequency: Time series frequency code (e.g., "H", "D", "W").
        used_covariates: Whether covariates were used in forecasting.
        processing_time: Server-side processing time in seconds.
    """
    context_length: int
    requested_horizon_length: int
    frequency: str
    used_covariates: bool
    processing_time: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelInfo":
        """Create ModelInfo from API response dictionary."""
        return cls(
            context_length=data.get("context_length", 0),
            requested_horizon_length=data.get("requested_horizon_length", 0),
            frequency=data.get("frequency", ""),
            used_covariates=data.get("used_covariates", False),
            processing_time=data.get("processing_time", 0.0)
        )


@dataclass
class ForecastResponse:
    """Response from the GradientCastFM forecasting endpoint.

    Attributes:
        forecast: Dictionary mapping series names to forecast values.
        model_info: Metadata about the forecast execution.
        raw: The raw API response dictionary.

    Example:
        >>> result = fm.forecast(data, horizon_len=10, freq="H")
        >>> print(result.forecast["my_series"])
        [145.2, 148.7, 151.3, ...]
        >>> print(result.model_info.processing_time)
        1.234
    """
    forecast: Dict[str, List[float]]
    model_info: ModelInfo
    raw: Dict[str, Any] = field(repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForecastResponse":
        """Create ForecastResponse from API response dictionary."""
        return cls(
            forecast=data.get("forecast", {}),
            model_info=ModelInfo.from_dict(data.get("model_info", {})),
            raw=data
        )

    def to_dataframe(self) -> "Any":
        """Convert forecast to a pandas DataFrame.

        Returns:
            DataFrame with columns: series, horizon_step, forecast

        Raises:
            ImportError: If pandas is not installed.

        Example:
            >>> df = result.to_dataframe()
            >>> print(df.head())
               series  horizon_step  forecast
            0  my_series          1     145.2
            1  my_series          2     148.7
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install with: pip install gradientcast[pandas]"
            )

        records = []
        for series_name, values in self.forecast.items():
            for i, value in enumerate(values):
                records.append({
                    "series": series_name,
                    "horizon_step": i + 1,
                    "forecast": value
                })

        return pd.DataFrame(records)

    def __getitem__(self, series_name: str) -> List[float]:
        """Get forecast for a specific series by name.

        Args:
            series_name: Name of the series.

        Returns:
            List of forecast values.

        Example:
            >>> result["my_series"]
            [145.2, 148.7, 151.3, ...]
        """
        return self.forecast[series_name]


# =============================================================================
# DenseAD Response Types
# =============================================================================

@dataclass
class MagnitudeInfo:
    """Magnitude metrics for an anomaly detection data point.

    Attributes:
        anomaly_score: Raw anomaly score from density analysis.
        normalized_score: Normalized anomaly score (0-100).
        zscore_24h: Z-score based on 24-hour rolling statistics.
        deviation_pct: Percentage deviation from expected value.
        severity: Severity level ("none", "low", "medium", "high", "critical").
        expected_value_24h: Expected value based on 24-hour rolling mean.
        std_dev_24h: Standard deviation based on 24-hour rolling window.
    """
    anomaly_score: float
    normalized_score: float
    zscore_24h: Optional[float]
    deviation_pct: float
    severity: str
    expected_value_24h: Optional[float]
    std_dev_24h: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MagnitudeInfo":
        """Create MagnitudeInfo from API response dictionary."""
        return cls(
            anomaly_score=data.get("lof_score", data.get("anomaly_score", 0.0)),
            normalized_score=data.get("normalized_score", 0.0),
            zscore_24h=data.get("zscore_24h"),
            deviation_pct=data.get("deviation_pct", 0.0),
            severity=data.get("severity", "none"),
            expected_value_24h=data.get("expected_value_24h"),
            std_dev_24h=data.get("std_dev_24h")
        )


@dataclass
class TimelinePoint:
    """A single point in the anomaly detection timeline.

    Attributes:
        timestamp: Timestamp of the data point.
        value: Actual observed value.
        raw_anomaly: Whether flagged as anomaly before filtering.
        confirmed_anomaly: Whether confirmed as anomaly after filtering.
        gap_filled: Whether this point was gap-filled.
        magnitude: Detailed magnitude metrics for this point.
    """
    timestamp: str
    value: int
    raw_anomaly: bool
    confirmed_anomaly: bool
    gap_filled: bool
    magnitude: MagnitudeInfo

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimelinePoint":
        """Create TimelinePoint from API response dictionary."""
        return cls(
            timestamp=data.get("datetime", ""),
            value=data.get("actual_value", 0),
            raw_anomaly=data.get("raw_anomaly", False),
            confirmed_anomaly=data.get("confirmed_anomaly", False),
            gap_filled=data.get("gap_filled", False),
            magnitude=MagnitudeInfo.from_dict(data.get("magnitude", {}))
        )


@dataclass
class DenseADResponse:
    """Response from the GradientCastDenseAD anomaly detection endpoint.

    Attributes:
        alert_status: Overall alert status ("no_alert" or "incident_active").
        alert_severity: Highest severity level of detected anomalies.
        model_used: Name of the detection algorithm used.
        timeline: List of timeline points with anomaly information.
        model_hyperparameters: Model hyperparameters used.
        valley_threshold_applied: Minimum value threshold applied.
        severity_thresholds: Severity classification thresholds.
        raw: The raw API response dictionary.

    Example:
        >>> result = ad.detect(data)
        >>> if result.has_anomaly:
        ...     print(f"Alert: {result.alert_severity}")
        ...     for point in result.anomalies:
        ...         print(f"  {point.timestamp}: {point.value}")
    """
    alert_status: str
    alert_severity: str
    model_used: str
    timeline: List[TimelinePoint]
    model_hyperparameters: Dict[str, Any]
    valley_threshold_applied: int
    severity_thresholds: Dict[str, float]
    raw: Dict[str, Any] = field(repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DenseADResponse":
        """Create DenseADResponse from API response dictionary."""
        timeline = [
            TimelinePoint.from_dict(point)
            for point in data.get("timeline", [])
        ]

        return cls(
            alert_status=data.get("alert_status", "no_alert"),
            alert_severity=data.get("alert_severity", "none"),
            model_used=data.get("model_used", ""),
            timeline=timeline,
            model_hyperparameters=data.get("model_hyperparameters", {}),
            valley_threshold_applied=data.get("valley_threshold_applied", 0),
            severity_thresholds=data.get("severity_thresholds", {}),
            raw=data
        )

    @property
    def has_anomaly(self) -> bool:
        """Check if any anomaly was detected.

        Returns:
            True if at least one anomaly was confirmed.
        """
        return self.alert_status == "incident_active"

    @property
    def anomalies(self) -> List[TimelinePoint]:
        """Get all confirmed anomaly points.

        Returns:
            List of TimelinePoint objects where confirmed_anomaly is True.
        """
        return [p for p in self.timeline if p.confirmed_anomaly]

    def to_dataframe(self) -> "Any":
        """Convert timeline to a pandas DataFrame.

        Returns:
            DataFrame with timeline data and magnitude metrics.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install with: pip install gradientcast[pandas]"
            )

        records = []
        for point in self.timeline:
            records.append({
                "timestamp": point.timestamp,
                "value": point.value,
                "raw_anomaly": point.raw_anomaly,
                "confirmed_anomaly": point.confirmed_anomaly,
                "gap_filled": point.gap_filled,
                "anomaly_score": point.magnitude.anomaly_score,
                "normalized_score": point.magnitude.normalized_score,
                "zscore_24h": point.magnitude.zscore_24h,
                "deviation_pct": point.magnitude.deviation_pct,
                "severity": point.magnitude.severity,
                "expected_value_24h": point.magnitude.expected_value_24h,
                "std_dev_24h": point.magnitude.std_dev_24h
            })

        return pd.DataFrame(records)


# =============================================================================
# PulseAD Response Types
# =============================================================================

@dataclass
class ThresholdConfig:
    """Configuration for AD anomaly thresholds.

    Attributes:
        default_percentage: Default percentage threshold for anomalies (0.0-1.0).
        default_minimum: Default minimum value threshold.
        per_dimension_overrides: Per-dimension threshold overrides.

    Example:
        >>> config = ThresholdConfig(
        ...     default_percentage=0.15,
        ...     default_minimum=100000,
        ...     per_dimension_overrides={
        ...         "AllUp": {"percentage_threshold": 0.10, "minimum_value_threshold": 3000000}
        ...     }
        ... )
    """
    default_percentage: float = 0.15
    default_minimum: int = 100000
    per_dimension_overrides: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to API payload format."""
        return {
            "default": {
                "percentage_threshold": self.default_percentage,
                "minimum_value_threshold": self.default_minimum
            },
            "per_dimension_overrides": self.per_dimension_overrides
        }


@dataclass
class ADResult:
    """A single result from AD anomaly detection.

    Attributes:
        timestamp: Timestamp of the data point.
        dimension: Dimension name this result belongs to.
        actual_value: Actual observed value.
        predicted_value: Forecasted/predicted value.
        delta: Difference between actual and predicted.
        percent_delta: Percentage deviation as a string (e.g., "16.13%").
        threshold: Applied threshold as a string (e.g., "10.00%").
        min_value_threshold: Minimum value threshold applied.
        is_anomaly: Whether this point is flagged as anomaly.
        time_of_report: Time when the report was generated.
    """
    timestamp: str
    dimension: str
    actual_value: float
    predicted_value: float
    delta: float
    percent_delta: str
    threshold: str
    min_value_threshold: int
    is_anomaly: bool
    time_of_report: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ADResult":
        """Create ADResult from API response dictionary."""
        return cls(
            timestamp=data.get("timestamp", ""),
            dimension=data.get("dimension", ""),
            actual_value=data.get("actual_value", 0.0),
            predicted_value=data.get("predicted_value", 0.0),
            delta=data.get("delta", 0.0),
            percent_delta=data.get("percent_delta", "0%"),
            threshold=data.get("threshold", "0%"),
            min_value_threshold=data.get("min_user_count", 0),
            is_anomaly=data.get("is_anomaly", False),
            time_of_report=data.get("time_of_report", "")
        )


@dataclass
class ADResponse:
    """Response from the GradientCastPulseAD endpoint.

    Attributes:
        results: List of detection results for each validated point.
        processing_time_ms: Total server-side processing time in milliseconds.
        fm_processing_time_ms: Time spent calling the FM endpoint in milliseconds.
        raw: The raw API response dictionary.

    Example:
        >>> result = ad.detect(time_series_data)
        >>> if result.has_anomaly:
        ...     for anomaly in result.anomalies:
        ...         print(f"{anomaly.dimension}: {anomaly.percent_delta} deviation")
    """
    results: List[ADResult]
    processing_time_ms: float
    fm_processing_time_ms: float
    raw: Dict[str, Any] = field(repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ADResponse":
        """Create ADResponse from API response dictionary."""
        results = [
            ADResult.from_dict(r)
            for r in data.get("results", [])
        ]

        return cls(
            results=results,
            processing_time_ms=data.get("processing_time_ms", 0.0),
            fm_processing_time_ms=data.get("fm_processing_time_ms", 0.0),
            raw=data
        )

    @property
    def has_anomaly(self) -> bool:
        """Check if any anomaly was detected.

        Returns:
            True if at least one result is flagged as anomaly.
        """
        return any(r.is_anomaly for r in self.results)

    @property
    def anomalies(self) -> List[ADResult]:
        """Get all anomalous results.

        Returns:
            List of ADResult objects where is_anomaly is True.
        """
        return [r for r in self.results if r.is_anomaly]

    def to_dataframe(self) -> "Any":
        """Convert results to a pandas DataFrame.

        Returns:
            DataFrame with detection results.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install with: pip install gradientcast[pandas]"
            )

        records = []
        for r in self.results:
            records.append({
                "timestamp": r.timestamp,
                "dimension": r.dimension,
                "actual_value": r.actual_value,
                "predicted_value": r.predicted_value,
                "delta": r.delta,
                "percent_delta": r.percent_delta,
                "threshold": r.threshold,
                "min_value_threshold": r.min_value_threshold,
                "is_anomaly": r.is_anomaly,
                "time_of_report": r.time_of_report
            })

        return pd.DataFrame(records)

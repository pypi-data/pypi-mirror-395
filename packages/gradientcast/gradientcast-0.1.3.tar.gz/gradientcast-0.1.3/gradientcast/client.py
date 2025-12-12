"""GradientCast client classes for FM, AD, and DenseAD endpoints."""

from typing import Any, Dict, List, Optional, Tuple, Union

from ._base import BaseClient
from ._exceptions import ValidationError
from .types import (
    ADResponse,
    DenseADResponse,
    ForecastResponse,
    ThresholdConfig,
)


class GradientCastFM(BaseClient):
    """Client for GradientCast Forecasting Model (FM).

    Provides time series forecasting using state-of-the-art foundation models.
    Supports single and multi-series forecasting with optional covariates.

    Example:
        >>> from gradientcast import GradientCastFM
        >>>
        >>> fm = GradientCastFM(api_key="your-api-key")
        >>> result = fm.forecast(
        ...     input_data={"daily_sales": [100, 120, 115, 130, 125, 140]},
        ...     horizon_len=7,
        ...     freq="D"
        ... )
        >>> print(result.forecast["daily_sales"])
        [145.2, 148.7, 151.3, ...]

    Args:
        api_key: Your GradientCast FM API key.
        environment: "production" (default) or "development".
        endpoint_url: Optional custom endpoint URL override.
        timeout: Request timeout in seconds (default 180).
        max_retries: Maximum retry attempts (default 3).
    """

    # Endpoint URLs
    PRODUCTION_URL = "https://gradientcastfm-prod-v1.eastus.inference.ml.azure.com/score"
    DEVELOPMENT_URL = "https://gradientcastfm-v1.eastus.inference.ml.azure.com/score"

    @property
    def endpoint_name(self) -> str:
        return "GradientCastFM"

    def _get_endpoint_urls(self) -> Tuple[str, str]:
        return (self.PRODUCTION_URL, self.DEVELOPMENT_URL)

    def forecast(
        self,
        input_data: Union[Dict[str, List[float]], List[float]],
        horizon_len: int,
        freq: str,
        *,
        xreg_mode: str = "xreg + timesfm",
        static_numerical_covariates: Optional[Dict[str, Dict[str, float]]] = None,
        static_categorical_covariates: Optional[Dict[str, Dict[str, str]]] = None,
        dynamic_numerical_covariates: Optional[Dict[str, Dict[str, List[float]]]] = None,
        dynamic_categorical_covariates: Optional[Dict[str, Dict[str, List[str]]]] = None
    ) -> ForecastResponse:
        """Generate time series forecasts.

        Args:
            input_data: Time series data. Can be either:
                - Dict mapping series names to value lists: {"series_a": [1, 2, 3]}
                - Single list for unnamed series: [1, 2, 3]
            horizon_len: Number of future time steps to forecast.
            freq: Frequency string:
                - "H" (hourly), "T"/"MIN" (minute)
                - "D" (daily), "B" (business day)
                - "W" (weekly)
                - "M" (monthly)
                - "Q" (quarterly)
                - "Y" (yearly)
            xreg_mode: Covariate processing mode (default "xreg + timesfm").
            static_numerical_covariates: Static numerical features per series.
                Format: {"feature_name": {"series_name": value}}
            static_categorical_covariates: Static categorical features per series.
                Format: {"feature_name": {"series_name": "category"}}
            dynamic_numerical_covariates: Time-varying numerical features.
                Format: {"feature_name": {"series_name": [values]}}
            dynamic_categorical_covariates: Time-varying categorical features.
                Format: {"feature_name": {"series_name": ["categories"]}}

        Returns:
            ForecastResponse containing forecasts and model metadata.

        Raises:
            ValidationError: If input validation fails.
            AuthenticationError: If API key is invalid.
            TimeoutError: If request times out.
            APIError: For other API errors.

        Example:
            >>> # Single series
            >>> result = fm.forecast([100, 120, 115, 130], horizon_len=7, freq="D")
            >>>
            >>> # Multiple series
            >>> result = fm.forecast(
            ...     input_data={
            ...         "product_a": [100, 120, 115, 130],
            ...         "product_b": [200, 220, 215, 230]
            ...     },
            ...     horizon_len=7,
            ...     freq="D"
            ... )
            >>>
            >>> # With covariates
            >>> result = fm.forecast(
            ...     input_data={"sales": [100, 120, 115, 130]},
            ...     horizon_len=7,
            ...     freq="D",
            ...     static_numerical_covariates={
            ...         "store_size": {"sales": 5000.0}
            ...     },
            ...     dynamic_numerical_covariates={
            ...         "temperature": {"sales": [72.0, 75.0, 78.0, 80.0, 82.0, 79.0, 76.0]}
            ...     }
            ... )
        """
        # Validate inputs
        if not input_data:
            raise ValidationError("input_data is required and cannot be empty")

        if horizon_len <= 0:
            raise ValidationError("horizon_len must be a positive integer")

        if not freq:
            raise ValidationError("freq is required")

        valid_freqs = {"H", "T", "MIN", "D", "B", "W", "M", "Q", "Y", "U"}
        if freq.upper() not in valid_freqs:
            raise ValidationError(
                f"Invalid freq '{freq}'. Must be one of: {', '.join(sorted(valid_freqs))}"
            )

        # Build payload
        payload: Dict[str, Any] = {
            "input_data": input_data,
            "horizon_len": horizon_len,
            "freq": freq,
            "xreg_mode": xreg_mode
        }

        # Add covariates if provided
        if static_numerical_covariates:
            payload["static_numerical_covariates"] = static_numerical_covariates

        if static_categorical_covariates:
            payload["static_categorical_covariates"] = static_categorical_covariates

        if dynamic_numerical_covariates:
            payload["dynamic_numerical_covariates"] = dynamic_numerical_covariates

        if dynamic_categorical_covariates:
            payload["dynamic_categorical_covariates"] = dynamic_categorical_covariates

        # Make request and parse response
        raw_response = self._make_request(payload)
        return ForecastResponse.from_dict(raw_response)

    def forecast_df(
        self,
        df: Any,
        value_column: str,
        horizon_len: int,
        freq: str,
        *,
        series_column: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """Generate forecasts from a pandas DataFrame.

        Args:
            df: Input DataFrame with historical data.
            value_column: Name of the column containing time series values.
            horizon_len: Number of future time steps to forecast.
            freq: Frequency string (see forecast() for options).
            series_column: Column name for series identifier (for multi-series).
                          If None, treats as single series.
            **kwargs: Additional arguments passed to forecast().

        Returns:
            DataFrame with forecasted values (columns: series, horizon_step, forecast).

        Raises:
            ImportError: If pandas is not installed.
            ValidationError: If input validation fails.

        Example:
            >>> import pandas as pd
            >>> df = pd.DataFrame({
            ...     "date": pd.date_range("2024-01-01", periods=30, freq="D"),
            ...     "sales": [100 + i*2 for i in range(30)],
            ...     "product": ["A"] * 30
            ... })
            >>> result_df = fm.forecast_df(
            ...     df, value_column="sales", series_column="product",
            ...     horizon_len=7, freq="D"
            ... )
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for forecast_df(). "
                "Install with: pip install gradientcast[pandas]"
            )

        # Convert DataFrame to input_data format
        if series_column is None:
            # Single series
            input_data = df[value_column].tolist()
        else:
            # Multiple series
            input_data = {}
            for series_name, group in df.groupby(series_column):
                input_data[str(series_name)] = group[value_column].tolist()

        result = self.forecast(input_data, horizon_len, freq, **kwargs)
        return result.to_dataframe()


class GradientCastDenseAD(BaseClient):
    """Client for GradientCast DenseAD - Intelligent Pattern Anomaly Detection.

    Detects anomalies in time series data using advanced density-based pattern
    analysis with configurable sensitivity and contiguity requirements.

    Note: DenseAD requires at least 25 data points for accurate detection
    due to rolling window feature calculations (12, 24, 48 hour windows).

    Example:
        >>> from gradientcast import GradientCastDenseAD
        >>> from datetime import datetime, timedelta
        >>>
        >>> ad = GradientCastDenseAD(api_key="your-api-key")
        >>>
        >>> # Generate 25+ hourly data points
        >>> base = datetime(2025, 1, 1)
        >>> data = [
        ...     {"timestamp": (base + timedelta(hours=i)).strftime("%m/%d/%Y, %I:%M %p"),
        ...      "value": 3000000 + i * 10000}
        ...     for i in range(25)
        ... ]
        >>> data[-1]["value"] = 500000  # Inject anomaly
        >>>
        >>> result = ad.detect(data)
        >>> if result.has_anomaly:
        ...     print(f"Alert: {result.alert_severity}")

    Args:
        api_key: Your GradientCast DenseAD API key.
        environment: "production" (default) or "development".
        endpoint_url: Optional custom endpoint URL override.
        timeout: Request timeout in seconds (default 180).
        max_retries: Maximum retry attempts (default 3).
    """

    # Endpoint URLs
    PRODUCTION_URL = "https://gradientcastdensead-prod-v1.eastus.inference.ml.azure.com/score"
    DEVELOPMENT_URL = "https://gradientcastdensead-v1.eastus.inference.ml.azure.com/score"

    # Default valley thresholds
    DEFAULT_VALLEY_THRESHOLD_ALLUP = 3_000_000
    DEFAULT_VALLEY_THRESHOLD_NONALLUP = 150_000

    # Minimum data points required for DenseAD (rolling windows use up to 48 hours)
    MIN_DATA_POINTS = 25

    @property
    def endpoint_name(self) -> str:
        return "GradientCastDenseAD"

    def _get_endpoint_urls(self) -> Tuple[str, str]:
        return (self.PRODUCTION_URL, self.DEVELOPMENT_URL)

    def _convert_to_api_format(
        self,
        data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Convert SDK format (timestamp/value) to API format (Date/UserCount)."""
        converted = []
        for point in data:
            # Accept both formats for flexibility
            if "Date" in point and "UserCount" in point:
                converted.append(point)
            elif "timestamp" in point and "value" in point:
                converted.append({
                    "Date": point["timestamp"],
                    "UserCount": int(point["value"])
                })
            else:
                raise ValidationError(
                    "Each data point must have 'timestamp' and 'value' keys "
                    "(or 'Date' and 'UserCount' for raw API format)"
                )
        return converted

    def detect(
        self,
        data: List[Dict[str, Any]],
        *,
        dimension_name: str = "AllUp",
        dimension_value: str = "AllUp",
        model_type: str = "LOF",
        return_window_hours: int = 24,
        valley_threshold: Optional[int] = None,
        contamination: float = 0.05,
        n_neighbors: int = 20,
        min_contiguous_anomalies: int = 2
    ) -> DenseADResponse:
        """Detect anomalies in time series data.

        Note: Requires at least 25 data points for accurate detection.

        Args:
            data: List of data points (minimum 25 required). Each point should have:
                - "timestamp": Datetime string (format: "MM/DD/YYYY, HH:MM AM/PM")
                - "value": Numeric value
            dimension_name: Dimension identifier (affects default thresholds).
                           Use "AllUp" for aggregate metrics.
            dimension_value: Dimension value for filtering.
            model_type: Detection algorithm variant (default is recommended).
            return_window_hours: Hours of data to return in the timeline.
            valley_threshold: Minimum value to consider for anomaly detection.
                            If None, uses 3M for "AllUp", 150K otherwise.
            contamination: Expected proportion of anomalies (0.0 to 0.5).
                          Lower values = fewer anomalies detected.
            n_neighbors: Number of neighbors for density calculation.
            min_contiguous_anomalies: Minimum consecutive anomalies required
                                     to confirm an alert.

        Returns:
            DenseADResponse with alert status and detailed timeline.

        Raises:
            ValidationError: If data is empty, malformed, or has fewer than 25 points.
            AuthenticationError: If API key is invalid.
            TimeoutError: If request times out.
            APIError: For other API errors.

        Example:
            >>> from datetime import datetime, timedelta
            >>> base = datetime(2025, 1, 1)
            >>> data = [
            ...     {"timestamp": (base + timedelta(hours=i)).strftime("%m/%d/%Y, %I:%M %p"),
            ...      "value": 3000000 + i * 10000}
            ...     for i in range(25)
            ... ]
            >>> data[-1]["value"] = 500000  # Inject anomaly
            >>>
            >>> result = ad.detect(data, contamination=0.05)
            >>> print(f"Status: {result.alert_status}")
            >>> print(f"Severity: {result.alert_severity}")
        """
        # Validate inputs
        if not data:
            raise ValidationError("data is required and cannot be empty")

        if not isinstance(data, list):
            raise ValidationError("data must be a list of dictionaries")

        if len(data) < self.MIN_DATA_POINTS:
            raise ValidationError(
                f"DenseAD requires at least {self.MIN_DATA_POINTS} data points for accurate "
                f"detection due to rolling window calculations. Received {len(data)} points."
            )

        if not 0.0 < contamination <= 0.5:
            raise ValidationError("contamination must be between 0.0 and 0.5")

        if n_neighbors < 1:
            raise ValidationError("n_neighbors must be at least 1")

        if min_contiguous_anomalies < 1:
            raise ValidationError("min_contiguous_anomalies must be at least 1")

        # Convert to API format (timestamp/value -> Date/UserCount)
        api_data = self._convert_to_api_format(data)

        # Build payload
        payload: Dict[str, Any] = {
            "new_data": api_data,
            "dimension_name": dimension_name,
            "dimension_value": dimension_value,
            "model_type": model_type,
            "return_window_hours": return_window_hours,
            "contamination": contamination,
            "n_neighbors": n_neighbors,
            "min_contiguous_anomalies": min_contiguous_anomalies
        }

        # Set valley threshold (use default based on dimension if not provided)
        if valley_threshold is not None:
            payload["valley_threshold"] = valley_threshold
        elif dimension_name == "AllUp":
            payload["valley_threshold"] = self.DEFAULT_VALLEY_THRESHOLD_ALLUP
        else:
            payload["valley_threshold"] = self.DEFAULT_VALLEY_THRESHOLD_NONALLUP

        # Make request and parse response
        raw_response = self._make_request(payload)
        return DenseADResponse.from_dict(raw_response)

    def detect_df(
        self,
        df: Any,
        timestamp_column: str = "timestamp",
        value_column: str = "value",
        **kwargs: Any
    ) -> DenseADResponse:
        """Detect anomalies from a pandas DataFrame.

        Args:
            df: Input DataFrame with time series data.
            timestamp_column: Name of the timestamp column.
            value_column: Name of the value column.
            **kwargs: Additional arguments passed to detect().

        Returns:
            DenseADResponse with detection results.

        Raises:
            ImportError: If pandas is not installed.

        Example:
            >>> import pandas as pd
            >>> df = pd.DataFrame({
            ...     "timestamp": ["01/01/2025, 12:00 AM", "01/01/2025, 01:00 AM"],
            ...     "value": [1500000, 1520000]
            ... })
            >>> result = ad.detect_df(df)
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for detect_df(). "
                "Install with: pip install gradientcast[pandas]"
            )

        # Convert DataFrame to list of dicts
        data = []
        for _, row in df.iterrows():
            ts = row[timestamp_column]
            # Handle pandas Timestamp
            if isinstance(ts, pd.Timestamp):
                ts = ts.strftime("%m/%d/%Y, %I:%M %p")
            data.append({
                "timestamp": str(ts),
                "value": int(row[value_column])
            })

        return self.detect(data, **kwargs)


class GradientCastPulseAD(BaseClient):
    """Client for GradientCast PulseAD - Intelligent Anomaly Detection.

    Detects anomalies by analyzing time series patterns and identifying
    significant deviations from expected behavior using dual-threshold logic.

    Example:
        >>> from gradientcast import GradientCastPulseAD
        >>>
        >>> ad = GradientCastPulseAD(api_key="your-api-key")
        >>> result = ad.detect(
        ...     time_series_data={
        ...         "user_count": [
        ...             {"timestamp": "01/01/2025, 12:00 AM", "value": 1500000.0},
        ...             {"timestamp": "01/01/2025, 01:00 AM", "value": 1520000.0},
        ...             # ... more data points (at least 6 for default settings)
        ...         ]
        ...     }
        ... )
        >>>
        >>> if result.has_anomaly:
        ...     for anomaly in result.anomalies:
        ...         print(f"{anomaly.dimension}: {anomaly.percent_delta} deviation")

    Args:
        api_key: Your GradientCast PulseAD API key.
        environment: "production" (default) or "development".
        endpoint_url: Optional custom endpoint URL override.
        timeout: Request timeout in seconds (default 180).
        max_retries: Maximum retry attempts (default 3).
    """

    # Endpoint URLs
    PRODUCTION_URL = "https://gradientcastad-prod-v1.eastus.inference.ml.azure.com/score"
    DEVELOPMENT_URL = "https://gradientcastad-v1.eastus.inference.ml.azure.com/score"

    # FM endpoint URLs (for dev/testing when server-side auth not available)
    FM_PRODUCTION_URL = "https://gradientcastfm-prod-v1.eastus.inference.ml.azure.com/score"
    FM_DEVELOPMENT_URL = "https://gradientcastfm-v1.eastus.inference.ml.azure.com/score"

    @property
    def endpoint_name(self) -> str:
        return "GradientCastPulseAD"

    def _get_endpoint_urls(self) -> Tuple[str, str]:
        return (self.PRODUCTION_URL, self.DEVELOPMENT_URL)

    def detect(
        self,
        time_series_data: Dict[str, List[Dict[str, Any]]],
        *,
        frequency: str = "H",
        forecast_horizon: int = 3,
        validation_points: int = 3,
        threshold_config: Optional[ThresholdConfig] = None,
        fm_api_key: Optional[str] = None,
        fm_endpoint_url: Optional[str] = None
    ) -> ADResponse:
        """Detect anomalies in time series data.

        Analyzes time series patterns to identify significant deviations
        from expected behavior using dual-threshold logic.

        Args:
            time_series_data: Dictionary mapping dimension names to lists
                            of data points. Each point needs:
                            - "timestamp": Datetime string
                            - "value": Numeric value
            frequency: Data frequency:
                - "H" (hourly, default)
                - "D" (daily)
                - "W" (weekly)
                - "M" (monthly)
                - "Q" (quarterly)
                - "Y" (yearly)
            forecast_horizon: Number of points to forecast ahead (default 3).
            validation_points: Number of latest points to validate against
                             forecasts (default 3, typically equals forecast_horizon).
            threshold_config: Custom threshold configuration. If None, uses:
                - Default percentage threshold: 15%
                - Default minimum value: 100,000 (3M for AllUp dimension)
            fm_api_key: Optional FM endpoint API key (only needed for
                       dev/testing when server-side auth is not configured).
            fm_endpoint_url: Optional FM endpoint URL override (only needed
                            for dev/testing).

        Returns:
            ADResponse with per-point detection results.

        Raises:
            ValidationError: If input validation fails.
            AuthenticationError: If API key is invalid.
            TimeoutError: If request times out.
            APIError: For other API errors.

        Example:
            >>> # Basic usage
            >>> result = tsfad.detect(
            ...     time_series_data={
            ...         "AllUp": [
            ...             {"timestamp": "01/01/2025, 12:00 AM", "value": 1500000.0},
            ...             {"timestamp": "01/01/2025, 01:00 AM", "value": 1520000.0},
            ...             # ... at least 6 points for default settings
            ...         ]
            ...     }
            ... )
            >>>
            >>> # With custom thresholds
            >>> from gradientcast import ThresholdConfig
            >>> config = ThresholdConfig(
            ...     default_percentage=0.20,  # 20% threshold
            ...     default_minimum=50000,
            ...     per_dimension_overrides={
            ...         "AllUp": {
            ...             "percentage_threshold": 0.10,
            ...             "minimum_value_threshold": 3000000
            ...         }
            ...     }
            ... )
            >>> result = tsfad.detect(time_series_data, threshold_config=config)
        """
        # Validate inputs
        if not time_series_data:
            raise ValidationError("time_series_data is required and cannot be empty")

        if not isinstance(time_series_data, dict):
            raise ValidationError("time_series_data must be a dictionary")

        valid_freqs = {"H", "D", "W", "M", "Q", "Y"}
        if frequency.upper() not in valid_freqs:
            raise ValidationError(
                f"Invalid frequency '{frequency}'. Must be one of: {', '.join(sorted(valid_freqs))}"
            )

        if forecast_horizon < 1:
            raise ValidationError("forecast_horizon must be at least 1")

        if validation_points < 1:
            raise ValidationError("validation_points must be at least 1")

        # Validate each dimension has enough data points
        min_points = validation_points + 1  # Need at least 1 training point
        for dimension, points in time_series_data.items():
            if len(points) < min_points:
                raise ValidationError(
                    f"Dimension '{dimension}' has {len(points)} points but needs "
                    f"at least {min_points} (validation_points + 1)"
                )

        # Build payload
        payload: Dict[str, Any] = {
            "time_series_data": time_series_data,
            "frequency": frequency,
            "forecast_horizon": forecast_horizon,
            "validation_points": validation_points
        }

        # Add threshold config if provided
        if threshold_config:
            payload["threshold_config"] = threshold_config.to_dict()

        # Add FM credentials if provided (for dev/testing)
        if fm_api_key:
            payload["fm_api_key"] = fm_api_key

            # Set FM endpoint URL
            if fm_endpoint_url:
                payload["fm_endpoint_url"] = fm_endpoint_url
            else:
                # Use matching environment
                payload["fm_endpoint_url"] = (
                    self.FM_PRODUCTION_URL if self.environment == "production"
                    else self.FM_DEVELOPMENT_URL
                )

        # Make request and parse response
        raw_response = self._make_request(payload)
        return ADResponse.from_dict(raw_response)

    def detect_df(
        self,
        df: Any,
        timestamp_column: str = "timestamp",
        value_column: str = "value",
        dimension_column: Optional[str] = None,
        **kwargs: Any
    ) -> ADResponse:
        """Detect anomalies from a pandas DataFrame.

        Args:
            df: Input DataFrame with time series data.
            timestamp_column: Name of the timestamp column.
            value_column: Name of the value column.
            dimension_column: Column for dimension names. If None,
                            uses "default" as dimension name.
            **kwargs: Additional arguments passed to detect().

        Returns:
            ADResponse with detection results.

        Raises:
            ImportError: If pandas is not installed.

        Example:
            >>> import pandas as pd
            >>> df = pd.DataFrame({
            ...     "timestamp": ["01/01/2025, 12:00 AM", ...],
            ...     "value": [1500000.0, ...],
            ...     "region": ["AllUp", ...]
            ... })
            >>> result = tsfad.detect_df(
            ...     df,
            ...     dimension_column="region"
            ... )
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for detect_df(). "
                "Install with: pip install gradientcast[pandas]"
            )

        # Convert DataFrame to time_series_data format
        if dimension_column is None:
            # Single dimension
            points = []
            for _, row in df.iterrows():
                ts = row[timestamp_column]
                if isinstance(ts, pd.Timestamp):
                    ts = ts.strftime("%m/%d/%Y, %I:%M %p")
                points.append({
                    "timestamp": str(ts),
                    "value": float(row[value_column])
                })
            time_series_data = {"default": points}
        else:
            # Multiple dimensions
            time_series_data = {}
            for dimension, group in df.groupby(dimension_column):
                points = []
                for _, row in group.iterrows():
                    ts = row[timestamp_column]
                    if isinstance(ts, pd.Timestamp):
                        ts = ts.strftime("%m/%d/%Y, %I:%M %p")
                    points.append({
                        "timestamp": str(ts),
                        "value": float(row[value_column])
                    })
                time_series_data[str(dimension)] = points

        return self.detect(time_series_data, **kwargs)

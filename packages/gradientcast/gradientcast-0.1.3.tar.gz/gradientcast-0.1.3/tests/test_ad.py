"""Tests for GradientCastPulseAD client."""

import pytest
import responses

from gradientcast import GradientCastPulseAD, ADResponse, ThresholdConfig, ValidationError


class TestGradientCastPulseADInit:
    """Tests for GradientCastPulseAD initialization."""

    def test_init_with_api_key(self):
        """Test basic initialization with API key."""
        ad = GradientCastPulseAD(api_key="test-key")
        assert ad.api_key == "test-key"
        assert ad.environment == "production"
        assert "prod" in ad.endpoint_url

    def test_init_development_environment(self):
        """Test initialization with development environment."""
        ad = GradientCastPulseAD(api_key="test-key", environment="development")
        assert ad.environment == "development"
        assert "prod" not in ad.endpoint_url


class TestGradientCastPulseADDetect:
    """Tests for GradientCastPulseAD.detect() method."""

    @responses.activate
    def test_detect_success_with_anomaly(self, ad_success_response, sample_ad_input):
        """Test successful detection with anomaly found."""
        responses.add(
            responses.POST,
            GradientCastPulseAD.PRODUCTION_URL,
            json=ad_success_response,
            status=200
        )

        ad = GradientCastPulseAD(api_key="test-key")
        result = ad.detect(time_series_data=sample_ad_input)

        assert isinstance(result, ADResponse)
        assert result.has_anomaly is True
        assert len(result.anomalies) == 1
        assert result.anomalies[0].is_anomaly is True

    @responses.activate
    def test_detect_success_no_anomaly(
        self, ad_no_anomaly_response, sample_ad_input
    ):
        """Test successful detection with no anomalies."""
        responses.add(
            responses.POST,
            GradientCastPulseAD.PRODUCTION_URL,
            json=ad_no_anomaly_response,
            status=200
        )

        ad = GradientCastPulseAD(api_key="test-key")
        result = ad.detect(time_series_data=sample_ad_input)

        assert isinstance(result, ADResponse)
        assert result.has_anomaly is False
        assert len(result.anomalies) == 0

    def test_detect_empty_data_raises(self):
        """Test that empty data raises ValidationError."""
        ad = GradientCastPulseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="time_series_data is required"):
            ad.detect(time_series_data={})

    def test_detect_invalid_frequency_raises(self):
        """Test that invalid frequency raises ValidationError."""
        ad = GradientCastPulseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="Invalid frequency"):
            ad.detect(
                time_series_data={"dim": [{"timestamp": "...", "value": 1.0}] * 10},
                frequency="X"
            )

    def test_detect_invalid_forecast_horizon_raises(self):
        """Test that invalid forecast_horizon raises ValidationError."""
        ad = GradientCastPulseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="forecast_horizon must be"):
            ad.detect(
                time_series_data={"dim": [{"timestamp": "...", "value": 1.0}] * 10},
                forecast_horizon=0
            )

    def test_detect_insufficient_data_raises(self):
        """Test that insufficient data points raises ValidationError."""
        ad = GradientCastPulseAD(api_key="test-key")

        # Default validation_points=3, so need at least 4 points
        with pytest.raises(ValidationError, match="has .* points but needs"):
            ad.detect(
                time_series_data={
                    "dim": [
                        {"timestamp": "01/01/2025, 12:00 AM", "value": 1.0},
                        {"timestamp": "01/01/2025, 01:00 AM", "value": 2.0},
                    ]
                }
            )

    @responses.activate
    def test_detect_with_threshold_config(
        self, ad_success_response, sample_ad_input
    ):
        """Test detection with custom threshold configuration."""
        responses.add(
            responses.POST,
            GradientCastPulseAD.PRODUCTION_URL,
            json=ad_success_response,
            status=200
        )

        config = ThresholdConfig(
            default_percentage=0.20,
            default_minimum=50000,
            per_dimension_overrides={
                "AllUp": {
                    "percentage_threshold": 0.10,
                    "minimum_value_threshold": 3000000
                }
            }
        )

        ad = GradientCastPulseAD(api_key="test-key")
        result = ad.detect(
            time_series_data=sample_ad_input,
            threshold_config=config
        )

        # Check the request payload
        request_body = responses.calls[0].request.body
        import json
        payload = json.loads(request_body)

        assert "threshold_config" in payload
        assert payload["threshold_config"]["default"]["percentage_threshold"] == 0.20
        assert "AllUp" in payload["threshold_config"]["per_dimension_overrides"]

    @responses.activate
    def test_detect_with_fm_credentials(
        self, ad_success_response, sample_ad_input
    ):
        """Test detection with optional FM credentials (for dev/testing)."""
        responses.add(
            responses.POST,
            GradientCastPulseAD.PRODUCTION_URL,
            json=ad_success_response,
            status=200
        )

        ad = GradientCastPulseAD(api_key="test-key")
        result = ad.detect(
            time_series_data=sample_ad_input,
            fm_api_key="fm-test-key",
            fm_endpoint_url="https://custom-fm.endpoint.com/score"
        )

        # Check the request payload
        request_body = responses.calls[0].request.body
        import json
        payload = json.loads(request_body)

        assert payload["fm_api_key"] == "fm-test-key"
        assert payload["fm_endpoint_url"] == "https://custom-fm.endpoint.com/score"


class TestThresholdConfig:
    """Tests for ThresholdConfig dataclass."""

    def test_default_values(self):
        """Test default threshold values."""
        config = ThresholdConfig()
        assert config.default_percentage == 0.15
        assert config.default_minimum == 100000
        assert config.per_dimension_overrides == {}

    def test_custom_values(self):
        """Test custom threshold values."""
        config = ThresholdConfig(
            default_percentage=0.20,
            default_minimum=50000,
            per_dimension_overrides={"AllUp": {"percentage_threshold": 0.10}}
        )
        assert config.default_percentage == 0.20
        assert config.default_minimum == 50000

    def test_to_dict(self):
        """Test conversion to API payload format."""
        config = ThresholdConfig(
            default_percentage=0.15,
            default_minimum=100000,
            per_dimension_overrides={"AllUp": {"percentage_threshold": 0.10}}
        )
        result = config.to_dict()

        assert result["default"]["percentage_threshold"] == 0.15
        assert result["default"]["minimum_value_threshold"] == 100000
        assert "AllUp" in result["per_dimension_overrides"]


class TestADResponse:
    """Tests for ADResponse dataclass."""

    def test_has_anomaly_true(self, ad_success_response):
        """Test has_anomaly property when anomalies exist."""
        response = ADResponse.from_dict(ad_success_response)
        assert response.has_anomaly is True

    def test_has_anomaly_false(self, ad_no_anomaly_response):
        """Test has_anomaly property when no anomalies."""
        response = ADResponse.from_dict(ad_no_anomaly_response)
        assert response.has_anomaly is False

    def test_anomalies_property(self, ad_success_response):
        """Test anomalies property returns only anomalous results."""
        response = ADResponse.from_dict(ad_success_response)
        anomalies = response.anomalies

        assert len(anomalies) == 1
        assert all(a.is_anomaly for a in anomalies)

    def test_processing_times(self, ad_success_response):
        """Test processing time properties."""
        response = ADResponse.from_dict(ad_success_response)

        assert response.processing_time_ms == 523.45
        assert response.fm_processing_time_ms == 450.12

    def test_to_dataframe(self, ad_success_response):
        """Test conversion to DataFrame."""
        pytest.importorskip("pandas")

        response = ADResponse.from_dict(ad_success_response)
        df = response.to_dataframe()

        assert len(df) == 2
        assert "timestamp" in df.columns
        assert "dimension" in df.columns
        assert "is_anomaly" in df.columns
        assert "percent_delta" in df.columns

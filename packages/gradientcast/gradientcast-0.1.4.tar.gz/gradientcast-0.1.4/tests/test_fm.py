"""Tests for GradientCastFM client."""

import json

import pytest
import responses

from gradientcast import GradientCastFM, ForecastResponse, ValidationError, AuthenticationError


class TestGradientCastFMInit:
    """Tests for GradientCastFM initialization."""

    def test_init_with_api_key(self):
        """Test basic initialization with API key."""
        fm = GradientCastFM(api_key="test-key")
        assert fm.api_key == "test-key"
        assert fm.environment == "production"
        assert "prod" in fm.endpoint_url

    def test_init_development_environment(self):
        """Test initialization with development environment."""
        fm = GradientCastFM(api_key="test-key", environment="development")
        assert fm.environment == "development"
        assert "prod" not in fm.endpoint_url

    def test_init_custom_endpoint(self):
        """Test initialization with custom endpoint URL."""
        custom_url = "https://custom.endpoint.com/score"
        fm = GradientCastFM(api_key="test-key", endpoint_url=custom_url)
        assert fm.endpoint_url == custom_url

    def test_init_custom_timeout(self):
        """Test initialization with custom timeout."""
        fm = GradientCastFM(api_key="test-key", timeout=300)
        assert fm.timeout == 300

    def test_init_custom_max_retries(self):
        """Test initialization with custom max retries."""
        fm = GradientCastFM(api_key="test-key", max_retries=5)
        assert fm.max_retries == 5

    def test_init_empty_api_key_raises(self):
        """Test that empty API key raises ValueError."""
        with pytest.raises(ValueError, match="api_key is required"):
            GradientCastFM(api_key="")

    def test_init_invalid_environment_raises(self):
        """Test that invalid environment raises ValueError."""
        with pytest.raises(ValueError, match="Invalid environment"):
            GradientCastFM(api_key="test-key", environment="staging")


class TestGradientCastFMForecast:
    """Tests for GradientCastFM.forecast() method."""

    @responses.activate
    def test_forecast_success(self, fm_success_response, sample_fm_input):
        """Test successful forecast request."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=fm_success_response,
            status=200
        )

        fm = GradientCastFM(api_key="test-key")
        result = fm.forecast(
            input_data=sample_fm_input,
            horizon_len=7,
            freq="D"
        )

        assert isinstance(result, ForecastResponse)
        assert "series_a" in result.forecast
        assert "series_b" in result.forecast
        assert len(result.forecast["series_a"]) == 7
        assert result.model_info.frequency == "D"

    @responses.activate
    def test_forecast_single_series(self, fm_single_series_response):
        """Test forecast with single series (list input)."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=fm_single_series_response,
            status=200
        )

        fm = GradientCastFM(api_key="test-key")
        result = fm.forecast(
            input_data=[100, 120, 115, 130, 125, 140],
            horizon_len=5,
            freq="H"
        )

        assert isinstance(result, ForecastResponse)
        assert "default" in result.forecast
        assert len(result.forecast["default"]) == 5

    @responses.activate
    def test_forecast_double_encoded_json(self, fm_success_response, sample_fm_input):
        """Test handling of double-encoded JSON response (Azure ML quirk)."""
        # Return double-encoded JSON
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=json.dumps(fm_success_response),  # Double encode
            status=200
        )

        fm = GradientCastFM(api_key="test-key")
        result = fm.forecast(
            input_data=sample_fm_input,
            horizon_len=7,
            freq="D"
        )

        assert isinstance(result, ForecastResponse)
        assert "series_a" in result.forecast

    def test_forecast_empty_input_raises(self):
        """Test that empty input raises ValidationError."""
        fm = GradientCastFM(api_key="test-key")

        with pytest.raises(ValidationError, match="input_data is required"):
            fm.forecast(input_data={}, horizon_len=7, freq="D")

    def test_forecast_invalid_horizon_raises(self):
        """Test that invalid horizon_len raises ValidationError."""
        fm = GradientCastFM(api_key="test-key")

        with pytest.raises(ValidationError, match="horizon_len must be a positive"):
            fm.forecast(input_data={"a": [1, 2, 3]}, horizon_len=0, freq="D")

    def test_forecast_invalid_freq_raises(self):
        """Test that invalid frequency raises ValidationError."""
        fm = GradientCastFM(api_key="test-key")

        with pytest.raises(ValidationError, match="Invalid freq"):
            fm.forecast(input_data={"a": [1, 2, 3]}, horizon_len=7, freq="X")

    @responses.activate
    def test_forecast_auth_error(self, error_response_auth, sample_fm_input):
        """Test authentication error handling."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=error_response_auth,
            status=401
        )

        fm = GradientCastFM(api_key="invalid-key")

        with pytest.raises(AuthenticationError):
            fm.forecast(input_data=sample_fm_input, horizon_len=7, freq="D")


class TestForecastResponse:
    """Tests for ForecastResponse dataclass."""

    def test_to_dataframe(self, fm_success_response):
        """Test conversion to DataFrame."""
        pytest.importorskip("pandas")

        response = ForecastResponse.from_dict(fm_success_response)
        df = response.to_dataframe()

        assert len(df) == 14  # 7 points * 2 series
        assert "series" in df.columns
        assert "horizon_step" in df.columns
        assert "forecast" in df.columns

    def test_getitem(self, fm_success_response):
        """Test dictionary-style access."""
        response = ForecastResponse.from_dict(fm_success_response)

        assert response["series_a"] == response.forecast["series_a"]
        assert len(response["series_a"]) == 7

    def test_raw_preserved(self, fm_success_response):
        """Test that raw response is preserved."""
        response = ForecastResponse.from_dict(fm_success_response)
        assert response.raw == fm_success_response

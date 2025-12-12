"""Tests for GradientCastDenseAD client."""

import pytest
import responses

from gradientcast import GradientCastDenseAD, DenseADResponse, ValidationError


class TestGradientCastDenseADInit:
    """Tests for GradientCastDenseAD initialization."""

    def test_init_with_api_key(self):
        """Test basic initialization with API key."""
        ad = GradientCastDenseAD(api_key="test-key")
        assert ad.api_key == "test-key"
        assert ad.environment == "production"
        assert "prod" in ad.endpoint_url

    def test_init_development_environment(self):
        """Test initialization with development environment."""
        ad = GradientCastDenseAD(api_key="test-key", environment="development")
        assert ad.environment == "development"
        assert "prod" not in ad.endpoint_url


class TestGradientCastDenseADDetect:
    """Tests for GradientCastDenseAD.detect() method."""

    @responses.activate
    def test_detect_success_with_anomaly(self, dense_ad_success_response, sample_dense_ad_input):
        """Test successful detection with anomaly found."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_success_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        result = ad.detect(data=sample_dense_ad_input)

        assert isinstance(result, DenseADResponse)
        assert result.has_anomaly is True
        assert result.alert_status == "incident_active"
        assert result.alert_severity == "medium"
        assert len(result.anomalies) == 1

    @responses.activate
    def test_detect_success_no_anomaly(self, dense_ad_no_anomaly_response, sample_dense_ad_input):
        """Test successful detection with no anomalies."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_no_anomaly_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        result = ad.detect(data=sample_dense_ad_input)

        assert isinstance(result, DenseADResponse)
        assert result.has_anomaly is False
        assert result.alert_status == "no_alert"
        assert len(result.anomalies) == 0

    def test_detect_empty_data_raises(self):
        """Test that empty data raises ValidationError."""
        ad = GradientCastDenseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="data is required"):
            ad.detect(data=[])

    def test_detect_invalid_contamination_raises(self):
        """Test that invalid contamination raises ValidationError."""
        ad = GradientCastDenseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="contamination must be"):
            ad.detect(
                data=[{"timestamp": "01/01/2025, 12:00 AM", "value": 100}],
                contamination=0.6
            )

    def test_detect_invalid_n_neighbors_raises(self):
        """Test that invalid n_neighbors raises ValidationError."""
        ad = GradientCastDenseAD(api_key="test-key")

        with pytest.raises(ValidationError, match="n_neighbors must be"):
            ad.detect(
                data=[{"timestamp": "01/01/2025, 12:00 AM", "value": 100}],
                n_neighbors=0
            )

    @responses.activate
    def test_detect_converts_timestamp_value_to_api_format(
        self, dense_ad_success_response, sample_dense_ad_input
    ):
        """Test that SDK format is converted to API format."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_success_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        result = ad.detect(data=sample_dense_ad_input)

        # Check the request payload
        request_body = responses.calls[0].request.body
        import json
        payload = json.loads(request_body)

        # Verify conversion happened
        assert "new_data" in payload
        assert "Date" in payload["new_data"][0]
        assert "UserCount" in payload["new_data"][0]

    @responses.activate
    def test_detect_accepts_raw_api_format(self, dense_ad_success_response):
        """Test that raw API format (Date/UserCount) is also accepted."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_success_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        raw_format_data = [
            {"Date": "01/01/2025, 12:00 AM", "UserCount": 1500000},
            {"Date": "01/01/2025, 01:00 AM", "UserCount": 1520000},
        ]
        result = ad.detect(data=raw_format_data)

        assert isinstance(result, DenseADResponse)

    @responses.activate
    def test_detect_default_valley_threshold_allup(
        self, dense_ad_success_response, sample_dense_ad_input
    ):
        """Test default valley threshold for AllUp dimension."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_success_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        ad.detect(data=sample_dense_ad_input, dimension_name="AllUp")

        # Check the request payload
        request_body = responses.calls[0].request.body
        import json
        payload = json.loads(request_body)

        assert payload["valley_threshold"] == 3_000_000

    @responses.activate
    def test_detect_default_valley_threshold_non_allup(
        self, dense_ad_success_response, sample_dense_ad_input
    ):
        """Test default valley threshold for non-AllUp dimension."""
        responses.add(
            responses.POST,
            GradientCastDenseAD.PRODUCTION_URL,
            json=dense_ad_success_response,
            status=200
        )

        ad = GradientCastDenseAD(api_key="test-key")
        ad.detect(data=sample_dense_ad_input, dimension_name="Region_East")

        # Check the request payload
        request_body = responses.calls[0].request.body
        import json
        payload = json.loads(request_body)

        assert payload["valley_threshold"] == 150_000


class TestDenseADResponse:
    """Tests for DenseADResponse dataclass."""

    def test_has_anomaly_true(self, dense_ad_success_response):
        """Test has_anomaly property when anomalies exist."""
        response = DenseADResponse.from_dict(dense_ad_success_response)
        assert response.has_anomaly is True

    def test_has_anomaly_false(self, dense_ad_no_anomaly_response):
        """Test has_anomaly property when no anomalies."""
        response = DenseADResponse.from_dict(dense_ad_no_anomaly_response)
        assert response.has_anomaly is False

    def test_anomalies_property(self, dense_ad_success_response):
        """Test anomalies property returns only confirmed anomalies."""
        response = DenseADResponse.from_dict(dense_ad_success_response)
        anomalies = response.anomalies

        assert len(anomalies) == 1
        assert all(a.confirmed_anomaly for a in anomalies)

    def test_to_dataframe(self, dense_ad_success_response):
        """Test conversion to DataFrame."""
        pytest.importorskip("pandas")

        response = DenseADResponse.from_dict(dense_ad_success_response)
        df = response.to_dataframe()

        assert len(df) == 2
        assert "timestamp" in df.columns
        assert "confirmed_anomaly" in df.columns
        assert "severity" in df.columns

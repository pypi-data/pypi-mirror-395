"""Tests for base client functionality."""

import json

import pytest
import responses

from gradientcast import GradientCastFM
from gradientcast._exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)


class TestBaseClientRetry:
    """Tests for retry logic in BaseClient."""

    @responses.activate
    def test_retry_on_500(self, fm_success_response, sample_fm_input):
        """Test retry on 500 error."""
        # First call fails, second succeeds
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json={"error": "Internal Server Error"},
            status=500
        )
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=fm_success_response,
            status=200
        )

        fm = GradientCastFM(api_key="test-key", max_retries=3)
        result = fm.forecast(
            input_data=sample_fm_input,
            horizon_len=7,
            freq="D"
        )

        assert len(responses.calls) == 2
        assert "series_a" in result.forecast

    @responses.activate
    def test_retry_on_429_rate_limit(self, fm_success_response, sample_fm_input):
        """Test retry on 429 rate limit error."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json={"error": "Rate limit exceeded"},
            status=429,
            headers={"Retry-After": "1"}
        )
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=fm_success_response,
            status=200
        )

        fm = GradientCastFM(api_key="test-key", max_retries=3)
        result = fm.forecast(
            input_data=sample_fm_input,
            horizon_len=7,
            freq="D"
        )

        assert len(responses.calls) == 2

    @responses.activate
    def test_no_retry_on_auth_error(self, sample_fm_input):
        """Test no retry on authentication error."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json={"error": "Authentication failed"},
            status=401
        )

        fm = GradientCastFM(api_key="invalid-key", max_retries=3)

        with pytest.raises(AuthenticationError):
            fm.forecast(
                input_data=sample_fm_input,
                horizon_len=7,
                freq="D"
            )

        # Should only have made one request (no retry)
        assert len(responses.calls) == 1

    @responses.activate
    def test_no_retry_on_validation_error(self, sample_fm_input):
        """Test no retry on validation error."""
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json={"error": "ValidationError", "message": "Invalid input"},
            status=400
        )

        fm = GradientCastFM(api_key="test-key", max_retries=3)

        with pytest.raises(ValidationError):
            fm.forecast(
                input_data=sample_fm_input,
                horizon_len=7,
                freq="D"
            )

        # Should only have made one request (no retry)
        assert len(responses.calls) == 1

    @responses.activate
    def test_max_retries_exceeded(self, sample_fm_input):
        """Test that error is raised after max retries exceeded."""
        # All calls fail
        for _ in range(4):  # max_retries + 1
            responses.add(
                responses.POST,
                GradientCastFM.PRODUCTION_URL,
                json={"error": "Internal Server Error"},
                status=500
            )

        fm = GradientCastFM(api_key="test-key", max_retries=3)

        with pytest.raises(APIError):
            fm.forecast(
                input_data=sample_fm_input,
                horizon_len=7,
                freq="D"
            )

        # Should have made max_retries + 1 requests
        assert len(responses.calls) == 4


class TestBaseClientContextManager:
    """Tests for context manager functionality."""

    def test_context_manager_closes_session(self):
        """Test that context manager closes session on exit."""
        with GradientCastFM(api_key="test-key") as fm:
            # Force session creation
            _ = fm._get_session()
            assert fm._session is not None

        # Session should be closed
        assert fm._session is None

    def test_manual_close(self):
        """Test manual session close."""
        fm = GradientCastFM(api_key="test-key")
        _ = fm._get_session()
        assert fm._session is not None

        fm.close()
        assert fm._session is None


class TestBaseClientRepr:
    """Tests for string representation."""

    def test_repr_production(self):
        """Test repr for production environment."""
        fm = GradientCastFM(api_key="test-key")
        repr_str = repr(fm)

        assert "GradientCastFM" in repr_str
        assert "production" in repr_str
        assert "prod" in repr_str

    def test_repr_development(self):
        """Test repr for development environment."""
        fm = GradientCastFM(api_key="test-key", environment="development")
        repr_str = repr(fm)

        assert "GradientCastFM" in repr_str
        assert "development" in repr_str


class TestDoubleEncodedJson:
    """Tests for double-encoded JSON handling."""

    @responses.activate
    def test_handles_double_encoded_response(self, fm_success_response, sample_fm_input):
        """Test that double-encoded JSON responses are handled correctly."""
        # Return double-encoded JSON (Azure ML quirk)
        double_encoded = json.dumps(fm_success_response)
        responses.add(
            responses.POST,
            GradientCastFM.PRODUCTION_URL,
            json=double_encoded,
            status=200
        )

        fm = GradientCastFM(api_key="test-key")
        result = fm.forecast(
            input_data=sample_fm_input,
            horizon_len=7,
            freq="D"
        )

        assert "series_a" in result.forecast

    @responses.activate
    def test_handles_normal_response(self, fm_success_response, sample_fm_input):
        """Test that normal JSON responses are also handled correctly."""
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

        assert "series_a" in result.forecast

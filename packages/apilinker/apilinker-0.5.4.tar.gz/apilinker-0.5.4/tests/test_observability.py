"""
Tests for OpenTelemetry observability integration.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from apilinker.core.observability import (
    ObservabilityConfig,
    TelemetryManager,
    get_telemetry_manager,
    initialize_telemetry,
    shutdown_telemetry,
    OTEL_AVAILABLE,
)


class TestObservabilityConfig:
    """Test observability configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ObservabilityConfig()
        assert config.enabled is True
        assert config.service_name == "apilinker"
        assert config.enable_tracing is True
        assert config.enable_metrics is True
        assert config.export_to_console is False
        assert config.export_to_prometheus is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ObservabilityConfig(
            enabled=False,
            service_name="test-service",
            enable_tracing=False,
            prometheus_port=8080,
        )
        assert config.enabled is False
        assert config.service_name == "test-service"
        assert config.enable_tracing is False
        assert config.prometheus_port == 8080


class TestTelemetryManager:
    """Test telemetry manager."""

    def test_initialization_disabled(self):
        """Test manager initialization when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        assert manager.config.enabled is False
        assert manager.tracer is None
        assert manager.meter is None

    def test_initialization_without_otel(self):
        """Test manager initialization without OpenTelemetry installed."""
        config = ObservabilityConfig(enabled=True)

        with patch('apilinker.core.observability.OTEL_AVAILABLE', False):
            manager = TelemetryManager(config)

            assert manager.config.enabled is False
            assert manager.tracer is None

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not installed")
    def test_initialization_with_otel(self):
        """Test manager initialization with OpenTelemetry installed."""
        config = ObservabilityConfig(
            enabled=True,
            export_to_console=True
        )
        manager = TelemetryManager(config)

        assert manager._initialized is True
        assert manager.tracer is not None

    def test_trace_sync_disabled(self):
        """Test trace_sync context manager when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        with manager.trace_sync("source", "target", "correlation-123") as span:
            assert span is None

    def test_trace_api_call_disabled(self):
        """Test trace_api_call context manager when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        with manager.trace_api_call("endpoint", "GET", "http://api.com", "source") as span:
            assert span is None

    def test_trace_transformation_disabled(self):
        """Test trace_transformation context manager when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        with manager.trace_transformation("lowercase", "email") as span:
            assert span is None

    def test_record_sync_completion_disabled(self):
        """Test record_sync_completion when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        # Should not raise any errors
        manager.record_sync_completion("source", "target", True, 10)

    def test_record_error_disabled(self):
        """Test record_error when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        # Should not raise any errors
        manager.record_error("validation", "sync", "Test error")

    def test_instrument_function_disabled(self):
        """Test instrument_function decorator when disabled."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        @manager.instrument_function("test_operation")
        def test_func():
            return "result"

        assert test_func() == "result"

    def test_instrument_function_with_exception(self):
        """Test instrument_function decorator with exception."""
        config = ObservabilityConfig(enabled=False)
        manager = TelemetryManager(config)

        @manager.instrument_function("test_operation")
        def test_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            test_func()


class TestGlobalTelemetryManager:
    """Test global telemetry manager functions."""

    def test_get_telemetry_manager(self):
        """Test getting global telemetry manager."""
        manager = get_telemetry_manager()
        assert isinstance(manager, TelemetryManager)

    def test_initialize_telemetry(self):
        """Test initializing global telemetry manager."""
        config = ObservabilityConfig(enabled=False)
        initialize_telemetry(config)

        manager = get_telemetry_manager()
        assert manager.config.enabled is False

    def test_shutdown_telemetry(self):
        """Test shutting down global telemetry manager."""
        initialize_telemetry(ObservabilityConfig(enabled=False))
        shutdown_telemetry()

        # Getting manager after shutdown should create a new one
        manager = get_telemetry_manager()
        assert isinstance(manager, TelemetryManager)


@pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not installed")
class TestTelemetryManagerWithOtel:
    """Test telemetry manager with OpenTelemetry available."""

    def test_trace_sync_with_success(self):
        """Test trace_sync with successful operation."""
        config = ObservabilityConfig(
            enabled=True,
            export_to_console=False
        )
        manager = TelemetryManager(config)

        with manager.trace_sync("source", "target", "test-123") as span:
            assert span is not None

    def test_trace_sync_with_exception(self):
        """Test trace_sync with exception."""
        config = ObservabilityConfig(
            enabled=True,
            export_to_console=False
        )
        manager = TelemetryManager(config)

        with pytest.raises(ValueError):
            with manager.trace_sync("source", "target", "test-123"):
                raise ValueError("Test error")

    def test_trace_api_call(self):
        """Test trace_api_call context manager."""
        config = ObservabilityConfig(
            enabled=True,
            export_to_console=False
        )
        manager = TelemetryManager(config)

        with manager.trace_api_call("get_users", "GET", "https://api.com/users", "source") as span:
            assert span is not None

    def test_trace_transformation(self):
        """Test trace_transformation context manager."""
        config = ObservabilityConfig(
            enabled=True,
            export_to_console=False
        )
        manager = TelemetryManager(config)

        with manager.trace_transformation("lowercase", "email") as span:
            assert span is not None

    def test_metrics_creation(self):
        """Test that metrics are created."""
        config = ObservabilityConfig(
            enabled=True,
            enable_metrics=True,
            export_to_console=True
        )
        manager = TelemetryManager(config)

        assert manager.sync_counter is not None
        assert manager.sync_duration_histogram is not None
        assert manager.api_call_counter is not None
        assert manager.error_counter is not None

    def test_record_sync_completion(self):
        """Test recording sync completion."""
        config = ObservabilityConfig(
            enabled=True,
            enable_metrics=True,
            export_to_console=True
        )
        manager = TelemetryManager(config)

        # Should not raise any errors
        manager.record_sync_completion("source", "target", True, 10)

    def test_record_error(self):
        """Test recording errors."""
        config = ObservabilityConfig(
            enabled=True,
            enable_metrics=True,
            export_to_console=True
        )
        manager = TelemetryManager(config)

        # Should not raise any errors
        manager.record_error("validation", "sync", "Test error")

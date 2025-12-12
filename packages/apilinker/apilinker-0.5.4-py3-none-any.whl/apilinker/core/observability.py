"""
OpenTelemetry integration for APILinker.

Provides distributed tracing, metrics collection, and observability for
production deployments. Supports Prometheus metrics export and custom
instrumentation.
"""

import logging
import time
from typing import Callable, Optional
from functools import wraps
from contextlib import contextmanager, nullcontext

try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import (
        PeriodicExportingMetricReader,
        ConsoleMetricExporter,
    )
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.trace import Status, StatusCode

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    # Provide mock implementations when OpenTelemetry is not installed
    trace = None
    metrics = None

logger = logging.getLogger(__name__)


class ObservabilityConfig:
    """Configuration for observability features."""

    def __init__(
        self,
        enabled: bool = True,
        service_name: str = "apilinker",
        enable_tracing: bool = True,
        enable_metrics: bool = True,
        export_to_console: bool = False,
        export_to_prometheus: bool = False,
        prometheus_host: str = "0.0.0.0",
        prometheus_port: int = 9090,
    ):
        """
        Initialize observability configuration.

        Args:
            enabled: Enable/disable observability
            service_name: Name of the service for telemetry
            enable_tracing: Enable distributed tracing
            enable_metrics: Enable metrics collection
            export_to_console: Export telemetry to console (debug)
            export_to_prometheus: Export metrics to Prometheus
            prometheus_host: Prometheus exporter host
            prometheus_port: Prometheus exporter port
        """
        self.enabled = enabled
        self.service_name = service_name
        self.enable_tracing = enable_tracing
        self.enable_metrics = enable_metrics
        self.export_to_console = export_to_console
        self.export_to_prometheus = export_to_prometheus
        self.prometheus_host = prometheus_host
        self.prometheus_port = prometheus_port


class TelemetryManager:
    """
    Manages OpenTelemetry tracing and metrics for APILinker.

    Provides distributed tracing for sync operations and metrics collection
    for monitoring API calls, transformations, and errors.
    """

    def __init__(self, config: Optional[ObservabilityConfig] = None):
        """
        Initialize the telemetry manager.

        Args:
            config: Observability configuration
        """
        self.config = config or ObservabilityConfig()
        self.tracer = None
        self.meter = None
        self._initialized = False

        # Metrics
        self.sync_counter = None
        self.sync_duration_histogram = None
        self.api_call_counter = None
        self.api_call_duration_histogram = None
        self.error_counter = None
        self.transformation_counter = None
        self.item_counter = None

        if self.config.enabled:
            self._initialize()

    def _initialize(self):
        """Initialize OpenTelemetry providers and instruments."""
        if not OTEL_AVAILABLE:
            logger.warning(
                "OpenTelemetry not available. Install with: "
                "pip install opentelemetry-api opentelemetry-sdk "
                "opentelemetry-exporter-prometheus"
            )
            self.config.enabled = False
            return

        try:
            # Create resource
            resource = Resource(attributes={SERVICE_NAME: self.config.service_name})

            # Initialize tracing
            if self.config.enable_tracing:
                self._initialize_tracing(resource)

            # Initialize metrics
            if self.config.enable_metrics:
                self._initialize_metrics(resource)

            self._initialized = True
            logger.info(
                f"Observability initialized for service: {self.config.service_name}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize observability: {e}")
            self.config.enabled = False

    def _initialize_tracing(self, resource):
        """Initialize distributed tracing."""
        trace_provider = TracerProvider(resource=resource)

        # Add exporters
        if self.config.export_to_console:
            trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

        # Set the global tracer provider
        trace.set_tracer_provider(trace_provider)
        self.tracer = trace.get_tracer(__name__)

        logger.info("Distributed tracing enabled")

    def _initialize_metrics(self, resource):
        """Initialize metrics collection."""
        # Create metric readers
        readers = []

        if self.config.export_to_console:
            readers.append(
                PeriodicExportingMetricReader(
                    ConsoleMetricExporter(), export_interval_millis=10000
                )
            )

        if self.config.export_to_prometheus:
            try:
                from opentelemetry.exporter.prometheus import PrometheusMetricReader
                from prometheus_client import start_http_server

                # Start Prometheus HTTP server
                start_http_server(
                    port=self.config.prometheus_port, addr=self.config.prometheus_host
                )
                readers.append(PrometheusMetricReader())
                logger.info(
                    f"Prometheus metrics available at "
                    f"http://{self.config.prometheus_host}:{self.config.prometheus_port}/metrics"
                )
            except ImportError:
                logger.warning(
                    "Prometheus exporter not available. Install with: "
                    "pip install opentelemetry-exporter-prometheus"
                )

        # Create meter provider
        if readers:
            meter_provider = MeterProvider(resource=resource, metric_readers=readers)
            metrics.set_meter_provider(meter_provider)
            self.meter = metrics.get_meter(__name__)

            # Create metrics
            self._create_metrics()

            logger.info("Metrics collection enabled")

    def _create_metrics(self) -> None:
        """Create metric instruments."""
        if not self.meter:
            return

        # Sync operations
        self.sync_counter = self.meter.create_counter(  # type: ignore[unreachable]
            name="apilinker.sync.count",
            description="Number of sync operations",
            unit="1",
        )

        self.sync_duration_histogram = self.meter.create_histogram(
            name="apilinker.sync.duration",
            description="Duration of sync operations",
            unit="ms",
        )

        # API calls
        self.api_call_counter = self.meter.create_counter(
            name="apilinker.api.calls",
            description="Number of API calls",
            unit="1",
        )

        self.api_call_duration_histogram = self.meter.create_histogram(
            name="apilinker.api.duration",
            description="Duration of API calls",
            unit="ms",
        )

        # Errors
        self.error_counter = self.meter.create_counter(
            name="apilinker.errors",
            description="Number of errors",
            unit="1",
        )

        # Transformations
        self.transformation_counter = self.meter.create_counter(
            name="apilinker.transformations",
            description="Number of data transformations",
            unit="1",
        )

        # Items processed
        self.item_counter = self.meter.create_counter(
            name="apilinker.items.processed",
            description="Number of items processed",
            unit="1",
        )

    @contextmanager
    def trace_sync(self, source: str, target: str, correlation_id: str):
        """
        Create a trace span for a sync operation.

        Args:
            source: Source endpoint name
            target: Target endpoint name
            correlation_id: Correlation ID for the sync

        Yields:
            Span context
        """
        if not self.config.enabled or not self.tracer:
            with nullcontext():
                yield None
        else:
            with self.tracer.start_as_current_span(  # type: ignore[unreachable]
                "sync_operation",
                attributes={
                    "sync.source": source,
                    "sync.target": target,
                    "sync.correlation_id": correlation_id,
                },
            ) as span:
                start_time = time.time()
                try:
                    yield span
                    span.set_status(Status(StatusCode.OK))
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    if self.sync_duration_histogram:
                        self.sync_duration_histogram.record(
                            duration_ms,
                            attributes={
                                "source": source,
                                "target": target,
                            },
                        )

    @contextmanager
    def trace_api_call(
        self, endpoint: str, method: str, url: str, call_type: str = "source"
    ):
        """
        Create a trace span for an API call.

        Args:
            endpoint: Endpoint name
            method: HTTP method
            url: API URL
            call_type: Type of call (source/target)

        Yields:
            Span context
        """
        if not self.config.enabled or not self.tracer:
            with nullcontext():
                yield None
        else:
            with self.tracer.start_as_current_span(  # type: ignore[unreachable]
                f"api_call_{call_type}",
                attributes={
                    "http.method": method,
                    "http.url": url,
                    "api.endpoint": endpoint,
                    "api.type": call_type,
                },
            ) as span:
                start_time = time.time()
                try:
                    yield span
                    span.set_status(Status(StatusCode.OK))
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    if self.api_call_duration_histogram:
                        self.api_call_duration_histogram.record(
                            duration_ms,
                            attributes={
                                "endpoint": endpoint,
                                "method": method,
                                "type": call_type,
                            },
                        )
                    if self.api_call_counter:
                        self.api_call_counter.add(
                            1,
                            attributes={
                                "endpoint": endpoint,
                                "method": method,
                                "type": call_type,
                            },
                        )

    @contextmanager
    def trace_transformation(self, transformer: str, field: str):
        """
        Create a trace span for a data transformation.

        Args:
            transformer: Transformer name
            field: Field being transformed

        Yields:
            Span context
        """
        if not self.config.enabled or not self.tracer:
            with nullcontext():
                yield None
        else:
            with self.tracer.start_as_current_span(  # type: ignore[unreachable]
                "transformation",
                attributes={
                    "transform.name": transformer,
                    "transform.field": field,
                },
            ) as span:
                try:
                    yield span
                    span.set_status(Status(StatusCode.OK))
                    if self.transformation_counter:
                        self.transformation_counter.add(
                            1, attributes={"transformer": transformer}
                        )
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

    def record_sync_completion(
        self, source: str, target: str, success: bool, count: int
    ) -> None:
        """
        Record completion of a sync operation.

        Args:
            source: Source endpoint
            target: Target endpoint
            success: Whether sync was successful
            count: Number of items synced
        """
        if not self.config.enabled or not self.sync_counter:
            return

        self.sync_counter.add(  # type: ignore[unreachable]
            1,
            attributes={
                "source": source,
                "target": target,
                "success": str(success).lower(),
            },
        )

        if self.item_counter:
            self.item_counter.add(
                count,
                attributes={
                    "source": source,
                    "target": target,
                },
            )

    def record_error(self, error_type: str, operation: str, details: str = "") -> None:
        """
        Record an error occurrence.

        Args:
            error_type: Type/category of error
            operation: Operation where error occurred
            details: Additional error details
        """
        if not self.config.enabled or not self.error_counter:
            return

        self.error_counter.add(  # type: ignore[unreachable]
            1,
            attributes={
                "error.type": error_type,
                "error.operation": operation,
            },
        )

    def instrument_function(self, operation_name: str):
        """
        Decorator to instrument a function with tracing.

        Args:
            operation_name: Name of the operation for the span

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.config.enabled or not self.tracer:
                    return func(*args, **kwargs)

                with self.tracer.start_as_current_span(operation_name) as span:  # type: ignore[unreachable]
                    try:
                        result = func(*args, **kwargs)
                        span.set_status(Status(StatusCode.OK))
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        span.record_exception(e)
                        raise

            return wrapper

        return decorator

    def shutdown(self):
        """Shutdown telemetry and flush pending data."""
        if self._initialized:
            logger.info("Shutting down observability")
            # OpenTelemetry SDK handles shutdown automatically


# Global telemetry manager instance
_telemetry_manager: Optional[TelemetryManager] = None


def get_telemetry_manager() -> TelemetryManager:
    """
    Get the global telemetry manager instance.

    Returns:
        TelemetryManager instance
    """
    global _telemetry_manager
    if _telemetry_manager is None:
        _telemetry_manager = TelemetryManager()
    return _telemetry_manager


def initialize_telemetry(config: Optional[ObservabilityConfig] = None):
    """
    Initialize the global telemetry manager.

    Args:
        config: Observability configuration
    """
    global _telemetry_manager
    _telemetry_manager = TelemetryManager(config)


def shutdown_telemetry():
    """Shutdown the global telemetry manager."""
    global _telemetry_manager
    if _telemetry_manager:
        _telemetry_manager.shutdown()
        _telemetry_manager = None

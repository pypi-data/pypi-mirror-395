"""
TracerManager - Singleton tracer with lazy initialization.

Based on msgflux telemetry architecture with thread-safe lazy loading.
"""

import os
import platform
from threading import RLock

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


class TracerManager:
    """
    Singleton tracer manager with lazy initialization.

    Features:
    - Thread-safe initialization (RLock)
    - Lazy loading (no overhead until first use)
    - Environment-based configuration
    - Zero-overhead when disabled (early return)
    - Idempotent initialization (multiple calls safe)
    """

    def __init__(self):
        self._tracer: trace.Tracer | None = None
        self._lock = RLock()
        self._initialized = False

    @property
    def tracer(self) -> trace.Tracer:
        """
        Get or create tracer instance.

        Returns:
            OpenTelemetry tracer instance.

        Thread-safe lazy initialization. Multiple threads calling this
        simultaneously will only initialize once.
        """
        # Fast path: already initialized
        if self._tracer is not None:
            return self._tracer

        # Slow path: need to initialize
        with self._lock:
            # Double-check: another thread may have initialized
            if self._tracer is not None:
                return self._tracer

            # Initialize tracer
            self._initialize()
            return self._tracer

    def _initialize(self):
        """
        Initialize OpenTelemetry tracer.

        Reads configuration from environment variables:
        - MSGTRACE_TELEMETRY_ENABLED: Enable/disable tracing (default: false)
        - MSGTRACE_OTLP_ENDPOINT: OTLP HTTP endpoint (default: http://localhost:8000/v1/traces)
        - MSGTRACE_EXPORTER: Exporter type - 'otlp' or 'console' (default: otlp)
        - MSGTRACE_SERVICE_NAME: Service name (default: 'msgtrace-app')
        - MSGTRACE_CAPTURE_PLATFORM: Include platform info (default: true)
        """
        # Check if telemetry is enabled
        enabled = os.getenv("MSGTRACE_TELEMETRY_ENABLED", "false").lower() == "true"
        if not enabled:
            # Create no-op tracer
            self._tracer = trace.get_tracer(__name__)
            self._initialized = True
            return

        # Get configuration
        service_name = os.getenv("MSGTRACE_SERVICE_NAME", "msgtrace-app")
        exporter_type = os.getenv("MSGTRACE_EXPORTER", "otlp")
        capture_platform = os.getenv("MSGTRACE_CAPTURE_PLATFORM", "true").lower() == "true"

        # Build resource attributes
        resource_attrs = {
            SERVICE_NAME: service_name,
        }

        if capture_platform:
            resource_attrs.update(
                {
                    "platform.system": platform.system(),
                    "platform.release": platform.release(),
                    "platform.machine": platform.machine(),
                    "python.version": platform.python_version(),
                }
            )

        resource = Resource(attributes=resource_attrs)

        # Create tracer provider
        provider = TracerProvider(resource=resource)

        # Configure exporter
        if exporter_type == "console":
            # Console exporter for debugging
            exporter = ConsoleSpanExporter()
        else:
            # OTLP HTTP exporter (default)
            endpoint = os.getenv(
                "MSGTRACE_OTLP_ENDPOINT", "http://localhost:8000/api/v1/traces/export"
            )
            exporter = OTLPSpanExporter(endpoint=endpoint)

        # Add batch processor (async export, non-blocking)
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)

        # Set as global tracer provider
        trace.set_tracer_provider(provider)

        # Create tracer instance
        self._tracer = trace.get_tracer(
            instrumenting_module_name="msgtrace.sdk",
            instrumenting_library_version="0.1.0",
        )

        self._initialized = True

    def is_enabled(self) -> bool:
        """
        Check if telemetry is enabled.

        Returns:
            True if MSGTRACE_TELEMETRY_ENABLED=true
        """
        return os.getenv("MSGTRACE_TELEMETRY_ENABLED", "false").lower() == "true"

    def shutdown(self):
        """
        Shutdown tracer and flush pending spans.

        Call this at application exit to ensure all spans are exported.
        """
        if self._tracer is not None:
            provider = trace.get_tracer_provider()
            if hasattr(provider, "shutdown"):
                provider.shutdown()


# Global singleton instance
tracer_manager = TracerManager()

# Convenience accessor
tracer = tracer_manager.tracer

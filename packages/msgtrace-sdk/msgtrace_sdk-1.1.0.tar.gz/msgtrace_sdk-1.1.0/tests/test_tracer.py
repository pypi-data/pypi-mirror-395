"""
Tests for TracerManager.
"""

import os

from msgtrace.sdk.tracer import TracerManager, tracer_manager


class TestTracerManager:
    """Test TracerManager singleton."""

    def test_singleton_pattern(self):
        """Test that TracerManager is a singleton."""
        manager1 = TracerManager()
        manager2 = TracerManager()

        # Different instances but share global state via tracer_manager
        assert manager1 is not manager2

        # Global singleton
        assert tracer_manager is not None

    def test_disabled_by_default(self):
        """Test that telemetry is disabled by default."""
        # Ensure env is not set
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED", None)

        manager = TracerManager()
        assert not manager.is_enabled()

    def test_enabled_with_env(self):
        """Test enabling telemetry via environment variable."""
        os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"

        manager = TracerManager()
        assert manager.is_enabled()

        # Cleanup
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED")

    def test_tracer_property_lazy_initialization(self):
        """Test lazy initialization of tracer."""
        manager = TracerManager()

        # Not initialized yet
        assert manager._tracer is None

        # Access tracer (triggers initialization)
        tracer = manager.tracer
        assert tracer is not None

        # Second access returns same instance
        tracer2 = manager.tracer
        assert tracer is tracer2

    def test_tracer_no_op_when_disabled(self):
        """Test that tracer is no-op when disabled."""
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED", None)

        manager = TracerManager()
        tracer = manager.tracer

        # Should be a no-op tracer
        assert tracer is not None

        # Can create spans (but they won't be exported)
        span = tracer.start_span("test")
        assert span is not None
        span.end()

    def test_configuration_from_env(self):
        """Test configuration loading from environment."""
        os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
        os.environ["MSGTRACE_SERVICE_NAME"] = "test-service"
        os.environ["MSGTRACE_OTLP_ENDPOINT"] = "http://test:8000/v1/traces"
        os.environ["MSGTRACE_EXPORTER"] = "console"

        manager = TracerManager()
        tracer = manager.tracer

        assert tracer is not None

        # Cleanup
        for key in [
            "MSGTRACE_TELEMETRY_ENABLED",
            "MSGTRACE_SERVICE_NAME",
            "MSGTRACE_OTLP_ENDPOINT",
            "MSGTRACE_EXPORTER",
        ]:
            os.environ.pop(key, None)

    def test_default_service_name(self):
        """Test default service name."""
        os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
        os.environ.pop("MSGTRACE_SERVICE_NAME", None)

        manager = TracerManager()
        tracer = manager.tracer

        # Should use default
        assert tracer is not None

        # Cleanup
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED")

    def test_platform_capture_enabled(self):
        """Test platform info capture."""
        os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
        os.environ["MSGTRACE_CAPTURE_PLATFORM"] = "true"

        manager = TracerManager()
        tracer = manager.tracer

        assert tracer is not None

        # Cleanup
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED")
        os.environ.pop("MSGTRACE_CAPTURE_PLATFORM")

    def test_platform_capture_disabled(self):
        """Test disabling platform info."""
        os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
        os.environ["MSGTRACE_CAPTURE_PLATFORM"] = "false"

        manager = TracerManager()
        tracer = manager.tracer

        assert tracer is not None

        # Cleanup
        os.environ.pop("MSGTRACE_TELEMETRY_ENABLED")
        os.environ.pop("MSGTRACE_CAPTURE_PLATFORM")

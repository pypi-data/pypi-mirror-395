# src/dimredtracer/otel_setup.py

import os
from typing import Optional

from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Globals to keep things idempotent
_INITIALIZED = False
_SPAN_PROCESSOR: Optional[BatchSpanProcessor] = None
_SESSION_ID: Optional[str] = None


class SessionIdSpanProcessor(SpanProcessor):
    """Span processor that automatically adds session_id to all spans."""

    def __init__(self, session_id: str):
        self.session_id = session_id

    def on_start(self, span: "trace.Span", parent_context: Optional[Context] = None) -> None:
        """Add session_id when span starts."""
        if span and span.is_recording():
            span.set_attribute("session.id", self.session_id)

    def on_end(self, span: ReadableSpan) -> None:
        """Called when span ends. Nothing to do."""
        pass

    def shutdown(self) -> None:
        """Called on shutdown. Nothing to do."""
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Called on flush. Nothing to do."""
        return True


def setup_tracing(session_id: Optional[str] = None) -> TracerProvider:
    """
    Initialize OpenTelemetry tracing using environment variables.

    Expected env vars:
      OTEL_EXPORTER_OTLP_TRACES_ENDPOINT  - full OTLP HTTP traces endpoint
      OTEL_SERVICE_NAME                   - logical service name
      DIMRED_TENANT_ID                    - optional tenant id (dimred.tenant_id)

    Args:
      session_id: Optional session identifier to add to all spans
    """
    global _INITIALIZED, _SPAN_PROCESSOR, _SESSION_ID

    if _INITIALIZED:
        # Tracer provider already configured; just return it
        return trace.get_tracer_provider()  # type: ignore[return-value]

    # 1. Read env vars
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    if not endpoint:
        raise RuntimeError(
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT is not set. "
        )

    service_name = os.environ.get("OTEL_SERVICE_NAME", "dimredtracer-service")
    tenant_id = os.environ.get("DIMRED_TENANT_ID")

    # 2. Build resource
    resource_attrs = {"service.name": service_name}
    if tenant_id:
        resource_attrs["dimred.tenant_id"] = tenant_id

    resource = Resource.create(resource_attrs)

    # 3. Create provider + exporter + processor
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # 4. Add session_id processor if provided
    if session_id:
        _SESSION_ID = session_id
        session_processor = SessionIdSpanProcessor(session_id)
        provider.add_span_processor(session_processor)

    exporter = OTLPSpanExporter(endpoint=endpoint)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    _SPAN_PROCESSOR = processor
    _INITIALIZED = True

    return provider


def force_flush(timeout_millis: int = 30000) -> None:
    """
    Force flush any buffered spans.

    Users call tracer.force_flush(), which delegates here.
    """
    global _SPAN_PROCESSOR
    if _SPAN_PROCESSOR is not None:
        try:
            _SPAN_PROCESSOR.force_flush(timeout_millis=timeout_millis)
        except TypeError:
            # Some OTEL versions use timeout_millis, others use no args; fail soft
            _SPAN_PROCESSOR.force_flush()

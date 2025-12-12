# src/dimredtracer/tracer.py

import uuid
from contextlib import contextmanager
from typing import Any, Optional

from opentelemetry import trace

from .otel_setup import setup_tracing, force_flush as _force_flush


class Tracer:
    """
    DimredTracer: minimal facade around OpenTelemetry + OpenInference.

    Usage:
      from dimredtracer import Tracer
      from openinference.instrumentation.openai import OpenAIInstrumentor

      tracer = Tracer(OpenAIInstrumentor())
      tracer.set_attribute("tenant.id", "acme")

      with tracer.start_span("preprocess"):
          tracer.set_attribute("chunks", 42)

      tracer.force_flush()
    """

    def __init__(self, instrumentation: Optional[Any] = None, name: str = "dimred.tracer", session_id: Optional[str] = None):
        """
        Initialize tracing + (optionally) an OpenInference instrumentation object.

        Args:
            instrumentation:
                An OpenInference instrumentation instance, such as
                OpenAIInstrumentor(). If provided and it has an .instrument()
                method, we'll call it after setting up the OTEL tracer provider.

            name:
                Logical name for the OTEL tracer to use.

            session_id:
                Optional session identifier. If not provided, a unique session_id
                will be automatically generated. This session_id is automatically
                added to all spans as an attribute.
        """
        # 1. Generate or use provided session_id
        self.session_id = session_id if session_id else f"session_{uuid.uuid4().hex[:16]}"

        # 2. Ensure OTEL provider + exporter are configured (env-driven)
        # Pass session_id so it gets added to all spans via SpanProcessor
        setup_tracing(session_id=self.session_id)

        # 3. Wire OpenInference instrumentation IF provided
        if instrumentation is not None:
            instrument_fn = getattr(instrumentation, "instrument", None)
            if callable(instrument_fn):
                try:
                    instrument_fn()
                except Exception:
                    # In case instrumentation is already active or fails,
                    # we don't want to break user code. Fail soft.
                    pass

        # 4. Grab the OTEL tracer
        self._otel_tracer = trace.get_tracer(name)

    # ---- Core User-Facing API ----

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Attach an attribute to the current active span (if any).

        Works seamlessly with OpenInference LLM spans because they are created
        as the current OTEL span around LLM calls.
        """
        span = trace.get_current_span()
        if span and span.is_recording():
            span.set_attribute(key, value)

    @contextmanager
    def start_span(self, name: str):
        """
        Create a custom span and make it the current span in this context.

        Attributes set via tracer.set_attribute() inside the with-block will
        attach to this custom span. The session_id is automatically added to
        every span via the SessionIdSpanProcessor.
        """
        with self._otel_tracer.start_as_current_span(name) as span:
            yield span

    def force_flush(self, timeout_millis: int = 30000) -> None:
        """
        Flush buffered spans from the batch processor.

        Call this at the end of a script or request if you want to ensure
        everything has been exported to your collector.
        """
        _force_flush(timeout_millis=timeout_millis)

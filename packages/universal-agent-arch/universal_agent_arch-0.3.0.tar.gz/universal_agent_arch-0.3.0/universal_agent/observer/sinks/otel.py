"""
universal_agent.observer.sinks.otel

OpenTelemetry sink converting agent events into distributed traces.
Maps graph execution to a root span and nodes to child spans, with manual
context propagation via GraphState to survive suspend/resume.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
except ImportError:  # pragma: no cover - optional dependency
    OTLPSpanExporter = None

from universal_agent.graph.state import GraphState, StepRecord, StepStatus
from universal_agent.manifests.schema import ObserverSinkKind, ObserverSinkSpec

logger = logging.getLogger(__name__)


class OpenTelemetrySink:
    """Observer sink that pushes agent events to an OTEL collector."""

    def __init__(self, spec: ObserverSinkSpec, service_name: str = "universal_agent") -> None:
        self.spec = spec
        resource = Resource.create({"service.name": service_name, "agent.version": "0.1.0"})
        self.provider = TracerProvider(resource=resource)

        if spec.kind == ObserverSinkKind.OTEL and OTLPSpanExporter:
            endpoint = spec.config.get("endpoint", os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"))
            logger.info("📡 Initializing OTLP Exporter to %s", endpoint)
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        else:
            logger.info("📝 Initializing Console Trace Exporter")
            processor = BatchSpanProcessor(ConsoleSpanExporter())

        self.provider.add_span_processor(processor)
        self.tracer = self.provider.get_tracer("universal_agent.observer")
        self.propagator = TraceContextTextMapPropagator()

    def on_execution_start(self, state: GraphState) -> None:
        """Start a root span for a graph execution and inject trace context into state."""
        span = self.tracer.start_span(
            name=f"Graph: {state.graph_name}",
            kind=SpanKind.SERVER,
            attributes={
                "graph.name": state.graph_name,
                "graph.version": state.graph_version,
                "execution.id": state.execution_id,
            },
        )

        carrier: Dict[str, str] = {}
        with trace.use_span(span, end_on_exit=False):
            self.propagator.inject(carrier)

        state.update_context({"__trace__": carrier})
        span.end()

    def on_step_start(self, state: GraphState, node_id: str, inputs: Dict[str, Any]):
        """Start a child span for a node execution."""
        carrier = state.context.get("__trace__", {})
        ctx = self.propagator.extract(carrier)

        span = self.tracer.start_span(
            name=f"Node: {node_id}",
            context=ctx,
            kind=SpanKind.INTERNAL,
            attributes={"node.id": node_id, "execution.id": state.execution_id},
        )

        safe_inputs = json.dumps(inputs, default=str)[:1000]
        span.set_attribute("node.inputs", safe_inputs)
        return span

    def on_step_end(self, span: object, record: StepRecord) -> None:
        """Finish the node span with status and metadata."""
        if not isinstance(span, trace.Span):
            return

        if record.status == StepStatus.SUCCESS:
            span.set_status(Status(StatusCode.OK))
        else:
            span.set_status(Status(StatusCode.ERROR, record.error_message))
            if record.error_message:
                span.record_exception(Exception(record.error_message))

        if record.outputs:
            if "token_usage" in record.outputs:
                usage = record.outputs["token_usage"]
                for k, v in usage.items():
                    span.set_attribute(f"llm.tokens.{k}", v)
            if "tool_calls" in record.outputs:
                span.add_event("tool_call", {"calls": json.dumps(record.outputs["tool_calls"], default=str)})

        span.end(end_time=record.end_time)

    def shutdown(self) -> None:
        """Flush and close provider."""
        self.provider.shutdown()


__all__ = ["OpenTelemetrySink"]


import importlib.util
import logging
import os
from typing import Optional

from ..api_options import TelemetryOptions

_spec_opentelemetry = importlib.util.find_spec("opentelemetry")

logger = logging.getLogger(__name__)


def configure_telemetry(options: Optional[TelemetryOptions]) -> bool:
    if options is None or not options.enable:
        logger.debug(f"telemetry options {'missing' if options is None else 'disabled'}.")
        return False

    if _spec_opentelemetry is None:
        logger.warning("telemetry enabled however a required dependency is missing.")
        return False

    endpoint = options.endpoint if options.endpoint is not None else os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    if endpoint is None:
        logger.warning("telemetry enabled however the endpoint is not specified.")
        return False

    from opentelemetry.sdk.resources import SERVICE_NAME, Resource

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    from opentelemetry import metrics
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    resource = Resource(attributes={SERVICE_NAME: "auto-trainer"})

    trace_provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)

    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics"))
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    return True

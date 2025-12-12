from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_open_telemetry(
    endpoint: str = "http://otel-collector-hni01.ftel.scc/v1/traces",
    service_name: str = "EasyCore",
    name: str = "core",
    environment: str = "dev",
) -> None:
    # Set up OpenTelemetry resources
    resource = Resource(
        attributes={
            SERVICE_NAME: f"{service_name}-{name}",
            "service.environment": environment,
        }
    )

    # Configure trace provider and OTLP exporter
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint,  # Default OTLP HTTP Collector endpoint
    )

    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    # Set the global trace provider
    trace.set_tracer_provider(provider)

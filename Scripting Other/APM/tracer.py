#consume this file as tracer.py

import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

#server is the main package of python code
import sample_app

trace.set_tracer_provider(TracerProvider())
otlp_endpoint = os.environ["LMOTEL_ENDPOINT"]
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True))
)

#server.main is main method of server package
if __name__ == "__main__":
  sample_app.main()
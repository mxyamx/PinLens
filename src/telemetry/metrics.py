from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

PIN_INGEST_COUNT = Counter(
    "pinlens_pins_ingested_total", 
    "Total number of ingested pins"
)

VALIDATION_FAILURES = Counter(
    "pinlens_validation_failures_total", 
    "Total number of AI metadata validation failures"
)

CACHE_HITS = Counter(
    "pinlens_cache_hits_total", 
    "Total number of cache hits for pin metadata"
)

PROCESSING_LATENCY = Histogram(
    "pinlens_processing_latency_seconds", 
    "Latency of AI extraction and validation pipeline"
)

def get_telemetry_metrics():
    return generate_latest(), CONTENT_TYPE_LATEST
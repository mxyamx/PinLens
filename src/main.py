from fastapi import FastAPI, HTTPException, status, Response
from src.models.raw_pin import RawPinIngest
from src.models.validated_pin import ValidatedPin
from src.services.validator import PinValidationEngine
from src.telemetry.metrics import get_telemetry_metrics

app = FastAPI(
    title="PinLens AI Metadata Ingestion Pipeline",
    version="1.0.0"
)

validator_engine = PinValidationEngine()

@app.get("/")
async def root():
    return {"status": "online", "service": "PinLens Ingestion Pipeline"}

@app.get("/metrics")
async def metrics():
    """
    Exposes Prometheus system metrics for latency and validation tracking.
    """
    data, content_type = get_telemetry_metrics()
    return Response(content=data, media_type=content_type)

@app.post("/api/v1/pins/ingest", response_model=ValidatedPin, status_code=status.HTTP_201_CREATED)
async def ingest_pin(payload: RawPinIngest):
    try:
        validated_result = await validator_engine.process_and_validate(payload)
        return validated_result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
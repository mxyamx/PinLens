from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PinLens Ingestion Pipeline")

# Enable CORS so your frontend can communicate with your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
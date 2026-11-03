from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PinLens Ingestion Pipeline")

# 1. Standard FastAPI CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Bulletproof Fallback: Explicit OPTIONS preflight handler for any route
@app.options("/{full_path:path}")
async def preflight_handler(request: Request, full_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

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
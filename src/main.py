from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

app = FastAPI(title="PinLens Ingestion Pipeline")

# Explicit CORS configuration for your static dashboard domain and local testing
origins = [
    "https://pinlens-dashboard.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.services.validator import PinValidationEngine, RawPinIngest
from src.telemetry.metrics import get_telemetry_metrics

validator_engine = PinValidationEngine()

@app.get("/")
async def root():
    return {"status": "online", "service": "PinLens Ingestion Pipeline"}

@app.get("/metrics")
async def metrics():
    """
    Exposes Prometheus system metrics for latency and validation tracking.
    """
    try:
        data, content_type = get_telemetry_metrics()
        return Response(content=data, media_type=content_type)
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        return Response(content="# Error generating metrics", media_type="text/plain", status_code=500)

@app.post("/api/v1/pins/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_pin(request: Request, payload: RawPinIngest):
    try:
        logger.info(f"Incoming payload received for pin_id: {payload.pin_id}")
        validated_result = await validator_engine.process_and_validate(payload)
        return validated_result
    except ValueError as e:
        logger.warning(f"Guardrail validation rejected pin: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Pipeline processing internal error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
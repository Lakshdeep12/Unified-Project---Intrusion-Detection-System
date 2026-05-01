import sys
import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load env variables from root .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.Routes import auth, logs, stats, alerts, metrics, config, health, predict

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("IDS_Backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.Database.models import create_tables

    logger.info("Initializing database tables...")
    create_tables()
    yield


app = FastAPI(title="Advanced IDS API", lifespan=lifespan)

@app.middleware("http")
async def global_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Global Error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."}
        )

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
allow_origins = ["*"] if FRONTEND_URL == "*" else [FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(logs.router, prefix="/api", tags=["Logs"])
app.include_router(stats.router, prefix="/api", tags=["Stats"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
app.include_router(config.router, prefix="/api", tags=["Config"])
app.include_router(predict.router, prefix="/api", tags=["Prediction"])

if __name__ == "__main__":
    import uvicorn
    from src.Database.models import create_tables
    logger.info("Initializing database tables...")
    create_tables()
    logger.info("Starting up server...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

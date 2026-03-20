import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, check, feedback
from app.db.database import init_db
from contextlib import asynccontextmanager


def _minimal_openapi_surface() -> bool:
    """NMVP2 demo / low-footprint: no Swagger, Redoc, or /openapi.json (saves cold-start + attack surface)."""
    return os.getenv("TRUTHLENS_MINIMAL_OPENAPI", "").strip().lower() in ("1", "true", "yes")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_ready = await init_db()
    app.state.db_ready = db_ready
    yield


_min = _minimal_openapi_surface()
app = FastAPI(
    title="TruthLens UA Analytics",
    description="Ukrainian fake news detection platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None if _min else "/docs",
    redoc_url=None if _min else "/redoc",
    openapi_url=None if _min else "/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(check.router, prefix="/check")
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["Active Learning"])


try:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
except ImportError:
    pass

@app.get("/")
async def root():
    return {
        "service": "TruthLens UA Analytics",
        "version": "1.0.0",
        "status": "running",
        "docs": None if _min else "/docs",
        "db_ready": getattr(app.state, "db_ready", False),
    }

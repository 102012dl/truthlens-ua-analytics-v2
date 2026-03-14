from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, check
from app.db.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown (if needed)
    pass


app = FastAPI(
    title="TruthLens UA Analytics",
    description="Ukrainian fake news detection platform",
    version="1.0.0",
    lifespan=lifespan
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


@app.get("/")
async def root():
    return {
        "service": "TruthLens UA Analytics",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }
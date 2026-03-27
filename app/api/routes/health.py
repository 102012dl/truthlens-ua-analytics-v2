from fastapi import APIRouter
from datetime import datetime, timezone

from app.db.database import check_db_connection

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns service status and database connectivity.
    """
    db_status = "connected" if await check_db_connection() else "disconnected"
    overall_status = "ok" if db_status == "connected" else "degraded"

    return {
        "status": overall_status,
        "db": db_status,
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

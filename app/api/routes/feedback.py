from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    check_id: int
    correct_verdict: str  # REAL / FAKE / SUSPICIOUS
    user_type: str = "anonymous"

@router.post("")
async def submit_feedback(req: FeedbackRequest,
                            db: AsyncSession = Depends(get_db)):
    from app.db.models import ClaimCheck
    from sqlalchemy import select, update
    from datetime import datetime
    
    check = await db.get(ClaimCheck, req.check_id)
    if check:
        check.user_feedback = req.correct_verdict
        check.feedback_at = datetime.utcnow()
        await db.commit()
    return {"status": "received", "check_id": req.check_id}

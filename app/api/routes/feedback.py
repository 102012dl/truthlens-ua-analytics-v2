from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db import models

router = APIRouter()

class FeedbackRequest(BaseModel):
    pool_id: int
    user_validation: str

@router.post("")
async def submit_feedback(request: FeedbackRequest, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to process user feedback for items in the Uncertainty Pool.
    user_validation should be 'Agree' or 'Disagree'.
    """
    if request.user_validation not in ["Agree", "Disagree"]:
        raise HTTPException(status_code=400, detail="user_validation must be 'Agree' or 'Disagree'")

    pool_item = await db.get(models.UncertaintyPool, request.pool_id)
    if not pool_item:
        raise HTTPException(status_code=404, detail="Item not found in Uncertainty Pool")

    feedback = models.UserFeedback(
        pool_id=request.pool_id,
        user_validation=request.user_validation
    )
    db.add(feedback)
    await db.commit()
    
    return {"status": "success", "message": "Feedback recorded for Active Learning.", "pool_id": request.pool_id}

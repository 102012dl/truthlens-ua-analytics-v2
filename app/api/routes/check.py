import os
import re
import time

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import TruthLensOrchestrator
from app.db import models, repository
from app.db.database import get_db
from app.limiter import limiter
from app.schemas.check import CheckRequest, CheckResponse

_rpm = max(1, int(os.environ.get("RATE_LIMIT_PER_MINUTE", "30")))
CHECK_RATE_LIMIT = f"{_rpm}/minute"

router = APIRouter()
_orchestrator = TruthLensOrchestrator()


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    match = re.search(r'https?://([^/]+)', url or "")
    return match.group(1) if match else "direct_input"


async def fetch_url_content(url: str) -> tuple[str, str]:
    """Fetch title and body from URL."""
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, follow_redirects=True)
        # Simple text extraction (no BeautifulSoup needed for MVP)
        text = response.text
        title = re.search(r'<title>(.*?)</title>', text, re.I)
        title = title.group(1) if title else ""
        # Remove HTML tags
        body = re.sub(r'<[^>]+>', ' ', text)
        body = re.sub(r'\s+', ' ', body)[:3000]
        return title.strip(), body.strip()


@router.post("", response_model=CheckResponse)
@limiter.limit(CHECK_RATE_LIMIT)
async def check_text(
    request: Request,
    payload: CheckRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Main analysis endpoint.
    Accepts URL or text, returns verdict + credibility analysis.
    """
    start = time.perf_counter()

    # 1. Prepare content
    if payload.url:
        try:
            title, body = await fetch_url_content(payload.url)
            text = f"{title}. {body}"
            domain = extract_domain(payload.url)
        except Exception as e:
            raise HTTPException(400, f"Cannot fetch URL: {e}")
    else:
        text = payload.text
        domain = "direct_input"
        title = text[:100] if text else ""

    if not text or len(text.strip()) < 5:
        raise HTTPException(400, "Text too short for analysis")

    # 2. Run orchestrator
    result = await _orchestrator.process(text, domain)

    article_id = 0
    source_credibility = result.get("source_credibility", 50.0)

    # 3. Persist to DB when available
    try:
        source = await repository.get_or_create_source(db, domain)
        source.article_count += 1
        await db.flush()

        article = models.Article(
            source_id=source.id,
            url=payload.url,
            title=title[:200] if title else None,
            body=text[:5000],
            language=payload.language,
        )
        db.add(article)
        await db.flush()

        claim = models.Claim(
            article_id=article.id,
            text=title[:500] or text[:200],
            is_primary=True,
        )
        db.add(claim)
        await db.flush()

        check = models.ClaimCheck(
            claim_id=claim.id,
            verdict=result["verdict"],
            credibility_score=result["credibility_score"],
            fake_score=result["fake_score"],
            confidence=result["confidence"],
            ipso_techniques=result["ipso_techniques"],
            explanation_uk=result["explanation_uk"],
            processing_time_ms=result["processing_time_ms"],
        )
        db.add(check)
        await db.flush()

        # NMVP2 Active Learning: Add to UncertaintyPool if verdict is SUSPICIOUS
        if result["verdict"] == "SUSPICIOUS":
            uncertainty_item = models.UncertaintyPool(
                text=text[:5000],
                model_verdict="SUSPICIOUS",
                confidence=result["fake_score"],
                manipulation_tags=result["ipso_techniques"]
            )
            db.add(uncertainty_item)

        await db.commit()
        article_id = article.id
        source_credibility = getattr(source, "credibility_score", source_credibility)
    except Exception as e:
        await db.rollback()
        print(f"[check] DB persistence skipped: {e}")

    total_ms = round((time.perf_counter() - start) * 1000, 2)

    return CheckResponse(
        article_id=article_id,
        verdict=result["verdict"],
        credibility_score=result["credibility_score"],
        fake_score=result["fake_score"],
        confidence=result["confidence"],
        ipso_techniques=result["ipso_techniques"],
        source_credibility=source_credibility,
        explanation_uk=result["explanation_uk"],
        source_domain=domain,
        language=payload.language,
        processing_time_ms=total_ms,
        formula_breakdown=result.get("formula_breakdown"),
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db import models, repository
from app.schemas.check import CheckRequest, CheckResponse
from app.agents.orchestrator import TruthLensOrchestrator
import httpx, re, time

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
async def check_text(request: CheckRequest, db: AsyncSession = Depends(get_db)):
    """
    Main analysis endpoint.
    Accepts URL or text, returns verdict + credibility analysis.
    """
    start = time.perf_counter()

    # 1. Prepare content
    if request.url:
        try:
            title, body = await fetch_url_content(request.url)
            text = f"{title}. {body}"
            domain = extract_domain(request.url)
        except Exception as e:
            raise HTTPException(400, f"Cannot fetch URL: {e}")
    else:
        text = request.text
        domain = "direct_input"
        title = text[:100] if text else ""

    if not text or len(text.strip()) < 5:
        raise HTTPException(400, "Text too short for analysis")

    # 2. Run orchestrator
    result = await _orchestrator.process(text, domain)

    # 3. Persist to DB
    # Get or create source
    source = await repository.get_or_create_source(db, domain)
    source.article_count += 1
    await db.flush()

    # Create article
    article = models.Article(
        source_id=source.id,
        url=request.url,
        title=title[:200] if title else None,
        body=text[:5000],
        language=request.language,
    )
    db.add(article)
    await db.flush()

    # Create claim (headline = primary claim for v1)
    claim = models.Claim(
        article_id=article.id,
        text=title[:500] or text[:200],
        is_primary=True,
    )
    db.add(claim)
    await db.flush()

    # Create claim check
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
    await db.commit()

    total_ms = round((time.perf_counter() - start) * 1000, 2)

    return CheckResponse(
        article_id=article.id,
        verdict=result["verdict"],
        credibility_score=result["credibility_score"],
        fake_score=result["fake_score"],
        confidence=result["confidence"],
        ipso_techniques=result["ipso_techniques"],
        source_credibility=result["source_credibility"],
        explanation_uk=result["explanation_uk"],
        source_domain=domain,
        language=request.language,
        processing_time_ms=total_ms,
    )
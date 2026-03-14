from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Source


async def get_or_create_source(db: AsyncSession, domain: str) -> Source:
    """Get existing source or create new one."""
    result = await db.execute(select(Source).where(Source.domain == domain))
    source = result.scalar_one_or_none()
    
    if not source:
        source = Source(domain=domain, name=domain)
        db.add(source)
        await db.flush()
    
    return source
"""Daily job to compute trends."""
import asyncio
from datetime import datetime, date, timedelta

async def compute_daily_analytics():
    from app.db.database import AsyncSessionLocal
    from app.db.models import ClaimCheck, AnalyticsTrend, DomainStats, Article, Source
    from sqlalchemy import select, func
    
    async with AsyncSessionLocal() as db:
        today = date.today()
        # Ensure we compute for the last 24h as a daily run
        q = select(ClaimCheck).where(
            func.date(ClaimCheck.created_at) == today
        )
        result = await db.execute(q)
        checks = result.scalars().all()
        
        if not checks:
            print(f"No checks to compute for {today}")
            return
            
        total = len(checks)
        fakes = sum(1 for c in checks if c.verdict == "FAKE")
        reals = sum(1 for c in checks if c.verdict == "REAL")
        suspicious = sum(1 for c in checks if c.verdict == "SUSPICIOUS")
        avg_cred = sum(c.credibility_score for c in checks) / total if total > 0 else 0
        
        # IPSO techniques 
        technique_counts = {}
        for c in checks:
            if c.ipso_techniques:
                for t in c.ipso_techniques:
                    technique_counts[t] = technique_counts.get(t, 0) + 1
        
        top_ipso = max(technique_counts, key=technique_counts.get) if technique_counts else None
        
        trend = AnalyticsTrend(
            date=datetime.combine(today, datetime.min.time()),
            total_checks=total,
            fake_count=fakes,
            real_count=reals,
            suspicious_count=suspicious,
            avg_credibility=avg_cred,
            top_ipso_technique=top_ipso
        )
        db.add(trend)
        await db.commit()
        print(f"Computed analytics for {today}: {total} checks, top IPSO: {top_ipso}")

if __name__ == "__main__":
    asyncio.run(compute_daily_analytics())

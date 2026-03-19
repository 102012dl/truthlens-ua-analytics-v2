from datetime import datetime
from sqlalchemy import Integer, String, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    credibility_score: Mapped[float] = mapped_column(Float, default=0.5)
    article_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    articles: Mapped[list["Article"]] = relationship(back_populates="source")

    def __repr__(self) -> str:
        return f"<Source(id={self.id}, domain='{self.domain}', credibility={self.credibility_score})>"


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=True, unique=True)
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="uk")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    source: Mapped[Source] = relationship(back_populates="articles")
    claims: Mapped[list["Claim"]] = relationship(back_populates="article")

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, language='{self.language}', title='{self.title[:50]}...')>"


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    article: Mapped[Article] = relationship(back_populates="claims")
    claim_checks: Mapped[list["ClaimCheck"]] = relationship(back_populates="claim")

    def __repr__(self) -> str:
        return f"<Claim(id={self.id}, is_primary={self.is_primary}, text='{self.text[:50]}...')>"


class ClaimCheck(Base):
    __tablename__ = "claim_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_id: Mapped[int] = mapped_column(Integer, ForeignKey("claims.id"), nullable=False)
    verdict: Mapped[str] = mapped_column(String(20), nullable=False)  # REAL/FAKE/SUSPICIOUS
    credibility_score: Mapped[float] = mapped_column(Float, nullable=False)
    fake_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    ipso_techniques: Mapped[dict] = mapped_column(JSON, nullable=True)
    explanation_uk: Mapped[str] = mapped_column(Text, nullable=False)
    formula_breakdown: Mapped[dict] = mapped_column(JSON, nullable=True) # From NMVP2
    processing_time_ms: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_feedback: Mapped[str] = mapped_column(String(20), nullable=True)
    feedback_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    claim: Mapped[Claim] = relationship(back_populates="claim_checks")

    def __repr__(self) -> str:
        return f"<ClaimCheck(id={self.id}, verdict='{self.verdict}', credibility={self.credibility_score})>"

class AnalyticsTrend(Base):
    __tablename__ = "analytics_trends"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    total_checks: Mapped[int] = mapped_column(Integer, default=0)
    fake_count: Mapped[int] = mapped_column(Integer, default=0)
    real_count: Mapped[int] = mapped_column(Integer, default=0)
    suspicious_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_credibility: Mapped[float] = mapped_column(Float, default=0.0)
    top_ipso_technique: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class DomainStats(Base):
    __tablename__ = "domain_stats"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    check_count: Mapped[int] = mapped_column(Integer, default=0)
    fake_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_credibility: Mapped[float] = mapped_column(Float, default=0.0)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# NMVP2 Active Learning Models

class UncertaintyPool(Base):
    """Stores texts with SUSPICIOUS verdicts for active learning."""
    __tablename__ = "uncertainty_pool"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    model_verdict: Mapped[str] = mapped_column(String(20), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    manipulation_tags: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    feedbacks: Mapped[list["UserFeedback"]] = relationship(back_populates="pool_item")


class UserFeedback(Base):
    """Stores user validations for items in the uncertainty pool."""
    __tablename__ = "user_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pool_id: Mapped[int] = mapped_column(Integer, ForeignKey("uncertainty_pool.id"), nullable=False)
    user_validation: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g., 'Agree', 'Disagree'
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    pool_item: Mapped[UncertaintyPool] = relationship(back_populates="feedbacks")


class DatasetRegistry(Base):
    """Tracks auto-generated datasets for retraining."""
    __tablename__ = "dataset_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    samples_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


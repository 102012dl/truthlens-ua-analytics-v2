"""Test configuration for TruthLens UA Analytics."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.main import app
from app.db.database import get_db


@pytest.fixture(scope="module")
def client():
    async def _mock_get_db():
        session = AsyncMock()
        session.get = AsyncMock(return_value=None)
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.add = AsyncMock()
        session.flush = AsyncMock()
        session.close = AsyncMock()
        yield session

    app.dependency_overrides[get_db] = _mock_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

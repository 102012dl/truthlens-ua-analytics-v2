"""Test configuration for TruthLens UA Analytics."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch

@pytest.fixture(scope="module")
def client():
    # Override database dependency for tests
    with patch("app.db.database.get_db") as mock_get_db:
        mock_get_db.return_value = AsyncMock()
        with TestClient(app) as c:
            yield c
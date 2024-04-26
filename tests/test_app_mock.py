from unittest.mock import MagicMock
import pytest
from src.app import home
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.query.return_value.all.return_value = []
    return db

def test_home(mock_db):
    result = home(req=MagicMock(), db=mock_db)
    assert result is not None  # Replace with an appropriate assertion



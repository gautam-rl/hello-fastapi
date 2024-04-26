from unittest.mock import MagicMock
from app import home
from sqlalchemy.orm import Session

# Create a mock database session
mock_db = MagicMock(spec=Session)

# Mock the `query` method to prevent actual database operations
mock_db.query.return_value.all.return_value = []

# Call the `home` function with the mock request and database session
result = home(req=MagicMock(), db=mock_db)

print("Mock test completed successfully, no errors.")

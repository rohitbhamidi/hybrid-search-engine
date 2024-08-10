import pytest
from src.database import Database

@pytest.fixture
def db():
    """Fixture for creating a new Database instance."""
    return Database()

@pytest.fixture
def sample_record():
    """Fixture for providing a sample record."""
    return {"name": "Sample Record", "value": 100}

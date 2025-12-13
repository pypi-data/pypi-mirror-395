import pytest
import os
from pathlib import Path

@pytest.fixture
def env_file(tmp_path):
    """Create a temporary .env file."""
    f = tmp_path / ".env"
    f.write_text("TEST_KEY=test_value\nINT_KEY=123\nBOOL_KEY=true\nLIST_KEY=a,b,c\nJSON_KEY={\"a\": 1}")
    return f

@pytest.fixture
def clean_env():
    """Clean up environment variables before and after test."""
    old_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(old_env)

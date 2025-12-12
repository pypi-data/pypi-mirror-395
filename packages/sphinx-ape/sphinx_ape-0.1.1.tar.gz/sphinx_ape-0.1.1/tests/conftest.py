import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_path():
    with tempfile.TemporaryDirectory() as temp:
        yield Path(temp).resolve()

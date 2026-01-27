import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db_url = f"sqlite:///{db_path}"
        app = create_app(db_url)
        with TestClient(app) as test_client:
            yield test_client

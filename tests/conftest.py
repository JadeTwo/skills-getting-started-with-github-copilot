import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Snapshot initial activities so each test starts from the same state
_snapshot = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset to the snapshot before each test
    app_module.activities = copy.deepcopy(_snapshot)
    yield
    # Also ensure it's reset after the test
    app_module.activities = copy.deepcopy(_snapshot)

@pytest.fixture
def client():
    return TestClient(app_module.app)

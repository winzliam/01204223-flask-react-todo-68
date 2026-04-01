from http import HTTPStatus
import pytest
from flask import g
from flask_jwt_extended.config import config

@pytest.fixture(autouse=True)
def no_jwt(monkeypatch):
    monkeypatch.setattr(
        "flask_jwt_extended.view_decorators.verify_jwt_in_request",
        lambda *args, **kwargs: None
    )
    # If routes call get_jwt_identity(), patch that too
    monkeypatch.setattr(
        "flask_jwt_extended.get_jwt_identity",
        lambda: 1  # Return a fake user ID
    )

def test_get_empty_todo_items(client):
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == []


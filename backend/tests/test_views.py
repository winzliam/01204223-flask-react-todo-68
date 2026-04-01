from http import HTTPStatus
import pytest
from flask import g
from flask_jwt_extended.config import config

@pytest.fixture(autouse=True)
def no_jwt(monkeypatch):
    # from https://github.com/vimalloc/flask-jwt-extended/issues/171
    def no_verify(*args, **kwargs):
        g._jwt_extended_jwt = {
            config.identity_claim_key: 'test_user'
        }

    from flask_jwt_extended import view_decorators

    monkeypatch.setattr(view_decorators, 'verify_jwt_in_request', no_verify)

def test_get_empty_todo_items(client):
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == []


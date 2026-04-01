import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from main import app as flask_app
from models import db, User
from flask_jwt_extended import create_access_token


@pytest.fixture
def app():
    flask_app.config.update(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        }
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()

    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def auth_client(app):
    """Test client ที่มี JWT token แนบไปกับทุก request อัตโนมัติ"""
    with app.app_context():
        # สร้าง token โดยไม่ต้องมี user จริงในฐานข้อมูล
        token = create_access_token(identity="test_user")

    client = app.test_client()

    # Override ให้ทุก request แนบ Authorization header อัตโนมัติ
    original_open = client.open

    def open_with_auth(*args, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {token}'
        return original_open(*args, headers=headers, **kwargs)

    client.open = open_with_auth
    return client
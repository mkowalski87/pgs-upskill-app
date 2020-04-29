import os
import tempfile

import pytest
from app import app, db

@pytest.fixture
def client():
    db_fd, fb_file_name = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + fb_file_name
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # create db file
            db.create_all()
            pass
        yield client

    os.close(db_fd)
    os.unlink(fb_file_name)


def test_no_users(client):
    response = client.get('api/user')
    assert [] == response.get_json()

def test_get_not_existing_user(client):
    response = client.get('api/user/999')
    assert response.status_code == 400
    assert {'error':'User not found'}, response.get_json()

def test_ad_and_get_user(client):
    response = client.post('api/user', json={'first_name':'test_user', 'last_name':'test_last_name'})
    assert response.status_code == 201
    response = client.get('api/user/1')
    assert response.status_code == 200

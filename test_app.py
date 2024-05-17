# from ChatGPT

import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_task(client):
    response = client.post('/tasks', json={'title': 'Test Task'})
    assert response.status_code == 201
    assert b'Task created' in response.data

def test_delete_task(client):
    task = Task(title='Test Task')
    db.session.add(task)
    db.session.commit()
    response = client.delete(f'/tasks/{task.id}')
    assert response.status_code == 200
    assert b'Task deleted' in response.data

def test_update_task(client):
    task = Task(title='Test Task')
    db.session.add(task)
    db.session.commit()
    response = client.put(f'/tasks/{task.id}', json={'title': 'Updated Task', 'completed': True})
    assert response.status_code == 200
    assert b'Task updated' in response.data

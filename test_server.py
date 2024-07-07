import os
import tempfile
import json
import pytest
from openai import OpenAIError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import app
from db import save_question
from model.question import Base, Question


# Fixture to set up a temporary database and test client
@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True

    # Set also the os DATABASE_URL from the environment variable
    # for the server.py functionality and creation of the session to work!
    os.environ["DATABASE_URL"] = os.getenv('TEST_DATABASE_URL')

    app.config['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL')

    with app.test_client() as client:
        with app.app_context():
            engine = create_engine(app.config['DATABASE_URL'])
            Base.metadata.create_all(bind=engine)
            session = sessionmaker(bind=engine)()
            yield client, session

        os.close(db_fd)
        os.unlink(db_path)


# Fixture to initialize the database session
@pytest.fixture
def init_database(client):
    _, session = client
    yield session
    session.close()


# Fixture to mock the OpenAI API
@pytest.fixture
def mock_openai(monkeypatch):
    async def mock_ask_openai(question):
        if "fail" in question:
            raise OpenAIError("Test failure")
        return "Test answer"

    monkeypatch.setattr("server.ask_openai", mock_ask_openai)


# Test case to check successful question handling
def test_ask_question_success(client, mock_openai):
    test_client, _ = client
    response = test_client.post('/ask', json={'question': 'What is AI?'})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['question'] == 'What is AI?'
    assert data['data']['answer'] == 'Test answer'


# Test case to check error handling when no data is provided
def test_ask_question_no_data(client):
    test_client, _ = client
    response = test_client.post('/ask', json={})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'error'
    assert data['error']['message'] == 'No question has been provided'


# Test case to check error handling when OpenAI API fails
def test_ask_question_openai_error(client, mock_openai):
    test_client, _ = client
    response = test_client.post('/ask', json={'question': 'fail'})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'error'
    assert data['error']['message'] == 'Ai error occurred: Test failure'

# Test case to check saving a question to the database


def test_save_question(init_database):
    session = init_database

    question_text = "What is Flask?"
    answer_text = "Flask is a web framework."
    save_question(session, question_text, answer_text)

    saved_question = session.query(Question).filter_by(question_data=question_text).first()

    assert saved_question is not None
    assert saved_question.question_data == question_text
    assert saved_question.answer_data == answer_text

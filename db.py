import os

from model.question import Question
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session(database_url: str):
    # Create an engine and session
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def save_question(session, question: str, answer: str) -> None:
    """
    Save the question to the database
    """
    question = Question(question_data=question, answer_data=answer)
    session.add(question)
    session.commit()

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from flask import Flask, request, jsonify
from ai import ask_openai, OpenAIError
from model.question import Question

app = Flask(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]


# Create an engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def save_question(question: str, answer: str) -> None:
    """
    Save the question to the database
    :param question:
    :param answer:
    :return:
    """
    question = Question(question_data=question, answer_data=answer)
    session.add(question)
    session.commit()


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or 'question' not in data:
        response = {
            "status": "error",
            "error": {
                "message": "No question has been provided"
            }
        }
    else:
        question = data.get('question')
        try:
            answer = asyncio.run(ask_openai(question))
            save_question(question, answer)
            response = {
                "status": "success",
                "data": {
                    "question": question,
                    "answer": answer
                }
            }
        except OpenAIError as ai_error:
            response = {
                "status": "error",
                "error": {
                    "message": f"Ai error occurred: {str(ai_error)}"
                }
            }

    return jsonify(response)


@app.route("/fetch", methods=["GET"])
def fetch():
    pass


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

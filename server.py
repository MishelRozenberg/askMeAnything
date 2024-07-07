import asyncio
import os

from flask import Flask, request, jsonify

import db
from ai import ask_openai, OpenAIError
from db import save_question

app = Flask(__name__)


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
            save_question(db.create_session(os.environ["DATABASE_URL"]), question, answer)
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

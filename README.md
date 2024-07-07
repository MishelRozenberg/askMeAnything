# AskMeAnything Project

## Introduction

This project is a Flask-based application that integrates with OpenAI's API to answer questions. It uses PostgreSQL for the database and is containerized using Docker. The project also includes testing setup using pytest.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- Docker and Docker Compose
- Python 3.8 or higher
- pip (Python package installer)

## Getting Started

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/MishelRozenberg/askMeAnything.git
    cd askMeAnything
    ```

2. Install Python dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Docker Setup

1. Navigate to the project directory where `docker-compose.yml` is located.

2. Open the `docker-compose.yml` file.

3. Replace the placeholder `your-openai-api-key-here` with your actual OpenAI API key:

    ```yaml
    version: '3'
    services:
        db:
            image: "postgres"
            container_name: db
            ports:
                - 5432:5432
            environment:
                - POSTGRES_USER=postgres
                - POSTGRES_PASSWORD=postgres
                - POSTGRES_DB=askai

        app:
            build: .
            environment:
                - DATABASE_URL=postgresql://postgres:postgres@db/askai
                - OPENAI_API_KEY=your-openai-api-key-here # <-- User should replace this value
            ports:
                - 5000:5000
    ```

4. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

5. The Flask application should now be running on `http://localhost:5000`.

## Running Tests

Before running the tests, set the `TEST_DATABASE_URL` environment variable.

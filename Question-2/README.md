# Jokes Application

The `app.py` script is a Flask-based application that fetches jokes from an external API and stores them in an SQLite database (`jokes.db`). It also provides endpoints to retrieve and display jokes.

## How to Run

1. Install the below dependencies using pip:
   - Flask
   - sqlite3
   - requests
2. Run the application:
    python app.py
3. Access the app:
    - Open your browser and navigate to http://0.0.0.0:5000/fetch-jokes.

## Features
Fetches jokes from an external API (e.g., JokeAPI).
Stores jokes in an SQLite database (jokes.db).

## Assumptions
    1. The external API is accessible and returns jokes in  JSON format.
    2. The database (jokes.db) is created automatically if it doesn’t exist.
from flask import Flask, jsonify
import requests
import sqlite3
import json

app = Flask(__name__)

def create_table():
    """
    Create the jokes table in the SQLite database if it does not exist.
    """
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            type TEXT,
            joke TEXT,
            setup TEXT,
            delivery TEXT,
            nsfw BOOLEAN,
            political BOOLEAN,
            sexist BOOLEAN,
            safe BOOLEAN,
            lang TEXT
        )
    """)
    conn.commit()
    conn.close()


def store_jokes(jokes):
    """
    Create & Store jokes in the jokes db.
    Parameters:
        jokes (list): List of jokes to be stored.
    Returns:
        None
    """
    # Create jokes schema if it does not exist
    create_table()
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()
    all_jokes = []
    
    for joke in jokes:
        if joke['type'] == 'single':
            joke_data = joke.get('joke', '')
            setup = None
            delivery = None
        elif joke['type'] == 'twopart':
            joke_data = None
            setup = joke.get('setup', '')
            delivery = joke.get('delivery', '')
        else:
            joke_data = None
            setup = None
            delivery = None

        joke_record = (
            joke["category"],
            joke["type"],
            joke_data,
            setup,
            delivery,
            joke["flags"].get("nsfw", False),
            joke["flags"].get("political", False),
            joke["flags"].get("sexist", False),
            joke["safe"],
            joke["lang"]
        )
        
        all_jokes.append(joke_record)
    
    joke_query = """
    INSERT INTO jokes (category, type, joke, setup, delivery, nsfw, political, sexist, safe, lang)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(joke_query, all_jokes)
    conn.commit()
    conn.close()

@app.route('/fetch-jokes', methods=['GET'])
def reading_jokes():
    """
    Fetch jokes from the API and store them in the SQLite jokes db.    
    """
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?amount=100")
        response.raise_for_status()
        if response.status_code == 200:
            jokes = response.json().get("jokes", [])
            if jokes:
                store_jokes(jokes)
                print(f'Fetched {len(jokes)} jokes from the API.')
                return jsonify(jokes), 200
            else:
                return jsonify({"error": "No jokes found in the response."}), 404
        else:
            return jsonify({"error": "Failed to fetch jokes"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

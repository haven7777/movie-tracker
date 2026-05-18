from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS watched_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            year TEXT,
            poster TEXT,
            rating INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    my_list = conn.execute('SELECT * FROM watched_movies ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', movies=[], watched_list=my_list)

@app.route('/search', methods=['GET'])
def search():
    user_input = request.args.get('movie_query', '').strip()
    if not user_input:
        return redirect(url_for('home'))

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={user_input}"

    try:
        response = requests.get(url)
        data = response.json()
        movie_results = data.get('Search', [])
    except Exception as e:
        print(f"DEBUG: Connection Error -> {e}")
        movie_results = []

    conn = get_db_connection()
    my_list = conn.execute('SELECT * FROM watched_movies ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', movies=movie_results, watched_list=my_list, query=user_input)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    year = request.form.get('year')
    poster = request.form.get('poster')
    rating = request.form.get('rating') or 5
    query = request.form.get('query', '')

    conn = get_db_connection()
    existing = conn.execute('SELECT id FROM watched_movies WHERE title = ?', (title,)).fetchone()
    if not existing:
        conn.execute('INSERT INTO watched_movies (title, year, poster, rating) VALUES (?, ?, ?, ?)',
                     (title, year, poster, rating))
        conn.commit()
    conn.close()

    if query:
        return redirect(url_for('search', movie_query=query))
    return redirect(url_for('home'))

# 🚨 NEW ROUTE: This handles the Remove button!
@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    conn = get_db_connection()
    # Deletes the movie that matches the specific ID
    conn.execute('DELETE FROM watched_movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
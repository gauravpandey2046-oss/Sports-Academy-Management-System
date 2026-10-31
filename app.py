from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database Initialize karne ka function
def init_sqlite_db():
    conn = sqlite3.connect('sports_academy.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sport TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournaments')
def tournaments():
    conn = sqlite3.connect('sports_academy.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tournaments")
    data = cursor.fetchall()
    conn.close()
    return render_template('tournaments.html', tournaments=data)

@app.route('/add', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        date = request.form['date']
        
        conn = sqlite3.connect('sports_academy.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tournaments (name, sport, date) VALUES (?, ?, ?)", (name, sport, date))
        conn.commit()
        conn.close()
        return redirect(url_for('tournaments'))
        
    return render_template('add_tournament.html')

if __name__ == '__main__':
    app.run(debug=True)